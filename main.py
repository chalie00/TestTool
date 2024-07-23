# -*- coding: utf-8 -*-
import tkinter
import tkinter as tk
import cv2
import threading
import time

import Constant as Cons
import MainFunction as Mf
import Communication as Comm
import VideoPlayer as Vp
import Ptz as pt
import OnOff_Switch as onoffSW
import Table as tb
import Response as Res
import System_Info as SysInfo

# from ttkwidgets import CheckboxTreeview
from tkinter import *
from PIL import ImageTk, Image
from tkinter import ttk


class TestTool(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        # Set Title
        parent.title('Test Tool')
        parent.geometry(f'{Cons.WINDOWS_SIZE["x"]}x{Cons.WINDOWS_SIZE["y"]}+'
                        f'{Cons.WINDOWS_POSITION["x"]}+{Cons.WINDOWS_POSITION["y"]}')
        parent.config(padx=15, pady=15)

        # self.canvas = tk.Canvas(parent, width=Cons.camera_resolution['w'],
        #                         height=Cons.camera_resolution['h'], bg='red')
        # self.canvas.place(x=0, y=0)

        self.thread_running = False

        # Check Main Window Position

        # Open RTSP and Get the Network Information from User Input
        def open_video_window():
            Cons.host_ip = ip_txt_fld.get()
            Cons.port = port_txt_fld.get()
            Cons.rtsp_port = rtsp_txt_fld.get()
            Cons.ipc_id = ipc_id_txt_fld.get()
            Cons.ipc_pw = ipc_pw_txt_fld.get()
            # Cons.rtsp_url = rf'rtsp://{ipc_id_txt_fld.get()}:{ipc_pw_txt_fld.get()}@{ip_txt_fld.get()}:{rtsp_txt_fld.get()}/cam0_0'
            Cons.rtsp_url = rf'rtsp://{ipc_id_txt_fld.get()}:{ipc_pw_txt_fld.get()}@{ip_txt_fld.get()}:{rtsp_txt_fld.get()}/test'
            # video_window = tk.Toplevel(parent)
            # video_window.title("RTSP Video Player")
            video_player = Vp.VideoPlayer(parent, Cons.rtsp_url)
            print(Cons.rtsp_url)
            video_player.start_video()

        # Get the stream from Camera
        def get_stream_from_camera():
            rtsp_add = Cons.rtsp_url
            print(rtsp_add)
            cap_file = cv2.VideoCapture(rtsp_add)
            width = cap_file.get(cv2.CAP_PROP_FRAME_WIDTH)
            height = cap_file.get(cv2.CAP_PROP_FRAME_HEIGHT)
            # stream_lbl = Label(parent)
            # stream_lbl.grid(row=3, column=0)
            _, frame = cap_file.read()
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            self.canvas.create_image(3, 0, image=imgtk, anchor=tkinter.center)
            parent.after(1, get_stream_from_camera())
            # stream_lbl.imgtk = imgtk
            # stream_lbl.configure(image=imgtk)
            # stream_lbl.after(1, get_stream_from_camera)

        # (2024.07.19): Model Drop Down Menu function
        def model_select(event):
            current_sel = sel_op.get()
            if current_sel in ['NYX Series', 'Uncooled']:
                Cons.selected_model = current_sel
                col_name = Cons.column_array
                col_count = len(col_name)
                command_data = Mf.get_data_from_csv(Cons.cmd_path)

                Mf.make_table(parent, col_count, Cons.tree_view_size['w'], col_name,
                              Cons.treeview_pos['x'], Cons.treeview_pos['y'], command_data)
                ptz_ui.refresh_ptz()

        # Search a protocol which user typed text
        def search_command():
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
            row_cmd_title = len(Cons.script_hex_arrays)
            col_interval = len(Cons.interval_arrays)

            for i, cmd_list in enumerate(Cons.interval_arrays):
                Cons.cmd_itv_arrays[i][0] = Cons.script_cmd_titles[i]
                Cons.cmd_itv_arrays[i][1] = Cons.interval_arrays[i]

            Mf.check_interval_active()
            print(Cons.cmd_itv_arrays)
            tb.Table(parent)

        # (2024.07.04): Start thread with selected script
        def start_thread():
            if not self.thread_running:
                self.thread_running = True
                self.thread = threading.Thread(target=run_script)
                self.thread.start()

        # (2024.07.04): Start thread with selected script
        def run_script() -> []:
            while self.thread_running:
                script_run_btn.config(state='disabled')
                script_stop_btn.config(state='normal')
                Cons.data_sending = True
                if Cons.script_toggle_flag:
                    print('run script')
                    interval = Cons.interval_arrays
                    repeat = int(repeat_txt_fld.get())
                    script = Cons.script_hex_arrays
                    titles = Cons.script_cmd_titles
                    Comm.send_data_with_interval(interval, repeat, script, titles, parent)
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
                    Comm.send_data_with_interval(interval, repeat, hex_protocol, titles, parent)

                    return hex_protocol
                time.sleep(1)

        # (2024.07.04): Stop Script(Threading Stop)
        def stop_script():
            Cons.data_sending = False
            script_run_btn.config(state='normal')
            script_stop_btn.config(state='disabled')
            print('stop script')
            self.thread_running = False
            self.thread.join()

        # (2024.07.04): Clear the Script Table
        def clr_script():
            Cons.data_sending = False
            script_run_btn.config(state='normal')
            script_stop_btn.config(state='normal')
            print('clear script')
            Mf.clr_table_arrays(parent)

        # ================================================ UI Layout ============================================

        # ======================================== Input User, Model Information ================================
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
        # model_option = ['Uncooled', 'NYX Series']
        model_option = Cons.model_option
        sel_op = tk.StringVar()
        drop_down = ttk.Combobox(parent, textvariable=sel_op)
        drop_down['values'] = model_option
        drop_down.current(0)
        drop_down.place(x=model_txt['x'], y=model_txt['y'], height=model_txt['h'], width=model_txt['w'] - 3)
        drop_down.bind('<<ComboboxSelected>>', model_select)

        # model_txt_fld = Mf.make_element(x=model_txt['x'], y=model_txt['y'],
        #                                 h=model_txt['h'], w=model_txt['w'], element='Entry',
        #                                 bg=model_txt['bg'])

        fw_lbl = Mf.make_element(x=fw['x'], y=fw['y'],
                                 h=fw['h'], w=fw['w'], element='Label',
                                 bg=fw['bg'], text=fw['text'], anchor='center')
        fw_txt_fld = Mf.make_element(x=fw_txt['x'], y=fw_txt['y'],
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

        register_btn = Mf.make_element(x=regi_btn['x'], y=regi_btn['y'],
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
        query_txt = search_txt_fld.get()
        # search_btn = Mf.make_element(x=sear_btn['x'], y=sear_btn['y'],
        #                              h=sear_btn['h'], w=sear_btn['w'], element='Button',
        #                              bg=sear_btn['bg'], text=sear_btn['text'],
        #                              anchor='center', command=search_command)

        search_btn = Mf.make_element(x=sear_btn['x'], y=sear_btn['y'],
                                     h=sear_btn['h'], w=sear_btn['w'], element='Button',
                                     bg=sear_btn['bg'], text=sear_btn['text'],
                                     anchor='center', command=search_command)

        # For Test Code
        test_txt = {'ip': '192.168.100.234', 'port': '39190', 'rtsp_port': '8554', 'id': 'root', 'pw': 'root'}
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

        script_run_btn = Mf.make_element(r_btn['x'], r_btn['y'],
                                         r_btn['h'], r_btn['w'],
                                         bg=r_btn['bg'], element='Button',
                                         text=r_btn['text'], anchor='center', command=start_thread)

        script_stop_btn = Mf.make_element(st_btn['x'], st_btn['y'],
                                          st_btn['h'], st_btn['w'],
                                          bg=st_btn['bg'], element='Button',
                                          text=st_btn['text'], anchor='center', command=stop_script)

        script_clear_btn = Mf.make_element(clr_btn['x'], clr_btn['y'],
                                           clr_btn['h'], clr_btn['w'],
                                           bg=clr_btn['bg'], element='Button',
                                           text=clr_btn['text'], anchor='center', command=clr_script)


if __name__ == '__main__':
    root = tk.Tk()

    app = TestTool(root)
    root.mainloop()


# TODO: (2024.07.19): Command File Import Function
# TODO: (2024.07.19): Generate exe format
# TODO: (2024.07.23): Need to modify Cooled Type System Information
