# (2024.07.11) Init
import tkinter as tk

from tkinter import ttk
from datetime import time, datetime
from tkinter import font
from decimal import Decimal

import Constant as Cons


# 2025.07.02: Divide 7byte
def split_by_bytes(hex_string: str):
    hex_string = hex_string.lower().replace(" ", "")  # 공백 제거 및 소문자 정리
    if len(hex_string) == 14:
        bytes = [hex_string[i:i + 14] for i in range(0, len(hex_string), 14)]
    elif len(hex_string) == 28:
        bytes = [hex_string[i:i + 28] for i in range(0, len(hex_string), 28)]
    else:
        bytes = [hex_string]
    return bytes

# 2025.11.04: The displayed value includes the value converted to an int of msb(By5) + lsb(By6)
def hex_to_signed(value: str, bits: int = 16) -> int:
    """주어진 16진수를 지정된 비트수의 signed 값으로 변환"""
    val = int(value, 16)
    if val >= 2 ** (bits - 1):
        val -= 2 ** bits
    return val


def convert_ascii_hex_to_position(ascii_hex, scale='0.01'):
    ascii_hex = str(ascii_hex).replace(' ', '')
    if len(ascii_hex) != 8:
        raise ValueError(f"ascii_hex must be 8 hex characters: {ascii_hex}")

    hex_text = ''.join(chr(int(ascii_hex[i:i + 2], 16)) for i in range(0, len(ascii_hex), 2))
    return (int(hex_text, 16) - 32768) * Decimal(str(scale))


def convert_speed_ascii_hex_to_dec(ascii_hex):
    ascii_hex = str(ascii_hex).replace(' ', '')
    if len(ascii_hex) != 4:
        raise ValueError(f"ascii_hex must be 4 hex characters: {ascii_hex}")

    hex_text = ''.join(chr(int(ascii_hex[i:i + 2], 16)) for i in range(0, len(ascii_hex), 2))

    return abs(int(hex_text, 16) - 64)


class Response:
    def __init__(self, root, pos):
        self.root = root
        self.pos = pos

        # 1) 바깥 컨테이너 Frame (이걸 root에 직접 배치)
        self.frame = tk.Frame(self.root, bg=pos['bg'])
        self.frame.place(x=pos['x'],
                         y=pos['y'] + 5,
                         width=pos['w'] - 30,
                         height=pos['h'] + 15)

        # 2) frame 안에서 Text + Scrollbar 를 pack으로 정렬
        self.text_widget = tk.Text(self.frame, bg='lightgray')
        self.text_font = font.Font(size=8)
        self.text_widget.configure(font=self.text_font)

        bold_font = font.Font(size=8, weight="bold")
        self.text_widget.tag_configure("bold", font=bold_font, foreground='green')

        scrollbar = tk.Scrollbar(self.frame,
                                 orient='vertical',
                                 command=self.text_widget.yview)

        # 왼쪽에 Text, 오른쪽에 Scrollbar
        self.text_widget.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

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

    # 2025.07.02 Display a Response Text for Multi
    # function drs_response_text have to modify
    def spaced_hex(self, hex_text):
        return " ".join([hex_text[i:i + 2] for i in range(0, len(hex_text), 2)])

    def insert_cmj_response(self, time_str, res_cmd, before_end, bold_ranges, after_start, label, value_text):
        before = self.spaced_hex(res_cmd[:before_end])
        after = self.spaced_hex(res_cmd[after_start:])

        self.text_widget.insert(tk.END, f"[{time_str}] {before} ")
        for idx, (start, end) in enumerate(bold_ranges):
            if idx > 0:
                self.text_widget.insert(tk.END, " ")
            self.text_widget.insert(tk.END, self.spaced_hex(res_cmd[start:end]), "bold")
        if after:
            self.text_widget.insert(tk.END, f" {after}")
        self.text_widget.insert(tk.END, f" : '{label}' {value_text}\n")

    def insert_cmj_pt_response(self, time_str, res_cmd):
        if res_cmd[6:10] in ['0181']:
            tilt_spd_raw = res_cmd[18:22]
            pan_spd_raw = res_cmd[22:26]
            pan = convert_speed_ascii_hex_to_dec(pan_spd_raw)
            tilt = convert_speed_ascii_hex_to_dec(tilt_spd_raw)
            self.insert_cmj_response(
                time_str=time_str,
                res_cmd=res_cmd,
                before_end=18,
                bold_ranges=[(18, 26)],
                after_start=26,
                label='Pan:Tilt Speed',
                value_text=f'{pan}:{tilt}',
            )
            return
        elif res_cmd[6:10] in ['0162', '3030']:
            if res_cmd[2:6] in ['3031']:
                print('No Error')
            else:
                pan_raw = res_cmd[10:18]
                tilt_raw = res_cmd[18:26]
                pan = convert_ascii_hex_to_position(pan_raw)
                tilt = convert_ascii_hex_to_position(tilt_raw)
                self.insert_cmj_response(
                    time_str=time_str,
                    res_cmd=res_cmd,
                    before_end=10,
                    bold_ranges=[(10, 18), (18, 26)],
                    after_start=26,
                    label='Pan:Tilt:',
                    value_text=f'{pan}:{tilt}',
                )
                return

    def multi_response(self, res_txt: str):
        current_time = datetime.now()
        time_str = current_time.strftime('%Y-%m-%d-%H:%M:%S')
        split_bytes = split_by_bytes(res_txt)

        for res_cmd in split_bytes:
            spaced = self.spaced_hex(res_cmd)
            if len(res_cmd) < 16:
                self.text_widget.insert(tk.END, f"[{time_str}] {spaced}\n")
                continue
            if Cons.selected_model in ['CMJ_PT']:
                self.insert_cmj_pt_response(time_str, res_cmd)
                continue
            else:
                pan = hex_to_signed(res_cmd[8:12], 16)
                tilt = hex_to_signed(res_cmd[12:16], 16)
            prefix = f"[{time_str}] {spaced} : 'Pan:Tilt:' "
            self.text_widget.insert(tk.END, prefix)
            self.text_widget.insert(tk.END, f"{pan}:{tilt}", "bold")
            self.text_widget.insert(tk.END, "\n")
        self.text_widget.see(tk.END)


