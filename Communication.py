import main

import binascii
import socket
import logging
import time as ti
from datetime import datetime

import Constant as Cons
import MainFunction as Mf
import Response as Res
import System_Info as SysInfo
import DRS_Response as DR_r

from socket import AF_INET, SOCK_STREAM

import Dialog


# Sending Command with hex
def send_cmd_for_uncooled(send_cmd, title, root_view):
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
            hex_data_14dig = [f'{hex_data[i:i + 14]} \n' for i in range(0, len(hex_data), 14)]
            # (2024.07.17) Add 22 blank spaces to all elements except the first one
            hex_data_14dig_24space = [f'{line}' if i == 0 else f'{" " * 22}{line}' for i, line in
                                      enumerate(hex_data_14dig)]
            # print(hex_data_14dig_24space)

            # Store Constant for display Query
            uncooled_store_response(root_view, title, hex_data)

            current_time = datetime.now()
            time_str = current_time.strftime('%Y-%m-%d-%H:%M:%S')
            hex_with_time = fr'{time_str} : {hex_data_14dig_24space[0]}'
            # print(response = {hex_with_time}\n')
            hex_data_14dig_24space[0] = hex_with_time
            for item in hex_data_14dig_24space:
                Cons.response_txt.append(item)
            # print(Cons.response_txt)
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


def send_cmd_to_ucooled_with_interval(interval: [float], repeat: int, send_cmds: [int], cmd_title: [str], root_view):
    current_time = datetime.now()
    time_str = current_time.strftime('%Y-%m-%d-%H-%M-%S')
    print(time_str)
    for i, protocol in enumerate(send_cmds):
        if Cons.data_sending:
            if protocol == Cons.capture_hex:
                path = Cons.capture_path['zoom']
                filename = rf'{path}/{cmd_title[i - 1]}-{time_str}-{i}.png'
                Mf.capture_image(root_view, filename)
            else:
                title = cmd_title[i - 1]
                if Cons.selected_model == 'Uncooled':
                    send_cmd_for_uncooled(protocol, 'Normal Query', root_view)
                elif Cons.selected_model == 'DRS':
                    send_cmd_for_drs(protocol, root_view)
                ti.sleep(interval[i])
        else:
            print('Protocol sending was stopped')


