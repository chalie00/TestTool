# (2024.09.30): Create preset file
import time
import tkinter as tk
import threading

import Constant as Cons
import Communication as Comm


class Preset:
    def __init__(self, root):
        self.root = root
        self.running = False

        self.canvas = tk.Canvas(root, width=Cons.preset_canvas['w'], height=Cons.preset_canvas['h'])
        self.canvas.place(x=Cons.preset_canvas['x'], y=Cons.preset_canvas['y'])

        self.init_ui()

    # (2024.10.02): Initialize a Preset UI
    def init_ui(self):
        preset_lbl = tk.Label(self.root, text='Preset', bg=Cons.preset_lbl['bg'])
        preset_lbl.place(x=Cons.preset_lbl['x'], y=Cons.preset_lbl['y'],
                         width=Cons.preset_lbl['w'], height=Cons.preset_lbl['h'])
        tour_lbl = tk.Label(self.root, text='Tour', bg=Cons.tour_lbl['bg'])
        tour_lbl.place(x=Cons.tour_lbl['x'], y=Cons.tour_lbl['y'],
                       width=Cons.tour_lbl['w'], height=Cons.tour_lbl['h'])

        self.preset_txt_fld = tk.Entry(self.root, justify='center')
        self.preset_txt_fld.place(x=Cons.preset_txt_fld['x'], y=Cons.preset_txt_fld['y'],
                                  width=Cons.preset_txt_fld['w'], height=Cons.preset_txt_fld['h'])
        self.preset_txt_fld.bind('<Return>', lambda event, type='call': self.send_preset_related_finetree(event, type))

        self.tour_txt_fld = tk.Entry(self.root, justify='center')
        self.tour_txt_fld.place(x=Cons.tour_txt_fld['x'], y=Cons.tour_txt_fld['y'],
                                width=Cons.tour_txt_fld['w'], height=Cons.tour_txt_fld['h'])
        self.tour_txt_fld.bind('<Return>', lambda event, type='call': self.send_tour_related_finetree(event, type))

        preset_save_btn = tk.Button(self.root, text=Cons.preset_save_btn['text'], bg=Cons.preset_save_btn['bg'])
        preset_save_btn.place(x=Cons.preset_save_btn['x'], y=Cons.preset_save_btn['y'],
                              width=Cons.preset_save_btn['w'], height=Cons.preset_save_btn['h'])
        save_params = {'presetsave': rf'{self.preset_txt_fld.get()}'}
        preset_save_btn.bind('<Button-1>', lambda event, type='save': self.send_preset_related_finetree(event, type))
        # preset_save_btn.bind('<Button-1>', self.send_save_preset_finetree)

        preset_call_btn = tk.Button(self.root, text=Cons.preset_call_btn['text'], bg=Cons.preset_call_btn['bg'])
        preset_call_btn.place(x=Cons.preset_call_btn['x'], y=Cons.preset_call_btn['y'],
                              width=Cons.preset_call_btn['w'], height=Cons.preset_call_btn['h'])
        call_params = {'preset': rf'{self.preset_txt_fld.get()}'}
        preset_call_btn.bind('<Button-1>', lambda event, type='call': self.send_preset_related_finetree(event, type))

        tour_save_btn = tk.Button(self.root, text=Cons.tour_save_btn['text'], bg=Cons.tour_save_btn['bg'])
        tour_save_btn.place(x=Cons.tour_save_btn['x'], y=Cons.tour_save_btn['y'],
                            width=Cons.tour_save_btn['w'], height=Cons.tour_save_btn['h'])
        tour_save_btn.bind('<Button-1>', lambda event, type='save': self.send_tour_related_finetree(event, type))

        tour_call_btn = tk.Button(self.root, text=Cons.tour_call_btn['text'], bg=Cons.tour_call_btn['bg'])
        tour_call_btn.place(x=Cons.tour_call_btn['x'], y=Cons.tour_call_btn['y'],
                            width=Cons.tour_call_btn['w'], height=Cons.tour_call_btn['h'])
        tour_call_btn.bind('<Button-1>', lambda event, type='call': self.send_tour_related_finetree(event, type))

        tour_stop_btn = tk.Button(self.root, text=Cons.tour_stop_btn['text'], bg=Cons.tour_stop_btn['bg'])
        tour_stop_btn.place(x=Cons.tour_stop_btn['x'], y=Cons.tour_stop_btn['y'],
                            width=Cons.tour_stop_btn['w'], height=Cons.tour_stop_btn['h'])
        tour_stop_btn.bind('<Button-1>', lambda event, type='stop': self.send_tour_related_finetree(event, type))

    # (2024.10.06): Save/Call a Preset
    def send_preset_related_finetree(self, event, type):
        print('called preset function')
        preset_txt_fld_info = self.preset_txt_fld.get()
        if type == 'save':
            params = {'presetsave': preset_txt_fld_info}
            self.preset_txt_fld.delete(0, tk.END)
        elif type == 'call':
            params = {'preset': preset_txt_fld_info}
            self.preset_txt_fld.delete(0, tk.END)
        preset_url = '/cgi-bin/ptz/control.php?'
        Comm.fine_tree_send_cgi(preset_url, params)

    # (2024.10.10): Sava/Call a Tour
    def send_tour_related_finetree(self, event, type):
        print('called tour function')
        tour_txt_fld_info = self.tour_txt_fld.get()
        if type == 'save':
            print('called save tour')
            tour_raw = tour_txt_fld_info.split(',')
            Cons.tour_lists = tour_raw
            print(Cons.tour_lists)
            self.tour_txt_fld.delete(0, tk.END)

        elif type == 'call':
            print('called run tour')
            tour_repeat = int(self.tour_txt_fld.get())
            self.tour_txt_fld.delete(0, tk.END)
            self.running = True
            thread = threading.Thread(target=self.run_tour, args=(tour_repeat,))
            thread.start()

        elif type == 'stop':
            print('called stop tour')
            self.running = False
            preset_url = '/cgi-bin/ptz/control.php?'
            params = {'move': 'stop'}
            Comm.fine_tree_send_cgi(preset_url, params)

    # (2024.11.11): seperate a tour run
    def run_tour(self, tour_repeat):
        for i in range(tour_repeat):
            if not self.running:
                break
            for tour_list in Cons.tour_lists:
                if not self.running:
                    break
                preset_url = '/cgi-bin/ptz/control.php?'
                params = {'preset': tour_list}
                Comm.fine_tree_send_cgi(preset_url, params)
                time.sleep(30.0)
