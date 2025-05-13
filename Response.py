# (2024.07.11) Init
import tkinter as tk

from tkinter import ttk
from datetime import time, datetime
from tkinter import font

import Constant as Cons


class Response:
    def __init__(self, root, pos):
        self.root = root
        self.pos = pos
        self.canvas = tk.Canvas(self.root, width=pos['w'] - 30, height=pos['h'] + 15, bg=pos['bg'])
        self.canvas.place(x=pos['x'], y=pos['y'] + 5)

        # Create Log Field
        self.text_widget = tk.Text(self.canvas, bg='lightgray', width=88, height=15)
        self.text_widget.place(x=0, y=0)
        self.text_font = font.Font(size=8)
        self.text_widget.configure(font=self.text_font)

        # Set bold to specified txt
        bold_font = font.Font(size=8, weight="bold")
        self.text_widget.tag_configure("bold", font=bold_font, foreground='green')

        scrollbar = tk.Scrollbar(orient='vertical', command=self.text_widget.yview)
        scrollbar.place(x=self.pos['x'] + self.pos['w'] - 25, y=self.pos['y'], height=self.pos['h'] - 10)
        self.text_widget.config(yscrollcommand=scrollbar.set)

        self.dis_response_text()

# (2024.10.31): Apply green color text to UncooledType response value
    # Response Text
    def dis_response_text(self):
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.delete(1.0, tk.END)  # 기존 텍스트 지우기

        if Cons.selected_model in ['Uncooled', 'NYX Series']:
            dis_txt = list(reversed(Cons.response_txt))
            for i, txt in enumerate(dis_txt[:30]):
                self.text_widget.insert(tk.END, txt + '\n')
                if Cons.selected_model == 'Uncooled':
                    # Get the start index for this line
                    line_index = f"{i + 1}.0"  # Start of line (i+1 because line index in tkinter starts from 1)
                    if len(txt) != 30 and len(txt) >= 12:  # 길이가 12 이상일 경우
                        start_index = f"{i + 1}.8"  # 8번째 문자부터
                        end_index = f"{i + 1}.12"  # 12번째 문자까지
                        self.text_widget.tag_add("bold", start_index, end_index)
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

