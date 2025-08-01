import logging
import threading
import time

from icecream import ic
from functools import partial

import Constant as Cons
import Communication as Comm
import Ptz

ptz_url = '/cgi-bin/ptz/control.php?'
ptz_ins = None
key_state = {
    'Up': False,
    'Down': False,
    'Left': False,
    'Right': False
}

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
    'Prior':'zoom_in',
    'Next': 'zoom_out',
    'Insert': 'far',
    'Delete': 'near',
    'End': 'af_on',
}

uncooled_keymap = {
    'Up': 'FF01E024000005',
    'Down': 'FF01E025000006',
    'Left':'FF01E022000003',
    'Right': 'FF01E023000004',
    'Prior': 'FF010020000021',  # Zoom in
    'Next': 'FF010040000041',  # Zoom Out
    'Insert': 'FF010080000081',  # Far
    'Delete': 'FF010100000002',  # Near
    'End': 'FF01A0110000B2',  # AF
    'Home': 'FF01E021000002',  # OSD
}


def initialize_ptz(root):
    global ptz_ins
    ptz_ins = Ptz.PTZ(root)
    return ptz_ins

def on_key_press(event):
    if event.keysym in key_state:
        key_state[event.keysym] = True

def on_key_release(event):
    if event.keysym in key_state:
        key_state[event.keysym] = False

def key_monitor_loop():
    prev_state = {}
    while True:
        try:
            for key, pressed in key_state.items():
                prev_pressed = prev_state.get(key, False)

                if pressed and not prev_pressed:
                    handle_ptz_move(key)

                elif not pressed and prev_pressed:
                    handle_ptz_stop(key)

            prev_state = key_state.copy()
            time.sleep(0.05)
        except Exception as e:
            logging.error(f"[KeyLoop] Error: {e}")

def handle_ptz_move(key):
    try:
        if Cons.selected_model == 'Multi':
            ptz_ins.send_pt_drv(key.lower(), 'pt_drv')
        elif Cons.selected_model == 'MiniGimbal':
            ptz_ins.send_miniGimbal(key.lower())
        elif Cons.selected_model == 'FineTree':
            params = {'move': key.lower()}
            Comm.fine_tree_send_cgi(ptz_url, params)
        elif Cons.selected_model == 'DRS':
            params = {'move': key.lower()}
            Comm.send_cmd_to_Finetree(ptz_url, params)
        elif Cons.selected_model == 'NYX Series':
            cmd_map = {
                'Up': 'NYX.SET#isp0_guic=up',
                'Down': 'NYX.SET#isp0_guic=down',
                'Left': 'NYX.SET#isp0_guic=left',
                'Right': 'NYX.SET#isp0_guic=right'
            }
            cmd = cmd_map.get(key)
            if cmd:
                Comm.send_data_with_cmd_for_nyx_ptz_without_root(cmd)
        elif Cons.selected_model == 'Uncooled':
            cmd = uncooled_keymap.get(key)
            if cmd:
                hex_array = [int(cmd[i:i + 2], 16) for i in range(0, len(cmd), 2)]
                Comm.send_cmd_for_uncooled_only_cmd(hex_array)
    except Exception as e:
        logging.error(f"[MOVE] Error: {e}")

def handle_ptz_stop(key):
    try:
        if Cons.selected_model == 'Multi':
            stop = 'FF010000000001'
            hex_array = [int(stop[i:i + 2], 16) for i in range(0, len(stop), 2)]
            Comm.send_cmd_only_for_multi(hex_array)
        elif Cons.selected_model == 'MiniGimbal':
            ptz_ins.send_miniGimbal('stop')
        elif Cons.selected_model == 'FineTree':
            params = {'move': 'stop'}
            Comm.fine_tree_send_cgi(ptz_url, params)
        elif Cons.selected_model == 'DRS':
            params = {'move': 'stop'}
            Comm.send_cmd_to_Finetree(ptz_url, params)
        elif Cons.selected_model == 'NYX Series':
            stop_cmd = 'NYX.SET#isp0_guic=stop'
            Comm.send_data_with_cmd_for_nyx_ptz_without_root(stop_cmd)
        elif Cons.selected_model == 'Uncooled':
            cmd = 'FF010000000001'
            if cmd:
                hex_array = [int(cmd[i:i + 2], 16) for i in range(0, len(cmd), 2)]
                Comm.send_cmd_for_uncooled_only_cmd(hex_array)
    except Exception as e:
        logging.error(f"[STOP] Error: {e}")

