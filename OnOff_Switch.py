import tkinter as tk

from tkinter import *

import Constant as Cons
import Ptz


class SwitchOnOff:
    # btn_id is only able 'PTZ_OSD and 'SCRIPT'
    def __init__(self, ptz_ins, root, btn_id, pos):
        self.root = root
        self.ptz_instance = ptz_ins
        self.id = btn_id

        self.canvas = tk.Canvas(root, width=50, height=50, bg='red')
        self.canvas.place(x=pos['x'], y=pos['y'])

        # Define our switch function
        def switch():
            # Determine is on or off
            if self.id == 'PTZ_OSD':
                if Cons.ptz_osd_toggle_flag:
                    on_button.config(image=off)
                    print(rf'osd off:{Cons.ptz_osd_toggle_flag}')
                    Cons.ptz_osd_toggle_flag = not Cons.ptz_osd_toggle_flag
                    self.ptz_instance.refresh_ptz()
                else:
                    on_button.config(image=on)
                    print(rf'osd on:{Cons.ptz_osd_toggle_flag}')
                    Cons.ptz_osd_toggle_flag = not Cons.ptz_osd_toggle_flag
                    self.ptz_instance.refresh_ptz()
            elif self.id == 'SCRIPT':
                if not Cons.script_toggle_flag:
                    on_button.config(image=on)
                    print(rf'script off:{Cons.script_toggle_flag}')
                    Cons.script_toggle_flag = not Cons.script_toggle_flag
                else:
                    on_button.config(image=off)
                    print(rf'script on:{Cons.script_toggle_flag}')
                    Cons.ptz_osd_toggle_flag = not Cons.ptz_osd_toggle_flag
                    Cons.script_toggle_flag = not Cons.script_toggle_flag

        # Define Our Images
        on = PhotoImage(file="Design/on1.png")
        off = PhotoImage(file="Design/off1.png")

        # Create A Button
        on_button = Button(self.canvas, image=off, bd=0, command=switch)
        on_button.pack()
