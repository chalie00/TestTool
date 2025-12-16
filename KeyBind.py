import logging
import threading
import time
import queue

from icecream import ic
from functools import partial

import Constant as Cons
import Communication as Comm
import Ptz
import ASYNC_Temp as Async

ptz_url = '/cgi-bin/ptz/control.php?'
ptz_ins = None

# 큐: 백그라운드나 이벤트로부터 실제 PTZ 명령은 메인 스레드에서만 실행
ptz_command_queue = queue.Queue()

# 방향키 상태 (디바운스용)
key_state = {
    'Up': False,
    'Down': False,
    'Left': False,
    'Right': False
}

# keymap 정리
nyx_keymap = {
    'Prior': 'NYX.SET#lens_zctl=narrow',
    'Next': 'NYX.SET#lens_zctl=wide',
    'Insert': 'NYX.SET#lens_fctl=far',
    'Delete': 'NYX.SET#lens_fctl=near',
    'End': 'NYX.SET#lens_afex=execute',
    'Home': 'NYX.SET#isp0_guic=set',
    'Pause': 'NYX.SET#isp0_guie=on'
}

fine_tree_keymap = {
    'Prior': {'zoom': 'tele'},
    'Next': {'zoom': 'wide'},
    'End': {'focus': 'pushaf'}
}

mini_gimbal_keymap = {
    'Prior': 'op_zoom_in',
    'Next': 'op_zoom_out',
    'End': 'op_af',
}

pt_drv_keymap = {
    'Prior': {'zoom': 'zoom_in'},
    'Next': {'zoom': 'zoom_out'},
    'End': {'focus': 'pushaf'}
}

pt_module_keymap = {
    'Prior': 'zoom_in',
    'Next': 'zoom_out',
    'Insert': 'far',
    'Delete': 'near',
    'End': 'af_on',
}

uncooled_keymap = {
    'Up': 'FF01E024000005',
    'Down': 'FF01E025000006',
    'Left': 'FF01E022000003',
    'Right': 'FF01E023000004',
    'Prior': 'FF010020000021',   # Zoom in
    'Next': 'FF010040000041',    # Zoom Out
    'Insert': 'FF010080000081',  # Far
    'Delete': 'FF010100000002',  # Near
    'End': 'FF01A0110000B2',     # AF
    'Home': 'FF01E021000002',   # OSD
}

# 2025.12.15: DRS keymap added
drs_keymap = {
    'Prior': 'FF002200000123',   # Zoom in
    'Next': 'FF002200000224',    # Zoom Out
    'Insert': 'FF002210000133',  # Far
    'Delete': 'FF002210000234',  # Near
    'End': 'FF002220000042',     # AF
}

def initialize_ptz(root):
    global ptz_ins
    ptz_ins = Ptz.PTZ(root)
    return ptz_ins


def on_arrow_key_press(event):
    """방향키 눌렀을 때 한 번만 move 요청."""
    key = event.keysym
    if key in key_state and not key_state[key]:
        key_state[key] = True
        ptz_command_queue.put(('move', key))


def on_arrow_key_release(event):
    """방향키 뗄 때 stop 요청."""
    key = event.keysym
    if key in key_state and key_state[key]:
        key_state[key] = False
        ptz_command_queue.put(('stop', key))


def key_monitor_loop():
    """필요하다면 방향키 외 추가 감시용. (현재는 비워두거나 다른 상태 체크)"""
    while True:
        try:
            # 현재 구조에서는 방향키는 이벤트 기반이므로 여기에 move/stop을 넣지 않음
            time.sleep(0.05)
        except Exception as e:
            logging.error(f"[KeyLoop] Error: {e}")


def process_ptz_queue(root):
    """메인 스레드에서 큐를 처리. 반드시 root.after로 주기 호출."""
    try:
        while not ptz_command_queue.empty():
            cmd_type, key = ptz_command_queue.get_nowait()
            if cmd_type == 'move':
                handle_ptz_move(key)
            elif cmd_type == 'stop':
                handle_ptz_stop(key)
    except Exception as e:
        logging.error(f"[PTZ Queue Processor] {e}")
    finally:
        # 20ms마다 재호출
        root.after(20, lambda: process_ptz_queue(root))


def hex_string_to_array(s: str):
    return [int(s[i:i + 2], 16) for i in range(0, len(s), 2)]


def normalized_model():
    return Cons.selected_model.strip().lower() if isinstance(Cons.selected_model, str) else ''


_last_sent = {'type': None, 'key': None, 'time': 0.0}


