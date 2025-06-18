import logging
import time

import Constant as Cons
import Communication as Comm
import Ptz

ptz_url = '/cgi-bin/ptz/control.php?'
ptz_ins = None
key_state = {}

# 키가 눌렸을 때 시간 기록 (중복 처리를 방지하기 위해)
TIME_THRESHOLD = 0.2  # 0.2초 간격으로만 명령을 보냄


# Logging Default Setting
# logging.basicConfig(
#     level=logging.DEBUG,
#     format="%(asctime)s - %(levelname)s - %(message)s",
#     handlers=[
#         logging.FileHandler("ptz_control.log"),
#         logging.StreamHandler()
#     ]
# )


def initialize_ptz(root):
    global ptz_ins
    ptz_ins = Ptz.PTZ(root)


# (2024.10.17): Add keyboard direction key function when key was
# 2025.05.13: Added keymap for NYX (Zoom In/Out, insert: near, delete: far, Direction: OSD, Home: OSD Set)
# noinspection PyUnresolvedReferences
def pressed_kbd_direction(event):
    try:
        if Cons.selected_model == 'FineTree':
            if event.keysym == 'Up':
                params = {'move': 'up'}
                Comm.fine_tree_send_cgi(ptz_url, params)
            elif event.keysym == 'Down':
                params = {'move': 'down'}
                Comm.fine_tree_send_cgi(ptz_url, params)
            elif event.keysym == 'Left':
                params = {'move': 'left'}
                Comm.fine_tree_send_cgi(ptz_url, params)
            elif event.keysym == 'Right':
                params = {'move': 'right'}
                Comm.fine_tree_send_cgi(ptz_url, params)
            elif event.keysym == 'Prior':
                params = {'zoom': 'tele'}
                Comm.fine_tree_send_cgi(ptz_url, params)
                return 'break'
            elif event.keysym == 'Next':
                params = {'zoom': 'wide'}
                Comm.fine_tree_send_cgi(ptz_url, params)
                return 'break'
            elif event.keysym == 'End':
                params = {'focus': 'pushaf'}
                Comm.fine_tree_send_cgi(ptz_url, params)
        elif Cons.selected_model == 'DRS':
            if event.keysym == 'Up':
                params = {'move': 'up'}
                Comm.send_cmd_to_Finetree(ptz_url, params)
            elif event.keysym == 'Down':
                params = {'move': 'down'}
                Comm.send_cmd_to_Finetree(ptz_url, params)
            elif event.keysym == 'Left':
                params = {'move': 'left'}
                Comm.send_cmd_to_Finetree(ptz_url, params)
            elif event.keysym == 'Right':
                params = {'move': 'right'}
                Comm.send_cmd_to_Finetree(ptz_url, params)
            elif event.keysym == 'Prior':
                params = {'zoom': 'tele'}
                Comm.send_cmd_to_Finetree(ptz_url, params)
                return 'break'
            elif event.keysym == 'Next':
                params = {'zoom': 'wide'}
                Comm.send_cmd_to_Finetree(ptz_url, params)
                return 'break'
            elif event.keysym == 'End':
                params = {'focus': 'pushaf'}
                Comm.send_cmd_to_Finetree(ptz_url, params)
        elif Cons.selected_model == 'MiniGimbal':
            if event.keysym == 'Up':
                ptz_ins.send_miniGimbal('up')
            elif event.keysym == 'Down':
                ptz_ins.send_miniGimbal('down')
            elif event.keysym == 'Left':
                ptz_ins.send_miniGimbal('left')
            elif event.keysym == 'Right':
                ptz_ins.send_miniGimbal('right')
            elif event.keysym == 'Prior':
                ptz_ins.send_miniGimbal('op_zoom_in')
                return 'break'
            elif event.keysym == 'Next':
                ptz_ins.send_miniGimbal('op_zoom_out')
                return 'break'
            elif event.keysym == 'End':
                ptz_ins.send_miniGimbal('op_af')
        if Cons.selected_model == 'NYX Series':
            if event.keysym == 'Up':
                up_cmd = 'NYX.SET#isp0_guic=up'
                Comm.send_data_with_cmd_for_nyx_ptz_without_root(up_cmd)
                return 'break'
            elif event.keysym == 'Down':
                down_cmd = 'NYX.SET#isp0_guic=down'
                Comm.send_data_with_cmd_for_nyx_ptz_without_root(down_cmd)
                return 'break'
            elif event.keysym == 'Left':
                left_cmd = 'NYX.SET#isp0_guic=left'
                Comm.send_data_with_cmd_for_nyx_ptz_without_root(left_cmd)
                return 'break'
            elif event.keysym == 'Right':
                right_cmd = 'NYX.SET#isp0_guic=right'
                Comm.send_data_with_cmd_for_nyx_ptz_without_root(right_cmd)
                return 'break'
            elif event.keysym == 'Prior':
                narrow = 'NYX.SET#lens_zctl=narrow'
                Comm.send_data_with_cmd_for_nyx_ptz_without_root(narrow)
                return 'break'
            elif event.keysym == 'Next':
                wide = 'NYX.SET#lens_zctl=wide'
                Comm.send_data_with_cmd_for_nyx_ptz_without_root(wide)
                return 'break'
            elif event.keysym == 'Insert':
                near = 'NYX.SET#lens_fctl=near'
                Comm.send_data_with_cmd_for_nyx_ptz_without_root(near)
            elif event.keysym == 'Delete':
                far = 'NYX.SET#lens_fctl=far'
                Comm.send_data_with_cmd_for_nyx_ptz_without_root(far)
            elif event.keysym == 'End':
                af = 'NYX.SET#lens_afex=execute'
                Comm.send_data_with_cmd_for_nyx_ptz_without_root(af)
            elif event.keysym == 'Home':
                set_cmd = 'NYX.SET#isp0_guic=set'
                Comm.send_data_with_cmd_for_nyx_ptz_without_root(set_cmd)
            elif event.keysym == 'Pause':
                osd_on = 'NYX.SET#isp0_guie=on'
                Comm.send_data_with_cmd_for_nyx_ptz_without_root(osd_on)

    except Exception as e:
        logging.error(f"Error in pressed_kbd_direction: {e}")
        return 'break'


