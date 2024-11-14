import tkinter as tk
import time as ti

import Communication as Comm
import Constant as Cons
import Communication as Th
import OnOff_Switch as onoffSW
import System_Info as sysinfo

d_click_detected = False
press_time = 0


class PTZ:
    def __init__(self, root):
        self.root = root

        self.canvas = tk.Canvas(root, width=Cons.ptz_canvas['w'], height=Cons.ptz_canvas['h'])
        self.canvas.place(x=Cons.ptz_canvas['x'], y=Cons.ptz_canvas['y'] + 5)

        ptz_osd_mode_btn = {'x': Cons.ptz_left_btn['x'] - (Cons.ptz_left_btn['w'] / 2) - 2,
                            'y': Cons.ptz_up_btn['y'] - Cons.ptz_up_btn['h']}
        btn_id = 'PTZ_OSD'
        self.ptz_osd_mode_ui = onoffSW.SwitchOnOff(self, self.canvas, btn_id, ptz_osd_mode_btn)

        self.ptz_url = '/cgi-bin/ptz/control.php?'

        self.refresh_ptz()

    # def create_button(self, text, push_cmd, release_cmd, x, y):
    #     if not Cons.ptz_osd_toggle_flag:
    #         btn = tk.Button(self.canvas, text=text, width=6, height=2, bg=Cons.my_color['bg'], command=push_cmd)
    #     else:
    #         btn = tk.Button(self.canvas, text=text, width=6, height=2, bg=Cons.my_color['bg'])
    #         btn.bind('<ButtonPress-1>', lambda event: push_cmd(event))
    #         btn.bind('<ButtonRelease-1>', lambda event: release_cmd(event))
    #     self.canvas.create_window(x, y, window=btn)

    def create_button(self, text, push_cmd, release_cmd, x, y):
        btn = tk.Button(self.canvas, text=text, bg=Cons.my_color['bg'])

        # Bind ButtonPress (push event) regardless of the flag
        btn.bind('<ButtonPress-1>', lambda event: push_cmd(event))
        # Bind ButtonRelease (release event)
        btn.bind('<ButtonRelease-1>', lambda event: release_cmd(event))

        # Place the button on the canvas
        self.canvas.create_window(x, y, window=btn, width=Cons.ptz_btn_size, height=Cons.ptz_btn_size)

    # (2024.09.26) Add diagonal direction Button
    def left_top(self, event=None):
        if not Cons.ptz_osd_toggle_flag:
            if Cons.selected_model == 'FineTree':
                params = {'move': 'upleft'}
                Comm.fine_tree_send_cgi(self.ptz_url, params)
            elif Cons.selected_model == 'DRS':
                params = {'move': 'upleft'}
                Comm.send_cmd_to_Finetree(self.ptz_url, params)
        else:
            print('Pressed Left Top')

    # (2024.07.19) modified so that commands sent from PTZ are also switched when model is changed
    # (20204.11.14): Added DRS Zoom Module
    def up_zoom_in(self, event=None):
        if not Cons.ptz_osd_toggle_flag:
            if Cons.selected_model == 'Uncooled':
                # OSD Uncooled
                self.send_data('FF01E024000005')
            elif Cons.selected_model == 'NYX Series':
                # OSD NYX
                up_cmd = 'NYX.SET#isp0_guic=up'
                Comm.send_data_with_cmd_for_nyx_ptz(self.root, up_cmd)
            elif Cons.selected_model == 'FineTree':
                params = {'move': 'up'}
                Comm.fine_tree_send_cgi(self.ptz_url, params)
            elif Cons.selected_model == 'DRS':
                params = {'move': 'up'}
                Comm.send_cmd_to_Finetree(self.ptz_url, params)

        else:
            if Cons.selected_model == 'Uncooled':
                # PTZ Uncooled
                self.send_data('FF010020000021')
            elif Cons.selected_model == 'NYX Series':
                # Zoom In NYX
                zoom_in = 'NYX.SET#lens_zctl=narrow'
                Comm.send_data_with_cmd_for_nyx_ptz(self.root, zoom_in)
            elif Cons.selected_model == 'FineTree':
                params = {'zoom': 'tele'}
                Comm.fine_tree_send_cgi(self.ptz_url, params)
            elif Cons.selected_model == 'DRS':
                host = Cons.selected_ch['ip']
                input_port = Cons.selected_ch['port']
                port = int(0) if Cons.port == '' else int(input_port)
                # Zoom In
                hex_array = [255, 0, 34, 0, 0, 1, 35]
                Comm.send_cmd_for_drs(host, port, hex_array, self.root)

    def right_top(self, event=None):
        if not Cons.ptz_osd_toggle_flag:
            if Cons.selected_model == 'FineTree':
                params = {'move': 'upright'}
                Comm.fine_tree_send_cgi(self.ptz_url, params)
            elif Cons.selected_model == 'DRS':
                params = {'move': 'upright'}
                Comm.send_cmd_to_Finetree(self.ptz_url, params)
        else:
            print('Pressed Right Top')

    def left_down(self, event=None):
        if not Cons.ptz_osd_toggle_flag:
            if Cons.selected_model == 'FineTree':
                params = {'move': 'downleft'}
                Comm.fine_tree_send_cgi(self.ptz_url, params)
            elif Cons.selected_model == 'DRS':
                params = {'move': 'downleft'}
                Comm.send_cmd_to_Finetree(self.ptz_url, params)
        else:
            print('Pressed Left Bottom')

    def down_zoom_out(self, event=None):
        if not Cons.ptz_osd_toggle_flag:
            if Cons.selected_model == 'Uncooled':
                # OSD Uncooled
                self.send_data('FF01E025000006')
            elif Cons.selected_model == 'NYX Series':
                # OSD NYX
                down_cmd = 'NYX.SET#isp0_guic=down'
                Comm.send_data_with_cmd_for_nyx_ptz(self.root, down_cmd)
            elif Cons.selected_model == 'FineTree':
                params = {'move': 'down'}
                Comm.fine_tree_send_cgi(self.ptz_url, params)
            elif Cons.selected_model == 'DRS':
                params = {'move': 'down'}
                Comm.send_cmd_to_Finetree(self.ptz_url, params)
        else:
            if Cons.selected_model == 'Uncooled':
                # Uncooled Zoom Out
                self.send_data('FF010040000041')
            elif Cons.selected_model == 'NYX Series':
                # Zoom Out NYX
                zoom_out = 'NYX.SET#lens_zctl=wide'
                Comm.send_data_with_cmd_for_nyx_ptz(self.root, zoom_out)
            elif Cons.selected_model == 'FineTree':
                params = {'zoom': 'wide'}
                Comm.fine_tree_send_cgi(self.ptz_url, params)
            elif Cons.selected_model == 'DRS':
                host = Cons.selected_ch['ip']
                input_port = Cons.selected_ch['port']
                port = int(0) if Cons.port == '' else int(input_port)
                # Zoom Out
                hex_array = [255, 0, 34, 0, 0, 2, 36]
                Comm.send_cmd_for_drs(host, port, hex_array, self.root)

    def right_down(self, event=None):
        if not Cons.ptz_osd_toggle_flag:
            if Cons.selected_model == 'FineTree':
                params = {'move': 'downright'}
                Comm.fine_tree_send_cgi(self.ptz_url, params)
            elif Cons.selected_model == 'DRS':
                params = {'move': 'downright'}
                Comm.send_cmd_to_Finetree(self.ptz_url, params)
        else:
            print('Pressed Right Bottom')

    def left_near(self, event=None):
        print("Left button pressed")
        if not Cons.ptz_osd_toggle_flag:
            if Cons.selected_model == 'Uncooled':
                # OSD Uncooled
                self.send_data('FF01E022000003')
            elif Cons.selected_model == 'NYX Series':
                # OSD NYX
                left_cmd = 'NYX.SET#isp0_guic=left'
                Comm.send_data_with_cmd_for_nyx_ptz(self.root, left_cmd)
            elif Cons.selected_model == 'FineTree':
                params = {'move': 'left'}
                Comm.fine_tree_send_cgi(self.ptz_url, params)
            elif Cons.selected_model == 'DRS':
                params = {'move': 'left'}
                Comm.send_cmd_to_Finetree(self.ptz_url, params)
        else:
            if Cons.selected_model == 'Uncooled':
                # Near Uncooled
                self.send_data('FF010100000002')
            elif Cons.selected_model == 'NYX Series':
                # Near NYX
                near = 'NYX.SET#lens_fctl=near'
                Comm.send_data_with_cmd_for_nyx_ptz(self.root, near)
            elif Cons.selected_model == 'FineTree':
                params = {'focus': 'near'}
                Comm.fine_tree_send_cgi(self.ptz_url, params)
            elif Cons.selected_model == 'DRS':
                host = Cons.selected_ch['ip']
                input_port = Cons.selected_ch['port']
                port = int(0) if Cons.port == '' else int(input_port)
                # Near
                hex_array = [255, 0, 34, 16, 0, 2, 52]
                Comm.send_cmd_for_drs(host, port, hex_array, self.root)

    def right_far(self, event=None):
        if not Cons.ptz_osd_toggle_flag:
            if Cons.selected_model == 'Uncooled':
                # OSD Uncooled
                self.send_data('FF01E023000004')
            elif Cons.selected_model == 'NYX Series':
                # OSD NYX
                right_cmd = 'NYX.SET#isp0_guic=right'
                Comm.send_data_with_cmd_for_nyx_ptz(self.root, right_cmd)
            elif Cons.selected_model == 'FineTree':
                params = {'move': 'right'}
                Comm.fine_tree_send_cgi(self.ptz_url, params)
            elif Cons.selected_model =='DRS':
                params = {'move': 'right'}
                Comm.send_cmd_to_Finetree(self.ptz_url, params)
        else:
            if Cons.selected_model == 'Uncooled':
                # Far Uncooled
                self.send_data('FF010080000081')
            elif Cons.selected_model == 'NYX Series':
                # Far NYX
                far = 'NYX.SET#lens_fctl=far'
                Comm.send_data_with_cmd_for_nyx_ptz(self.root, far)
            elif Cons.selected_model == 'FineTree':
                params = {'focus': 'far'}
                Comm.fine_tree_send_cgi(self.ptz_url, params)
            elif Cons.selected_model == 'DRS':
                host = Cons.selected_ch['ip']
                input_port = Cons.selected_ch['port']
                port = int(0) if Cons.port == '' else int(input_port)
                # Far
                hex_array = [255, 0, 34, 16, 0, 1, 51]
                Comm.send_cmd_for_drs(host, port, hex_array, self.root)

    def osd_af(self, event):
        if not Cons.ptz_osd_toggle_flag:
            if Cons.selected_model == 'Uncooled':
                # OSD Uncooled
                self.send_data('FF01E021000002')
            elif Cons.selected_model == 'NYX Series':
                # OSD NYX
                osd_cmd = 'NYX.SET#isp0_guie=on'
                Comm.send_data_with_cmd_for_nyx_ptz(self.root, osd_cmd)
        else:
            if Cons.selected_model == 'Uncooled':
                # AF Uncooled
                sys_info_pos = Cons.sys_info_tab
                sys_info = sysinfo.SysInfo(self.root, sys_info_pos)
                self.send_data('FF01A0110000B2')
                if Cons.ptz_osd_toggle_flag:
                    ti.sleep(10)
                    sys_info.update_with_protocol()
                else:
                    return
            elif Cons.selected_model == 'NYX Series':
                # AF NYX
                af = 'NYX.SET#lens_afex=execute'
                Comm.send_data_with_cmd_for_nyx_ptz(self.root, af)
            elif Cons.selected_model == 'FineTree':
                params = {'focus': 'pushaf'}
                Comm.fine_tree_send_cgi(self.ptz_url, params)
            elif Cons.selected_model == 'DRS':
                host = Cons.selected_ch['ip']
                input_port = Cons.selected_ch['port']
                port = int(0) if Cons.port == '' else int(input_port)
                # AF
                hex_array = [255, 0, 34, 32, 0, 0, 66]
                Comm.send_cmd_for_drs(host, port, hex_array, self.root)

    def release_cmd(self, event):
        print("Button released")
        btn = event.widget
        btn_text = btn.cget('text')

        sys_info_pos = Cons.sys_info_tab
        sys_info = sysinfo.SysInfo(self.root, sys_info_pos)
        ptz_text_arr = ['Left\nTop', 'Up', 'Right\nTop', 'Left\nDown', 'Down', 'Right\nDown', 'Left', 'Right']

        if Cons.selected_model == 'Uncooled':
            # All Stop
            self.send_data('FF010000000001')
            if Cons.ptz_osd_toggle_flag:
                ti.sleep(0.2)
                sys_info.update_with_protocol()
            else:
                return

        elif Cons.selected_model == 'NYX Series':
            if btn_text in ['Zoom\nIn', 'Zoom\nOut']:
                self.zoom_focus_stop_for_nyx('zoom')
            elif btn_text in ['Near', 'Far']:
                self.zoom_focus_stop_for_nyx('focus')
        elif Cons.selected_model == 'FineTree':
            if btn_text in ['Zoom\nIn', 'Zoom\nOut']:
                print('fi zoom')
                params = {'zoom': 'stop'}
                Comm.fine_tree_send_cgi(self.ptz_url, params)
            elif btn_text in ['Near', 'Far']:
                print('fi focus')
                params = {'focus': 'stop'}
                Comm.fine_tree_send_cgi(self.ptz_url, params)
            elif btn_text in ptz_text_arr:
                print('fi PTZ')
                params = {'move': 'stop'}
                Comm.fine_tree_send_cgi(self.ptz_url, params)
        elif Cons.selected_model == 'DRS':
            if btn_text in ['Zoom\nIn', 'Zoom\nOut']:
                print('DRS zoom')
                host = Cons.selected_ch['ip']
                input_port = Cons.selected_ch['port']
                port = int(0) if Cons.port == '' else int(input_port)
                # Zoom Stop
                hex_array = [255, 0, 34, 4, 0, 0, 38]
                Comm.send_cmd_for_drs(host, port, hex_array, self.root)
            elif btn_text in ['Near', 'Far']:
                print('DRS focus')
                host = Cons.selected_ch['ip']
                input_port = Cons.selected_ch['port']
                port = int(0) if Cons.port == '' else int(input_port)
                # Focus Stop
                hex_array = [255, 0, 34, 19, 0, 0, 53]
                Comm.send_cmd_for_drs(host, port, hex_array, self.root)
            elif btn_text in ptz_text_arr:
                print('DRS PTZ')
                params = {'move': 'stop'}
                Comm.send_cmd_to_Finetree(self.ptz_url, params)

        ti.sleep(0.1)

    def zoom_focus_stop_for_nyx(self, btn_str):
        if btn_str == 'zoom':
            zoom_stop = 'NYX.SET#lens_zctl=stop'
            Comm.send_data_with_cmd_for_nyx_ptz(self.root, 'NYX.SET#lens_zctl=stop')
        elif btn_str == 'focus':
            focus_stop = 'NYX.SET#lens_fctl=stop'
            Comm.send_data_with_cmd_for_nyx_ptz(self.root, 'NYX.SET#lens_fctl=stop')

    def set_nyx_osd(self, event=None):
        set_cmd = 'NYX.SET#isp0_guic=set'
        Comm.send_data_with_cmd_for_nyx_ptz(self.root, set_cmd)

    def send_data(self, cmd):
        hex_array = [int(cmd[i:i + 2], 16) for i in range(0, len(cmd), 2)]
        Th.send_cmd_for_uncooled(hex_array, 'Normal Query', self.root)

    def create_circle_button(self, x, y, r, color, text, command):
        oval = self.canvas.create_oval(x - r + 5, y - r - 12, x + r, y + r - 14, fill=color, outline=color)
        text_id = self.canvas.create_text(x + 3, y - 14, text=text)

        def on_press(event):
            self.canvas.itemconfig(oval, fill='beige', outline='beige')

        def on_release(event):
            self.canvas.itemconfig(oval, fill=color, outline=color)
            command(event)

        self.canvas.tag_bind(oval, '<ButtonPress-1>', on_press)
        self.canvas.tag_bind(oval, '<ButtonRelease-1>', on_release)

        self.canvas.tag_bind(text_id, '<ButtonPress-1>', on_press)
        self.canvas.tag_bind(text_id, '<ButtonRelease-1>', on_release)

        return oval

    # (2024.09.25): add a PTZ 8 Direction UI(move toggle sw and set button)
    def refresh_ptz(self):
        self.canvas.delete('all')
        if not Cons.ptz_osd_toggle_flag:
            button_configurations = [
                ('Left\nTop', self.left_top, self.release_cmd, Cons.ptz_up_left_btn['x'], Cons.ptz_up_left_btn['y']),
                ('Up', self.up_zoom_in, self.release_cmd, Cons.ptz_up_btn['x'], Cons.ptz_up_btn['y']),
                ('Right\nTop', self.right_top, self.release_cmd, Cons.ptz_up_right_btn['x'],
                 Cons.ptz_up_right_btn['y']),
                ('Left\nDown', self.left_down, self.release_cmd, Cons.ptz_down_left_btn['x'],
                 Cons.ptz_down_left_btn['y']),
                ('Down', self.down_zoom_out, self.release_cmd, Cons.ptz_down_btn['x'], Cons.ptz_down_btn['y']),
                ('Right\nDown', self.right_down, self.release_cmd, Cons.ptz_down_right_btn['x'],
                 Cons.ptz_down_right_btn['y']),
                ('Left', self.left_near, self.release_cmd, Cons.ptz_left_btn['x'], Cons.ptz_left_btn['y']),
                ('Right', self.right_far, self.release_cmd, Cons.ptz_right_btn['x'], Cons.ptz_right_btn['y']),
            ]

        else:
            button_configurations = [
                ('Zoom\nIn', self.up_zoom_in, self.release_cmd, Cons.ptz_up_btn['x'], Cons.ptz_up_btn['y']),
                ('Zoom\nOut', self.down_zoom_out, self.release_cmd, Cons.ptz_down_btn['x'], Cons.ptz_down_btn['y']),
                ('Near', self.left_near, self.release_cmd, Cons.ptz_left_btn['x'], Cons.ptz_left_btn['y']),
                ('Far', self.right_far, self.release_cmd, Cons.ptz_right_btn['x'], Cons.ptz_right_btn['y'])
            ]

        for text, push_cmd, release_cmd, x, y in button_configurations:
            self.create_button(text, push_cmd, release_cmd, x, y)

        center_text = 'AF' if Cons.ptz_osd_toggle_flag else 'OSD'
        self.create_circle_button(Cons.ptz_canvas['w'] / 2, Cons.ptz_canvas['h'] / 2, 22, Cons.my_color['bg'],
                                  center_text, self.osd_af)

        # Create a Set Button for NYX Series
        if (not Cons.ptz_osd_toggle_flag) and (Cons.selected_model == 'NYX Series'):
            set_btn = tk.Button(self.canvas, text='Set', bg=Cons.my_color['bg'],
                                command=self.set_nyx_osd)
            self.canvas.create_window(Cons.set_nyx_btn['x'], Cons.set_nyx_btn['y'] + 5, window=set_btn, width=40,
                                      height=20)
            set_btn.config(state='normal')
        else:
            set_btn = tk.Button(self.canvas, text='Set', bg=Cons.my_color['bg'],
                                command=self.set_nyx_osd)
            self.canvas.create_window(Cons.set_nyx_btn['x'], Cons.set_nyx_btn['y'] + 5, window=set_btn, width=40,
                                      height=20)
            set_btn.config(state='disabled')