# (2024.07.12) Save the response data in 14-digit increments.
def uncooled_store_response(root_view, title, response):
    # res_arrays = []
    # for i in range(0, len(response), 14):
    #     res_data = response[i:i + 14]
    #     res_arrays.append(res_data)
    res_arrays = [response[i:i + 14] for i in range(0, len(response), 14)]
    print(res_arrays)
    queries = {
        'Normal Query': (
            'uncooled_normal_q', ['normal']
        ),
        'Zoom Query': (
            'uncooled_zoom_q', ['zoom', 'magnification']
        ),
        'Focus Query': (
            'uncooled_focus_q', ['focus']
        ),
        'Lens Query': (
            'uncooled_lens_q',
            ['af_trigger', 'zoom_spd', 'focus_spd', 'af_mode', 'af_interval', 'fov_position', 'query_mode']
        ),
        'Comm Query': (
            'uncooled_comm_q', ['mode', 'add', 'baud', 'word', 'stop', 'parity', 'protocol']
        ),
        'Image Query': (
            'uncooled_image_q', ['dis', 'dnr', 'flip', 'mirror', 'freeze', 'dzoom', 'dzoom_position']
        ),
        'Sensor Query': (
            'uncooled_sensor_q', ['histogram', 'brightness', 'contrast', 'white_hot', 'pseudo', 'edge']
        ),
        'Cali. Query': (
            'uncooled_cali_q', ['trigger', 'mode', 'interval']
        ),
        'ETC Query': (
            'uncooled_etc_q', ['save', 'cvbs', 'display']
        ),
        'Status Query': (
            'uncooled_status_q', ['boot', 'board_t', 'lens_t', 'sensor_t', 'fan', 'telemetry', 'calibration', 'af']
        ),
        'Version Query': (
            'uncooled_version_q', ['sensor', 'lens', 'main', 'main_y', 'main_m_d', 'osd', 'osd_y', 'osd_m_d']
        ),
        'Encoder Query': (
            'uncooled_encoder_q', ['zoom_max', 'zoom_min', 'focus_max', 'focus_min']
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

    convert_str_with_hex(root_view)


# (2024.07.15) Convert to String from hex Data
def convert_str_with_hex(root_view):
    def extract_hex_value(data_list):
        result = []
        for item in data_list:
            data_chunks = [item[i:i + 2] for i in range(0, len(item), 2)]
            int_value = 0
            if len(data_chunks) > 4:
                msb = data_chunks[4]
                lsb = data_chunks[5]
                hex_str = '0x' + msb + lsb
                int_value = int(hex_str, 16)
                # print(int_value)
            result.append(int_value)
        return result

    # (2024.07.16) Get the System Info. Table Data From Constant
    zoom_msb_lsb = [Cons.uncooled_zoom_q['zoom'], Cons.uncooled_lens_q['zoom_spd'],
                    Cons.uncooled_image_q['dzoom'], Cons.uncooled_image_q['dzoom_position']]
    focus_msb_lsb = [Cons.uncooled_focus_q['focus'], Cons.uncooled_lens_q['focus_spd'], Cons.uncooled_lens_q['af_mode']]
    fov_msb_lsb = [Cons.uncooled_lens_q['fov_position']]

    zoom_str = extract_hex_value(zoom_msb_lsb)
    focus_str = extract_hex_value(focus_msb_lsb)
    fov_str = extract_hex_value(fov_msb_lsb)
    Cons.zoom_msb_lsb = zoom_str
    Cons.focus_msb_lsb = focus_str
    Cons.fov_msb_lsb = fov_str
    SysInfo.SysInfo(root_view, Cons.sys_info_tab)


# (2024.07.19): Open socket and send cmd to nyx
def send_cmd_to_nyx(root, cmd):
    host = Cons.host_ip
    input_port = Cons.port
    send_port = int(0) if Cons.port == '' else int(input_port)
    buf_size = Cons.buf_size
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, send_port))
        s.sendall(cmd.encode('utf-8'))
        response = s.recv(1024)

        current_time = datetime.now()
        time_str = current_time.strftime('%Y-%m-%d-%H:%M:%S')

        print(f"Received response: {response.decode('utf-8')}")
        response_with_time = fr'{time_str} : {response.decode('utf-8')}'
        Cons.response_txt.append(response_with_time)
        log_pos = Cons.log_txt_fld_info
        log_fld = Res.Response(root, log_pos)


# (2024.07.24): Open socket and store to Constant after send cmd with interval
def send_cmd_to_nyx_with_interval(root, titles, cmds, intervals_sec, response_file_name):
    host = Cons.host_ip
    input_port = Cons.port
    send_port = int(0) if Cons.port == '' else int(input_port)
    buf_size = Cons.buf_size

    send_cmds = []

    for cmd in cmds:
        send_cmd = create_form(cmd)
        send_cmds.append(send_cmd)
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, send_port))
            for i, s_cmd in enumerate(send_cmds):
                s.sendall(s_cmd.encode('utf-8'))
                response = s.recv(1024)
                current_time = datetime.now()
                time_str = current_time.strftime('%Y-%m-%d-%H-%M-%S')

                if response_file_name:
                    # Open file in write mode (creates a new file)
                    with open(response_file_name, 'a') as a:
                        response_with_time = fr'{time_str} : {response.decode('utf-8')}'
                        a.write(response_with_time + '\n')
                else:
                    with open(response_file_name, 'w') as w:
                        response_with_time = fr'{time_str} : {response.decode('utf-8')}'
                        w.write(response_with_time + '\n')

                print(f"Received response: {response.decode('utf-8')}")

                if (
                        'NYX.ACK#syst_stat=standby&lens_fpos' not in response.decode('utf-8') or
                        'NYX.ACK#lens_zpos=' not in response.decode('utf-8') or
                        'NYX.ACK#lens_fpos=' not in response.decode('utf-8') or
                        'NYX.ACK#lens_zctl=' not in response.decode('utf-8') or
                        'NYX.ACK#lens_fctl=' not in response.decode('utf-8')
                ):
                    response_with_time = fr'{time_str} : {(response.decode('utf-8').split('\n'))[0]}'
                else:
                    response_with_time = fr'{time_str} : {response.decode('utf-8')}'

                Cons.response_txt.append(response_with_time)
                log_pos = Cons.log_txt_fld_info
                ti.sleep(intervals_sec[i])
                log_fld = Res.Response(root, log_pos)

    except Exception as e:
        print(f"An error occurred: {e}")
    ti.sleep(3)


