import logging
import threading
import time
import queue

from icecream import ic
from functools import partial

import Constant as Cons
import Communication as Comm
import Ptz

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
            ptz_ins.send_pt_drv(key.lower(), 'pt_drv')
        elif model == 'minigimbal':
            ptz_ins.send_miniGimbal(key.lower())
        elif model == 'finetree':
            params = {'move': key.lower()}
            Comm.fine_tree_send_cgi(ptz_url, params)
        elif model == 'drs':
            params = {'move': key.lower()}
            Comm.send_cmd_to_Finetree(ptz_url, params)
        elif model == 'nyx series':
            cmd_map = {
                'Up': 'NYX.SET#isp0_guic=up',
                'Down': 'NYX.SET#isp0_guic=down',
                'Left': 'NYX.SET#isp0_guic=left',
                'Right': 'NYX.SET#isp0_guic=right'
            }
            cmd = cmd_map.get(key)
            if cmd:
                Comm.send_data_with_cmd_for_nyx_ptz_without_root(cmd)
        elif model == 'uncooled':
            cmd = uncooled_keymap.get(key)
            if cmd:
                hex_array = hex_string_to_array(cmd)
                Comm.send_cmd_for_uncooled_only_cmd(hex_array)
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
            Comm.send_cmd_for_uncooled_only_cmd(hex_array)
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
                Comm.send_cmd_for_uncooled_only_cmd(hex_array)
                return 'break'
    except Exception as e:
        logging.error(f"[ExtraKey] Error: {e}")
        return 'break'


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


