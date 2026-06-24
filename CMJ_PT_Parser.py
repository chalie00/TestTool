from decimal import Decimal, ROUND_HALF_UP
from typing import Literal


# 2026.06.23 Implemented a parser for camera status and moved the conversion functions.
def convert_position_to_ascii_hex(position, scale):
    if Decimal(str(scale)) == 0:
        raise ValueError("scale must not be zero")

    rounded = Decimal(str(position)) / Decimal(str(scale))
    rounded = rounded.quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    converted_hex = f"{32768 + int(rounded):04X}"
    return " ".join(f"{ord(char):02X}" for char in converted_hex)


def convert_ascii_hex_to_position(ascii_hex, scale='0.01'):
    ascii_hex = str(ascii_hex).replace(' ', '')
    if len(ascii_hex) != 8:
        raise ValueError(f"ascii_hex must be 8 hex characters: {ascii_hex}")

    hex_text = ''.join(chr(int(ascii_hex[i:i + 2], 16)) for i in range(0, len(ascii_hex), 2))
    return (int(hex_text, 16) - 32768) * Decimal(str(scale))


def convert_ascii_hex_to_dec_encoder(ascii_hex):
    ascii_hex = str(ascii_hex).replace(' ', '')
    if len(ascii_hex) != 8:
        raise ValueError(f"ascii_hex must be 8 hex characters: {ascii_hex}")

    hex_text = ''.join(chr(int(ascii_hex[i:i + 2], 16)) for i in range(0, len(ascii_hex), 2))
    return int(hex_text, 16)


def convert_2byte_ascii_hex_to_dec(ascii_hex):
    ascii_hex = str(ascii_hex).replace(' ', '')
    if len(ascii_hex) != 4:
        raise ValueError(f"ascii_hex must be 4 hex characters: {ascii_hex}")

    dec_text = ''.join(chr(int(ascii_hex[i:i + 2], 16)) for i in range(0, len(ascii_hex), 2))
    return int(dec_text, 16)


def convert_1byte_ascii_hex_to_status(ascii_hex):
    ascii_hex = str(ascii_hex).replace(' ', '')
    if len(ascii_hex) != 2:
        raise ValueError(f"ascii_hex must be 2 hex characters: {ascii_hex}")

    status_text = chr(int(ascii_hex, 16))
    if status_text not in ['0', '1']:
        raise ValueError(f"status must be ASCII 0 or 1: {ascii_hex}")
    return status_text == '1'


def convert_dzoom_raw_to_rate(dzoom_raw):
    if not 0 <= dzoom_raw <= 70:
        raise ValueError(f"dzoom out of range: {dzoom_raw}")
    if dzoom_raw % 10 != 0:
        raise ValueError(f"dzoom must increase by 10: {dzoom_raw}")

    return 1 + (dzoom_raw // 10)


def parse_camera_status(res_cmd):
    res_cmd = str(res_cmd).replace(' ', '')
    if len(res_cmd) < 36:
        raise ValueError(f"res_cmd must include byte 18: {res_cmd}")

    zoom_pos = convert_ascii_hex_to_dec_encoder(res_cmd[10:18])
    focus_pos = convert_ascii_hex_to_dec_encoder(res_cmd[18:26])
    dzoom_raw = convert_2byte_ascii_hex_to_dec(res_cmd[26:30])
    dzoom_rate = convert_dzoom_raw_to_rate(dzoom_raw)
    defog = convert_2byte_ascii_hex_to_dec(res_cmd[30:34])
    stabilizer = convert_1byte_ascii_hex_to_status(res_cmd[34:36])

    if not 0 <= zoom_pos <= 65535:
        raise ValueError(f"zoom_pos out of range: {zoom_pos}")
    if not 0 <= focus_pos <= 65535:
        raise ValueError(f"focus_pos out of range: {focus_pos}")
    if not 0 <= defog <= 100:
        raise ValueError(f"defog out of range: {defog}")

    return {
        'zoom_pos': zoom_pos,
        'focus_pos': focus_pos,
        'dzoom': f'x{dzoom_rate}',
        'defog': defog,
        'dis': stabilizer,
    }


def generate_cmd(ctl_mode: Literal['Angle', 'Speed'],
                 add: str, cmd: str, data: str, *, dir_ctrl=None, zoom=None, focus=None):
    add = str(add).replace(' ', '')
    cmd = str(cmd).replace(' ', '')
    data = '' if data is None else str(data).replace(' ', '')

    if ctl_mode == 'Angle':
        send_cmd = f'FF{add}{cmd}{data}EF'
        print(send_cmd)
    elif ctl_mode == 'Speed':
        zoom = '3430' if zoom is None else str(zoom).replace(' ', '')
        focus = '3430' if focus is None else str(focus).replace(' ', '')
        if dir_ctrl in ['up', 'down']:
            send_cmd = f'FF{add}{cmd}{zoom}{focus}{data}3430EF'
        else:
            send_cmd = f'FF{add}{cmd}{zoom}{focus}3430{data}EF'
    else:
        raise ValueError(f"unsupported control mode: {ctl_mode}")

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
