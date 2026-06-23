import tkinter as tk
import socket
import logging
from typing import Literal

import Constant as Cons
import ASYNC_Temp as Async
from CMJ_PT_Parser import (
    convert_position_to_ascii_hex,
    generate_cmd,
    hex_text_to_int_array,
)

from socket import AF_INET, SOCK_STREAM


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
