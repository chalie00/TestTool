import array
from tkinter import *

import MainFunction as Mf

# Set the Application Size, Position with System Resolution
SYS_RESOLUTION = {'x': 1920, 'y': 1080}
WINDOWS_SIZE = {'x': 1850, 'y': 900}
WINDOWS_POSITION = {"x": int((SYS_RESOLUTION['x'] - WINDOWS_SIZE['x']) / 2),
                    "y": int((SYS_RESOLUTION['y'] - WINDOWS_SIZE['y']) / 2)}

POPUP_SIZE = {'x': int(WINDOWS_SIZE['x'] / 2), 'y': int(WINDOWS_SIZE['y'] / 4)}
POPUP_POSITION = {'x': int(WINDOWS_POSITION['x'] + WINDOWS_SIZE['x'] / 2 - POPUP_SIZE['x'] / 2),
                  'y': int(WINDOWS_POSITION['y'] + WINDOWS_SIZE['y'] / 2 - POPUP_SIZE['y'] / 2)}

my_color = {
    'bg': '#FFF8E3',  # Beige
    'fg': '#F3D7CA',  # Peach
    'spare_fir': '#F5EEE6',  # Gray
    'spare_sec': '#E6A4B4',  # Pink
    'noti_bg': '#FFFC9B',  # Yellow
    'noti_txt': '#FFA447'  # Orange
}

camera_resolution = {'w': 1280, 'h': 720}

# information Label and Text Field Size, Position
info_start_pos = {'x': camera_resolution['w'] + 30, 'y': 0}
lbl_size = {'h': WINDOWS_SIZE['y'] / 50, 'w': WINDOWS_SIZE['x'] / 20}

# Command File Position
cmd_path = rf'Command/Command.xlsx'

# Table Data
# column_array = ['Function', 'Command', 'Remark'] : 'Remark' is Deleted due to addition of VLC player
column_array = ['Function', 'Command']
# 0xff, 0x00, 0x21, 0x13, 0x00, 0x01, 0x35
# command_array = [('Color Mode Gray', 'ff002113000034'),
#                  ('Color Mode Rainbow', 'ff002113000135'),
#                  ('Color Mode Iron', 'ff002113000236'),
#                  ('Color Mode Jet', 'ff002113000337'),
#                  ]

# Command from CSV File
command_array = Mf.get_data_from_csv(cmd_path)

# Script Variable
script_toggle_flag = None
# script_hex_arrays = []
# script_cmd_titles = []
# interval_arrays = []
# cmd_itv_arrays = []

# ScreenShot Hex Value
capture_hex = [255, 1, 0, 0, 0, 0, 0]

# For Test Arrays (Zoom Out -> All Stop -> AF -> Zoom In -> All Stop -> AF)
script_hex_arrays = [[255, 1, 0, 64, 0, 0, 65], [255, 1, 0, 0, 0, 0, 1], [255, 1, 160, 17, 0, 0, 178],
                     [255, 1, 0, 0, 0, 0, 0],
                     [255, 1, 0, 32, 0, 0, 33], [255, 1, 0, 0, 0, 0, 1], [255, 1, 160, 17, 0, 0, 178],
                     [255, 1, 0, 0, 0, 0, 0],
                     [255, 1, 0, 128, 0, 0, 129], [255, 1, 0, 0, 0, 0, 1], [255, 1, 160, 17, 0, 0, 178],
                     [255, 1, 0, 0, 0, 0, 0],
                     [255, 1, 1, 0, 0, 0, 2], [255, 1, 0, 0, 0, 0, 1], [255, 1, 160, 17, 0, 0, 178],
                     [255, 1, 0, 0, 0, 0, 0]
                     ]
script_cmd_titles = ['Zoom Out', 'All Stop', 'AF', 'ScreenShot',
                     'Zoom In', 'All Stop', 'AF', 'ScreenShot',
                     'Far', 'All Stop', 'AF', 'ScreenShot',
                     'Near', 'All Stop', 'AF', 'ScreenShot'
                     ]
interval_arrays = [2.5, 0.3, 3.0, 1.0,
                   2.5, 0.3, 3.0, 1.0,
                   2.5, 0.3, 3.0, 1.0,
                   2.5, 0.3, 3.0, 1.0
                   ]
cmd_itv_arrays = [['Zoom Out', 2.5], ['All Stop', 0.3], ['AF', 3.0], ['ScreenShot', 1.0],
                  ['Zoom In', 2.5], ['All Stop', 0.3], ['AF', 3.0], ['ScreenShot', 1.0],
                  ['Far', 2.5], ['All Stop', 0.3], ['AF', 3.0], ['ScreenShot', 1.0],
                  ['Near', 2.5], ['All Stop', 0.3], ['AF', 3.0], ['ScreenShot', 1.0]
                  ]