def pressed_kbd_direction(event):
    try:
        # PT Drv에 대한 Zoom, Focus, AF 등 구현 필요 (TMS-10 첫 검증 시 비 정상 동작 했음)
        key = event.keysym
        model = Cons.selected_model
        ic('pressed_kbd_direction in KeyBind', model)

        if model == 'FineTree':
            cmd = fine_tree_keymap.get(key)
            if cmd:
                Comm.fine_tree_send_cgi(ptz_url, cmd)
                return 'break'
        elif model == 'MiniGimbal':
            cmd = mini_gimbal_keymap.get(key)
            if cmd:
                ptz_ins.send_miniGimbal(cmd)
                return 'break'
        elif model == 'NYX Series':
            cmd = nyx_keymap.get(key)
            if cmd:
                Comm.send_data_with_cmd_for_nyx_ptz_without_root(cmd)
                return 'break'
        elif model == 'Uncooled':
            cmd = uncooled_keymap.get(key)
            ic('pressed_kbd_direction in KeyBind', cmd)
            if cmd:
                hex_array = [int(cmd[i:i + 2], 16) for i in range(0, len(cmd), 2)]
                Comm.send_cmd_for_uncooled_only_cmd(hex_array)

    except Exception as e:
        logging.error(f"[ExtraKey] Error: {e}")
        return 'break'

def control_preset(event, type, num):
    if type == 'Save_Preset':
        params = {'presetsave': num}
        Comm.fine_tree_send_cgi(ptz_url, params)
    elif type == 'Call_Preset':
        params = {'preset': num}
        Comm.fine_tree_send_cgi(ptz_url, params)

def bind_system_kbd(root):
    root.bind_all("<KeyPress>", on_key_press)
    extra_keys = ['Prior', 'Next', 'Insert', 'Delete', 'End', 'Home', 'Pause']
    for key in extra_keys:
        root.bind_all(f"<KeyPress-{key}>", pressed_kbd_direction)
        root.bind_all(f"<KeyRelease-{key}>", handle_ptz_stop)
    root.bind_all("<KeyRelease>", on_key_release)
    threading.Thread(target=key_monitor_loop, daemon=True).start()

    # Preset 단축키
    for i in range(1, 10):
        root.bind(rf"<Control-Key-{i}>",
                  partial(control_preset, type='Call_Preset', num=i))
        root.bind(rf"<F{i}>",
                  partial(control_preset, type='Save_Preset', num=i))