def handle_ptz_move(key):
    if not ptz_ins:
        logging.warning("[MOVE] PTZ instance not ready.")
        return

    now = time.time()
    # 동일한 move를 너무 빠르게 반복 보내지 않도록 디바운스 (100ms)
    if _last_sent['type'] == 'move' and _last_sent['key'] == key and now - _last_sent['time'] < 0.1:
        return
    _last_sent.update({'type': 'move', 'key': key, 'time': now})

    try:
        model = normalized_model()
        if model == 'multi':
            # ptz_ins.send_pt_drv(key.lower(), 'pt_drv')
            file_name = f"Multi_{Cons.start_time}.txt"
            Async.async_send(fn=lambda:ptz_ins.send_pt_drv(key.lower(), 'pt_drv'), log_name=file_name)
        elif model == 'minigimbal':
            ptz_ins.send_miniGimbal(key.lower())
        elif model == 'finetree':
            params = {'move': key.lower()}
            # Comm.fine_tree_send_cgi(ptz_url, params)
            file_name = f"Finetree_{Cons.start_time}.txt"
            Async.async_send(fn=lambda:Comm.fine_tree_send_cgi(ptz_url, params), log_name=file_name)
        elif model == 'drs':
            params = {'move': key.lower()}
            # Comm.send_cmd_to_Finetree(ptz_url, params)
            file_name = f"DRS_{Cons.start_time}.txt"
            Async.async_send(fn=lambda:Comm.send_cmd_to_Finetree(ptz_url, params), log_name=file_name)
        elif model == 'nyx series':
            cmd_map = {
                'Up': 'NYX.SET#isp0_guic=up',
                'Down': 'NYX.SET#isp0_guic=down',
                'Left': 'NYX.SET#isp0_guic=left',
                'Right': 'NYX.SET#isp0_guic=right'
            }
            cmd = cmd_map.get(key)
            if cmd:
                # Comm.send_data_with_cmd_for_nyx_ptz_without_root(cmd)
                file_name = f"NYX_{Cons.start_time}.txt"
                Async.async_send(fn=lambda:Comm.send_data_with_cmd_for_nyx_ptz_without_root(cmd), log_name=file_name)
        elif model == 'uncooled':
            cmd = uncooled_keymap.get(key)
            if cmd:
                hex_array = hex_string_to_array(cmd)
                # Comm.send_cmd_for_uncooled_only_cmd(hex_array)
                Comm.send_cmd_for_TTL_uncooled_async(hex_array)
            else:
                logging.debug(f"[MOVE][Uncooled] no mapping for key '{key}'")
        else:
            logging.debug(f"[MOVE] Unknown model '{Cons.selected_model}' for key '{key}'")
    except Exception as e:
        logging.error(f"[MOVE] Error: {e}")


def handle_ptz_stop(key):
    if not ptz_ins:
        logging.warning("[STOP] PTZ instance not ready.")
        return

    now = time.time()
    # stop도 연속적인 동일 명령은 무시
    if _last_sent['type'] == 'stop' and _last_sent['key'] == key and now - _last_sent['time'] < 0.1:
        return
    _last_sent.update({'type': 'stop', 'key': key, 'time': now})

    try:
        model = normalized_model()
        if model == 'multi':
            stop = 'FF010000000001'
            hex_array = hex_string_to_array(stop)
            Comm.send_cmd_only_for_multi(hex_array)
        elif model == 'minigimbal':
            ptz_ins.send_miniGimbal('stop')
        elif model == 'finetree':
            params = {'move': 'stop'}
            Comm.fine_tree_send_cgi(ptz_url, params)
        elif model == 'drs':
            params = {'move': 'stop'}
            Comm.send_cmd_to_Finetree(ptz_url, params)
        elif model == 'nyx series':
            stop_cmd = 'NYX.SET#isp0_guic=stop'
            Comm.send_data_with_cmd_for_nyx_ptz_without_root(stop_cmd)
        elif model == 'uncooled':
            cmd = 'FF010000000001'
            hex_array = hex_string_to_array(cmd)
            # Comm.send_cmd_for_uncooled_only_cmd(hex_array)
            Comm.send_cmd_for_TTL_uncooled_async(hex_array)
        else:
            logging.debug(f"[STOP] Unknown model '{Cons.selected_model}' for key '{key}'")
    except Exception as e:
        logging.error(f"[STOP] Error: {e}")