# Network Information form User Input
data_sending = True
host_ip: str = ""
port: int = 0  # Default 32000
rtsp_port: int = 0
buf_size = 4096
response_txt = []

# RTSP Information
rtsp_url = ''
ipc_id = ''
ipc_pw = ''

# PTZ/OSD Toggle Variable
ptz_osd_toggle_flag = False

# (2024.07.12) Query Data Store
zoom_q = {'zoom': '', 'magnification': ''}
focus_q = {'focus': ''}
comm_q = {'mode': '', 'add': '', 'baud': '', 'word': '',
          'stop': '', 'parity': '', 'protocol': ''}
lens_q = {'af_trigger': '', 'zoom_spd': '', 'focus_spd': '', 'af_mode': '',
          'af_interval': '', 'fov_position': '', 'query_mode': ''}
image_q = {'dis': '', 'dnr': '', 'flip': '', 'mirror': '',
           'freeze': '', 'dzoom': '', 'dzoom_position': ''}
sensor_q = {'histogram': '', 'brightness': '', 'contrast': '', 'white_hot': '',
            'pseudo': '', 'edge': ''}
cali_q = {'trigger': '', 'mode': '', 'interval': ''}
etc_q = {'save': '', 'cvbs': '', 'display': ''}
status_q = {'boot': '', 'board_t': '', 'lens_t': '', 'sensor_t': '',
            'fan': '', 'telemetry': '', 'calibration': '', 'af': ''}
version_q = {'sensor': '', 'lens': '', 'main': '', 'main_y': '',
             'main_m_d': '', 'osd': '', 'osd_y': '', 'osd_m_d': ''}
encoder_q = {'zoom_max': '', 'zoom_min': '', 'focus_max': '', 'focus_min': ''}

# User, Model Information
left_label_size = int(WINDOWS_SIZE['x'] * 0.01875)
right_text_fd_size = int(WINDOWS_SIZE['x'] * 0.01875)

rtsp_pos = {'x': 0, 'y': 0,
            'h': camera_resolution['w'], 'w': camera_resolution['w']}

validator_lbl = {'x': info_start_pos['x'], 'y': info_start_pos['y'],
                 'h': lbl_size['h'], 'w': lbl_size['w'],
                 'bg': my_color['fg'], 'text': 'Validator'}
validator_txt_fld = {'x': validator_lbl['x'] + validator_lbl['w'], 'y': validator_lbl['y'],
                     'h': validator_lbl['h'], 'w': validator_lbl['w'] * 1.5, 'bg': my_color['spare_fir']}

model_lbl = {'x': validator_lbl['x'], 'y': validator_lbl['y'] + validator_lbl['h'],
             'h': validator_lbl['h'], 'w': validator_lbl['w'],
             'bg': my_color['fg'], 'text': 'Model'}
model_txt_fld = {'x': model_lbl['x'] + model_lbl['w'], 'y': model_lbl['y'],
                 'h': model_lbl['h'], 'w': model_lbl['w'] * 1.5, 'bg': my_color['spare_fir']}

fw_lbl = {'x': model_lbl['x'], 'y': model_lbl['y'] + model_lbl['h'],
          'h': model_lbl['h'], 'w': model_lbl['w'],
          'bg': my_color['fg'], 'text': 'FW Info'}
fw_txt_fld = {'x': fw_lbl['x'] + fw_lbl['w'], 'y': fw_lbl['y'],
              'h': fw_lbl['h'], 'w': fw_lbl['w'] * 1.5, 'bg': my_color['spare_fir']}

# Network Information
ip_lbl_info = {'x': validator_txt_fld['x'] + validator_txt_fld['w'], 'y': validator_txt_fld['y'],
               'h': lbl_size['h'], 'w': lbl_size['w'],
               'bg': my_color['fg'], 'text': 'IP Address'}
ip_txt_fld_info = {'x': ip_lbl_info['x'] + ip_lbl_info['w'], 'y': ip_lbl_info['y'],
                   'h': lbl_size['h'], 'w': lbl_size['w'] * 1.5, 'bg': my_color['spare_fir']}

port_lbl_info = {'x': ip_lbl_info['x'], 'y': ip_lbl_info['y'] + ip_lbl_info['h'],
                 'h': lbl_size['h'], 'w': lbl_size['w'],
                 'bg': my_color['fg'], 'text': 'Port No'}
port_txt_fld_info = {'x': ip_txt_fld_info['x'], 'y': ip_txt_fld_info['y'] + ip_txt_fld_info['h'],
                     'h': lbl_size['h'], 'w': lbl_size['w'] * 1.5, 'bg': my_color['spare_fir']}