# 2024.07.19): Calculate LRC for NYX
def calc_lrc(send_form):
    lrc_key = 0x40
    lrc = 0

    for char in send_form:
        # convert each character of string to unicode int
        lrc += ord(char)

    lrc = (lrc ^ 0xFF) + 0x01
    lrc_hi = lrc_key + ((lrc >> 4) & 0x0F)
    lrc_lo = lrc_key + (lrc & 0x0F)

    return chr(lrc_hi), chr(lrc_lo)


# (2024.07.19): Create Protocol form for NYX
def create_form(cmd):
    lrc_hi, lrc_lo = calc_lrc(cmd)
    cmd += lrc_hi + lrc_lo + '\n'
    return cmd


# (2024.07.19): Protocol send function for NYX
def send_data_for_nyx(event, root):
    tree = event.widget
    # get id of select item
    selected_item = tree.selection()[0]
    # get item of selected id
    item = tree.item(selected_item)
    values = item['values'][1]
    form = create_form(values)
    send_cmd_to_nyx(root, form)


# (2024.7.22): Protocol send with command for NYX
def send_data_with_cmd_for_nyx_ptz(root, cmd):
    value = cmd
    print(f'value = {value}')
    form = create_form(value)
    send_cmd_to_nyx(root, form)


# (2024.07.30): query for information
def send_data_with_cmd_for_info(root, cmds):
    host = Cons.host_ip
    input_port = Cons.port
    send_port = int(0) if Cons.port == '' else int(input_port)
    buf_size = Cons.buf_size

    responses = []
    for cmd in cmds:
        form = create_form(cmd)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, send_port))
            s.sendall(form.encode('utf-8'))
            response = s.recv(1024)
            res_decode = response.decode('utf-8')
            start_digi = len(cmd)
            info_data = res_decode[start_digi:-3]
            responses.append(info_data)
    Cons.cooled_lens_pos_spd = responses


# def send_cmd_for_drs(send_cmd, root_view):
#     host = Cons.host_ip
#     input_port = Cons.port
#     port = int(0) if Cons.port == '' else int(input_port)
#     buf_size = Cons.buf_size
#     client = socket.socket(AF_INET, SOCK_STREAM)
#     try:
#         client.settimeout(3)
#         client.connect((host, port))
#         # client.send(bytearray([0xff, 0x00, 0x21, 0x13, 0x00, 0x01, 0x35]))
#         # client.send(bytes([0xff, 0x00, 0x21, 0x13, 0x00, 0x01, 0x35]))
#         client.send(bytes(send_cmd))
#         reply = client.recv(buf_size)
#         lsb = reply[::2]
#         msb = reply[1::2]
#         binary = [format(m, '08b') + format(l, '08b') for m, l in zip(msb, lsb)]
#         for i, binary_pair in enumerate(binary):
#             # print(rf'{i} = {binary_pair}')
#             if i == 1:
#                 DR_r.check_data01(binary_pair)
#             elif i == 2:
#                 DR_r.check_data02(binary_pair)
#             elif i == 3:
#                 position_x = DR_r.convert_to_deci(binary_pair)
#                 Cons.drs_response['roi_x_start_x_pos'] = position_x
#             elif i == 4:
#                 position_y = DR_r.convert_to_deci(binary_pair)
#                 Cons.drs_response['roi_x_start_y_pos'] = position_y
#             elif i == 5:
#                 DR_r.check_data05(binary_pair)
#             elif i == 6:
#                 DR_r.check_data06(binary_pair)
#             elif i == 7:
#                 contrast = DR_r.convert_to_deci(binary_pair)
#                 Cons.drs_response['contrast'] = contrast
#             elif i == 8:
#                 brightness = DR_r.convert_to_deci(binary_pair)
#                 Cons.drs_response['brightness'] = brightness
#             elif i == 9:
#                 DR_r.check_data09(binary_pair)
#             elif i == 10:
#                 serial = DR_r.convert_to_deci(binary_pair)
#                 serial_hex = format(serial, 'x')
#                 Cons.drs_response['serial'] = serial_hex
#             elif i == 11:
#                 shutter_temp = DR_r.convert_to_deci(binary_pair)
#                 cal_shutter_temp = (shutter_temp - 27300) / 100
#                 Cons.drs_response['shutter_temp'] = cal_shutter_temp
#
#         log_pos = Cons.log_txt_fld_info
#         log_fld = Res.Response(root_view, log_pos)
#         # print(Cons.drs_response)
#
#     except socket.error as err:
#         print(f'network error:{err}')
#         dialog_txt = f'Network Error \n Please check a network info.\n {err}'
#         Dialog.DialogBox(root_view, dialog_txt)
#         logging.error(err)
#     finally:
#         client.close()

