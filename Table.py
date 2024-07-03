import array
import tkinter as tk

from tkinter import *
from tkinter import ttk
from ttkwidgets import CheckboxTreeview

import Constant as Cons


class Table:
    def __init__(self, root):
        self.root = root

        self.canvas = tk.Canvas(root, bg='white', width=Cons.script_tb_pos['w'],
                                height=Cons.WINDOWS_SIZE['y'] - Cons.camera_resolution['h'] - 10)
        self.canvas.place(x=Cons.script_tb_pos['x'], y=Cons.script_tb_pos['y'])

        self.inner_frame = tk.Frame(self.canvas)
        self.canvas.create_window(((int(self.canvas['width']) / 2), (int(self.canvas['height']) / 2)),
                                  window=self.inner_frame, anchor='center')

        column_num = len(Cons.script_column)
        column = [i + 1 for i in range(column_num)]
        dis_column = [str(n) for n in column]
        # cmd_data = Cons.script_cmd_titles
        cmd_data = Cons.cmd_itv_arrays
        tv = CheckboxTreeview(self.inner_frame, height=5, columns=dis_column, displaycolumns=dis_column)
        self.style = ttk.Style()
        self.style.configure('script Table', background='lightgray')
        # tv.grid(row=0, column=0, columnspan=column_num, sticky='nsew')
        tv.pack(fill=tk.BOTH, expand=True)

        # Set the Table No Tab
        tv.column('#0', width=70, anchor='center', stretch='yes')
        tv.heading('#0', text='No', anchor='center')

        # Create each column(name, width, anchor)
        for i in range(column_num):
            tv.column(dis_column[i], width=Cons.script_tb_pos['c'], anchor='center')
            tv.heading(dis_column[i], text=Cons.script_column[i], anchor='center')

        # Remove the space of each element
        for i, data in enumerate(cmd_data):
            # values = (data, '')
            tv.insert('', 'end', text=i + 1, values=data, iid=str(i) + '번', tags=('checked',))
            tv.column(dis_column[0], anchor='center')
