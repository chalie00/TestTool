# (2024.07.15) Init
import tkinter as tk
import time as ti

import Constant as Cons
import Communication as Comm

from tkinter import ttk


class SysInfo:
    def __init__(self, root, pos):
        self.root = root
        self.pos = pos
        self.canvas = tk.Canvas(self.root, width=pos['w'], height=pos['h'] - 1, bg=pos['bg'])
        self.canvas.place(x=pos['x'], y=pos['y'])
        pos_spd_mode_cons = {'x': Cons.sys_info_tab['x'] + 60, 'y': Cons.sys_info_tab['y'] + 5}

        pos_lbl = tk.Label(self.root, text='Position', bg=Cons.my_color['fg'])
        pos_lbl.place(x=pos_spd_mode_cons['x'], y=pos_spd_mode_cons['y'])
        spd_lbl = tk.Label(self.root, text='Speed', bg=Cons.my_color['fg'])
        spd_lbl.place(x=pos_spd_mode_cons['x'] + 70, y=pos_spd_mode_cons['y'])
        mode_lbl = tk.Label(self.root, text='Mode', bg=Cons.my_color['fg'])
        mode_lbl.place(x=pos_spd_mode_cons['x'] + 135, y=pos_spd_mode_cons['y'])

        # Zoom column Position
        zoom_pos_cons = {'x': Cons.sys_info_tab['x'] + 5, 'y': Cons.sys_info_tab['y'] + Cons.lbl_size['h'] + 10}

        zoom_pos_lbl = tk.Label(self.root, text='Zoom', bg=Cons.my_color['fg'])
        zoom_pos_lbl.place(x=zoom_pos_cons['x'] + 5, y=zoom_pos_cons['y'])
        self.zoom_pos_txt_fld = tk.Entry(self.root, width=7, justify='center')
        self.zoom_pos_txt_fld.place(x=zoom_pos_cons['x'] + 55, y=zoom_pos_cons['y'])
        self.zoom_spd_txt_fld = tk.Entry(self.root, width=7, justify='center')
        self.zoom_spd_txt_fld.place(x=zoom_pos_cons['x'] + 117, y=zoom_pos_cons['y'])
        self.zoom_mode_txt_fld = tk.Entry(self.root, width=7, justify='center')
        self.zoom_mode_txt_fld.place(x=zoom_pos_cons['x'] + 179, y=zoom_pos_cons['y'])

        # Focus column Position
        focus_pos_cons = {'x': Cons.sys_info_tab['x'] + 5, 'y': Cons.sys_info_tab['y'] + Cons.lbl_size['h'] * 2 + 15}

        focus_pos_lbl = tk.Label(self.root, text='Focus', bg=Cons.my_color['fg'])
        focus_pos_lbl.place(x=focus_pos_cons['x'] + 5, y=focus_pos_cons['y'])
        self.focus_pos_txt_fld = tk.Entry(self.root, width=7, justify='center')
        self.focus_pos_txt_fld.place(x=focus_pos_cons['x'] + 55, y=focus_pos_cons['y'])
        self.focus_spd_txt_fld = tk.Entry(self.root, width=7, justify='center')
        self.focus_spd_txt_fld.place(x=focus_pos_cons['x'] + 117, y=focus_pos_cons['y'])
        self.focus_mode_txt_fld = tk.Entry(self.root, width=7, justify='center')
        self.focus_mode_txt_fld.place(x=focus_pos_cons['x'] + 179, y=focus_pos_cons['y'])

        # FOV column Position
        fov_pos_cons = {'x': Cons.sys_info_tab['x'] + 5, 'y': Cons.sys_info_tab['y'] + Cons.lbl_size['h'] * 3 + 20}
        fov_pos_lbl = tk.Label(self.root, text='FOV', bg=Cons.my_color['fg'])
        fov_pos_lbl.place(x=fov_pos_cons['x'] + 5, y=fov_pos_cons['y'])
        self.fov_pos_txt_fld = tk.Entry(self.root, width=7, justify='center')
        self.fov_pos_txt_fld.place(x=fov_pos_cons['x'] + 55, y=fov_pos_cons['y'])

        # (2024.07.17) Information Update Btn
        update_btn_pos = {'x': Cons.sys_info_update_btn['x'] - 15, 'y': Cons.sys_info_update_btn['y'] + 20,
                          'w': Cons.sys_info_update_btn['w'], 'h': Cons.sys_info_update_btn['h']}
        self.update_btn = tk.Button(self.root, width=6, height=1, command=self.update_with_protocol, text='UPDATE')
        self.update_btn.place(x=update_btn_pos['x'], y=update_btn_pos['y'])

        self.update_ui()

    # (2024.07.16) Update Query Data
    def update_ui(self):
        self.canvas.delete('all')
        self.zoom_pos_txt_fld.insert(0, Cons.zoom_msb_lsb[0])
        self.zoom_spd_txt_fld.insert(0, Cons.zoom_msb_lsb[1])
        self.zoom_mode_txt_fld.insert(0, Cons.zoom_msb_lsb[2])

        self.focus_pos_txt_fld.insert(0, Cons.focus_msb_lsb[0])
        self.focus_spd_txt_fld.insert(0, Cons.focus_msb_lsb[1])
        self.focus_mode_txt_fld.insert(0, Cons.focus_msb_lsb[2])

        self.fov_pos_txt_fld.insert(0, Cons.fov_msb_lsb[0])

    # Update Infromation All Element
    def update_with_protocol(self):
        print('Hello')
        # Zoom Query -> Focus Query -> Lens Query -> Image Query
        protocols = [
            [255, 1, 0, 85, 0, 0, 86], [255, 1, 1, 85, 0, 0, 87],
            [255, 1, 161, 16, 0, 0, 178], [255, 1, 161, 32, 0, 0, 194]
        ]
        titles = {
            'Normal Query': (
                [255, 1, 0, 85, 0, 0, 86]
            ),
            'Zoom Query': (
                [255, 1, 1, 85, 0, 0, 86]
            ),
            'Focus Query': (
                [255, 1, 161, 16, 0, 0, 87]
            ),
            'Lens Query': (
                [255, 1, 161, 16, 0, 0, 178]
            ),
            'Image Query': (
                [255, 1, 161, 32, 0, 0, 194]
            )
        }
        interval = [1.0, 1.0, 1.0, 1.0]

        for title, protocol in titles:
            Comm.send_data(protocol, title, self.root)
        self.root.after(100, self.update_ui)
