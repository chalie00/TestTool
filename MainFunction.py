import openpyxl
import tkinter
import string
import socket
import time as ti


import Dialog
import Communication as Th
import Constant as Cons
import Table as tb
import Response as Res

from tkinter import *
from tkinter import ttk
from ttkwidgets import CheckboxTreeview
from PIL import ImageGrab
from screeninfo import get_monitors
from datetime import time, datetime


# Set element(label, text field, button) as specified position and size
def make_element(x, y, h, w, element, *args, **kwargs):
    f = Frame(height=h, width=w)
    f.pack_propagate(0)  # don't shrink
    f.place(x=x, y=y)
    if element.lower() == 'label':
        label = Label(f, *args, **kwargs)
        label.pack(fill=BOTH, expand=1)
        return label
    elif element.lower() == 'entry':
        text_field = Entry(f, *args, **kwargs)
        text_field.pack(fill=BOTH, expand=1)
        return text_field
    elif element.lower() == 'button':
        btn = Button(f, *args, **kwargs)
        btn.pack(fill=BOTH, expand=1)
        return btn


# Set Command Table
# (2024.02.15) CheckBox Change a treeview to CheckTreeView  and event is changed to
#  Double-Button-1, CheckBox is controlled with tag
def make_table(root: tkinter, column_num: int, width: int, column_title: [string], x: int, y: int,
               cmd_data: []) -> CheckboxTreeview:
    # Create a table, column is name of column,
    # The displaycolumn shows the order in which the table is executed.

    host = Cons.host_ip
    input_port = Cons.port
    port = int(0) if Cons.port == '' else int(input_port)
    buf_size = Cons.buf_size

    column = [i + 1 for i in range(column_num)]
    dis_column = [str(n) for n in column]
    tv = CheckboxTreeview(root, height=29, columns=dis_column, displaycolumns=dis_column)
    # set the treeview scroll
    vsb = ttk.Scrollbar(root, orient='vertical', command=tv.yview)
    vsb.place(x=width * column_num + 100 + Cons.camera_resolution['w'], y=y, height=Cons.tree_view_size['h'])
    # tv = tkinter.ttk.Treeview(root, columns=column, displaycolumns=dis_column)
    # Treeview의 width, height 글자 수로 정해 진다.
    # tv.configure(height=len(Cons.command_array) + 1)
    tv.place(x=x, y=y)
    tv.configure(yscrollcommand=vsb.set)

    # Set the Table No Tab
    tv.column('#0', width=70, anchor='center', stretch='yes')
    tv.heading('#0', text='No', anchor='center')

    # Create each column(name, width, anchor)
    for i in range(column_num):
        tv.column(dis_column[i], width=width, anchor='center')
        tv.heading(dis_column[i], text=column_title[i], anchor='center')

    # Insert the command data in Table
    for i in range(len(cmd_data)):
        tv.insert('', 'end', text=i + 1, values=cmd_data[i], iid=str(i) + '번', tags=('unchecked',))
        # CMD Title Left Align
        # tv.column(dis_column[1], anchor='center')
        # tv.bind('<<TreeviewSelect>>', selectItem)
        # tv.bind('<<TreeviewSelect>>', lambda event, root_view=root: check_network_Info(event, root_view))
        model = Cons.selected_model

        if model == 'NYX Series':
            tv.bind('<Double-Button-1>', lambda event, root_view=root: send_data_for_nyx(event, root_view))
        elif model == 'Uncooled':
            tv.bind('<Double-Button-1>',
                    lambda event, root_view=root, tree=tv: clicked_table_element(event, root_view, tv))
    return tv


def convert_str_to_hex(hex_str_arr) -> []:
    hex_array = []
    for i in range(0, len(hex_str_arr), 2):
        hex_str = '0x' + hex_str_arr[i:i + 2]
        hex_int = int(hex_str, 16)
        hex_array.append(hex_int)

    return hex_array


def select_item(event, root_view) -> []:
    hex_array = []
    tree = event.widget
    # selection = [tree.item(item)["text"] for item in tree.selection()]
    selection = [tree.item(item)['values'][1] for item in tree.selection()]
    for i in range(0, len(selection[0]), 2):
        hex_str = '0x' + selection[0][i:i + 2]
        hex_int = int(hex_str, 16)
        hex_array.append(hex_int)

    return hex_array


# Check Whether Interval Button Active
def check_interval_active():
    Cons.interval_button.config(state='normal')
    cmd_title_count = len(Cons.script_hex_arrays)
    interval_count = len(Cons.interval_arrays)
    if cmd_title_count > interval_count:
        Cons.interval_button.configure(state='normal')
    else:
        Cons.interval_button.configure(state='disabled')


# Called when table element was clicked
def clicked_table_element(event, root_view, tv):
    host = Cons.host_ip
    input_port = Cons.port
    port = int(0) if Cons.port == '' else int(input_port)
    iden = tv.identify_row(event.y)
    tags = tv.item(iden, 'tags')
    item = tv.item(iden)
    # value is title that user was clicked
    value = item['values'][0]

    if not host or not port:
        print("Invalid command")
        show_network_dialog(root_view, 'Please enter a network info.')
        return

    if Cons.script_toggle_flag:
        handle_script_mode(event, value, root_view)
    else:
        handle_normal_mode(event, tags, iden, value, root_view, tv)


