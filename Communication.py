import binascii
import socket
import logging
import time as ti
from datetime import time, datetime

import Constant as Cons
import MainFunction as Mf
import Response as Res

from socket import AF_INET, SOCK_STREAM

import Dialog


# Sending Command with hex
def send_data(send_cmd, value, root_view):
    host = Cons.host_ip
    input_port = Cons.port
    port = int(0) if Cons.port == '' else int(input_port)
    buf_size = Cons.buf_size
    client = socket.socket(AF_INET, SOCK_STREAM)
    try:
        client.settimeout(3)
        # -*- coding: utf-8 -*-
        client.connect((host, port))
        # client.send(bytearray([0xff, 0x00, 0x21, 0x13, 0x00, 0x01, 0x35]))
        # client.send(bytes([0xff, 0x00, 0x21, 0x13, 0x00, 0x01, 0x35]))
        if Cons.data_sending:
            client.send(bytes(send_cmd))
            reply = client.recv(buf_size)
            hex_data = binascii.hexlify(reply).decode('utf-8')

            store_response(value, hex_data)

            current_time = datetime.now()
            time_str = current_time.strftime('%Y-%m-%d-%H:%M:%S')
            hex_with_time = fr'{time_str} : {hex_data}'
            print(rf'response = {hex_with_time}\n')
            Cons.response_txt.append(hex_with_time)
            log_pos = Cons.log_txt_fld_info
            log_fld = Res.Response(root_view, log_pos)

        else:
            print('Protocol sending was stopped')

    except socket.error as err:
        print(f'network error:{err}')
        dialog_txt = f'Network Error \n Please check a network info.\n {err}'
        Dialog.DialogBox(root_view, dialog_txt)
        logging.error(err)
    finally:
        client.close()


def send_data_with_interval(interval: [float], repeat: int, send_cmds: [int], cmd_title: [str], root_view):
    for i in range(repeat):
        current_time = datetime.now()
        time_str = current_time.strftime('%Y-%m-%d-%H:%M:%S')
        print(i)
        print(time_str)
        for i, protocol in enumerate(send_cmds):
            if Cons.data_sending:
                if protocol == Cons.capture_hex:
                    path = Cons.capture_path['zoom']
                    filename = rf'{path}/{cmd_title[i - 1]}-{time_str}-{i}.png'
                    Mf.capture_image(root_view, filename)
                else:
                    send_data(protocol, root_view)
                    ti.sleep(interval[i])
            else:
                print('Protocol sending was stopped')


# (2024.07.12) Save the response data in 14-digit increments.
def store_response(title, response):
    # res_arrays = []
    # for i in range(0, len(response), 14):
    #     res_data = response[i:i + 14]
    #     res_arrays.append(res_data)
    res_arrays = [response[i:i + 14] for i in range(0, len(response), 14)]
    print(res_arrays)
    queries = {
        'Zoom Query': (
            'zoom_q', ['zoom', 'magnification']
        ),
        'Focus Query': (
            'focus_q', ['focus']
        ),
        'Lens Query': (
            'lens_q', ['af_trigger', 'zoom_spd', 'focus_spd', 'af_mode', 'af_interval', 'fov_position', 'query_mode']
        ),
        'Comm Query': (
            'comm_q', ['mode', 'add', 'baud', 'word', 'stop', 'parity', 'protocol']
        ),
        'Image Query': (
            'image_q', ['dis', 'dnr', 'flip', 'mirror', 'freeze', 'dzoom', 'dzoom_position']
        ),
        'Sensor Query': (
            'sensor_q', ['histogram', 'brightness', 'contrast', 'white_hot', 'pseudo', 'edge']
        ),
        'Cali. Query': (
            'cali_q', ['trigger', 'mode', 'interval']
        ),
        'ETC Query': (
            'etc_q', ['save', 'cvbs', 'display']
        ),
        'Status Query': (
            'status_q', ['boot', 'board_t', 'lens_t', 'sensor_t', 'fan', 'telemetry', 'calibration', 'af']
        ),
        'Version Query': (
            'version_q', ['sensor', 'lens', 'main', 'main_y', 'main_m_d', 'osd', 'osd_y', 'osd_m_d']
        ),
        'Encoder Query': (
            'encoder_q', ['zoom_max', 'zoom_min', 'focus_max', 'focus_min']
        )
    }

    if title in queries:
        attr_name, keys = queries[title]
        if hasattr(Cons, attr_name):
            query_dict = getattr(Cons, attr_name)
            for i, key in enumerate(keys):
                if i < len(res_arrays):
                    query_dict[key] = res_arrays[i]
                else:
                    query_dict[key] = []
            print(query_dict)
        else:
            print(f"Error: {attr_name} not found in Cons.")
    else:
        print(f"Error: {title} is not a valid query title.")