rtsp_lbl_info = {'x': port_lbl_info['x'], 'y': port_lbl_info['y'] + port_lbl_info['h'],
                 'h': lbl_size['h'], 'w': lbl_size['w'],
                 'bg': my_color['fg'], 'text': 'RTSP Port'}
rtsp_txt_fld_info = {'x': port_txt_fld_info['x'], 'y': port_txt_fld_info['y'] + port_txt_fld_info['h'],
                     'h': lbl_size['h'], 'w': lbl_size['w'] * 1.5, 'bg': my_color['spare_fir']}

# Camera ID, PW Information
ipc_id_info = {'x': fw_lbl['x'], 'y': fw_lbl['y'] + fw_lbl['h'] + 10,
               'h': lbl_size['h'], 'w': lbl_size['w'], 'bg': my_color['fg'], 'text': 'Camera ID'}
ipc_id_txt_fld_info = {'x': ipc_id_info['x'] + ipc_id_info['w'], 'y': ipc_id_info['y'],
                       'h': lbl_size['h'], 'w': lbl_size['w'], 'bg': my_color['spare_fir']}

ipc_pw_info = {'x': ipc_id_txt_fld_info['x'] + ipc_id_txt_fld_info['w'] + 2,
               'y': rtsp_lbl_info['y'] + rtsp_txt_fld_info['h'] + 10,
               'h': lbl_size['h'], 'w': lbl_size['w'], 'bg': my_color['fg'], 'text': 'Camera PW'}
ipc_pw_txt_fld_info = {'x': ipc_pw_info['x'] + ipc_pw_info['w'], 'y': ipc_pw_info['y'],
                       'h': lbl_size['h'], 'w': lbl_size['w'], 'bg': my_color['spare_fir']}

register_btn = {'x': ipc_pw_txt_fld_info['x'] + ipc_pw_txt_fld_info['w'] + 5, 'y': ipc_id_info['y'] - 2,
                'h': lbl_size['h'] + 2, 'w': lbl_size['w'] - 7,
                'bg': my_color['bg'], 'text': 'Register'}

# Searching UI element position and size
search_txt_fld_info = {'x': info_start_pos['x'], 'y': register_btn['y'] + register_btn['h'] + 10,
                       'h': lbl_size['h'], 'w': lbl_size['w'] * 4,
                       'bg': my_color['spare_fir']}

search_btn = {'x': register_btn['x'], 'y': search_txt_fld_info['y'] - 2,
              'h': lbl_size['h'] + 2, 'w': lbl_size['w'] - 7,
              'bg': my_color['bg'], 'fg': my_color['fg'], 'text': 'Search'}

# Treeview Position and Size
treeview_pos = {'x': camera_resolution['w'] + 30, 'y': search_btn['y'] + search_btn['h'] + 10}
tree_view_size = {'w': int((WINDOWS_SIZE['x'] - 1280) / 2.7), 'h': WINDOWS_SIZE['y'] - (lbl_size['h'] * 17) + 7}

# Script Table
script_tb_pos = {'x': camera_resolution['w'] * 67 / 100, 'y': treeview_pos['y'] + tree_view_size['h'],
                 'w': int(camera_resolution['w'] / 3), 'h': WINDOWS_SIZE['y'] - (lbl_size['h'] * 17),
                 'c': int(camera_resolution['w'] / 8)}
script_column = ['Function', 'Interval']

# Log Field Position and Size
log_txt_fld_info = {'x': 0, 'y': script_tb_pos['y'],
                    'h': lbl_size['h'] * 8 + 9, 'w': lbl_size['w'] * 6,
                    'bg': my_color['spare_fir'], 'fg': my_color['bg']}

# (2024.07.10) PTZ/OSD Mode Toggle
ptz_osd_mode_lbl = {'x': info_start_pos['x'], 'y': treeview_pos['y'] + tree_view_size['h'],
                    'h': lbl_size['h'] * 2, 'w': lbl_size['w'] / 2,
                    'bg': my_color['fg'], 'text': 'PTZ\nMode'}
ptz_osd_mode_btn = {'x': ptz_osd_mode_lbl['x'], 'y': ptz_osd_mode_lbl['y'] + ptz_osd_mode_lbl['h'],
                    'h': lbl_size['h'], 'w': lbl_size['w'],
                    'bg': my_color['bg'], 'fg': my_color['fg'], 'text': 'Script Mode'}

# PTZ UI
ptz_canvas = {'x': info_start_pos['x'], 'y': treeview_pos['y'] + tree_view_size['h'],
              'w': 160, 'h': 160}
