import tkinter as tk

import Constant as Cons
import MainFunction as Mf
import Communication as Th


class PTZ:
    def __init__(self, root):
        self.root = root

        self.canvas = tk.Canvas(root, width=Cons.ptz_canvas['w'], height=Cons.ptz_canvas['h'])
        self.canvas.place(x=Cons.ptz_canvas['x'], y=Cons.ptz_canvas['y'])

        # PTZ Function
        def up_cmd():
            print('Pressed Up')
            cmd = 'FF01E024000005'
            send_data(cmd)

        def down_cmd():
            print('Pressed down')
            cmd = 'FF01E025000006'
            send_data(cmd)

        def left_cmd():
            print('Pressed left')
            cmd = 'FF01E022000003'
            send_data(cmd)

        def right_cmd():
            print('Pressed right')
            cmd = 'FF01E023000004'
            send_data(cmd)

        def osd_cmd(event):
            print('Pressed af')
            cmd = 'FF01E021000002'
            send_data(cmd)

        def send_data(cmd):
            hex_array = []
            for i in range(0, len(cmd), 2):
                hex_str = '0x' + cmd[i:i + 2]
                hex_int = int(hex_str, 16)
                hex_array.append(hex_int)

            Th.send_data(hex_array, root)

        # Create Circle
        def create_circle_button(canvas, x, y, r, color, command):
            # Draw the circle
            oval = canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, outline=color)

            # Bind the click event to the circle
            canvas.tag_bind(oval, '<Button-1>', command)

            # Optional: Add text in the middle of the circle
            text = canvas.create_text(x, y, text="OSD", fill="black", font=("Arial", 9))

            # Bind the click event to the text as well
            canvas.tag_bind(text, '<Button-1>', command)

            return oval

        # Create a PTZ UI
        up_btn = tk.Button(self.canvas, text='UP', width=6, height=2, bg=Cons.my_color['bg'], command=up_cmd)
        self.canvas.create_window(Cons.ptz_up_btn['x'], Cons.ptz_up_btn['y'], window=up_btn)

        down_btn = tk.Button(self.canvas, text='DOWN', width=6, height=2, bg=Cons.my_color['bg'], command=down_cmd)
        self.canvas.create_window(Cons.ptz_down_btn['x'], Cons.ptz_down_btn['y'], window=down_btn)

        left_btn = tk.Button(self.canvas, text='LEFT', width=6, height=2, bg=Cons.my_color['bg'], command=left_cmd)
        self.canvas.create_window(Cons.ptz_left_btn['x'], Cons.ptz_left_btn['y'], window=left_btn)

        right_btn = tk.Button(self.canvas, text='RIGHT', width=6, height=2, bg=Cons.my_color['bg'], command=right_cmd)
        self.canvas.create_window(Cons.ptz_right['x'], Cons.ptz_right['y'], window=right_btn)

        center_btn = create_circle_button(self.canvas, Cons.ptz_canvas['w'] / 2, Cons.ptz_canvas['h'] / 2 + 3, 25,
                                          Cons.my_color['bg'], command=osd_cmd)