# 2024.07.04: Operating script mode
def handle_script_mode(event, value, root_view):
    Cons.data_sending = True
    hex_value = select_item(event, root_view)
    Cons.script_hex_arrays.append(hex_value)
    Cons.script_cmd_titles.append(value)
    print(Cons.script_cmd_titles)
    if not Cons.cmd_itv_arrays:
        Cons.cmd_itv_arrays = Cons.cmd_itv_arrays or [[0] * 2 for _ in range(len(Cons.script_cmd_titles))]
        for i, cmd_title in enumerate(Cons.script_cmd_titles):
            Cons.cmd_itv_arrays[i][0] = cmd_title
            print(Cons.cmd_itv_arrays[i])
    else:
        added = [value, 0]
        Cons.cmd_itv_arrays.append(added)
        print(f'added = {added}')
        print(Cons.cmd_itv_arrays)
        print(Cons.script_hex_arrays)
    script_tb = tb.Table(root_view)
    check_interval_active()


# 2024.07.04: Operating normal mode
def handle_normal_mode(event, tags, iden, value, root_view, tv):
    Cons.data_sending = True
    if 'checked' in tags:
        tv.item(iden, tags='unchecked')
    else:
        tv.item(iden, tags='checked')
    hex_value = select_item(event, root_view)
    print(hex_value)
    Th.send_data(hex_value, value, root_view)


# (2024.07.04): Clear the Script Arrays
def clr_table_arrays(root):
    Cons.script_hex_arrays = []
    Cons.script_cmd_titles = []
    Cons.interval_arrays = []
    Cons.cmd_itv_arrays = []
    tb.Table(root)


# PopUp when network textfield is empty
def show_network_dialog(root_view, dialog_text):
    # network_notification()
    dialog_txt = 'Please enter a network info.'
    dialog = Dialog.DialogBox(root_view, dialog_txt)


# Get the Command from csv file
# (2024.07.29) change protocol list base on selected model
def get_data_from_csv(file_path) -> [(str, str)]:
    wb = openpyxl.load_workbook(file_path, data_only=True)
    sel_model = Cons.selected_model
    command_data = []

    if sel_model in ['Uncooled', 'NYX Series']:
        sh = wb[f'{sel_model}']
    else:
        return command_data

    max_column = sh.max_column
    max_row = sh.max_row
    for i, row in enumerate(sh.iter_rows(max_col=max_column - 2, max_row=max_row - 2), start=3):
        cmd_title = sh.cell(row=i, column=2).value
        cmd_data = sh.cell(row=i, column=3).value
        cmd_pair = (cmd_title, cmd_data)
        command_data.append(cmd_pair)

    return command_data


# (2024.07.05) Capture a Image from RTSP
def capture_image(root, filename):
    x = root.winfo_rootx()
    y = root.winfo_rooty()
    w = root.winfo_width()
    h = root.winfo_height()
    print(x, y, w, h)
    # bbox = (x, y, Cons.camera_resolution['w'], Cons.camera_resolution['h'])
    bbox = (x, y, 1340, 860)
    image = ImageGrab.grab(bbox=bbox)
    image.save(filename)


def print_monitor_info():
    monitors = get_monitors()
    for i, monitor in enumerate(monitors):
        print(f"Monitor {i}:")
        print(f"  - X: {monitor.x}")
        print(f"  - Y: {monitor.y}")
        print(f"  - Width: {monitor.width}")
        print(f"  - Height: {monitor.height}")
        print()


# (2024.07.05) Get a Monitor Information
def get_secondary_monitor_bbox():
    monitors = get_monitors()
    if len(monitors) > 1:
        secondary_monitor = monitors[1]
        print(secondary_monitor.x, secondary_monitor.y,
              secondary_monitor.x + secondary_monitor.width,
              secondary_monitor.y + secondary_monitor.height)
        return (secondary_monitor.x, secondary_monitor.y,
                secondary_monitor.x + secondary_monitor.width,
                secondary_monitor.y + secondary_monitor.height)
    return None


def send_frame_to_server(root, send_form, host='192.168.100.234', send_port=39190):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, send_port))
        s.sendall(send_form.encode('utf-8'))
        response = s.recv(1024)

        current_time = datetime.now()
        time_str = current_time.strftime('%Y-%m-%d-%H:%M:%S')

        print(f"Received response: {response.decode('utf-8')}")
        response_with_time = fr'{time_str} : {response.decode('utf-8')}'
        Cons.response_txt.append(response_with_time)
        log_pos = Cons.log_txt_fld_info
        log_fld = Res.Response(root, log_pos)


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
    send_frame_to_server(root, form)


# (2024.7.22): Protocol send with command for NYX
def send_data_with_cmd_for_nyx(root, cmd):
    value = cmd
    print(f'value = {value}')
    form = create_form(value)
    send_frame_to_server(root, form)
