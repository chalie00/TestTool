import tkinter

import Constant as Cons
import Communication as Comm


ptz_url = '/cgi-bin/ptz/control.php?'


# (2024.10.17): Add keyboard direction key function when key was pushed
def pressed_kbd_direction(event):
    print('kbd pressed')

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
        elif event.keysym == 'Next':
            params = {'zoom': 'wide'}
            Comm.fine_tree_send_cgi(ptz_url, params)
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
        elif event.keysym == 'Next':
            params = {'zoom': 'wide'}
            Comm.send_cmd_to_Finetree(ptz_url, params)
        elif event.keysym == 'End':
            params = {'focus': 'pushaf'}
            Comm.send_cmd_to_Finetree(ptz_url, params)

# (2024.10.17): send stop cmd when key was released
def release_stop(event, type):
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
    else:
        print('stop cmd was not sent because model is not finetree')
        return


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

    # AF
    root.bind("<KeyPress-End>", pressed_kbd_direction)

    # Preset
    # when Number Key was pressed Move Preset, FNumkey is to save a preset
    for i in range(1, 10):
        root.bind(rf"<Control-Key-{i}>", lambda event, type='Call_Preset',
                                                num=i: control_preset(event, type, num))
        root.bind(rf"<F{i}>", lambda event, type='Save_Preset', num=i: control_preset(event, type, num))
        # root.bind(rf"<F{i}>", lambda event, type='Save_Preset', num=i: control_preset(event, type, num))