# (2024.08.13): Added send cmd function for DRS
def send_cmd_for_drs(send_cmd, root_view):
    host = Cons.host_ip
    port = int(0) if Cons.port == '' else int(Cons.port)
    buf_size = Cons.buf_size

    client = socket.socket(AF_INET, SOCK_STREAM)
    try:
        client.settimeout(3)
        client.connect((host, port))
        client.send(bytes(send_cmd))
        reply = client.recv(buf_size)

        # 데이터 파싱 함수 호출
        parse_drs_reply(reply)

        # 로그 창에 응답 표시
        log_pos = Cons.log_txt_fld_info
        log_fld = Res.Response(root_view, log_pos)
    except socket.error as err:
        handle_network_error(err, root_view)
    finally:
        client.close()


def parse_drs_reply(reply):
    lsb = reply[::2]
    msb = reply[1::2]
    binary_pairs = [format(m, '08b') + format(l, '08b') for m, l in zip(msb, lsb)]

    handlers = {
        1: DR_r.check_data01,
        2: DR_r.check_data02,
        3: lambda binary: update_drs_response('roi_x_start_x_pos', DR_r.convert_to_deci(binary)),
        4: lambda binary: update_drs_response('roi_x_start_y_pos', DR_r.convert_to_deci(binary)),
        5: DR_r.check_data05,
        6: DR_r.check_data06,
        7: lambda binary: update_drs_response('contrast', DR_r.convert_to_deci(binary)),
        8: lambda binary: update_drs_response('brightness', DR_r.convert_to_deci(binary)),
        9: DR_r.check_data09,
        10: lambda binary: update_drs_response('serial', format(DR_r.convert_to_deci(binary), 'x')),
        11: lambda binary: update_drs_response('shutter_temp', (DR_r.convert_to_deci(binary) - 27300) / 100),
        12: lambda binary: update_drs_response('roi_x_threshold_temp', format(DR_r.convert_to_deci(binary), 'x')),
        13: lambda binary: update_drs_response('center_temp', (DR_r.convert_to_deci(binary) / 10)),
        14: DR_r.check_data14,
        15: lambda binary: update_drs_response('zoom_pos', DR_r.convert_to_deci(binary)),
        16: lambda binary: update_drs_response('focus_pos', DR_r.convert_to_deci(binary)),


    }

    for i, binary_pair in enumerate(binary_pairs):
        if i in handlers:
            handlers[i](binary_pair)


def update_drs_response(key, value):
    Cons.drs_response[key] = value


def handle_network_error(err, root_view):
    print(f'network error: {err}')
    dialog_txt = f'Network Error \n Please check a network info.\n {err}'
    Dialog.DialogBox(root_view, dialog_txt)
    logging.error(err)
