import tkinter as tk

import UI_Function as Ufn
import Video_RTSP as Vr
import Constant as Cons
import MainFunction as Mf
import OnOff_Switch as onoffSW
import Ptz as pt
import Preset as Pre

from tkinter import ttk


class UIInit:
    def __init__(self, root, parent, app):
        self.root = root
        self.parent = parent
        self.app = app

        Init_Info(root, parent)
        Init_Network(root, parent)
        Init_Search(root, parent, app)

        # ======================================== Set Command Table ===========================================================
        column_name = Cons.column_array
        column_count = len(column_name)
        cmd_data = Cons.command_array

        self.treeview = Mf.make_table(parent, column_count, Cons.tree_view_size['w'], column_name,
                                      Cons.treeview_pos['x'], Cons.treeview_pos['y'], cmd_data)

        Init_Ptz_Preset_Script(root, parent, app, treeview=self.treeview)


# ======================================== CH Button, Input User, Model Information ====================================
def Init_Info(root, parent):
    Cons.channel_buttons = {}
    for i in range(1, 5):
        btn_pos = getattr(Cons, f'ch{i}_btn_pos')
        button = tk.Button(parent, text=f'CH{i}', command=lambda ch_name=f'CH{i}': Vr.pushed_ch_btn(parent, ch_name))
        button.place(x=btn_pos['x'], y=btn_pos['y'], width=btn_pos['w'], height=btn_pos['h'])
        Cons.channel_buttons[f'CH{i}'] = button

    validator = Cons.validator_lbl
    validator_txt = Cons.validator_txt_fld
    model = Cons.model_lbl
    model_txt = Cons.model_txt_fld
    fw = Cons.fw_lbl
    fw_txt = Cons.fw_txt_fld
    ch_user_input_model_groups = [validator, validator_txt, model, model_txt, fw, fw_txt]

    makeUI_Groups(ch_user_input_model_groups, 'model')

    # (2024.07.19): Change a model entry to selectable drop down menu (NYX Series, Uncooled type)
    # model_option = ['Uncooled', 'DRS', 'FineTree', 'NYX Series', 'MiniGimbal']
    model_option = Cons.model_option
    sel_op = tk.StringVar()
    drop_down = ttk.Combobox(parent, textvariable=sel_op)
    drop_down['values'] = model_option
    current_model = drop_down.current(3)
    drop_down.place(x=model_txt['x'], y=model_txt['y'], height=model_txt['h'], width=model_txt['w'] - 3)
    drop_down.bind('<<ComboboxSelected>>', lambda event: Ufn.model_select(event, parent, sel_op))


# ============================================ Set Network Information =================================================
def Init_Network(root, parent):
    ip = Cons.ip_lbl_info
    ip_txt = Cons.ip_txt_fld_info
    port = Cons.port_lbl_info
    port_txt = Cons.port_txt_fld_info
    rtsp = Cons.rtsp_lbl_info
    rtsp_txt = Cons.rtsp_txt_fld_info
    ipc_id = Cons.ipc_id_info
    ipc_id_txt = Cons.ipc_id_txt_fld_info
    ipc_pw = Cons.ipc_pw_info
    ipc_pw_txt = Cons.ipc_pw_txt_fld_info

    network_ui_groups = [ip, ip_txt, port, port_txt, rtsp, rtsp_txt, ipc_id, ipc_id_txt, ipc_pw, ipc_pw_txt]
    makeUI_Groups(network_ui_groups, 'network')


# ======================================== Set Command Table ===========================================================
def Init_table_view(root, parent):
    column_name = Cons.column_array
    column_count = len(column_name)
    cmd_data = Cons.command_array

    treeview = Mf.make_table(parent, column_count, Cons.tree_view_size['w'], column_name,
                             Cons.treeview_pos['x'], Cons.treeview_pos['y'], cmd_data)


# ===================================== Set Searching a command and Register ===========================================
def Init_Search(root, parent, app):
    column_name = Cons.column_array
    column_count = len(column_name)
    sear_txt = Cons.search_txt_fld_info
    sear_btn = Cons.search_btn

    search_txt_fld = Mf.make_element(x=sear_txt['x'], y=sear_txt['y'],
                                     h=sear_txt['h'], w=sear_txt['w'],
                                     bg=sear_txt['bg'], element='Entry')
    search_txt_fld.bind('<Return>',
                        lambda event: Ufn.search_command(event, parent, search_txt_fld, column_name, column_count))

    search_btn = Mf.make_element(
        x=sear_btn['x'], y=sear_btn['y'],
        h=sear_btn['h'], w=sear_btn['w'], element='Button',
        bg=sear_btn['bg'], text=sear_btn['text'],
        anchor='center'
    )
    search_btn.bind("<Button-1>",
                    lambda event: Ufn.search_command(event, parent, search_txt_fld, column_name, column_count))

    regi_btn = Cons.register_btn
    register_btn = Mf.make_element(x=regi_btn['x'], y=regi_btn['y'],
                    h=regi_btn['h'], w=regi_btn['w'], element='Button',
                    bg=regi_btn['bg'], text=regi_btn['text'],
                    anchor='center',
                    command=Vr.open_video_window)
    register_btn.pack()
    app.register_btn = register_btn


