import tkinter as tk

from tkinter import *

import Constant as Cons


class SwitchOnOff:
    def __init__(self, root):
        self.root = root

        self.canvas = tk.Canvas(root, width=50, height=50, bg='red')
        self.canvas.place(x=Cons.script_mode_btn['x'], y=Cons.script_mode_btn['y'])

        # Create Label
        # my_label = Label(root,
        #                  text="The Switch Is On!",
        #                  fg="green",
        #                  font=("Helvetica", 32))
        #
        # my_label.pack(pady=20)

        # Define our switch function
        def switch():
            # Determine is on or off
            if Cons.script_mode_value:
                on_button.config(image=off)
                # my_label.config(text="The Switch is Off", fg="grey")
                print('off')
                Cons.script_mode_value = False
            else:
                on_button.config(image=on)
                # my_label.config(text="The Switch is On", fg="green")
                print('on')
                Cons.script_mode_value = True

        # Define Our Images
        on = PhotoImage(file="Design/on1.png")
        off = PhotoImage(file="Design/off1.png")

        # Create A Button
        on_button = Button(self.canvas, image=off, bd=0,
                           command=switch)
        on_button.pack()