ptz_up_btn = {'x': ptz_canvas['w'] / 2 + 2, 'y': ptz_canvas['h'] / 3 / 2 + 5,
              'h': 40, 'w': 50,
              'bg': my_color['bg'], 'fg': my_color['fg'], 'text': 'UP'}
ptz_down_btn = {'x': ptz_up_btn['x'], 'y': ptz_canvas['h'] / 3 / 2 + 100 + 5,
                'h': 40, 'w': 50,
                'bg': my_color['bg'], 'fg': my_color['fg'], 'text': 'DOWN'}
ptz_left_btn = {'x': ptz_canvas['w'] / 3 / 2, 'y': ptz_canvas['w'] / 3 + 29,
                'h': 50, 'w': 50,
                'bg': my_color['bg'], 'fg': my_color['fg'], 'text': 'LEFT'}
ptz_right = {'x': ptz_canvas['w'] / 3 / 2 + 100 + 7, 'y': ptz_left_btn['y'],
             'h': 50, 'w': 50,
             'bg': my_color['bg'], 'fg': my_color['fg'], 'text': 'RIGHT'}
ptz_center = {'x': 53, 'y': 70,
              'h': 50, 'w': 50,
              'bg': my_color['bg'], 'fg': my_color['fg'], 'text': 'AF'}

# Script(Repeat, interval) Position Setting
interval_lbl = {'x': search_btn['x'] - 150, 'y': treeview_pos['y'] + tree_view_size['h'] + 10,
                'h': lbl_size['h'], 'w': lbl_size['w'],
                'bg': my_color['fg'], 'fg': my_color['fg'], 'text': 'Interval(msec)'}
interval_txt_fld = {'x': interval_lbl['x'] + interval_lbl['w'] + 10, 'y': interval_lbl['y'],
                    'h': lbl_size['h'], 'w': lbl_size['w'],
                    'bg': my_color['spare_fir'], 'fg': my_color['fg']}
interval_add_btn = {'x': interval_txt_fld['x'] + interval_txt_fld['w'] + 5, 'y': interval_txt_fld['y'],
                    'h': lbl_size['h'], 'w': lbl_size['w'] / 2,
                    'bg': my_color['bg'], 'fg': my_color['fg'], 'text': 'Add'}
interval_button = None

repeat_lbl = {'x': interval_lbl['x'], 'y': interval_lbl['y'] + interval_lbl['h'] + 5,
              'h': lbl_size['h'], 'w': lbl_size['w'],
              'bg': my_color['fg'], 'fg': my_color['fg'], 'text': 'Repeat'}
repeat_txt_fld = {'x': repeat_lbl['x'] + repeat_lbl['w'] + 10, 'y': repeat_lbl['y'],
                  'h': lbl_size['h'], 'w': lbl_size['w'],
                  'bg': my_color['spare_fir'], 'fg': my_color['fg']}

script_mode_lbl = {'x': repeat_lbl['x'], 'y': repeat_lbl['y'] + repeat_lbl['h'] + 5,
                   'h': lbl_size['h'], 'w': lbl_size['w'],
                   'bg': my_color['fg'], 'fg': my_color['fg'], 'text': 'Script Mode'}
script_mode_btn = {'x': script_mode_lbl['x'] + script_mode_lbl['w'] + 5, 'y': script_mode_lbl['y'],
                   'h': lbl_size['h'], 'w': lbl_size['w'],
                   'bg': my_color['bg'], 'fg': my_color['fg'], 'text': 'Script Mode'}

script_run_btn = {'x': script_mode_lbl['x'] + 30, 'y': script_mode_lbl['y'] + script_mode_lbl['h'] + 5,
                  'h': lbl_size['h'], 'w': lbl_size['w'],
                  'bg': my_color['bg'], 'fg': my_color['fg'], 'text': 'Script Run'}
script_stop_btn = {'x': script_run_btn['x'], 'y': script_run_btn['y'] + script_run_btn['h'] + 5,
                   'h': lbl_size['h'], 'w': lbl_size['w'],
                   'bg': my_color['bg'], 'fg': my_color['fg'], 'text': 'Script Stop'}
script_clear_btn = {'x': script_stop_btn['x'], 'y': script_stop_btn['y'] + script_stop_btn['h'] + 5,
                    'h': lbl_size['h'], 'w': lbl_size['w'],
                    'bg': my_color['bg'], 'fg': my_color['fg'], 'text': 'Script Clear'}

capture_pos = {'x': rtsp_pos['x'], 'y': rtsp_pos['y'],
               'h': rtsp_pos['h'], 'w': rtsp_pos['w']}
capture_path = {'zoom': rf'Capture/Zoom', 'focus': rf'Capture/Focus'}