# ============= Set PTZ UI, Preset UI, interval, repeat, script mode, script run/stop/clear ============================
def Init_Ptz_Preset_Script(root, parent, app, treeview):
    ptz_ui = pt.PTZ(parent)
    preset_ui = Pre.Preset(parent)

    inter_lbl = Cons.interval_lbl
    inter_txt = Cons.interval_txt_fld
    repe_lbl = Cons.repeat_lbl
    repe_txt = Cons.repeat_txt_fld
    scr_mode_lbl = Cons.script_mode_lbl

    etc_ui_groups = [inter_lbl, inter_txt, repe_lbl, repe_txt, scr_mode_lbl]
    # repeat_txt_fld.insert(0, 1)
    makeUI_Groups(etc_ui_groups, 'ptz')

    scr_mode_btn = Cons.script_mode_btn
    inter_add_btn = Cons.interval_add_btn
    r_btn = Cons.script_run_btn
    st_btn = Cons.script_stop_btn
    clr_btn = Cons.script_clear_btn

    # Set Interval, repeat lbl, textfield and Run Button
    Cons.interval_button = Mf.make_element(x=inter_add_btn['x'], y=inter_add_btn['y'],
                                           h=inter_add_btn['h'], w=inter_add_btn['w'], element='Button',
                                           bg=inter_add_btn['bg'], text=inter_add_btn['text'],
                                           anchor='center', command=lambda: Ufn.interval_add(parent, inter_txt))

    # Set a Script Mode Slide and Run Button
    script_btn_id = 'SCRIPT'
    script_mode_ui = onoffSW.SwitchOnOff(parent, None, script_btn_id, Cons.script_mode_btn)

    script_run_btn = Mf.make_element(r_btn['x'], r_btn['y'],
                                     r_btn['h'], r_btn['w'],
                                     bg=r_btn['bg'], element='Button',
                                     text=r_btn['text'], anchor='center',
                                     command=lambda: Ufn.start_thread(parent, app, repe_txt, inter_txt,
                                                                      treeview, script_run_btn, script_stop_btn))

    script_stop_btn = Mf.make_element(st_btn['x'], st_btn['y'],
                                      st_btn['h'], st_btn['w'],
                                      bg=st_btn['bg'], element='Button',
                                      text=st_btn['text'], anchor='center',
                                      command=lambda: Ufn.stop_script(script_run_btn, script_stop_btn))

    script_clear_btn = Mf.make_element(clr_btn['x'], clr_btn['y'],
                                       clr_btn['h'], clr_btn['w'],
                                       bg=clr_btn['bg'], element='Button',
                                       text=clr_btn['text'], anchor='center',
                                       command=lambda: Ufn.clr_script(parent, script_run_btn, script_stop_btn))


def makeUI_Groups(ui_groups: [], type: str):
    for i, group in enumerate(ui_groups):
        text = group.get('text')
        security = group.get('security')
        if text:
            Mf.make_element(group['x'], group['y'], group['h'], group['w'], element='Label',
                            bg=group['bg'], text=group['text'], anchor='center')
        else:
            if type == 'network':
                net_name = ['ip', 'ip_txt', 'port', 'port_txt', 'rtsp', 'rtsp_txt',
                            'ipc_id', 'ipc_id_txt', 'ipc_pw', 'ipc_pw_txt']
                entry = Mf.make_element(group['x'], group['y'], group['h'], group['w'], element='Entry',
                                        bg=group['bg'])
                Cons.network_obj[rf'{net_name[i]}'] = entry
                if security:
                    entry.configure(show='*')
            elif type == 'model':
                model_name = ['validator', 'validator_txt', 'model', 'model_txt', 'fw', 'fw_txt']
                entry = Mf.make_element(group['x'], group['y'], group['h'], group['w'], element='Entry',
                                        bg=group['bg'])
                Cons.model_obj[rf'{model_name[i]}'] = entry
            elif type == 'ptz':
                etc_name = ['inter_lbl', 'inter_txt', 'repe_lbl', 'repe_txt', 'scr_mode_lbl']
                entry = Mf.make_element(group['x'], group['y'], group['h'], group['w'], element='Entry',
                                        bg=group['bg'])
                Cons.etc_obj[rf'{etc_name[i]}'] = entry


def test_code():
    # Test Code
    test_txt = {'ip': '192.168.100.158', 'port': '39190', 'rtsp_port': '8554', 'id': 'root', 'pw': 'root'}  # NYX
    # test_txt = {'ip': '192.168.100.155', 'port': '32000', 'rtsp_port': '554', 'id': 'root', 'pw': 'root'}
    # test_txt = {'ip': '192.168.100.152', 'port': '8081', 'rtsp_port': '554', 'id': 'admin', 'pw': 'admin1357'}
    # test_txt = {'ip': '192.168.100.154', 'port': '31000', 'rtsp_port': '554', 'id': 'root', 'pw': 'root'}  #Qred
    Cons.model_obj['ip_txt'].insert(test_txt['ip'], test_txt['port'])
    Cons.model_obj['port_txt'].insert(test_txt['port'], test_txt['rtsp_port'])
    Cons.model_obj['rtsp_txt'].insert(test_txt['rtsp_port'], test_txt['ipc_id'])
    Cons.model_obj['ipc_id_txt'].insert(test_txt['ipc_id'], test_txt['ipc_pw'])
    Cons.model_obj['ipc_pw_txt'].insert(test_txt['ipc_pw'], test_txt['ipc_pw'])