def pressed_kbd_direction(event):
    """Prior/Next/Insert/Delete/End 등 특수 키 처리"""
    try:
        key = event.keysym
        model = normalized_model()
        # ic('pressed_kbd_direction in KeyBind', model, key)

        if model == 'finetree':
            cmd = fine_tree_keymap.get(key)
            if cmd:
                Comm.fine_tree_send_cgi(ptz_url, cmd)
                return 'break'
        elif model == 'minigimbal':
            cmd = mini_gimbal_keymap.get(key)
            if cmd:
                ptz_ins.send_miniGimbal(cmd)
                return 'break'
        elif model == 'nyx series':
            cmd = nyx_keymap.get(key)
            if cmd:
                Comm.send_data_with_cmd_for_nyx_ptz_without_root(cmd)
                return 'break'
        elif model == 'uncooled':
            cmd = uncooled_keymap.get(key)
            ic('[ExtraKey][Uncooled]', key, cmd)
            if cmd:
                hex_array = hex_string_to_array(cmd)
                # Comm.send_cmd_for_uncooled_only_cmd(hex_array)
                Comm.send_cmd_for_TTL_uncooled_async(hex_array)
                return 'break'
        elif model == 'drs':
            host = Cons.selected_ch['ip']
            port = int(Cons.selected_ch['port']) if Cons.selected_ch['port'] else 0
            cmd = drs_keymap.get(key)
            hex_array = hex_string_to_array(cmd)
            if cmd: 
                Comm.send_cmd_for_drs(host=host, port=port, send_cmd=hex_array)
    except Exception as e:
        logging.error(f"[ExtraKey] Error: {e}")
        return 'break'

# 2025.12.15: FineTree, DRS's cmd has been added
def extra_key_release(event):
    """Nyx 같은 곳에서 release 시 stop 처리 (zoom/focus 등)"""
    key = event.keysym
    model = normalized_model()
    try:
        if model == 'nyx series':
            if key in ['Prior', 'Next']:
                Comm.send_data_with_cmd_for_nyx_ptz_without_root('NYX.SET#lens_zctl=stop')
                return 'break'
            if key in ['Insert', 'Delete']:
                Comm.send_data_with_cmd_for_nyx_ptz_without_root('NYX.SET#lens_fctl=stop')
                return 'break'
        elif model == 'finetree':
            if key in ['Prior', 'Next']:
                params = {'move': 'stop'}
                Comm.fine_tree_send_cgi(ptz_url, params)
                return 'break'
        elif model == 'drs':
            if key in ['Prior', 'Next']:
                host = Cons.selected_ch['ip']
                port = int(Cons.selected_ch['port']) if Cons.selected_ch['port'] else 0
                cmd = 'FF002204000026' # Zoom Stop
                hex_array = hex_string_to_array(cmd)
                if cmd: 
                    Comm.send_cmd_for_drs(host=host, port=port, send_cmd=hex_array)
            if key in ['Insert', 'Delete']:
                host = Cons.selected_ch['ip']
                port = int(Cons.selected_ch['port']) if Cons.selected_ch['port'] else 0
                cmd = 'FF002213000035' # Foucs Stop
                hex_array = hex_string_to_array(cmd)
                if cmd: 
                    Comm.send_cmd_for_drs(host=host, port=port, send_cmd=hex_array)
            
        # 다른 모델/키 조합이 필요하면 여기에 확장
    except Exception as e:
        logging.error(f"[ExtraKeyRelease] Error: {e}")


def control_preset(event, type, num):
    if type == 'Save_Preset':
        params = {'presetsave': num}
        Comm.fine_tree_send_cgi(ptz_url, params)
    elif type == 'Call_Preset':
        params = {'preset': num}
        Comm.fine_tree_send_cgi(ptz_url, params)


def bind_system_kbd(root):
    # 방향키: press/release 각각 전용 핸들러
    root.bind_all("<KeyPress-Up>", on_arrow_key_press)
    root.bind_all("<KeyRelease-Up>", on_arrow_key_release)
    root.bind_all("<KeyPress-Down>", on_arrow_key_press)
    root.bind_all("<KeyRelease-Down>", on_arrow_key_release)
    root.bind_all("<KeyPress-Left>", on_arrow_key_press)
    root.bind_all("<KeyRelease-Left>", on_arrow_key_release)
    root.bind_all("<KeyPress-Right>", on_arrow_key_press)
    root.bind_all("<KeyRelease-Right>", on_arrow_key_release)

    # 기타 키 (Zoom, Focus, AF 등)
    extra_keys = ['Prior', 'Next', 'Insert', 'Delete', 'End', 'Home', 'Pause']
    for key in extra_keys:
        root.bind_all(f"<KeyPress-{key}>", pressed_kbd_direction)
        root.bind_all(f"<KeyRelease-{key}>", extra_key_release)

    # 프리셋 단축키
    for i in range(1, 10):
        root.bind(rf"<Control-Key-{i}>",
                  partial(control_preset, type='Call_Preset', num=i))
        root.bind(rf"<F{i}>",
                  partial(control_preset, type='Save_Preset', num=i))

    # 백그라운드 루프 (필요하다면)
    threading.Thread(target=key_monitor_loop, daemon=True).start()

    # 큐 처리 시작 (메인 스레드)
    root.after(20, lambda: process_ptz_queue(root))
