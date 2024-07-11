import socket
import logging
import time as ti
from datetime import time, datetime

import Constant as Cons
import MainFunction as Mf

from socket import AF_INET, SOCK_STREAM

import Dialog

# Sending Command with hex
def send_data(send_cmd, root_view):
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
            print(reply)
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
        time_str = current_time.strftime('%Y-%m-%d-%H.%M.%S')
        print(i)
        print(time_str)
        for i, protocol in enumerate(send_cmds):
            if Cons.data_sending:
                if protocol == Cons.capture_hex:
                    path = Cons.capture_path['zoom']
                    filename = rf'{path}/{cmd_title[i-1]}-{time_str}-{i}.png'
                    Mf.capture_image(root_view, filename)
                else:
                    send_data(protocol, root_view)
                    ti.sleep(interval[i])
            else:
                print('Protocol sending was stopped')
