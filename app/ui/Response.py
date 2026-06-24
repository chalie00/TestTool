# (2024.07.11) Init
import tkinter as tk

from tkinter import ttk
from datetime import time, datetime
from tkinter import font

from app.config import Constant as Cons
from app.parsers.CMJ_PT_Parser import (
    convert_ascii_hex_to_position, parse_camera_status,
    convert_ascii_hex_to_dec_encoder, convert_2byte_ascii_hex_to_dec,
    convert_dzoom_raw_to_rate
)


# 2025.07.02: Divide 7byte
def split_by_bytes(hex_string: str):
    # Normalize the input by removing spaces and converting to lowercase.
    hex_string = hex_string.lower().replace(" ", "")
    if len(hex_string) == 14:
        bytes = [hex_string[i:i + 14] for i in range(0, len(hex_string), 14)]
    elif len(hex_string) == 28:
        bytes = [hex_string[i:i + 28] for i in range(0, len(hex_string), 28)]
    else:
        bytes = [hex_string]
    return bytes


# 2025.11.04: The displayed value includes the value converted to an int of msb(By5) + lsb(By6)
def hex_to_signed(value: str, bits: int = 16) -> int:
    """Convert a hex string to a signed integer with the given bit width."""
    val = int(value, 16)
    if val >= 2 ** (bits - 1):
        val -= 2 ** bits
    return val


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

        # Outer container frame for the response text area.
        self.frame = tk.Frame(self.root, bg=pos['bg'])
        self.frame.place(x=pos['x'],
                         y=pos['y'] + 5,
                         width=pos['w'] - 30,
                         height=pos['h'] + 15)

        # Place the text widget and scrollbar inside the frame.
        self.text_widget = tk.Text(self.frame, bg='lightgray')
        self.text_font = font.Font(size=8)
        self.text_widget.configure(font=self.text_font)

        bold_font = font.Font(size=8, weight="bold")
        self.text_widget.tag_configure("bold", font=bold_font, foreground='green')

        scrollbar = tk.Scrollbar(self.frame,
                                 orient='vertical',
                                 command=self.text_widget.yview)

        # Text on the left, scrollbar on the right.
        self.text_widget.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        self.text_widget.config(yscrollcommand=scrollbar.set)

        self.dis_response_text()

    # (2024.10.31): Apply green color text to UncooledType response value
    # Response Text
    def dis_response_text(self):
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.delete(1.0, tk.END)  # Clear existing text.

        if Cons.selected_model in ['Uncooled', 'NYX Series']:
            dis_txt = list(reversed(Cons.response_txt))
            for i, txt in enumerate(dis_txt[:30]):
                self.text_widget.insert(tk.END, txt + '\n')
                if Cons.selected_model == 'Uncooled':
                    # Get the start index for this line
                    line_index = f"{i + 1}.0"  # Tkinter text lines are 1-based.
                    if len(txt) != 30 and len(txt) >= 12:  # Highlight bytes 8-12 when present.
                        start_index = f"{i + 1}.8"  # Start at the 8th character.
                        end_index = f"{i + 1}.12"  # End at the 12th character.
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

    def insert_cmj_response(self, time_str, res_cmd,
                            before_end=None, bold_ranges=None, after_start=None, label=None, value_text=None):
        before = self.spaced_hex(res_cmd[:before_end])
        after = self.spaced_hex(res_cmd[after_start:])

        self.text_widget.insert(tk.END, f"[{time_str}] {before} ")
        for idx, (start, end) in enumerate(bold_ranges):
            if idx > 0:
                self.text_widget.insert(tk.END, " ")
            self.text_widget.insert(tk.END, self.spaced_hex(res_cmd[start:end]), "bold")
        if after:
            self.text_widget.insert(tk.END, f" {after}")
        self.text_widget.insert(tk.END, f" : {label} {value_text}\n")

    def insert_camera_status_response(self, time_str, camera_sta):
        status_text = ", ".join([f"{key}: {value}" for key, value in camera_sta.items()])
        self.text_widget.insert(tk.END, f"[{time_str}] {status_text}\n")

    def insert_cmj_pt_response(self, time_str, res_cmd):
        addr = res_cmd[2:6]
        cmd = res_cmd[6:10]

        if addr in ['3031', '3032'] and cmd in ['0162', '3030']:
            if len(res_cmd) == 20:
                encoder = convert_ascii_hex_to_dec_encoder(res_cmd[10:18])
                self.insert_cmj_response(
                    time_str=time_str,
                    res_cmd=res_cmd,
                    before_end=10,
                    bold_ranges=[(10, 18)],
                    after_start=18,
                    label='Encoder value is',
                    value_text=f'{encoder}',
                )
                return
            elif len(res_cmd) == 16:
                defog = convert_2byte_ascii_hex_to_dec(res_cmd[10:14])
                dzoom_raw = convert_2byte_ascii_hex_to_dec(res_cmd[10:14])
                if dzoom_raw <= 70 and dzoom_raw%10 == 0:
                    dzoom = convert_dzoom_raw_to_rate(dzoom_raw)
                else:
                    dzoom = 'XXX'
                self.insert_cmj_response(
                    time_str=time_str,
                    res_cmd=res_cmd,
                    before_end=10,
                    bold_ranges=[(10, 14)],
                    after_start=14,
                    label=f'\n If the query is dzoom, the dzoom is x{dzoom}, otherwise, the value for defog is {defog}.',
                    value_text=f'',
                )
                return
            elif len(res_cmd) == 14:
                dis_raw = res_cmd[10:12]
                dis = 'OFF' if dis_raw == '30' else 'ON'
                self.insert_cmj_response(
                    time_str=time_str,
                    res_cmd=res_cmd,
                    before_end=10,
                    bold_ranges=[(10, 12)],
                    after_start=12,
                    label=f'DIS is ',
                    value_text=f'{dis}',
                )
                return
            camera_sta = parse_camera_status(res_cmd)
            print(camera_sta)
            self.insert_camera_status_response(time_str, camera_sta)
            return

        if cmd in ['0181']:
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

        if cmd in ['0162', '3030']:
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
            if Cons.selected_model in ['CMJ_PT'] and len(res_cmd) > 12:
                self.insert_cmj_pt_response(time_str, res_cmd)
                continue
            if len(res_cmd) <= 12:
                self.text_widget.insert(tk.END, f"[{time_str}] {spaced}\n")
                continue
            else:
                pan = hex_to_signed(res_cmd[8:12], 16)
                tilt = hex_to_signed(res_cmd[12:16], 16)
            prefix = f"[{time_str}] {spaced} : 'Pan:Tilt:' "
            self.text_widget.insert(tk.END, prefix)
            self.text_widget.insert(tk.END, f"{pan}:{tilt}", "bold")
            self.text_widget.insert(tk.END, "\n")
        self.text_widget.see(tk.END)

