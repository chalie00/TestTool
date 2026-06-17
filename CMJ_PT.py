import tkinter as tk
import socket
import logging

import Constant as Cons
import Communication as Comm

from decimal import Decimal, ROUND_HALF_UP
from socket import AF_INET, SOCK_STREAM


# 2026.06.17 Pan/Tilt Angle, Speed class was implemented
def convert_position_to_ascii_hex(position, scale):
    if Decimal(str(scale)) == 0:
        raise ValueError("scale must not be zero")

    rounded = Decimal(str(position)) / Decimal(str(scale))
    rounded = rounded.quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    converted_hex = f"{32768 + int(rounded):04X}"
    return " ".join(f"{ord(char):02X}" for char in converted_hex)


def generate_cmd(add: str, cmd: str, data: str | None = None):
    add = str(add).replace(' ', '')
    cmd = str(cmd).replace(' ', '')
    data = '' if data is None else str(data).replace(' ', '')
    send_cmd = f'FF{add}{cmd}{data}EF'
    # ex) FF3030 0162 38303030 38303030 EF
    print(send_cmd)
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
        self.pan_tilt_txt_fld.bind('<Return>', lambda event: self.convert_dec_to_ascii_hex())

        self.pan_tilt_spd_txt_fld = tk.Entry(self.root, justify='center')
        self.pan_tilt_spd_txt_fld.place(x=Cons.cmj_pan_tilt_spd_txt_fld['x'], y=Cons.cmj_pan_tilt_spd_txt_fld['y'],
                                        width=Cons.cmj_pan_tilt_spd_txt_fld['w'],
                                        height=Cons.cmj_pan_tilt_spd_txt_fld['h'])

        self.call_move_btn = tk.Button(self.root, text=Cons.cmj_move_call_btn['text'],
                                       bg=Cons.cmj_move_call_btn['bg'],
                                       command=self.convert_dec_to_ascii_hex)
        self.call_move_btn.place(x=Cons.cmj_move_call_btn['x'], y=Cons.cmj_move_call_btn['y'],
                                 width=Cons.cmj_move_call_btn['w'], height=Cons.cmj_move_call_btn['h'])

    def convert_dec_to_ascii_hex(self, scale='0.01'):
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
        val = pan_ascii_hex + tilt_ascii_hex
        cmd_txt = generate_cmd(3030, '0162', val)
        self.send_cmd_to_cmj_pt(cmd_txt)

        return cmd_txt

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
        except socket.error as err:
            print(f"network error:{err}")
            logging.error(err)
        finally:
            client.close()

    def send_dec_ascii_hex_to_ip(self, dec_value, scale, host, port, wait_reply=False, timeout=3):
        """
        Convert DEC with convert_dec_to_excel_ascii_hex() and send it to host:port by TCP.
        The sent bytes are the ASCII HEX text itself.

        Example:
            "38 30 30 30" is sent as b"38 30 30 30".
        """
        ascii_hex = self.convert_dec_to_ascii_hex(dec_value, scale)
        payload = ascii_hex.encode("ascii")

        client = socket.socket(AF_INET, SOCK_STREAM)
        try:
            client.settimeout(timeout)
            client.connect((host, int(port)))
            client.sendall(payload)
            logging.info("send_dec_ascii_hex_to_ip host=%s port=%s tx=%s",
                         host, port, payload.decode("ascii"))

            if wait_reply:
                reply = client.recv(Cons.READ_MAX_BYTES)
                logging.info("send_dec_ascii_hex_to_ip rx=%s", reply.hex())
                return reply

            return None

        except socket.error as err:
            print(f"network error:{err}")
            logging.error(err)
            return None
        finally:
            client.close()

    # 0xFF Add1 Add2 Cmd1 Cmd2 Data 0xEF
    # PT Add: 3030, EO Add: 3031, IR Add: 3032

