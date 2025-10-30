import tkinter as tk
import time as ti
import threading

import Communication as Comm
import Constant as Cons
import Communication as Th
import OnOff_Switch as onoffSW
import System_Info as sysinfo

from icecream import ic

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
        self.ft_sending_flag = False

        self.buttons = {}

        self.refresh_ptz()

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
            elif Cons.selected_model == 'MiniGimbal':
                self.send_miniGimbal('up_left')
            elif Cons.selected_model == 'Multi':
                self.send_pt_drv('left_top', 'pt_drv')

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
                # it should be modified to http://ip/cgi-bin/ptz/conmtrol.php?move=up&pspd=63
                params = {'move': 'up'}
                Comm.fine_tree_send_cgi(self.ptz_url, params)
            elif Cons.selected_model == 'DRS':
                params = {'move': 'up'}
                Comm.send_cmd_to_Finetree(self.ptz_url, params)
            elif Cons.selected_model == 'MiniGimbal':
                # Move Up
                self.send_miniGimbal('up')
            elif Cons.selected_model == 'Multi':
                self.send_pt_drv('up', 'pt_drv')

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
                port = int(Cons.selected_ch['port']) if Cons.selected_ch['port'] else 0
                # Zoom In
                hex_array = [255, 0, 34, 0, 0, 1, 35]
                Comm.send_cmd_for_drs(host, port, hex_array, self.root)
            elif Cons.selected_model == 'MiniGimbal':
                # Optical Zoom In
                self.send_miniGimbal('op_zoom_in')
            elif Cons.selected_model == 'Multi':
                self.send_pt_drv('zoom_in', 'eo')
                self.send_pt_drv('zoom_in', 'ir')

    def right_top(self, event=None):
        if not Cons.ptz_osd_toggle_flag:
            if Cons.selected_model == 'FineTree':
                params = {'move': 'upright'}
                Comm.fine_tree_send_cgi(self.ptz_url, params)
            elif Cons.selected_model == 'DRS':
                params = {'move': 'upright'}
                Comm.send_cmd_to_Finetree(self.ptz_url, params)
            elif Cons.selected_model == 'MiniGimbal':
                self.send_miniGimbal('up_right')
            elif Cons.selected_model == 'Multi':
                self.send_pt_drv('right_top', 'pt_drv')
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
            elif Cons.selected_model == 'MiniGimbal':
                self.send_miniGimbal('down_left')
            elif Cons.selected_model == 'Multi':
                self.send_pt_drv('left_down', 'pt_drv')
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
            elif Cons.selected_model == 'MiniGimbal':
                # Move Down
                self.send_miniGimbal('down')
            elif Cons.selected_model == 'Multi':
                self.send_pt_drv('down', 'pt_drv')
        else:
            if Cons.selected_model in ['Uncooled', 'Multi']:
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
                port = int(Cons.selected_ch['port']) if Cons.selected_ch['port'] else 0
                # Zoom Out
                hex_array = [255, 0, 34, 0, 0, 2, 36]
                Comm.send_cmd_for_drs(host, port, hex_array, self.root)
            elif Cons.selected_model == 'MiniGimbal':
                # Optical Zoom Out
                self.send_miniGimbal('op_zoom_out')
            elif Cons.selected_model == 'Multi':
                self.send_pt_drv('zoom_out', 'eo')
                self.send_pt_drv('zoom_out', 'ir')

    def right_down(self, event=None):
        if not Cons.ptz_osd_toggle_flag:
            if Cons.selected_model == 'FineTree':
                params = {'move': 'downright'}
                Comm.fine_tree_send_cgi(self.ptz_url, params)
            elif Cons.selected_model == 'DRS':
                params = {'move': 'downright'}
                Comm.send_cmd_to_Finetree(self.ptz_url, params)
            elif Cons.selected_model == 'MiniGimbal':
                self.send_miniGimbal('down_right')
            elif Cons.selected_model == 'Multi':
                self.send_pt_drv('right_down', 'pt_drv')
        else:
            print('Pressed Right Bottom')

    # (2024.11.15) Send finetree focus cmd every 1 second
    def send_ft_command_periodically(self, ptz_url, params, interval=0.1):
        def send_command():
            if self.ft_sending_flag:
                Comm.fine_tree_send_cgi(self.ptz_url, params)
                threading.Timer(interval, send_command).start()

        send_command()

    def left_near(self, event=None):
        # print("Left button pressed")
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
            elif Cons.selected_model == 'MiniGimbal':
                # Move Left
                self.send_miniGimbal('left')
            elif Cons.selected_model == 'Multi':
                self.send_pt_drv('left', 'pt_drv')
        else:
            if Cons.selected_model == 'Uncooled':
                # Near Uncooled
                self.send_data('FF010100000002')
            elif Cons.selected_model == 'NYX Series':
                # Near NYX
                near = 'NYX.SET#lens_fctl=near'
                Comm.send_data_with_cmd_for_nyx_ptz(self.root, near)
            elif Cons.selected_model == 'FineTree':
                self.ft_sending_flag = True
                params = {'focus': 'near_step'}
                self.send_ft_command_periodically(self.ptz_url, params)
            elif Cons.selected_model == 'DRS':
                host = Cons.selected_ch['ip']
                port = int(Cons.selected_ch['port']) if Cons.selected_ch['port'] else 0
                # Near
                hex_array = [255, 0, 34, 16, 0, 2, 52]
                Comm.send_cmd_for_drs(host, port, hex_array, self.root)
            elif Cons.selected_model == 'MiniGimbal':
                # Near
                self.send_miniGimbal('op_near')
            elif Cons.selected_model == 'Multi':
                self.send_pt_drv('near', 'eo')
                self.send_pt_drv('near', 'ir')

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
            elif Cons.selected_model == 'DRS':
                params = {'move': 'right'}
                Comm.send_cmd_to_Finetree(self.ptz_url, params)
            elif Cons.selected_model == 'MiniGimbal':
                # Move Right
                self.send_miniGimbal('right')
            elif Cons.selected_model == 'Multi':
                self.send_pt_drv('right', 'pt_drv')
        else:
            if Cons.selected_model == 'Uncooled':
                # Far Uncooled
                self.send_data('FF010080000081')
            elif Cons.selected_model == 'NYX Series':
                # Far NYX
                far = 'NYX.SET#lens_fctl=far'
                Comm.send_data_with_cmd_for_nyx_ptz(self.root, far)
            elif Cons.selected_model == 'FineTree':
                self.ft_sending_flag = True
                params = {'focus': 'far_step'}
                self.send_ft_command_periodically(self.ptz_url, params)
            elif Cons.selected_model == 'DRS':
                host = Cons.selected_ch['ip']
                port = int(Cons.selected_ch['port']) if Cons.selected_ch['port'] else 0
                # Far
                hex_array = [255, 0, 34, 16, 0, 1, 51]
                Comm.send_cmd_for_drs(host, port, hex_array, self.root)
            elif Cons.selected_model == 'MiniGimbal':
                # Far
                self.send_miniGimbal('op_far')
            elif Cons.selected_model == 'Multi':
                self.send_pt_drv('far', 'eo')
                self.send_pt_drv('far', 'ir')

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
                port = int(Cons.selected_ch['port']) if Cons.selected_ch['port'] else 0
                # AF
                hex_array = [255, 0, 34, 32, 0, 0, 66]
                Comm.send_cmd_for_drs(host, port, hex_array, self.root)
            elif Cons.selected_model == 'MiniGimbal':
                # Far
                self.send_miniGimbal('op_af')

    def release_cmd(self, event):
        # print("Button released")
        btn = event.widget
        btn_text = btn.cget('text')

        ptz_text_arr = ['Left\nTop', 'Up', 'Right\nTop', 'Left\nDown', 'Down', 'Right\nDown', 'Left', 'Right']

        if Cons.selected_model == 'Uncooled':
            # All Stop
            self.send_data('FF010000000001')
            if Cons.ptz_osd_toggle_flag:
                ti.sleep(0.2)
                sys_info_pos = Cons.sys_info_tab
                sys_info = sysinfo.SysInfo(self.root, sys_info_pos)
                sys_info.update_with_protocol()
        elif Cons.selected_model in ['NYX Series', 'FineTree', 'DRS', 'MiniGimbal']:
            if btn_text in ['Zoom\nIn', 'Zoom\nOut']:
                self.stop_zoom_focus(Cons.selected_model, 'zoom')
            elif btn_text in ['Near', 'Far']:
                self.ft_sending_flag = False
                self.stop_zoom_focus(Cons.selected_model, 'focus')
            elif btn_text in ptz_text_arr:
                self.stop_ptz(Cons.selected_model)
        elif Cons.selected_model == 'Multi':
            if btn_text in ['Zoom\nIn', 'Zoom\nOut', 'Near', 'Far']:
                self.send_pt_drv('stop', 'eo')
                self.send_pt_drv('stop', 'ir')
            elif btn_text in ptz_text_arr:
                self.send_pt_drv('stop', 'pt_drv')

    def stop_zoom_focus(self, model, command_type):
        if model == 'NYX Series':
            self.zoom_focus_stop_for_nyx(command_type)
        elif model == 'FineTree':
            params = {command_type: 'stop'}
            Comm.fine_tree_send_cgi(self.ptz_url, params)
        elif model == 'DRS':
            host = Cons.selected_ch['ip']
            port = int(Cons.selected_ch['port']) if Cons.selected_ch['port'] else 0
            hex_array = [255, 0, 34, 4, 0, 0, 38] if command_type == 'zoom' else [255, 0, 34, 19, 0, 0, 53]
            Comm.send_cmd_for_drs(host, port, hex_array, self.root)
        elif Cons.selected_model == 'MiniGimbal':
            if command_type == 'zoom':
                self.send_miniGimbal('op_zoom_stop')
            elif command_type == 'focus':
                self.send_miniGimbal('op_focus_stop')

    def stop_ptz(self, model):
        if model == 'FineTree':
            params = {'move': 'stop'}
            Comm.fine_tree_send_cgi(self.ptz_url, params)
        elif model == 'DRS':
            params = {'move': 'stop'}
            Comm.send_cmd_to_Finetree(self.ptz_url, params)
        elif model == 'MiniGimbal':
            # Move Stop
            self.send_miniGimbal('stop')

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
        ic('send_data in PTZ', cmd)
        hex_array = [int(cmd[i:i + 2], 16) for i in range(0, len(cmd), 2)]
        Th.send_cmd_for_uncooled(hex_array, 'Normal Query', self.root)

    # (2024.12.03): Send the CMD to Minigimbal
    def send_miniGimbal(self, dir_str):
        host = Cons.selected_ch['ip']
        port = int(Cons.selected_ch['port'])
        ptz_cmd = {'up': 'FF00000800FF07', 'down': 'FF00001000FF0F',
                   'right': 'FF000002FF0001', 'left': 'FF000004FF0003',
                   'up_left': 'FF00000C7F3FCA', 'up_right': 'FF00000A7F3FC8',
                   'down_left': 'FF0000147F3FD2', 'down_right': 'FF0000127F3FD0',
                   'stop': 'FF000000000000',

                   'op_zoom_in': 'FF00BA000010CA', 'op_zoom_out': 'FF00BA000020DA',
                   'op_zoom_stop': 'FF00BA000000BA',

                   'op_af': 'FF00BF000000BF',
                   'op_near': 'FF00BB000010CB', 'op_far': 'FF00BB000020DB',
                   'op_focus_stop': 'FF00BB000000BB',
                   }
        send_cmd = [int(ptz_cmd[dir_str][i:i + 2], 16) for i in range(0, len(ptz_cmd[dir_str]), 2)]
        # Comm.send_cmd_for_drs(host, port, send_cmd, self.root)
        Comm.send_to_mini(Cons.only_socket, send_cmd)

    # 2025.06.30: Send the CMD to PT Driver
    def send_pt_drv(self, dir_str, model):
        pt_drv_cmd = {'up': 'FF010008404089', 'down': 'FF010010404091',
                      'right': 'FF010002404083', 'left': 'FF010004404085',
                      'left_top': 'FF01000C40408D', 'right_top': 'FF01000A40408B',
                      'left_down': 'FF010014404095', 'right_down': 'FF010012404093',
                      'stop': 'FF010000000001',
                      }
        eo_cmd = {'stop': 'FF020000000002',
                  'zoom_in': 'FF020020000022', 'zoom_out': 'FF020040000042',
                  'far': 'FF020080000082', 'near': 'FF020100000003',
                  'zoom_spd_4': 'FF02002500042B', 'focus_spd_4': 'FF02002700042D',
                  'af_on': 'FF02002B00002D', 'af_off': 'FF02002B00012E',
                  'reboot': 'FF02000F000011', 'reset_default': 'FF02002900002B',
                  }

        ir_cmd = {'stop': 'FF030000000003',
                  'zoom_in': 'FF030020000023', 'zoom_out': 'FF030040000043',
                  'far': 'FF030080000083', 'near': 'FF030100000004',
                  'zoom_spd_4': 'FF03002500042C', 'focus_spd_4': 'FF03002700042E',
                  'af_on': 'FF03002B00002E', 'af_off': 'FF03002B00012F',
                  'reboot': 'FF03000F000012', 'reset_default': 'FF03002900002C',
                  }
        if model == 'pt_drv':
            hex_array = [int(pt_drv_cmd[dir_str][i:i + 2], 16) for i in range(0, len(pt_drv_cmd[dir_str]), 2)]
            Th.send_cmd_only_for_multi(hex_array)
        elif model == 'eo':
            hex_array = [int(eo_cmd[dir_str][i:i + 2], 16) for i in range(0, len(eo_cmd[dir_str]), 2)]
            Th.send_cmd_only_for_multi(hex_array)
        elif model == 'ir':
            hex_array = [int(ir_cmd[dir_str][i:i + 2], 16) for i in range(0, len(ir_cmd[dir_str]), 2)]
            Th.send_cmd_only_for_multi(hex_array)
        # print(hex_array)
        # Th.send_cmd_only_for_multi(hex_array)

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
            self.buttons[text] = self.create_button(text, push_cmd, release_cmd, x, y)

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