# (2024.10.17): send stop cmd when key was released
# noinspection PyUnresolvedReferences
def release_stop(event, type):
    try:
        if Cons.selected_model == 'FineTree':
            if type in ['PTZ']:
                ptz_url = '/cgi-bin/ptz/control.php?'
                params = {'move': 'stop'}
                Comm.fine_tree_send_cgi(ptz_url, params)
            elif type in ['Zoom']:
                ptz_url = '/cgi-bin/ptz/control.php?'
                params = {'zoom': 'stop'}
                Comm.fine_tree_send_cgi(ptz_url, params)
        elif Cons.selected_model == 'DRS':
            if type in ['PTZ']:
                ptz_url = '/cgi-bin/ptz/control.php?'
                params = {'move': 'stop'}
                Comm.send_cmd_to_Finetree(ptz_url, params)
            elif type in ['Zoom']:
                ptz_url = '/cgi-bin/ptz/control.php?'
                params = {'zoom': 'stop'}
                Comm.send_cmd_to_Finetree(ptz_url, params)
        elif Cons.selected_model == 'MiniGimbal':
            if type in ['PTZ']:
                logging.info('PTZ Stop')
                ptz_ins.send_miniGimbal('stop')
            elif type in ['Zoom']:
                ptz_ins.send_miniGimbal('op_zoom_stop')
        elif Cons.selected_model == 'NYX Series':
            if type in ['Focus']:
                focus_stop = 'NYX.SET#lens_fctl=stop'
                Comm.send_data_with_cmd_for_nyx_ptz_without_root(focus_stop)
            elif type in ['Zoom']:
                zoom_stop = 'NYX.SET#lens_zctl=stop'
                Comm.send_data_with_cmd_for_nyx_ptz_without_root(zoom_stop)
                return 'break'
        else:
            print('stop cmd was not sent because model is not finetree')
            return
    except Exception as e:
        logging.error(f"Error in release_stop: {e}")


# (2024.10.17): Set a short-cut Keyboard
def control_preset(event, type, num):
    print('called control preset')
    if type == 'Save_Preset':
        print('Save_Preset')
        params = {'presetsave': num}
        Comm.fine_tree_send_cgi(ptz_url, params)
    elif type == 'Call_Preset':
        print('Call_Preset')
        params = {'preset': num}
        Comm.fine_tree_send_cgi(ptz_url, params)


# (2024.10.17): Add System KBD Bind
def bind_system_kbd(root):
    # 4 Direction PTZ
    root.bind("<KeyPress-Up>", pressed_kbd_direction)
    root.bind("<KeyPress-Down>", pressed_kbd_direction)
    root.bind("<KeyPress-Left>", pressed_kbd_direction)
    root.bind("<KeyPress-Right>", pressed_kbd_direction)
    root.bind("<KeyRelease-Up>", lambda event, type='PTZ': release_stop(event, type))
    root.bind("<KeyRelease-Down>", lambda event, type='PTZ': release_stop(event, type))
    root.bind("<KeyRelease-Left>", lambda event, type='PTZ': release_stop(event, type))
    root.bind("<KeyRelease-Right>", lambda event, type='PTZ': release_stop(event, type))

    # Zoom In/Out
    root.bind("<KeyPress-Prior>", pressed_kbd_direction)
    root.bind("<KeyPress-Next>", pressed_kbd_direction)
    root.bind("<KeyRelease-Prior>", lambda event, type='Zoom': release_stop(event, type))
    root.bind("<KeyRelease-Next>", lambda event, type='Zoom': release_stop(event, type))

    # for NYX (Focus near / far)
    root.bind("<KeyPress-Insert>", pressed_kbd_direction)
    root.bind("<KeyPress-Delete>", pressed_kbd_direction)
    root.bind("<KeyRelease-Insert>", lambda event, type='Focus': release_stop(event, type))
    root.bind("<KeyRelease-Delete>", lambda event, type='Focus': release_stop(event, type))

    # for NYX OSD Display
    root.bind("<KeyRelease-Pause>", pressed_kbd_direction)

    # for NYX OSD Set
    root.bind("<KeyRelease-Home>", pressed_kbd_direction)

    # AF
    root.bind("<KeyPress-End>", pressed_kbd_direction)

    # Preset
    # when Number Key was pressed Move Preset, FNumkey is to save a preset
    for i in range(1, 10):
        root.bind(rf"<Control-Key-{i}>", lambda event, type='Call_Preset',
                                                num=i: control_preset(event, type, num))
        root.bind(rf"<F{i}>", lambda event, type='Save_Preset', num=i: control_preset(event, type, num))
        # root.bind(rf"<F{i}>", lambda event, type='Save_Preset', num=i: control_preset(event, type, num))
