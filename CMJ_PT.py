import tkinter as tk
import socket
import logging
from typing import Literal, Optional

import Constant as Cons
import Communication as Comm
import ASYNC_Temp as Async

from decimal import Decimal, ROUND_HALF_UP
from socket import AF_INET, SOCK_STREAM


# 2026.06.17 Pan/Tilt Angle, Speed class was implemented
def convert_position_to_ascii_hex(position, scale):
    if Decimal(str(scale)) == 0:
        raise ValueError("scale must not be zero")

    rounded = Decimal(str(position)) / Decimal(str(scale))
    rounded = rounded.quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    converted_hex = f"{32768 + int(rounded):04X}"  # 04X: 4자리포멧 대문자 빈자리 앞은 0으로 채움
    return " ".join(f"{ord(char):02X}" for char in converted_hex)


# 0xFF Add1 Add2 Cmd1 Cmd2 Data 0xEF
# PT Add: 3030, EO Add: 3031, IR Add: 3032
# dir_ctrl is ['up', 'down', 'left', 'right']
def generate_cmd(ctl_mode: Literal['Angle', 'Speed'],
                 add: str, cmd: str, data: str, *, dir_ctrl=None, zoom=None, focus=None):
    add = str(add).replace(' ', '')
    cmd = str(cmd).replace(' ', '')
    data = '' if data is None else str(data).replace(' ', '')

    if ctl_mode == 'Angle':
        send_cmd = f'FF{add}{cmd}{data}EF'
        # ex) FF3030 0162 38303030 38303030 EF
        print(send_cmd)

    elif ctl_mode == 'Speed':
        zoom = '3430' if zoom is None else str(zoom).replace(' ', '')
        focus = '3430' if focus is None else str(focus).replace(' ', '')
        if dir_ctrl in ['up', 'down']:
            send_cmd = f'FF{add}{cmd}{zoom}{focus}{data}3430EF'
            # ex) FF3030 0181 Zoom stop(3430) focus stop(3430) Tilt Pan EF
        else:
            send_cmd = f'FF{add}{cmd}{zoom}{focus}3430{data}EF'

    return send_cmd


def hex_text_to_int_array(hex_text: str):
    hex_text = str(hex_text).replace(' ', '')
    if len(hex_text) % 2 != 0:
        raise ValueError(f"hex text length must be even: {hex_text}")

    hex_array = []
    for i in range(0, len(hex_text), 2):
        hex_str = '0x' + hex_text[i:i + 2]
        hex_int = int(hex_str, 16)
        hex_array.append(hex_int)
    return hex_array