# import logging
#
# from functools import partial
#
# import Constant as Cons
# import Communication as Comm
# import Ptz
#
# ptz_url = '/cgi-bin/ptz/control.php?'
# ptz_ins = None
# key_state = {}
#
# def initialize_ptz(root):
#     global ptz_ins
#     ptz_ins = Ptz.PTZ(root)
#     return ptz_ins
#
#
# # (2024.10.17): Add keyboard direction key function when key was
# # 2025.05.13: Added keymap for NYX (Zoom In/Out, insert: near, delete: far, Direction: OSD, Home: OSD Set)
# # noinspection PyUnresolvedReferences
# def pressed_kbd_direction(event):
#     try:
#         if Cons.selected_model == 'FineTree':
#             if event.keysym == 'Up':
#                 params = {'move': 'up'}
#                 Comm.fine_tree_send_cgi(ptz_url, params)
#             elif event.keysym == 'Down':
#                 params = {'move': 'down'}
#                 Comm.fine_tree_send_cgi(ptz_url, params)
#             elif event.keysym == 'Left':
#                 params = {'move': 'left'}
#                 Comm.fine_tree_send_cgi(ptz_url, params)
#             elif event.keysym == 'Right':
#                 params = {'move': 'right'}
#                 Comm.fine_tree_send_cgi(ptz_url, params)
#             elif event.keysym == 'Prior':
#                 params = {'zoom': 'tele'}
#                 Comm.fine_tree_send_cgi(ptz_url, params)
#                 return 'break'
#             elif event.keysym == 'Next':
#                 params = {'zoom': 'wide'}
#                 Comm.fine_tree_send_cgi(ptz_url, params)
#                 return 'break'
#             elif event.keysym == 'End':
#                 params = {'focus': 'pushaf'}
#                 Comm.fine_tree_send_cgi(ptz_url, params)
#         elif Cons.selected_model == 'DRS':
#             if event.keysym == 'Up':
#                 params = {'move': 'up'}
#                 Comm.send_cmd_to_Finetree(ptz_url, params)
#             elif event.keysym == 'Down':
#                 params = {'move': 'down'}
#                 Comm.send_cmd_to_Finetree(ptz_url, params)
#             elif event.keysym == 'Left':
#                 params = {'move': 'left'}
#                 Comm.send_cmd_to_Finetree(ptz_url, params)
#             elif event.keysym == 'Right':
#                 params = {'move': 'right'}
#                 Comm.send_cmd_to_Finetree(ptz_url, params)
#             elif event.keysym == 'Prior':
#                 params = {'zoom': 'tele'}
#                 Comm.send_cmd_to_Finetree(ptz_url, params)
#                 return 'break'
#             elif event.keysym == 'Next':
#                 params = {'zoom': 'wide'}
#                 Comm.send_cmd_to_Finetree(ptz_url, params)
#                 return 'break'
#             elif event.keysym == 'End':
#                 params = {'focus': 'pushaf'}
#                 Comm.send_cmd_to_Finetree(ptz_url, params)
#         elif Cons.selected_model == 'MiniGimbal':
#             if event.keysym == 'Up':
#                 ptz_ins.send_miniGimbal('up')
#             elif event.keysym == 'Down':
#                 ptz_ins.send_miniGimbal('down')
#             elif event.keysym == 'Left':
#                 ptz_ins.send_miniGimbal('left')
#             elif event.keysym == 'Right':
#                 ptz_ins.send_miniGimbal('right')
#             elif event.keysym == 'Prior':
#                 ptz_ins.send_miniGimbal('op_zoom_in')
#                 return 'break'
#             elif event.keysym == 'Next':
#                 ptz_ins.send_miniGimbal('op_zoom_out')
#                 return 'break'
#             elif event.keysym == 'End':
#                 ptz_ins.send_miniGimbal('op_af')
#         if Cons.selected_model == 'NYX Series':
#             if event.keysym == 'Up':
#                 up_cmd = 'NYX.SET#isp0_guic=up'
#                 Comm.send_data_with_cmd_for_nyx_ptz_without_root(up_cmd)
#                 return 'break'
#             elif event.keysym == 'Down':
#                 down_cmd = 'NYX.SET#isp0_guic=down'
#                 Comm.send_data_with_cmd_for_nyx_ptz_without_root(down_cmd)
#                 return 'break'
#             elif event.keysym == 'Left':
#                 left_cmd = 'NYX.SET#isp0_guic=left'
#                 Comm.send_data_with_cmd_for_nyx_ptz_without_root(left_cmd)
#                 return 'break'
#             elif event.keysym == 'Right':
#                 right_cmd = 'NYX.SET#isp0_guic=right'
#                 Comm.send_data_with_cmd_for_nyx_ptz_without_root(right_cmd)
#                 return 'break'
#             elif event.keysym == 'Prior':
#                 narrow = 'NYX.SET#lens_zctl=narrow'
#                 Comm.send_data_with_cmd_for_nyx_ptz_without_root(narrow)
#                 return 'break'
#             elif event.keysym == 'Next':
#                 wide = 'NYX.SET#lens_zctl=wide'
#                 Comm.send_data_with_cmd_for_nyx_ptz_without_root(wide)
#                 return 'break'
#             elif event.keysym == 'Insert':
#                 near = 'NYX.SET#lens_fctl=near'
#                 Comm.send_data_with_cmd_for_nyx_ptz_without_root(near)
#             elif event.keysym == 'Delete':
#                 far = 'NYX.SET#lens_fctl=far'
#                 Comm.send_data_with_cmd_for_nyx_ptz_without_root(far)
#             elif event.keysym == 'End':
#                 af = 'NYX.SET#lens_afex=execute'
#                 Comm.send_data_with_cmd_for_nyx_ptz_without_root(af)
#             elif event.keysym == 'Home':
#                 set_cmd = 'NYX.SET#isp0_guic=set'
#                 Comm.send_data_with_cmd_for_nyx_ptz_without_root(set_cmd)
#             elif event.keysym == 'Pause':
#                 osd_on = 'NYX.SET#isp0_guie=on'
#                 Comm.send_data_with_cmd_for_nyx_ptz_without_root(osd_on)
#         if Cons.selected_model == 'Multi':
#             if event.keysym == 'Up':
#                 ptz_ins.send_pt_drv('up', 'pt_drv')
#                 return 'break'
#             elif event.keysym == 'Down':
#                 ptz_ins.send_pt_drv('down', 'pt_drv')
#                 return 'break'
#             elif event.keysym == 'Left':
#                 ptz_ins.send_pt_drv('left', 'pt_drv')
#                 return 'break'
#             elif event.keysym == 'Right':
#                 ptz_ins.send_pt_drv('right', 'pt_drv')
#                 return 'break'
#
#     except Exception as e:
#         logging.error(f"Error in pressed_kbd_direction: {e}")
#         return 'break'
#
#
# # (2024.10.17): send stop cmd when key was released
# # noinspection PyUnresolvedReferences
# def release_stop(event, type):
#     try:
#         if Cons.selected_model == 'FineTree':
#             if type in ['PTZ']:
#                 ptz_url = '/cgi-bin/ptz/control.php?'
#                 params = {'move': 'stop'}
#                 Comm.fine_tree_send_cgi(ptz_url, params)
#             elif type in ['Zoom']:
#                 ptz_url = '/cgi-bin/ptz/control.php?'
#                 params = {'zoom': 'stop'}
#                 Comm.fine_tree_send_cgi(ptz_url, params)
#         elif Cons.selected_model == 'DRS':
#             if type in ['PTZ']:
#                 ptz_url = '/cgi-bin/ptz/control.php?'
#                 params = {'move': 'stop'}
#                 Comm.send_cmd_to_Finetree(ptz_url, params)
#             elif type in ['Zoom']:
#                 ptz_url = '/cgi-bin/ptz/control.php?'
#                 params = {'zoom': 'stop'}
#                 Comm.send_cmd_to_Finetree(ptz_url, params)
#         elif Cons.selected_model == 'MiniGimbal':
#             if type in ['PTZ']:
#                 logging.info('PTZ Stop')
#                 ptz_ins.send_miniGimbal('stop')
#             elif type in ['Zoom']:
#                 ptz_ins.send_miniGimbal('op_zoom_stop')
#         elif Cons.selected_model == 'NYX Series':
#             if type in ['Focus']:
#                 focus_stop = 'NYX.SET#lens_fctl=stop'
#                 Comm.send_data_with_cmd_for_nyx_ptz_without_root(focus_stop)
#             elif type in ['Zoom']:
#                 zoom_stop = 'NYX.SET#lens_zctl=stop'
#                 Comm.send_data_with_cmd_for_nyx_ptz_without_root(zoom_stop)
#                 return 'break'
#         elif Cons.selected_model == 'Multi':
#             print('Multi Stop')
#             # if type in ['PTZ']:
#             #     ptz_ins.send_pt_drv('stop', 'pt_drv')
#             stop = 'FF010000000001'
#             hex_array = [int(stop[i:i + 2], 16) for i in range(0, len(stop), 2)]
#             Comm.send_cmd_only_for_multi(hex_array)
#             return 'break'
#         else:
#             print('stop cmd was not sent because model is not finetree')
#             return
#     except Exception as e:
#         logging.error(f"Error in release_stop: {e}")
#
#
# # (2024.10.17): Set a short-cut Keyboard
# def control_preset(event, type, num):
#     print('called control preset')
#     if type == 'Save_Preset':
#         print('Save_Preset')
#         params = {'presetsave': num}
#         Comm.fine_tree_send_cgi(ptz_url, params)
#     elif type == 'Call_Preset':
#         print('Call_Preset')
#         params = {'preset': num}
#         Comm.fine_tree_send_cgi(ptz_url, params)
#
#
# # (2024.10.17): Add System KBD Bind
# def bind_system_kbd(root):
#     # 4 Direction PTZ
#     root.bind_all("<KeyPress-Up>", pressed_kbd_direction)
#     root.bind_all("<KeyPress-Down>", pressed_kbd_direction)
#     root.bind_all("<KeyPress-Left>", pressed_kbd_direction)
#     root.bind_all("<KeyPress-Right>", pressed_kbd_direction)
#     root.bind_all("<KeyRelease-Up>", lambda event, type='PTZ': release_stop(event, type))
#     root.bind_all("<KeyRelease-Down>", lambda event, type='PTZ': release_stop(event, type))
#     root.bind_all("<KeyRelease-Left>", lambda event, type='PTZ': release_stop(event, type))
#     root.bind_all("<KeyRelease-Right>", lambda event, type='PTZ': release_stop(event, type))
#
#     # Zoom In/Out
#     root.bind("<KeyPress-Prior>", pressed_kbd_direction)
#     root.bind("<KeyPress-Next>", pressed_kbd_direction)
#     root.bind("<KeyRelease-Prior>", lambda event, type='Zoom': release_stop(event, type))
#     root.bind("<KeyRelease-Next>", lambda event, type='Zoom': release_stop(event, type))
#
#     # for NYX (Focus near / far)
#     root.bind("<KeyPress-Insert>", pressed_kbd_direction)
#     root.bind("<KeyPress-Delete>", pressed_kbd_direction)
#     root.bind("<KeyRelease-Insert>", lambda event, type='Focus': release_stop(event, type))
#     root.bind("<KeyRelease-Delete>", lambda event, type='Focus': release_stop(event, type))
#
#     # for NYX OSD Display
#     root.bind("<KeyRelease-Pause>", pressed_kbd_direction)
#
#     # for NYX OSD Set
#     root.bind("<KeyRelease-Home>", pressed_kbd_direction)
#
#     # AF
#     root.bind("<KeyPress-End>", pressed_kbd_direction)
#
#     # Preset
#     # when Number Key was pressed Move Preset, FNumkey is to save a preset
#     # for i in range(1, 10):
#     #     root.bind(rf"<Control-Key-{i}>", lambda event, type='Call_Preset',
#     #                                             num=i: control_preset(event, type, num))
#     #     root.bind(rf"<F{i}>", lambda event, type='Save_Preset', num=i: control_preset(event, type, num))
#     #     # root.bind(rf"<F{i}>", lambda event, type='Save_Preset', num=i: control_preset(event, type, num))
#     for i in range(1, 10):
#         root.bind(rf"<Control-Key-{i}>",
#                   partial(control_preset, type='Call_Preset', num=i))
#         root.bind(rf"<F{i}>",
#                   partial(control_preset, type='Save_Preset', num=i))
#
#
