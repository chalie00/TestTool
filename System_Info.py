# (2024.07.15) Init
import tkinter as tk
import time as ti
import threading

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
        mode_lbl = tk.Label(self.root, text='DZoom', bg=Cons.my_color['fg'])
        mode_lbl.place(x=pos_spd_mode_cons['x'] + 135, y=pos_spd_mode_cons['y'])

        # Zoom column Position
        zoom_pos_cons = {'x': Cons.sys_info_tab['x'] + 5, 'y': Cons.sys_info_tab['y'] + Cons.lbl_size['h'] + 10}

        zoom_pos_lbl = tk.Label(self.root, text='Zoom', bg=Cons.my_color['fg'])
        zoom_pos_lbl.place(x=zoom_pos_cons['x'] + 5, y=zoom_pos_cons['y'])
        self.zoom_pos_txt_fld = tk.Entry(self.root, width=7, justify='center')
        self.zoom_pos_txt_fld.place(x=zoom_pos_cons['x'] + 55, y=zoom_pos_cons['y'])
        self.zoom_spd_txt_fld = tk.Entry(self.root, width=7, justify='center')
        self.zoom_spd_txt_fld.place(x=zoom_pos_cons['x'] + 117, y=zoom_pos_cons['y'])
        self.zoom_dzoom_txt_fld = tk.Entry(self.root, width=7, justify='center')
        self.zoom_dzoom_txt_fld.place(x=zoom_pos_cons['x'] + 179, y=zoom_pos_cons['y'])

        # Focus column Position
        focus_pos_cons = {'x': Cons.sys_info_tab['x'] + 5, 'y': Cons.sys_info_tab['y'] + Cons.lbl_size['h'] * 2 + 15}

        focus_pos_lbl = tk.Label(self.root, text='Focus', bg=Cons.my_color['fg'])
        focus_pos_lbl.place(x=focus_pos_cons['x'] + 5, y=focus_pos_cons['y'])
        self.focus_pos_txt_fld = tk.Entry(self.root, width=7, justify='center')
        self.focus_pos_txt_fld.place(x=focus_pos_cons['x'] + 55, y=focus_pos_cons['y'])
        self.focus_spd_txt_fld = tk.Entry(self.root, width=7, justify='center')
        self.focus_spd_txt_fld.place(x=focus_pos_cons['x'] + 117, y=focus_pos_cons['y'])
        self.focus_dzoom_rate_txt_fld = tk.Entry(self.root, width=7, justify='center')
        self.focus_dzoom_rate_txt_fld.place(x=focus_pos_cons['x'] + 179, y=focus_pos_cons['y'])

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

        self.data_lock = threading.Lock()
        self.data_ready = False

        self.update_ui()

    # (2024.07.24): Added for all entry text delete
    def clear_entries(self):
        self.zoom_pos_txt_fld.delete(0, tk.END)
        self.zoom_spd_txt_fld.delete(0, tk.END)
        self.zoom_dzoom_txt_fld.delete(0, tk.END)

        self.focus_pos_txt_fld.delete(0, tk.END)
        self.focus_spd_txt_fld.delete(0, tk.END)
        self.focus_dzoom_rate_txt_fld.delete(0, tk.END)

        self.fov_pos_txt_fld.delete(0, tk.END)

    # (2024.07.16) Update Query Data
    def update_ui(self):
        self.canvas.delete('all')
        self.clear_entries()

        if Cons.selected_model == 'Uncooled':
            self.zoom_pos_txt_fld.insert(0, Cons.zoom_msb_lsb[0])
            self.zoom_spd_txt_fld.insert(0, Cons.zoom_msb_lsb[1])
            # Convert D-Zoom value to On/Off
            if Cons.zoom_msb_lsb and len(Cons.zoom_msb_lsb) > 0:
                try:
                    if Cons.zoom_msb_lsb[2] == 1:
                        self.zoom_dzoom_txt_fld.insert(0, 'On')
                    elif Cons.zoom_msb_lsb[2] == 0:
                        self.zoom_dzoom_txt_fld.insert(0, 'Off')
                except ValueError:
                    print("Invalid value in Cons.zoom_msb_lsb[2]:", Cons.zoom_msb_lsb[2])
            else:
                print("Cons.fov_msb_lsb is empty or not properly initialized.")


            self.focus_pos_txt_fld.insert(0, Cons.focus_msb_lsb[0])
            self.focus_spd_txt_fld.insert(0, Cons.focus_msb_lsb[1])
            # Calculate a d-Zoom rate
            if Cons.zoom_msb_lsb and len(Cons.zoom_msb_lsb) > 0:
                try:
                    dzoom_rate = (float(Cons.zoom_msb_lsb[3]) + 10) / 10
                    self.focus_dzoom_rate_txt_fld.insert(0, dzoom_rate)
                except ValueError:
                    print("Invalid value in Cons.zoom_msb_lsb[3]:", Cons.zoom_msb_lsb[3])
            else:
                print("Cons.fov_msb_lsb is empty or not properly initialized.")

            # Calculate a FOV
            if Cons.fov_msb_lsb and len(Cons.fov_msb_lsb) > 0:
                try:
                    fov_value = float(Cons.fov_msb_lsb[0]) / 100
                    self.fov_pos_txt_fld.insert(0, fov_value)
                except ValueError:
                    print("Invalid value in Cons.fov_msb_lsb[0]:", Cons.fov_msb_lsb[0])
            else:
                print("Cons.fov_msb_lsb is empty or not properly initialized.")

        elif Cons.selected_model == 'NYX Series':
            self.zoom_pos_txt_fld.insert(0, Cons.cooled_lens_pos_spd[0])
            self.zoom_spd_txt_fld.insert(0, Cons.cooled_lens_pos_spd[3])
            self.zoom_dzoom_txt_fld.insert(0, Cons.cooled_lens_pos_spd[5])

            self.focus_pos_txt_fld.insert(0, Cons.cooled_lens_pos_spd[1])
            self.focus_spd_txt_fld.insert(0, Cons.cooled_lens_pos_spd[4])
            self.focus_dzoom_rate_txt_fld.insert(0, Cons.cooled_lens_pos_spd[6])

            self.fov_pos_txt_fld.insert(0, Cons.cooled_lens_pos_spd[2])

    # Update Information All Element
    # def update_with_protocol(self):
    #     self.update_btn.config(state='disabled')
    #     if Cons.selected_model == 'Uncooled':
    #         # Zoom Query -> Focus Query -> Lens Query -> Image Query
    #         protocols = [
    #             [255, 1, 0, 85, 0, 0, 86], [255, 1, 1, 85, 0, 0, 87],
    #             [255, 1, 161, 16, 0, 0, 178], [255, 1, 161, 32, 0, 0, 194]
    #         ]
    #         titles = {
    #             'Zoom Query': (
    #                 [255, 1, 0, 85, 0, 0, 86]
    #             ),
    #             # 'Normal Query': (
    #             #     [255, 1, 1, 85, 0, 0, 86]
    #             # ),
    #             'Focus Query': (
    #                 # [255, 1, 161, 16, 0, 0, 87]
    #                 [255, 1, 1, 85, 0, 0, 87]
    #             ),
    #             'Lens Query': (
    #                 [255, 1, 161, 16, 0, 0, 178]
    #             ),
    #             'Image Query': (
    #                 [255, 1, 161, 32, 0, 0, 194]
    #             )
    #         }
    #         interval = [1.0, 1.0, 1.0, 1.0]
    #
    #         for title, protocol in titles.items():
    #             # print(title)
    #             # print(protocol)
    #             Comm.send_cmd_for_uncooled(protocol, title, self.root)
    #     elif Cons.selected_model == 'NYX Series':
    #         print('NYX Updated')
    #         # NYX.GET#lens_wnmm -> NYX.GET#lens_wnen
    #         Cons.cooled_lens_pos_spd = []
    #         lens_pos_q = ['NYX.GET#lens_zpos=', 'NYX.GET#lens_fpos=', 'NYX.GET#lens_cfov=',
    #                       'NYX.GET#lens_zspd=', 'NYX.GET#lens_fspd=', 'NYX.GET#isp0_dzen=',
    #                       'NYX.GET#isp0_dzra='
    #                       ]
    #         Comm.send_data_with_cmd_for_info(self.root, lens_pos_q)
    #     elif Cons.selected_model == 'FineTree':
    #         return
    #
    #     self.root.after(100, self.update_ui)
    #     self.update_btn.config(state='normal')

    ############ Caution: Update use when Query mode Off of TQM-1M #########################
    def update_with_protocol(self):
        self.update_btn.config(state='disabled')  # 버튼 비활성화

        def run_commands():
            try:
                if Cons.selected_model_obj == 'Uncooled':
                    protocols = [
                        [255, 1, 0, 85, 0, 0, 86], [255, 1, 1, 85, 0, 0, 87],
                        [255, 1, 161, 16, 0, 0, 178], [255, 1, 161, 32, 0, 0, 194]
                    ]
                    titles = {
                        'Zoom Query': [255, 1, 0, 85, 0, 0, 86],
                        'Focus Query': [255, 1, 1, 85, 0, 0, 87],
                        'Lens Query': [255, 1, 161, 16, 0, 0, 178],
                        'Image Query': [255, 1, 161, 32, 0, 0, 194]
                    }

                    for title, protocol in titles.items():
                        Comm.send_cmd_for_uncooled(protocol, title, self.root)

                elif Cons.selected_model_obj == 'NYX Series':
                    print('NYX Updated')
                    lens_pos_q = [
                        'NYX.GET#lens_zpos=', 'NYX.GET#lens_fpos=',
                        'NYX.GET#lens_cfov=', 'NYX.GET#lens_zspd=',
                        'NYX.GET#lens_fspd=', 'NYX.GET#isp0_dzen=',
                        'NYX.GET#isp0_dzra='
                    ]
                    Comm.send_data_with_cmd_for_info(self.root, lens_pos_q)

                elif Cons.selected_model_obj == 'FineTree':
                    return

                # 데이터 준비 완료 플래그 설정
                with self.data_lock:
                    self.data_ready = True

            except Exception as e:
                print(f"Error during command execution: {e}")

            # UI 업데이트를 위해 메인 스레드로 돌아가기
            self.root.after(100, self.update_ui)
            self.update_btn.config(state='normal')

        # 별도의 스레드에서 작업 실행
        threading.Thread(target=run_commands).start()