class CMJ_PT:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=Cons.cmj_canvas['w'], height=Cons.ptz_canvas['h'])

        self.pan_tilt_lbl = tk.Label(self.root, text=Cons.cmj_pan_tilt_lbl['text'], bg=Cons.cmj_pan_tilt_lbl['bg'])
        self.pan_tilt_lbl.place(x=Cons.cmj_pan_tilt_lbl['x'], y=Cons.cmj_pan_tilt_lbl['y'],
                                width=Cons.cmj_pan_tilt_lbl['w'], height=Cons.cmj_pan_tilt_lbl['h'])
        self.pan_tilt_spd_lbl = tk.Label(self.root, text=Cons.cmj_pan_tilt_spd_lbl['text'],
                                         bg=Cons.cmj_pan_tilt_spd_lbl['bg'])
        self.pan_tilt_spd_lbl.place(x=Cons.cmj_pan_tilt_spd_lbl['x'], y=Cons.cmj_pan_tilt_spd_lbl['y'],
                                    width=Cons.cmj_pan_tilt_spd_lbl['w'], height=Cons.cmj_pan_tilt_spd_lbl['h'])

        self.canvas.place(x=Cons.cmj_canvas['x'], y=Cons.cmj_canvas['y'])
        self.pan_tilt_txt_fld = tk.Entry(self.root, justify='center')
        self.pan_tilt_txt_fld.place(x=Cons.cmj_pan_tilt_txt_fld['x'], y=Cons.cmj_pan_tilt_txt_fld['y'],
                                    width=Cons.cmj_pan_tilt_txt_fld['w'], height=Cons.cmj_pan_tilt_txt_fld['h'])
        self.pan_tilt_txt_fld.bind('<Return>', lambda event: self.send_angle_async())

        self.pan_tilt_spd_txt_fld = tk.Entry(self.root, justify='center')
        self.pan_tilt_spd_txt_fld.place(x=Cons.cmj_pan_tilt_spd_txt_fld['x'], y=Cons.cmj_pan_tilt_spd_txt_fld['y'],
                                        width=Cons.cmj_pan_tilt_spd_txt_fld['w'],
                                        height=Cons.cmj_pan_tilt_spd_txt_fld['h'])
        self.pan_tilt_spd_txt_fld.insert(0, 10)
        # self.pan_tilt_spd_txt_fld.bind('<Return>', lambda event: self.send_speed_async())

        self.call_move_btn = tk.Button(self.root, text=Cons.cmj_move_call_btn['text'],
                                       bg=Cons.cmj_move_call_btn['bg'],
                                       command=self.send_angle_async)
        self.call_move_btn.place(x=Cons.cmj_move_call_btn['x'], y=Cons.cmj_move_call_btn['y'],
                                 width=Cons.cmj_move_call_btn['w'], height=Cons.cmj_move_call_btn['h'])

    def convert_angle_dec_to_ascii_hex(self, scale='0.01'):
        """
        Convert DEC to the same ASCII HEX format as this Excel formula:
        DEC2HEX(CODE(MID(DEC2HEX(32768+ROUND(dec/scale,0),4),n,1)),2)

        Example:
            converted HEX text: "8000"
            returned ASCII HEX: "38 30 30 30"
        """
        dec_value = self.pan_tilt_txt_fld.get()
        pan_txt, tilt_txt = dec_value.split(',')

        pan_ascii_hex = convert_position_to_ascii_hex(pan_txt.strip(), scale)
        tilt_ascii_hex = convert_position_to_ascii_hex(tilt_txt.strip(), scale)

        print(pan_ascii_hex, tilt_ascii_hex)
        angle_val = pan_ascii_hex + tilt_ascii_hex
        cmd_txt = generate_cmd('Angle', 3030, '0162', angle_val)
        self.pan_tilt_txt_fld.delete(0, tk.END)

        return cmd_txt

    def convert_spd_dec_to_2digit_ascii_hex(self,
                                            direction: Literal['up', 'down', 'left', 'right', 'stop'] | None = None):
        dec_value = self.pan_tilt_spd_txt_fld.get()
        if direction in ['up', 'right']:
            converted_hex = f"{int(dec_value) * (-1) + 64:02X}"
        elif direction == 'stop':
            converted_hex = f"{int(0) + 64:02X}"
        else:
            converted_hex = f"{int(dec_value) + 64:02X}"
        spd_val = ''.join(f"{ord(char):02X}" for char in converted_hex)
        cmd_txt = generate_cmd('Speed', 3030, '0181', spd_val, dir_ctrl=direction)
        print(cmd_txt)

        return cmd_txt

    def send_angle_async(self):
        cmd_txt = self.convert_angle_dec_to_ascii_hex()
        Async.async_send(
            fn=lambda: self.send_cmd_to_cmj_pt(cmd_txt),
            title='CMJ_PT Angle',
            root_view=self.root,
        )

    # forward is pan CW and tilt up, reverse is pan CCW and tilt down
    def send_speed_async(self, direction: str):
        cmd_txt = self.convert_spd_dec_to_2digit_ascii_hex(direction=direction)
        Async.async_send(
            fn=lambda: self.send_cmd_to_cmj_pt(cmd_txt),
            title='CMJ_PT Speed',
            root_view=self.root,
        )

    def send_cmd_to_cmj_pt(self, cmd_txt, timeout=3):
        hex_array = hex_text_to_int_array(cmd_txt)
        payload = bytes(hex_array)
        host = Cons.tms_rtsp_info[2]['ip']
        port = int(Cons.tms_rtsp_info[2]['port'])

        client = socket.socket(AF_INET, SOCK_STREAM)
        try:
            client.settimeout(timeout)
            client.connect((host, port))
            client.sendall(payload)
            logging.info("send_cmd_to_cmj_pt host=%s port=%s tx=%s", host, port, payload.hex().upper())
            print(f"sent: {payload.hex().upper()}")
            return payload.hex().upper()
        except socket.error as err:
            print(f"network error:{err}")
            logging.error(err)
        finally:
            client.close()

# TODO: 2026.06.29 Script Test add