# import logging
# import threading
# import time
# import  queue
#
#
# from icecream import ic
# from functools import partial
#
# import Constant as Cons
# import Communication as Comm
# import Ptz
#
# ptz_url = '/cgi-bin/ptz/control.php?'
# ptz_ins = None
# ptz_command_queue = queue.Queue()
#
# key_state = {
#     'Up': False,
#     'Down': False,
#     'Left': False,
#     'Right': False
# }
#
# nyx_keymap = {
#     'Prior': 'NYX.SET#lens_zctl=narrow',
#     'Next': 'NYX.SET#lens_zctl=wide',
#     'Insert': 'NYX.SET#lens_fctl=far',
#     'Delete': 'NYX.SET#lens_fctl=near',
#     'End': 'NYX.SET#lens_afex=execute',
#     'Home': 'NYX.SET#isp0_guic=set',
#     'Pause': 'NYX.SET#isp0_guie=on'
# }
#
# fine_tree_keymap = {
#     'Prior': {'zoom': 'tele'},
#     'Next': {'zoom': 'wide'},
#     'End': {'focus': 'pushaf'}
# }
#
# mini_gimbal_keymap = {
#     'Prior': 'op_zoom_in',
#     'Next': 'op_zoom_out',
#     'End': 'op_af',
# }
#
# pt_drv_keymap = {
#     'Prior': {'zoom': 'zoom_in'},
#     'Next': {'zoom': 'zoom_out'},
#     'End': {'focus': 'pushaf'}
# }
#
# pt_module_keymap = {
#     'Prior':'zoom_in',
#     'Next': 'zoom_out',
#     'Insert': 'far',
#     'Delete': 'near',
#     'End': 'af_on',
# }
#
# uncooled_keymap = {
#     'Up': 'FF01E024000005',
#     'Down': 'FF01E025000006',
#     'Left':'FF01E022000003',
#     'Right': 'FF01E023000004',
#     'Prior': 'FF010020000021',  # Zoom in
#     'Next': 'FF010040000041',  # Zoom Out
#     'Insert': 'FF010080000081',  # Far
#     'Delete': 'FF010100000002',  # Near
#     'End': 'FF01A0110000B2',  # AF
#     'Home': 'FF01E021000002',  # OSD
# }
#
#
# def initialize_ptz(root):
#     global ptz_ins
#     ptz_ins = Ptz.PTZ(root)
#     return ptz_ins
#
# def on_key_press(event):
#     if event.keysym in key_state:
#         if not key_state[event.keysym]:
#             key_state[event.keysym] = True
#             ptz_command_queue.put(('move', event.keysym))
#
# def on_key_release(event):
#     if event.keysym in key_state:
#         if key_state[event.keysym]:
#             key_state[event.keysym] = False
#             ptz_command_queue.put(('stop', event.keysym))
#
#
# # def on_key_press(event):
# #     if event.keysym in key_state:
# #         key_state[event.keysym] = True
# #
# # def on_key_release(event):
# #     if event.keysym in key_state:
# #         key_state[event.keysym] = False
#
# # def key_monitor_loop():
# #     prev_state = {}
# #     while True:
# #         try:
# #             for key, pressed in key_state.items():
# #                 prev_pressed = prev_state.get(key, False)
# #
# #                 if pressed and not prev_pressed:
# #                     handle_ptz_move(key)
# #
# #                 elif not pressed and prev_pressed:
# #                     handle_ptz_stop(key)
# #
# #             prev_state = key_state.copy()
# #             time.sleep(0.05)
# #         except Exception as e:
# #             logging.error(f"[KeyLoop] Error: {e}")
#
# def key_monitor_loop():
#     prev_state = {}
#     while True:
#         try:
#             for key, pressed in key_state.items():
#                 prev_pressed = prev_state.get(key, False)
#                 if pressed and not prev_pressed:
#                     ptz_command_queue.put(('move', key))
#                 elif not pressed and prev_pressed:
#                     ptz_command_queue.put(('stop', key))
#             prev_state = key_state.copy()
#             time.sleep(0.05)
#         except Exception as e:
#             logging.error(f"[KeyLoop] Error: {e}")
#
#
# def process_ptz_queue():
#     try:
#         while not ptz_command_queue.empty():
#             cmd_type, key = ptz_command_queue.get_nowait()
#             if cmd_type == 'move':
#                 handle_ptz_move(key)
#             elif cmd_type == 'stop':
#                 handle_ptz_stop(key)
#     except Exception as e:
#         logging.error(f"[PTZ Queue Processor] {e}")
#     finally:
#         # 계속 재귀 호출: 20ms 마다 체크
#         if ptz_ins:  # ptz_ins가 초기화된 후부터
#             ptz_ins.root.after(20, process_ptz_queue)  # 또는 `root.after`
#
#
# def handle_ptz_move(key):
#     if not ptz_ins:
#         logging.warning("PTZ instance not ready.")
#         return
#     try:
#         if Cons.selected_model == 'Multi':
#             ptz_ins.send_pt_drv(key.lower(), 'pt_drv')
#         elif Cons.selected_model == 'MiniGimbal':
#             ptz_ins.send_miniGimbal(key.lower())
#         elif Cons.selected_model == 'FineTree':
#             params = {'move': key.lower()}
#             Comm.fine_tree_send_cgi(ptz_url, params)
#         elif Cons.selected_model == 'DRS':
#             params = {'move': key.lower()}
#             Comm.send_cmd_to_Finetree(ptz_url, params)
#         elif Cons.selected_model == 'NYX Series':
#             cmd_map = {
#                 'Up': 'NYX.SET#isp0_guic=up',
#                 'Down': 'NYX.SET#isp0_guic=down',
#                 'Left': 'NYX.SET#isp0_guic=left',
#                 'Right': 'NYX.SET#isp0_guic=right'
#             }
#             cmd = cmd_map.get(key)
#             if cmd:
#                 Comm.send_data_with_cmd_for_nyx_ptz_without_root(cmd)
#         elif Cons.selected_model == 'Uncooled':
#             cmd = uncooled_keymap.get(key)
#             if cmd:
#                 hex_array = [int(cmd[i:i + 2], 16) for i in range(0, len(cmd), 2)]
#                 Comm.send_cmd_for_uncooled_only_cmd(hex_array)
#     except Exception as e:
#         logging.error(f"[MOVE] Error: {e}")
#
# def handle_ptz_stop(key):
#     if not ptz_ins:
#         logging.warning("PTZ instance not ready.")
#         return
#     try:
#         if Cons.selected_model == 'Multi':
#             stop = 'FF010000000001'
#             hex_array = [int(stop[i:i + 2], 16) for i in range(0, len(stop), 2)]
#             Comm.send_cmd_only_for_multi(hex_array)
#         elif Cons.selected_model == 'MiniGimbal':
#             ptz_ins.send_miniGimbal('stop')
#         elif Cons.selected_model == 'FineTree':
#             params = {'move': 'stop'}
#             Comm.fine_tree_send_cgi(ptz_url, params)
#         elif Cons.selected_model == 'DRS':
#             params = {'move': 'stop'}
#             Comm.send_cmd_to_Finetree(ptz_url, params)
#         elif Cons.selected_model == 'NYX Series':
#             stop_cmd = 'NYX.SET#isp0_guic=stop'
#             Comm.send_data_with_cmd_for_nyx_ptz_without_root(stop_cmd)
#         elif Cons.selected_model == 'Uncooled':
#             cmd = 'FF010000000001'
#             if cmd:
#                 hex_array = [int(cmd[i:i + 2], 16) for i in range(0, len(cmd), 2)]
#                 Comm.send_cmd_for_uncooled_only_cmd(hex_array)
#     except Exception as e:
#         logging.error(f"[STOP] Error: {e}")
#
# def pressed_kbd_direction(event):
#     try:
#         # PT Drv에 대한 Zoom, Focus, AF 등 구현 필요 (TMS-10 첫 검증 시 비 정상 동작 했음)
#         key = event.keysym
#         model = Cons.selected_model
#         ic('pressed_kbd_direction in KeyBind', model)
#
#         if model == 'FineTree':
#             cmd = fine_tree_keymap.get(key)
#             if cmd:
#                 Comm.fine_tree_send_cgi(ptz_url, cmd)
#                 return 'break'
#         elif model == 'MiniGimbal':
#             cmd = mini_gimbal_keymap.get(key)
#             if cmd:
#                 ptz_ins.send_miniGimbal(cmd)
#                 return 'break'
#         elif model == 'NYX Series':
#             cmd = nyx_keymap.get(key)
#             if cmd:
#                 Comm.send_data_with_cmd_for_nyx_ptz_without_root(cmd)
#                 return 'break'
#         elif model == 'Uncooled':
#             cmd = uncooled_keymap.get(key)
#             ic('pressed_kbd_direction in KeyBind', cmd)
#             if cmd:
#                 hex_array = [int(cmd[i:i + 2], 16) for i in range(0, len(cmd), 2)]
#                 Comm.send_cmd_for_uncooled_only_cmd(hex_array)
#
#     except Exception as e:
#         logging.error(f"[ExtraKey] Error: {e}")
#         return 'break'
#
# def control_preset(event, type, num):
#     if type == 'Save_Preset':
#         params = {'presetsave': num}
#         Comm.fine_tree_send_cgi(ptz_url, params)
#     elif type == 'Call_Preset':
#         params = {'preset': num}
#         Comm.fine_tree_send_cgi(ptz_url, params)
#
#
# def bind_system_kbd(root):
#     # 방향키 바인딩 (이전처럼)
#     root.bind_all("<KeyPress-Up>", on_key_press)
#     root.bind_all("<KeyRelease-Up>", on_key_release)
#     root.bind_all("<KeyPress-Down>", on_key_press)
#     root.bind_all("<KeyRelease-Down>", on_key_release)
#     root.bind_all("<KeyPress-Left>", on_key_press)
#     root.bind_all("<KeyRelease-Left>", on_key_release)
#     root.bind_all("<KeyPress-Right>", on_key_press)
#     root.bind_all("<KeyRelease-Right>", on_key_release)
#
#     # 기타 키
#     extra_keys = ['Prior', 'Next', 'Insert', 'Delete', 'End', 'Home', 'Pause']
#     for key in extra_keys:
#         root.bind_all(f"<KeyPress-{key}>", pressed_kbd_direction)
#         root.bind_all(f"<KeyRelease-{key}>", extra_key_release)  # 기존에 만든 release 핸들러
#
#     for i in range(1, 10):
#         root.bind(rf"<Control-Key-{i}>",
#                   partial(control_preset, type='Call_Preset', num=i))
#         root.bind(rf"<F{i}>",
#                   partial(control_preset, type='Save_Preset', num=i))
#
#     threading.Thread(target=key_monitor_loop, daemon=True).start()
#     # 큐 처리기 시작 (메인 스레드 타이머)
#     root.after(20, process_ptz_queue)
#
#
# # def bind_system_kbd(root):
# #     root.bind_all("<KeyPress>", on_key_press)
# #     extra_keys = ['Prior', 'Next', 'Insert', 'Delete', 'End', 'Home', 'Pause']
# #     for key in extra_keys:
# #         root.bind_all(f"<KeyPress-{key}>", pressed_kbd_direction)
# #         root.bind_all(f"<KeyRelease-{key}>", handle_ptz_stop)
# #     root.bind_all("<KeyRelease>", on_key_release)
# #     threading.Thread(target=key_monitor_loop, daemon=True).start()
# #
# #     # Preset 단축키
# #     for i in range(1, 10):
# #         root.bind(rf"<Control-Key-{i}>",
# #                   partial(control_preset, type='Call_Preset', num=i))
# #         root.bind(rf"<F{i}>",
# #                   partial(control_preset, type='Save_Preset', num=i))
#
# # import logging
# #
# # from functools import partial
# #
# # import Constant as Cons
# # import Communication as Comm
# # import Ptz
# #
# # ptz_url = '/cgi-bin/ptz/control.php?'
# # ptz_ins = None
# # key_state = {}
# #
# # def initialize_ptz(root):
# #     global ptz_ins
# #     ptz_ins = Ptz.PTZ(root)
# #     return ptz_ins
# #
# #
# # # (2024.10.17): Add keyboard direction key function when key was
# # # 2025.05.13: Added keymap for NYX (Zoom In/Out, insert: near, delete: far, Direction: OSD, Home: OSD Set)
# # # noinspection PyUnresolvedReferences
# # def pressed_kbd_direction(event):
# #     try:
# #         if Cons.selected_model == 'FineTree':
# #             if event.keysym == 'Up':
# #                 params = {'move': 'up'}
# #                 Comm.fine_tree_send_cgi(ptz_url, params)
# #             elif event.keysym == 'Down':
# #                 params = {'move': 'down'}
# #                 Comm.fine_tree_send_cgi(ptz_url, params)
# #             elif event.keysym == 'Left':
# #                 params = {'move': 'left'}
# #                 Comm.fine_tree_send_cgi(ptz_url, params)
# #             elif event.keysym == 'Right':
# #                 params = {'move': 'right'}
# #                 Comm.fine_tree_send_cgi(ptz_url, params)
# #             elif event.keysym == 'Prior':
# #                 params = {'zoom': 'tele'}
# #                 Comm.fine_tree_send_cgi(ptz_url, params)
# #                 return 'break'
# #             elif event.keysym == 'Next':
# #                 params = {'zoom': 'wide'}
# #                 Comm.fine_tree_send_cgi(ptz_url, params)
# #                 return 'break'
# #             elif event.keysym == 'End':
# #                 params = {'focus': 'pushaf'}
# #                 Comm.fine_tree_send_cgi(ptz_url, params)
# #         elif Cons.selected_model == 'DRS':
# #             if event.keysym == 'Up':
# #                 params = {'move': 'up'}
# #                 Comm.send_cmd_to_Finetree(ptz_url, params)
# #             elif event.keysym == 'Down':
# #                 params = {'move': 'down'}
# #                 Comm.send_cmd_to_Finetree(ptz_url, params)
# #             elif event.keysym == 'Left':
# #                 params = {'move': 'left'}
# #                 Comm.send_cmd_to_Finetree(ptz_url, params)
# #             elif event.keysym == 'Right':
# #                 params = {'move': 'right'}
# #                 Comm.send_cmd_to_Finetree(ptz_url, params)
# #             elif event.keysym == 'Prior':
# #                 params = {'zoom': 'tele'}
# #                 Comm.send_cmd_to_Finetree(ptz_url, params)
# #                 return 'break'
# #             elif event.keysym == 'Next':
# #                 params = {'zoom': 'wide'}
# #                 Comm.send_cmd_to_Finetree(ptz_url, params)
# #                 return 'break'
# #             elif event.keysym == 'End':
# #                 params = {'focus': 'pushaf'}
# #                 Comm.send_cmd_to_Finetree(ptz_url, params)
# #         elif Cons.selected_model == 'MiniGimbal':
# #             if event.keysym == 'Up':
# #                 ptz_ins.send_miniGimbal('up')
# #             elif event.keysym == 'Down':
# #                 ptz_ins.send_miniGimbal('down')
# #             elif event.keysym == 'Left':
# #                 ptz_ins.send_miniGimbal('left')
# #             elif event.keysym == 'Right':
# #                 ptz_ins.send_miniGimbal('right')
# #             elif event.keysym == 'Prior':
# #                 ptz_ins.send_miniGimbal('op_zoom_in')
# #                 return 'break'
# #             elif event.keysym == 'Next':
# #                 ptz_ins.send_miniGimbal('op_zoom_out')
# #                 return 'break'
# #             elif event.keysym == 'End':
# #                 ptz_ins.send_miniGimbal('op_af')
# #         if Cons.selected_model == 'NYX Series':
# #             if event.keysym == 'Up':
# #                 up_cmd = 'NYX.SET#isp0_guic=up'
# #                 Comm.send_data_with_cmd_for_nyx_ptz_without_root(up_cmd)
# #                 return 'break'
# #             elif event.keysym == 'Down':
# #                 down_cmd = 'NYX.SET#isp0_guic=down'
# #                 Comm.send_data_with_cmd_for_nyx_ptz_without_root(down_cmd)
# #                 return 'break'
# #             elif event.keysym == 'Left':
# #                 left_cmd = 'NYX.SET#isp0_guic=left'
# #                 Comm.send_data_with_cmd_for_nyx_ptz_without_root(left_cmd)
# #                 return 'break'
# #             elif event.keysym == 'Right':
# #                 right_cmd = 'NYX.SET#isp0_guic=right'
# #                 Comm.send_data_with_cmd_for_nyx_ptz_without_root(right_cmd)
# #                 return 'break'
# #             elif event.keysym == 'Prior':
# #                 narrow = 'NYX.SET#lens_zctl=narrow'
# #                 Comm.send_data_with_cmd_for_nyx_ptz_without_root(narrow)
# #                 return 'break'
# #             elif event.keysym == 'Next':
# #                 wide = 'NYX.SET#lens_zctl=wide'
# #                 Comm.send_data_with_cmd_for_nyx_ptz_without_root(wide)
# #                 return 'break'
# #             elif event.keysym == 'Insert':
# #                 near = 'NYX.SET#lens_fctl=near'
# #                 Comm.send_data_with_cmd_for_nyx_ptz_without_root(near)
# #             elif event.keysym == 'Delete':
# #                 far = 'NYX.SET#lens_fctl=far'
# #                 Comm.send_data_with_cmd_for_nyx_ptz_without_root(far)
# #             elif event.keysym == 'End':
# #                 af = 'NYX.SET#lens_afex=execute'
# #                 Comm.send_data_with_cmd_for_nyx_ptz_without_root(af)
# #             elif event.keysym == 'Home':
# #                 set_cmd = 'NYX.SET#isp0_guic=set'
# #                 Comm.send_data_with_cmd_for_nyx_ptz_without_root(set_cmd)
# #             elif event.keysym == 'Pause':
# #                 osd_on = 'NYX.SET#isp0_guie=on'
# #                 Comm.send_data_with_cmd_for_nyx_ptz_without_root(osd_on)
# #         if Cons.selected_model == 'Multi':
# #             if event.keysym == 'Up':
# #                 ptz_ins.send_pt_drv('up', 'pt_drv')
# #                 return 'break'
# #             elif event.keysym == 'Down':
# #                 ptz_ins.send_pt_drv('down', 'pt_drv')
# #                 return 'break'
# #             elif event.keysym == 'Left':
# #                 ptz_ins.send_pt_drv('left', 'pt_drv')
# #                 return 'break'
# #             elif event.keysym == 'Right':
# #                 ptz_ins.send_pt_drv('right', 'pt_drv')
# #                 return 'break'
# #
# #     except Exception as e:
# #         logging.error(f"Error in pressed_kbd_direction: {e}")
# #         return 'break'
# #
# #
# # # (2024.10.17): send stop cmd when key was released
# # # noinspection PyUnresolvedReferences
# # def release_stop(event, type):
# #     try:
# #         if Cons.selected_model == 'FineTree':
# #             if type in ['PTZ']:
# #                 ptz_url = '/cgi-bin/ptz/control.php?'
# #                 params = {'move': 'stop'}
# #                 Comm.fine_tree_send_cgi(ptz_url, params)
# #             elif type in ['Zoom']:
# #                 ptz_url = '/cgi-bin/ptz/control.php?'
# #                 params = {'zoom': 'stop'}
# #                 Comm.fine_tree_send_cgi(ptz_url, params)
# #         elif Cons.selected_model == 'DRS':
# #             if type in ['PTZ']:
# #                 ptz_url = '/cgi-bin/ptz/control.php?'
# #                 params = {'move': 'stop'}
# #                 Comm.send_cmd_to_Finetree(ptz_url, params)
# #             elif type in ['Zoom']:
# #                 ptz_url = '/cgi-bin/ptz/control.php?'
# #                 params = {'zoom': 'stop'}
# #                 Comm.send_cmd_to_Finetree(ptz_url, params)
# #         elif Cons.selected_model == 'MiniGimbal':
# #             if type in ['PTZ']:
# #                 logging.info('PTZ Stop')
# #                 ptz_ins.send_miniGimbal('stop')
# #             elif type in ['Zoom']:
# #                 ptz_ins.send_miniGimbal('op_zoom_stop')
# #         elif Cons.selected_model == 'NYX Series':
# #             if type in ['Focus']:
# #                 focus_stop = 'NYX.SET#lens_fctl=stop'
# #                 Comm.send_data_with_cmd_for_nyx_ptz_without_root(focus_stop)
# #             elif type in ['Zoom']:
# #                 zoom_stop = 'NYX.SET#lens_zctl=stop'
# #                 Comm.send_data_with_cmd_for_nyx_ptz_without_root(zoom_stop)
# #                 return 'break'
# #         elif Cons.selected_model == 'Multi':
# #             print('Multi Stop')
# #             # if type in ['PTZ']:
# #             #     ptz_ins.send_pt_drv('stop', 'pt_drv')
# #             stop = 'FF010000000001'
# #             hex_array = [int(stop[i:i + 2], 16) for i in range(0, len(stop), 2)]
# #             Comm.send_cmd_only_for_multi(hex_array)
# #             return 'break'
# #         else:
# #             print('stop cmd was not sent because model is not finetree')
# #             return
# #     except Exception as e:
# #         logging.error(f"Error in release_stop: {e}")
# #
# #
# # # (2024.10.17): Set a short-cut Keyboard
# # def control_preset(event, type, num):
# #     print('called control preset')
# #     if type == 'Save_Preset':
# #         print('Save_Preset')
# #         params = {'presetsave': num}
# #         Comm.fine_tree_send_cgi(ptz_url, params)
# #     elif type == 'Call_Preset':
# #         print('Call_Preset')
# #         params = {'preset': num}
# #         Comm.fine_tree_send_cgi(ptz_url, params)
# #
# #
# # # (2024.10.17): Add System KBD Bind
# # def bind_system_kbd(root):
# #     # 4 Direction PTZ
# #     root.bind_all("<KeyPress-Up>", pressed_kbd_direction)
# #     root.bind_all("<KeyPress-Down>", pressed_kbd_direction)
# #     root.bind_all("<KeyPress-Left>", pressed_kbd_direction)
# #     root.bind_all("<KeyPress-Right>", pressed_kbd_direction)
# #     root.bind_all("<KeyRelease-Up>", lambda event, type='PTZ': release_stop(event, type))
# #     root.bind_all("<KeyRelease-Down>", lambda event, type='PTZ': release_stop(event, type))
# #     root.bind_all("<KeyRelease-Left>", lambda event, type='PTZ': release_stop(event, type))
# #     root.bind_all("<KeyRelease-Right>", lambda event, type='PTZ': release_stop(event, type))
# #
# #     # Zoom In/Out
# #     root.bind("<KeyPress-Prior>", pressed_kbd_direction)
# #     root.bind("<KeyPress-Next>", pressed_kbd_direction)
# #     root.bind("<KeyRelease-Prior>", lambda event, type='Zoom': release_stop(event, type))
# #     root.bind("<KeyRelease-Next>", lambda event, type='Zoom': release_stop(event, type))
# #
# #     # for NYX (Focus near / far)
# #     root.bind("<KeyPress-Insert>", pressed_kbd_direction)
# #     root.bind("<KeyPress-Delete>", pressed_kbd_direction)
# #     root.bind("<KeyRelease-Insert>", lambda event, type='Focus': release_stop(event, type))
# #     root.bind("<KeyRelease-Delete>", lambda event, type='Focus': release_stop(event, type))
# #
# #     # for NYX OSD Display
# #     root.bind("<KeyRelease-Pause>", pressed_kbd_direction)
# #
# #     # for NYX OSD Set
# #     root.bind("<KeyRelease-Home>", pressed_kbd_direction)
# #
# #     # AF
# #     root.bind("<KeyPress-End>", pressed_kbd_direction)
# #
# #     # Preset
# #     # when Number Key was pressed Move Preset, FNumkey is to save a preset
# #     # for i in range(1, 10):
# #     #     root.bind(rf"<Control-Key-{i}>", lambda event, type='Call_Preset',
# #     #                                             num=i: control_preset(event, type, num))
# #     #     root.bind(rf"<F{i}>", lambda event, type='Save_Preset', num=i: control_preset(event, type, num))
# #     #     # root.bind(rf"<F{i}>", lambda event, type='Save_Preset', num=i: control_preset(event, type, num))
# #     for i in range(1, 10):
# #         root.bind(rf"<Control-Key-{i}>",
# #                   partial(control_preset, type='Call_Preset', num=i))
# #         root.bind(rf"<F{i}>",
# #                   partial(control_preset, type='Save_Preset', num=i))
# #
# #
