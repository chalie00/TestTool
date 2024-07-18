import tkinter as tk

import Constant as Cons
import MainFunction as Mf
import Communication as Th
import OnOff_Switch as onoffSW


class PTZ:
    def __init__(self, root):
        self.root = root

        self.canvas = tk.Canvas(root, width=Cons.ptz_canvas['w'], height=Cons.ptz_canvas['h'])
        self.canvas.place(x=Cons.ptz_canvas['x'], y=Cons.ptz_canvas['y'] + 5)

        ptz_osd_mode_btn = {'x': Cons.ptz_up_btn['x'] + Cons.ptz_up_btn['w'] / 2 + 5,
                            'y': Cons.ptz_up_btn['y'] - Cons.ptz_up_btn['h'] / 2}
        btn_id = 'PTZ_OSD'
        self.ptz_osd_mode_ui = onoffSW.SwitchOnOff(self, self.canvas, btn_id, ptz_osd_mode_btn)

        self.refresh_ptz()

    def create_button(self, text, push_cmd, release_cmd, x, y):
        if not Cons.ptz_osd_toggle_flag:
            btn = tk.Button(self.canvas, text=text, width=6, height=2, bg=Cons.my_color['bg'], command=push_cmd)
        else:
            btn = tk.Button(self.canvas, text=text, width=6, height=2, bg=Cons.my_color['bg'])
            btn.bind('<ButtonPress-1>', push_cmd)
            btn.bind('<ButtonRelease-1>', release_cmd)
        self.canvas.create_window(x, y, window=btn)

    def up_zoom_in(self, event=None):
        if not Cons.ptz_osd_toggle_flag:
            self.send_data('FF01E024000005')
        else:
            self.send_data('FF010020000021')

    def down_zoom_out(self, event=None):
        if not Cons.ptz_osd_toggle_flag:
            self.send_data('FF01E025000006')
        else:
            self.send_data('FF010040000041')

    def left_near(self, event=None):
        if not Cons.ptz_osd_toggle_flag:
            self.send_data('FF01E022000003')
        else:
            self.send_data('FF010100000002')

    def right_far(self, event=None):
        if not Cons.ptz_osd_toggle_flag:
            self.send_data('FF01E023000004')
        else:
            self.send_data('FF010080000081')

    def osd_af(self, event=None):
        if not Cons.ptz_osd_toggle_flag:
            self.send_data('FF01E021000002')
        else:
            self.send_data('FF01A0110000B2')

    def release_cmd(self, event=None):
        self.send_data('FF010000000001')

    def send_data(self, cmd):
        hex_array = [int(cmd[i:i + 2], 16) for i in range(0, len(cmd), 2)]
        Th.send_data(hex_array, 'Normal Query', self.root)

    def create_circle_button(self, x, y, r, color, text, command):
        oval = self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, outline=color)
        text_id = self.canvas.create_text(x, y, text=text)

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

    def refresh_ptz(self):
        self.canvas.delete('all')
        if not Cons.ptz_osd_toggle_flag:
            button_configurations = [
                ('UP', self.up_zoom_in, self.release_cmd, Cons.ptz_up_btn['x'], Cons.ptz_up_btn['y']),
                ('DOWN', self.down_zoom_out, self.release_cmd, Cons.ptz_down_btn['x'], Cons.ptz_down_btn['y']),
                ('LEFT', self.left_near, self.release_cmd, Cons.ptz_left_btn['x'], Cons.ptz_left_btn['y']),
                ('RIGHT', self.right_far, self.release_cmd, Cons.ptz_right['x'], Cons.ptz_right['y'])
            ]
        else:
            button_configurations = [
                ('Zoom\nIn', self.up_zoom_in, self.release_cmd, Cons.ptz_up_btn['x'], Cons.ptz_up_btn['y']),
                ('Zoom\nOut', self.down_zoom_out, self.release_cmd, Cons.ptz_down_btn['x'], Cons.ptz_down_btn['y']),
                ('Near', self.left_near, self.release_cmd, Cons.ptz_left_btn['x'], Cons.ptz_left_btn['y']),
                ('Far', self.right_far, self.release_cmd, Cons.ptz_right['x'], Cons.ptz_right['y'])
            ]

        for text, push_cmd, release_cmd, x, y in button_configurations:
            self.create_button(text, push_cmd, release_cmd, x, y)

        center_text = 'AF' if Cons.ptz_osd_toggle_flag else 'OSD'
        self.create_circle_button(Cons.ptz_canvas['w'] / 2, Cons.ptz_canvas['h'] / 2 + 3, 25, Cons.my_color['bg'],
                                  center_text, self.osd_af)
