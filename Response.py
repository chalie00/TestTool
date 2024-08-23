# (2024.07.11) Init
import tkinter as tk

from tkinter import ttk
from datetime import time, datetime

import Constant as Cons


class Response:
    def __init__(self, root, pos):
        self.root = root
        self.pos = pos
        self.canvas = tk.Canvas(self.root, width=pos['w'] - 30, height=pos['h'] - 1, bg=pos['bg'])
        self.canvas.place(x=pos['x'], y=pos['y'] + 5)

        # Create Lof Field
        self.text_widget = tk.Text(self.canvas, bg='lightgray', width=79, height=12)
        self.text_widget.place(x=0, y=5)
        scrollbar = tk.Scrollbar(orient=tk.VERTICAL, command=self.text_widget.yview)
        scrollbar.place(x=self.pos['x'] + self.pos['w'] - 25, y=self.pos['y'] + 5, height=self.pos['h'] - 10)
        self.text_widget.config(yscrollcommand=scrollbar.set)

        self.dis_response_text()

    # Response Text
    def dis_response_text(self):
        if Cons.selected_model in ['Uncooled', 'NYX Series']:
            dis_txt = list(reversed(Cons.response_txt))
            for i, txt in enumerate(dis_txt[:20]):
                self.text_widget.insert(tk.END, txt + '\n')
                # (2024.07.17) Move last line
                # self.text_widget.see(tk.END)
            self.text_widget.config(state=tk.DISABLED)
        elif Cons.selected_model in ['DRS']:
            dis_txt = Cons.drs_response.items()
            for key, v in dis_txt:
                self.text_widget.insert(tk.END, f'{key}: {v}\n')
                # (2024.07.17) Move last line
                # self.text_widget.see(tk.END)
            self.text_widget.config(state=tk.DISABLED)

