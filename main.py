# -*- coding: utf-8 -*-

import tkinter as tk
import threading
import time
from datetime import datetime

import Constant as Cons
import MainFunction as Mf
import Communication as Comm
import VideoPlayer as Vp
import Ptz as pt
import OnOff_Switch as onoffSW
import Table as tb
import Response as Res
import System_Info as SysInfo

from tkinter import ttk


class TestTool(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        # Set Title
        self.parent.title('Test Tool')
        self.parent.geometry(f'{Cons.WINDOWS_SIZE["x"]}x{Cons.WINDOWS_SIZE["y"]}+'
                             f'{Cons.WINDOWS_POSITION["x"]}+{Cons.WINDOWS_POSITION["y"]}')
        self.parent.config(padx=15, pady=15)

        # self.canvas = tk.Canvas(parent, width=Cons.camera_resolution['w'],
        #                         height=Cons.camera_resolution['h'], bg='red')
        # self.canvas.place(x=0, y=0)

        # self.thread_running = False
        self.thread_running = threading.Event()
        self.thread = None

        # (2024.08.05): Called when ch button was pushed
        def pushed_ch_btn(btn, ch_name):
            info = getattr(Cons, f'{ch_name.lower()}_rtsp_info')
            info.update({
                'model': sel_op.get(),
                'ch': ch_name.lower(),
                'ip': ip_txt_fld.get(),
                'port': port_txt_fld.get(),
                'rtsp_port': rtsp_txt_fld.get(),
                'id': ipc_id_txt_fld.get(),
                'pw': ipc_pw_txt_fld.get()
            })

            url_patterns = {
                'NYX Series': rf'rtsp://{info["id"]}:{info["pw"]}@{info["ip"]}:{info["rtsp_port"]}/test',
                'Uncooled': rf'rtsp://{info["id"]}:{info["pw"]}@{info["ip"]}:{info["rtsp_port"]}/cam0_0',
                'DRS': rf'rtsp://{info["id"]}:{info["pw"]}@{info["ip"]}:{info["rtsp_port"]}/cam0_0'
            }
            info['url'] = url_patterns.get(info['model'], 'Invalid model')

            btn.config(bg='green')

            if ch_name.lower() == 'ch1':
                ch_info = Cons.ch1_rtsp_info
                pos = {'x': ch_info['x'], 'y': ch_info['y'], 'h': ch_info['h'], 'w': ch_info['w']}
                Cons.video_player_ch1 = Vp.VideoPlayer(parent, info['url'], pos, ch_name)
            elif ch_name.lower() == 'ch2':
                ch_info = Cons.ch2_rtsp_info
                pos = {'x': ch_info['x'], 'y': ch_info['y'], 'h': ch_info['h'], 'w': ch_info['w']}
                Cons.video_player_ch2 = Vp.VideoPlayer(parent, info['url'], pos, ch_name)
            elif ch_name.lower() == 'ch3':
                ch_info = Cons.ch3_rtsp_info
                pos = {'x': ch_info['x'], 'y': ch_info['y'], 'h': ch_info['h'], 'w': ch_info['w']}
                Cons.video_player_ch3 = Vp.VideoPlayer(parent, info['url'], pos, ch_name)
            elif ch_name.lower() == 'ch4':
                ch_info = Cons.ch4_rtsp_info
                pos = {'x': ch_info['x'], 'y': ch_info['y'], 'h': ch_info['h'], 'w': ch_info['w']}
                Cons.video_player_ch4 = Vp.VideoPlayer(parent, info['url'], pos, ch_name)

        # Check Main Window Position
        # Open RTSP and Get the Network Information from User Input
        def open_video_window():
            Cons.host_ip = ip_txt_fld.get()
            Cons.port = port_txt_fld.get()
            Cons.rtsp_port = rtsp_txt_fld.get()
            Cons.ipc_id = ipc_id_txt_fld.get()
            Cons.ipc_pw = ipc_pw_txt_fld.get()
            # Set CH Button to default Color
            for i in range(1, 5):
                channel_names[f'CH{i}'].config(bg=Cons.ch1_btn_pos['bg'])

            videos = [Cons.video_player_ch1, Cons.video_player_ch2, Cons.video_player_ch3, Cons.video_player_ch4]
            for video in videos:
                if video:
                    video.start_video()

        # (2024.07.19): Model Drop Down Menu function
        def model_select(event):
            current_sel = sel_op.get()
            if current_sel in ['NYX Series', 'DRS', 'Uncooled']:
                Cons.selected_model = current_sel
                col_name = Cons.column_array
                col_count = len(col_name)
                command_data = Mf.get_data_from_csv(Cons.cmd_path)

                Mf.make_table(parent, col_count, Cons.tree_view_size['w'], col_name,
                              Cons.treeview_pos['x'], Cons.treeview_pos['y'], command_data)
                ptz_ui.refresh_ptz()

        # Search a protocol which user typed text
        def search_command(event):
            query = search_txt_fld.get().lower()
            selected_item = []
            command_data = Mf.get_data_from_csv(Cons.cmd_path)
            for item in command_data:
                if query in item[0].lower():
                    selected_item.append(item)

            Mf.make_table(parent, column_count, Cons.tree_view_size['w'], column_name,
                          Cons.treeview_pos['x'], Cons.treeview_pos['y'], selected_item)
            print('searching is completed')

        # Add interval to each script command
        def interval_add():
            cur_interval = float(int(interval_txt_fld.get()) / 1000)
            Cons.interval_arrays.append(cur_interval)
            row_cmd_title = len(Cons.script_hex_nyx_cmd_arrays)
            col_interval = len(Cons.interval_arrays)

            for i, cmd_list in enumerate(Cons.interval_arrays):
                Cons.cmd_itv_arrays[i][0] = Cons.script_cmd_titles[i]
                Cons.cmd_itv_arrays[i][1] = Cons.interval_arrays[i]

            Mf.check_interval_active()
            print(Cons.cmd_itv_arrays)
            tb.Table(parent)

        # (2024.07.04): Start thread with selected script
        def start_thread():
            if not self.thread_running.is_set():
                self.thread_running.set()
                self.thread = threading.Thread(target=run_script)
                self.thread.start()

        # (2024.07.04): Start thread with selected script
        def run_script() -> []:
            current_time = datetime.now()
            time_str = current_time.strftime('%Y-%m-%d-%H-%M-%S')
            response_file_name = rf'{Cons.log_path}_{time_str}.txt'
            try:
                while self.thread_running.is_set():
                    self.script_run_btn.config(state='disabled')
                    self.script_stop_btn.config(state='normal')
                    Cons.data_sending = True
                    if Cons.script_toggle_flag:
                        print('run script')
                        interval = Cons.interval_arrays
                        repeat = int(repeat_txt_fld.get())
                        script = Cons.script_hex_nyx_cmd_arrays
                        titles = Cons.script_cmd_titles
                        if Cons.selected_model in ['Uncooled', 'DRS']:
                            Comm.send_cmd_to_ucooled_with_interval(interval, repeat, script, titles, parent)
                        elif Cons.selected_model == 'NYX Series':
                            Comm.send_cmd_to_nyx_with_interval(parent, titles, script, interval, response_file_name)
                    else:
                        protocol_str_arr = []
                        hex_protocol = []
                        for id in treeview.get_checked():
                            item = treeview.set(id)
                            protocol_str = item['2']
                            protocol_str_arr.append(protocol_str)
                        for protocol in protocol_str_arr:
                            converted_hex = Mf.convert_str_to_hex(protocol)
                            hex_protocol.append(converted_hex)
                        print(hex_protocol)
                        interval = float(int(interval_txt_fld.get()) / 1000)
                        repeat = int(repeat_txt_fld.get())
                        titles = Cons.script_cmd_titles
                        Comm.send_cmd_to_ucooled_with_interval(interval, repeat, hex_protocol, titles, parent)

                        return hex_protocol
                    time.sleep(0.1)
            finally:
                self.script_run_btn.config(state='normal')
                self.script_stop_btn.config(state='disabled')
                Cons.data_sending = False
                print('stop script')

        # (2024.07.04): Stop Script(Threading Stop)
        def stop_script():
            Cons.data_sending = False
            self.script_run_btn.config(state='normal')
            self.script_stop_btn.config(state='disabled')
            print('stop script')

            self.thread_running.clear()
            if self.thread and self.thread.is_alive():
                self.thread.join(timeout=1)  # Allow GUI to process events while waiting
                self.thread = None

        # (2024.07.04): Clear the Script Table
        def clr_script():
            Cons.data_sending = False
            self.script_run_btn.config(state='normal')
            self.script_stop_btn.config(state='normal')
            print('clear script')
            Mf.clr_table_arrays(parent)

        # ================================================ UI Layout ============================================

        # ======================================== CH Button, Input User, Model Information ================================
        # (2024.08.05) Create a CH Button
        channel_names = {}
        for i in range(1, 5):
            btn_pos = getattr(Cons, f'ch{i}_btn_pos')
            channel_names[f'CH{i}'] = Mf.make_element(btn_pos['x'], btn_pos['y'], btn_pos['h'], btn_pos['w'],
                                                      'Button', bg=btn_pos['bg'], text=btn_pos['text'], font=(None, 8),
                                                      anchor='center')

            channel_names[f'CH{i}'].bind('<Button-1>',
                                         lambda event, btn=channel_names[f'CH{i}'],
                                                ch_name=btn_pos['text']: pushed_ch_btn(
                                             btn, ch_name))

        validator = Cons.validator_lbl
        validator_txt = Cons.validator_txt_fld
        model = Cons.model_lbl
        model_txt = Cons.model_txt_fld
        fw = Cons.fw_lbl
        fw_txt = Cons.fw_txt_fld

        val_lbl = Mf.make_element(x=validator['x'], y=validator['y'],
                                  h=validator['h'], w=validator['w'], element='Label',
                                  bg=validator['bg'], text=validator['text'], anchor='center')
        val_txt_fld = Mf.make_element(x=validator_txt['x'], y=validator_txt['y'],
                                      h=validator_txt['h'], w=validator_txt['w'], element='Entry',
                                      bg=validator_txt['bg'])

        model_lbl = Mf.make_element(x=model['x'], y=model['y'],
                                    h=model['h'], w=model['w'], element='Label',
                                    bg=model['bg'], text=model['text'], anchor='center')

        # (2024.07.19): Change a model entry to selectable drop down menu (NYX Series, Uncooled type)
        # model_option = ['Uncooled', 'DRS', 'NYX Series']
        model_option = Cons.model_option
        sel_op = tk.StringVar()
        drop_down = ttk.Combobox(parent, textvariable=sel_op)
        drop_down['values'] = model_option
        drop_down.current(1)
        drop_down.place(x=model_txt['x'], y=model_txt['y'], height=model_txt['h'], width=model_txt['w'] - 3)
        drop_down.bind('<<ComboboxSelected>>', model_select)

        # model_txt_fld = Mf.make_element(x=model_txt['x'], y=model_txt['y'],
        #                                 h=model_txt['h'], w=model_txt['w'], element='Entry',
        #                                 bg=model_txt['bg'])

        fw_lbl = Mf.make_element(x=fw['x'], y=fw['y'],
                                 h=fw['h'], w=fw['w'], element='Label',
                                 bg=fw['bg'], text=fw['text'], anchor='center')
        self.fw_txt_fld = Mf.make_element(x=fw_txt['x'], y=fw_txt['y'],
                                     h=fw_txt['h'], w=fw_txt['w'], element='Entry',
                                     bg=fw_txt['bg'])

        # ============================================ Set Network Information ================================
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
        regi_btn = Cons.register_btn

        ip_lbl = Mf.make_element(x=ip['x'], y=ip['y'],
                                 h=ip['h'], w=ip['w'], element='Label',
                                 bg=ip['bg'], text=ip['text'], anchor='center')
        ip_txt_fld = Mf.make_element(x=ip_txt['x'], y=ip_txt['y'],
                                     h=ip_txt['h'], w=ip_txt['w'], element='Entry',
                                     bg=ip_txt['bg'])

        port_lbl = Mf.make_element(x=port['x'], y=port['y'],
                                   h=port['h'], w=port['w'], element='Label',
                                   bg=port['bg'], text=port['text'], anchor='center')
        port_txt_fld = Mf.make_element(x=port_txt['x'], y=port_txt['y'],
                                       h=port_txt['h'], w=port_txt['w'], element='Entry',
                                       bg=port_txt['bg'])

        rtsp_lbl = Mf.make_element(x=rtsp['x'], y=rtsp['y'],
                                   h=rtsp['h'], w=rtsp['w'], element='Label',
                                   bg=rtsp['bg'], text=rtsp['text'], anchor='center')
        rtsp_txt_fld = Mf.make_element(x=rtsp_txt['x'], y=rtsp_txt['y'],
                                       h=rtsp_txt['h'], w=rtsp_txt['w'], element='Entry',
                                       bg=rtsp_txt['bg'])

        ipc_id_lbl = Mf.make_element(x=ipc_id['x'], y=ipc_id['y'],
                                     h=ipc_id['h'], w=ipc_id['w'], element='Label',
                                     bg=ipc_id['bg'], text=ipc_id['text'], anchor='w')
        ipc_id_txt_fld = Mf.make_element(x=ipc_id_txt['x'], y=ipc_id_txt['y'],
                                         h=ipc_id_txt['h'], w=ipc_id_txt['w'], element='Entry',
                                         bg=ipc_id_txt['bg'])
        ipc_id_txt_fld.configure(show='*')

        ipc_pw_lbl = Mf.make_element(x=ipc_pw['x'], y=ipc_pw['y'],
                                     h=ipc_pw['h'], w=ipc_pw['w'], element='Label',
                                     bg=ipc_pw['bg'], text=ipc_pw['text'], anchor='w')
        ipc_pw_txt_fld = Mf.make_element(x=ipc_pw_txt['x'], y=ipc_pw_txt['y'],
                                         h=ipc_pw_txt['h'], w=ipc_pw_txt['w'], element='Entry',
                                         bg=ipc_pw_txt['bg'])
        ipc_pw_txt_fld.configure(show='*')

        self.register_btn = Mf.make_element(x=regi_btn['x'], y=regi_btn['y'],
                                            h=regi_btn['h'], w=regi_btn['w'], element='Button',
                                            bg=regi_btn['bg'], text=regi_btn['text'],
                                            anchor='center',
                                            command=open_video_window)

        # ===================================== Set Searching a command UI =====================================
        sear_txt = Cons.search_txt_fld_info
        sear_btn = Cons.search_btn

        search_txt_fld = Mf.make_element(x=sear_txt['x'], y=sear_txt['y'],
                                         h=sear_txt['h'], w=sear_txt['w'],
                                         bg=sear_txt['bg'], element='Entry')
        search_txt_fld.bind('<Return>', search_command)
        query_txt = search_txt_fld.get()
        # search_btn = Mf.make_element(x=sear_btn['x'], y=sear_btn['y'],
        #                              h=sear_btn['h'], w=sear_btn['w'], element='Button',
        #                              bg=sear_btn['bg'], text=sear_btn['text'],
        #                              anchor='center', command=search_command)

        self.search_btn = Mf.make_element(x=sear_btn['x'], y=sear_btn['y'],
                                          h=sear_btn['h'], w=sear_btn['w'], element='Button',
                                          bg=sear_btn['bg'], text=sear_btn['text'],
                                          anchor='center', command=search_command)

        # For Test Code
        # test_txt = {'ip': '192.168.100.153', 'port': '39190', 'rtsp_port': '8554', 'id': 'root', 'pw': 'root'}
        test_txt = {'ip': '192.168.100.155', 'port': '32000', 'rtsp_port': '554', 'id': 'root', 'pw': 'root'}
        ip_txt_fld.insert(0, test_txt['ip'])
        port_txt_fld.insert(0, test_txt['port'])
        rtsp_txt_fld.insert(0, test_txt['rtsp_port'])
        ipc_id_txt_fld.insert(0, test_txt['id'])
        ipc_pw_txt_fld.insert(0, test_txt['pw'])

        # ======================================== Set Command Table ===========================================
        column_name = Cons.column_array
        column_count = len(column_name)
        cmd_data = Cons.command_array

        treeview = Mf.make_table(parent, column_count, Cons.tree_view_size['w'], column_name,
                                 Cons.treeview_pos['x'], Cons.treeview_pos['y'], cmd_data)

        # ========================================== Log Text Field ============================================
        log_pos = Cons.log_txt_fld_info
        log_fld = Res.Response(parent, log_pos)

        # ========================================== System Information  ============================================
        sys_info_pos = Cons.sys_info_tab
        sys_info = SysInfo.SysInfo(parent, sys_info_pos)

        # ========================================= Set Script Table ===========================================
        script_tb = tb.Table(parent)

        # ======================== Set PTZ UI, interval, repeat, script mode, script run/stop/clear ============
        ptz_ui = pt.PTZ(parent)

        inter_lbl = Cons.interval_lbl
        inter_txt = Cons.interval_txt_fld
        inter_add_btn = Cons.interval_add_btn
        repe_lbl = Cons.repeat_lbl
        repe_txt = Cons.repeat_txt_fld
        scr_mode_lbl = Cons.script_mode_lbl
        scr_mode_btn = Cons.script_mode_btn
        r_btn = Cons.script_run_btn
        st_btn = Cons.script_stop_btn
        clr_btn = Cons.script_clear_btn

        # Set Interval, repeat lbl, textfield and Run Button
        interval_lbl = Mf.make_element(inter_lbl['x'], inter_lbl['y'],
                                       inter_lbl['h'], inter_lbl['w'],
                                       bg=inter_lbl['bg'], element='Label',
                                       text=inter_lbl['text'], anchor='center')

        interval_txt_fld = Mf.make_element(inter_txt['x'], inter_txt['y'],
                                           inter_txt['h'], inter_txt['w'],
                                           bg=inter_txt['bg'], element='Entry')

        Cons.interval_button = Mf.make_element(x=inter_add_btn['x'], y=inter_add_btn['y'],
                                               h=inter_add_btn['h'], w=inter_add_btn['w'], element='Button',
                                               bg=inter_add_btn['bg'], text=inter_add_btn['text'],
                                               anchor='center', command=interval_add)

        repeat_lbl = Mf.make_element(repe_lbl['x'], repe_lbl['y'],
                                     repe_lbl['h'], repe_lbl['w'],
                                     bg=repe_lbl['bg'], element='Label',
                                     text=repe_lbl['text'], anchor='center')

        repeat_txt_fld = Mf.make_element(repe_txt['x'], repe_txt['y'],
                                         repe_txt['h'], repe_txt['w'],
                                         bg=repe_txt['bg'], element='Entry')
        repeat_txt_fld.insert(0, 1)

        # Set a Script Mode Slide and Run Button
        scr_mode_lbl = Mf.make_element(scr_mode_lbl['x'], scr_mode_lbl['y'],
                                       scr_mode_lbl['h'], scr_mode_lbl['w'],
                                       bg=scr_mode_lbl['bg'], element='Label',
                                       text=scr_mode_lbl['text'], anchor='center')
        script_btn_id = 'SCRIPT'
        script_mode_ui = onoffSW.SwitchOnOff(parent, None, script_btn_id, Cons.script_mode_btn)

        self.script_run_btn = Mf.make_element(r_btn['x'], r_btn['y'],
                                              r_btn['h'], r_btn['w'],
                                              bg=r_btn['bg'], element='Button',
                                              text=r_btn['text'], anchor='center', command=start_thread)

        self.script_stop_btn = Mf.make_element(st_btn['x'], st_btn['y'],
                                               st_btn['h'], st_btn['w'],
                                               bg=st_btn['bg'], element='Button',
                                               text=st_btn['text'], anchor='center', command=stop_script)

        self.script_clear_btn = Mf.make_element(clr_btn['x'], clr_btn['y'],
                                                clr_btn['h'], clr_btn['w'],
                                                bg=clr_btn['bg'], element='Button',
                                                text=clr_btn['text'], anchor='center', command=clr_script)


# TODO: (2024.07.19): Command File Import Function
# TODO: (2024.07.19): Generate exe format
# TODO: (2024.07.25): When script mode, need to apply repeat count

if __name__ == '__main__':
    root = tk.Tk()

    app = TestTool(root)
    root.mainloop()
