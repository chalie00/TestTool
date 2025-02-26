import array
from tkinter import *

import MainFunction as Mf

# Set the Application Size, Position with System Resolution
SYS_RESOLUTION = {'x': 1920, 'y': 1080}
WINDOWS_SIZE = {'x': 1850, 'y': 950}
WINDOWS_POSITION = {"x": int((SYS_RESOLUTION['x'] - WINDOWS_SIZE['x']) / 2),
                    "y": int((SYS_RESOLUTION['y'] - WINDOWS_SIZE['y']) / 2) - 30}

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

cam1_resolution = {'w': 1280, 'h': 720}

# information Label and Text Field Size, Position
info_start_pos = {'x': cam1_resolution['w'] + 30, 'y': 10}
lbl_size = {'h': WINDOWS_SIZE['y'] / 50, 'w': WINDOWS_SIZE['x'] / 20}

# (2024.07.19): Model Flag (Uncooled, NTX Series)
selected_model = 'Uncooled'
model_option = ['Uncooled', 'DRS', 'FineTree', 'NYX Series', 'MiniGimbal']

only_socket = None

# Command File Path
cmd_path = rf'Command/Command.xlsx'

# Log File Path
log_path = rf'Log/'

# Table Data
column_array = ['Function', 'Command']
column_array_fine_tree = ['Function', 'Parameter']
# 0xff, 0x00, 0x21, 0x13, 0x00, 0x01, 0x35
# command_array = [('Color Mode Gray', 'ff002113000034'),
#                  ('Color Mode Rainbow', 'ff002113000135'),
#                  ('Color Mode Iron', 'ff002113000236'),
#                  ('Color Mode Jet', 'ff002113000337'),
#                  ]

# Command from CSV File
command_array = Mf.get_data_from_csv(cmd_path)
# 0: parameter, 1: value, 2: BaseUrl
fine_tree_cmd_data = []
finetree_parms_arrays = []

# Script Variable
script_toggle_flag = None

# script_hex_nyx_cmd_arrays = []
# script_cmd_titles = []
# interval_arrays = []
# cmd_itv_arrays = []

# script_itv_arrs = []
# script_cmd_arrs = []
# script_cmd_titles = []
# script_cmd_itv_arrs = []

# ScreenShot Hex Value
capture_hex = [255, 1, 0, 0, 0, 0, 0]
uncooled_query_arrays = [
    'Zoom Query', 'Focus Query', 'Lens Query', 'Comm Query',
    'Image Query', 'Sensor Query', 'Cali. Query', 'ETC Query',
    'Status Query', 'Version Query', 'Encoder Query'
]
# MiniGimbal
# script_itv_arrs = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5,
#                    0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5,
#                    0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5,
#                    0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5,
#                    0.5, 0.5]
# script_cmd_arrs = [
#     [255, 0, 177, 0, 0, 1, 178], [255, 0, 192, 0, 0, 1, 193], [255, 0, 177, 0, 0, 0, 177], [255, 0, 192, 0, 0, 2, 194],
#     [255, 0, 178, 0, 0, 1, 179],
#     [255, 0, 192, 0, 0, 3, 195], [255, 0, 178, 0, 0, 0, 178], [255, 0, 192, 0, 0, 4, 196], [255, 0, 179, 0, 0, 1, 180],
#     [255, 0, 192, 0, 0, 5, 197],
#     [255, 0, 179, 0, 0, 0, 179], [255, 0, 192, 0, 0, 6, 198], [255, 0, 180, 0, 0, 0, 180], [255, 0, 192, 0, 0, 7, 199],
#     [255, 0, 180, 0, 0, 1, 181],
#     [255, 0, 192, 0, 0, 8, 200], [255, 0, 180, 0, 0, 2, 182], [255, 0, 193, 0, 0, 0, 193], [255, 0, 181, 0, 0, 0, 181],
#     [255, 0, 193, 0, 0, 1, 194],
#     [255, 0, 181, 0, 0, 5, 186], [255, 0, 193, 0, 0, 2, 195], [255, 0, 181, 0, 0, 10, 191], [255, 0, 193, 0, 0, 3, 196],
#     [255, 0, 183, 0, 0, 0, 183],
#     [255, 0, 193, 0, 0, 4, 197], [255, 0, 183, 0, 0, 5, 188], [255, 0, 193, 0, 0, 5, 198], [255, 0, 183, 0, 0, 10, 193],
#     [255, 0, 193, 0, 0, 6, 199],
#     [255, 0, 184, 0, 0, 1, 185], [255, 0, 193, 0, 0, 7, 200], [255, 0, 184, 0, 0, 0, 184], [255, 0, 193, 0, 0, 8, 201],
#     [255, 0, 193, 0, 0, 9, 202],
#     [255, 0, 176, 0, 0, 1, 177], [255, 0, 194, 0, 0, 0, 194], [255, 0, 176, 0, 0, 0, 176], [255, 0, 194, 0, 0, 1, 195],
#     [255, 0, 195, 0, 0, 1, 196],
#     [255, 0, 195, 0, 0, 0, 195], [255, 0, 196, 0, 0, 0, 196]
# ]
#
# script_cmd_titles = [
#     'WDR On', 'IR D-Zoom x1', 'WDR Off', 'IR D-Zoom x2', 'BLC On',
#     'IR D-Zoom x3', 'BLC Off', 'IR D-Zoom x4', 'DIS On', 'IR D-Zoom x5',
#     'DIS Off', 'IR D-Zoom x6', 'DN Day', 'IR D-Zoom x7', 'DN Night',
#     'IR D-Zoom x8', 'DN Auto', 'White', 'Brighteness 0', 'Black',
#     'Brighteness 5', 'Rainbow', 'Brighteness 10', 'Rainbow HC', 'Sharpness 0',
#     'Iron', 'Sharpness 5', 'Lava', 'Sharpness 10', 'Sky',
#     'Defog On', 'Medium Gray', 'Defog Off', 'Gray-Red', 'Purple Orange',
#     'EO D-Zoom On', 'AGC Auto 1', 'EO D-Zoom Off', 'AGC Auto 2', 'DDE On',
#     'DDE Off', 'Calibration Exe'
# ]
#
# script_cmd_itv_arrs = [
#     ['WDR On', 0.5], ['IR D-Zoom x1', 0.5], ['WDR Off', 0.5], ['IR D-Zoom x2', 0.5], ['BLC On', 0.5],
#     ['IR D-Zoom x3', 0.5], ['BLC Off', 0.5], ['IR D-Zoom x4', 0.5], ['DIS On', 0.5], ['IR D-Zoom x5', 0.5],
#     ['DIS Off', 0.5], ['IR D-Zoom x6', 0.5], ['DN Day', 0.5], ['IR D-Zoom x7', 0.5], ['DN Night', 0.5],
#     ['IR D-Zoom x8', 0.5], ['DN Auto', 0.5], ['White', 0.5], ['Brighteness 0', 0.5], ['Black', 0.5],
#     ['Brighteness 5', 0.5], ['Rainbow', 0.5], ['Brighteness 10', 0.5], ['Rainbow HC', 0.5], ['Sharpness 0', 0.5],
#     ['Iron', 0.5], ['Sharpness 5', 0.5], ['Lava', 0.5], ['Sharpness 10', 0.5], ['Sky', 0.5],
#     ['Defog On', 0.5], ['Medium Gray', 0.5], ['Defog Off', 0.5], ['Gray-Red', 0.5], ['Purple Orange', 0.5],
#     ['EO D-Zoom On', 0.5], ['AGC Auto 1', 0.5], ['EO D-Zoom Off', 0.5], ['AGC Auto 2', 0.5], ['DDE On', 0.5],
#     ['DDE Off', 0.5], ['Calibration Exe', 0.5]]
# Mini Gimbal PTZ
# interval_constant = 0.3
# script_itv_arrs = [interval_constant, interval_constant, interval_constant, interval_constant,
#                    interval_constant, interval_constant, interval_constant, interval_constant,
#                    interval_constant, interval_constant, interval_constant, interval_constant]
# script_cmd_arrs = [
#     [255, 0, 0, 8, 0, 255, 7], [255, 0, 0, 0, 0, 0, 0],  [255, 0, 0, 16, 0, 255, 15], [255, 0, 0, 0, 0, 0, 0],
#     [255, 0, 0, 4, 255, 0, 3], [255, 0, 0, 0, 0, 0, 0],  [255, 0, 0, 2, 255, 0, 1], [255, 0, 0, 0, 0, 0, 0],
#     [255, 0, 186, 0, 0, 16, 202], [255, 0, 186, 0, 0, 0, 186], [255, 0, 186, 0, 0, 32, 218], [255, 0, 186, 0, 0, 0, 186],
# ]
#
# script_cmd_titles = [
#     'Up', 'Stop', 'Down', 'Stop', 'Left', 'Stop', 'Right', 'Stop',
#     'Zoom In', 'Stop', 'Zoom Out', 'Stop'
# ]
#
# script_cmd_itv_arrs = [
#     ['Up', interval_constant], ['Stop', interval_constant], ['Down', interval_constant], ['Stop', interval_constant], ['Left', interval_constant], ['Stop', interval_constant],
#     ['Right', interval_constant], ['Stop', interval_constant], ['Zoom In', interval_constant], ['Stop', interval_constant], ['Zoom Out', interval_constant], ['Stop', interval_constant],
# ]


# DRS Default Code
# script_hex_nyx_cmd_arrays = [[255, 0, 32, 34, 0, 0, 66], [255, 0, 32, 35, 0, 0, 67],
#                              [255, 0, 32, 36, 0, 0, 68], [255, 0, 32, 49, 0, 1, 82],
#                              [255, 0, 33, 16, 0, 10, 59], [255, 0, 33, 19, 0, 0, 52],
#                              [255, 0, 35, 0, 0, 0, 35], [255, 0, 35, 1, 0, 0, 36],
#                              [255, 0, 35, 2, 0, 98, 135], [255, 0, 33, 0, 0, 3, 36]]
# script_cmd_titles = [' Mirror Off', ' Flip Off', 'Invert Off', 'Cali Auto',
#                      'IDE 10', 'Gray', 'Temp Info Off', 'Temp User Offset 0',
#                      'Emissivity 98', 'AGC High']
# interval_arrays = [3.0, 3.0, 3.0, 3.0,
#                    3.0, 3.0, 3.0, 3.0,
#                    3.0, 3.0]
# cmd_itv_arrays = [[' Mirror Off', 3.0], [' Flip Off', 3.0], [' Invert Off', 3.0], ['Cali Auto', 3.0],
#                   ['IDE 10', 3.0], ['Gray', 3.0], ['Temp Info Off', 3.0], ['Temp User Offset 0', 3.0],
#                   ['Emissivity 98', 3.0], ['AGC High', 3.0]]
# script_hex_nyx_cmd_arrays = [
#     [255, 0, 34, 16, 0, 1, 51], [255, 0, 34, 19, 0, 0, 53], [255, 0, 34, 32, 0, 0, 66], [255, 1, 0, 0, 0, 0, 0],
#     [255, 0, 34, 16, 0, 2, 52], [255, 0, 34, 19, 0, 0, 53], [255, 0, 34, 32, 0, 0, 66],[255, 1, 0, 0, 0, 0, 0]
# ]
# script_cmd_titles = ['Far', 'Focus Stop', 'AF', 'ScreenShot',
#                      'Near', 'Focus Stop', 'AF', 'ScreenShot']
#
# interval_arrays = [5.0, 5.0, 5.0, 5.0,
#                    5.0, 5.0, 5.0, 5.0,
#                    ]
# cmd_itv_arrays = [
#     ['Far', 5.0], ['Focus Stop', 5.0], ['AF', 5.0], ['ScreenShot', 5.0],
#     ['Near', 5.0], ['Focus Stop', 5.0], ['AF', 5.0], ['ScreenShot', 5.0]
# ]

# Uncooled Type Zoom In/Out AF Test Code
# For Test Arrays (Zoom Out -> All Stop -> AF -> Zoom In -> All Stop -> AF)
script_cmd_arrs = [
    [255, 1, 0, 64, 0, 0, 65], [255, 1, 0, 0, 0, 0, 1], [255, 1, 160, 17, 0, 0, 178],
    [255, 1, 0, 0, 0, 0, 0],
    [255, 1, 0, 128, 0, 0, 129], [255, 1, 0, 0, 0, 0, 1], [255, 1, 160, 17, 0, 0, 178],
    [255, 1, 0, 0, 0, 0, 0],
    [255, 1, 1, 0, 0, 0, 2], [255, 1, 0, 0, 0, 0, 1], [255, 1, 160, 17, 0, 0, 178],
    [255, 1, 0, 0, 0, 0, 0],
    [255, 1, 0, 32, 0, 0, 33], [255, 1, 0, 0, 0, 0, 1], [255, 1, 160, 17, 0, 0, 178],
    [255, 1, 0, 0, 0, 0, 0],
    [255, 1, 0, 128, 0, 0, 129], [255, 1, 0, 0, 0, 0, 1], [255, 1, 160, 17, 0, 0, 178],
    [255, 1, 0, 0, 0, 0, 0],
    [255, 1, 1, 0, 0, 0, 2], [255, 1, 0, 0, 0, 0, 1], [255, 1, 160, 17, 0, 0, 178],
    [255, 1, 0, 0, 0, 0, 0]
]
script_cmd_titles = [
    'Zoom Out', 'All Stop', 'AF', 'ScreenShot',
    'Far', 'All Stop', 'AF', 'ScreenShot',
    'Near', 'All Stop', 'AF', 'ScreenShot',
    'Zoom In', 'All Stop', 'AF', 'ScreenShot',
    'Far', 'All Stop', 'AF', 'ScreenShot',
    'Near', 'All Stop', 'AF', 'ScreenShot'
]
script_itv_arrs = [
    2.0, 0.3, 12.0, 1.0,
    2.0, 0.3, 12.0, 1.0,
    2.0, 0.3, 12.0, 1.0,
    2.0, 0.3, 12.0, 1.0,
    2.0, 0.3, 12.0, 1.0,
    2.0, 0.3, 12.0, 1.0
]
script_cmd_itv_arrs = [
    ['Zoom Out', 2.0], ['All Stop', 0.3], ['AF', 12.0], ['ScreenShot', 1.0],
    ['Far', 2.0], ['All Stop', 0.3], ['AF', 12.0], ['ScreenShot', 1.0],
    ['Near', 2.0], ['All Stop', 0.3], ['AF', 12.0], ['ScreenShot', 1.0],
    ['Zoom In', 2.0], ['All Stop', 0.3], ['AF', 12.0], ['ScreenShot', 1.0],
    ['Far', 2.0], ['All Stop', 0.3], ['AF', 12.0], ['ScreenShot', 1.0],
    ['Near', 2.0], ['All Stop', 0.3], ['AF', 12.0], ['ScreenShot', 1.0]
]

# NYX Series Zoom In/Out AF Test Code
# For Test Arrays (Zoom Out -> All Stop -> AF -> Zoom In -> All Stop -> AF)
# script_hex_nyx_cmd_arrays = [
#     'NYX.SET#lens_zctl=narrow', 'NYX.SET#lens_zctl=stop', 'NYX.SET#lens_afex=execute',
#     'NYX.SET#lens_zctl=wide', 'NYX.SET#lens_zctl=stop', 'NYX.SET#lens_afex=execute',
#     'NYX.SET#lens_fctl=near', 'NYX.SET#lens_fctl=stop', 'NYX.SET#lens_afex=execute',
#     'NYX.SET#lens_fctl=far', 'NYX.SET#lens_fctl=stop', 'NYX.SET#lens_afex=execute'
# ]
# script_cmd_titles = ['zoom narrow', 'zoom stop', 'af execute',
#                      'zoom wide', 'zoom stop', 'af execute',
#                      'focus near', 'focus stop', 'af execute',
#                      'focus far', 'focus stop', 'af execute'
#                      ]
# interval_arrays = [2.0, 1.0, 4.0,
#                    2.5, 1.0, 4.0,
#                    2.0, 1.0, 4.0,
#                    2.0, 1.0, 4.0,
#                    ]
# cmd_itv_arrays = [
#     ['zoom narrow', 2.0], ['zoom stop', 1.0], ['af execute', 4.0],
#     ['zoom wide', 2.0], ['zoom stop', 1.0], ['af execute', 4.0],
#     ['focus near', 2.0], ['focus stop', 1.0], ['af execute', 4.0],
#     ['focus far', 2.0], ['focus stop', 1.0], ['af execute', 4.0],
# ]

# Network Information form User Input
data_sending = True
host_ip: str = ""
port: int = 0  # Default 32000
rtsp_port: int = 0
buf_size = 4096

###################################################### DRS Response ###################################################
response_txt = []
drs_response = {
    'mirror': '', 'flip': '', 'invert': '', 'dzoom': '', 'color': '',
    'gamma': '', 'agc_mode': '',
    'roi_x_start_x_pos': '',
    'roi_x_start_y_pos': '',
    'ide': '', 'agc_frame': '',
    'cal_mode': '', 'cal_interval_time': '',
    'contrast': '',
    'brightness': '',
    'fw': '',
    'serial': '',
    'shutter_temp': '',
    'roi_x_threshold_temp': '',
    'center_temp': '',
    'temp_info': '', 'colorbar': '', 'center_mark': '', 'min_max': '',
    'zoom_pos': '',
    'focus_pos': '',
    'focal_len': '', 'TBD': '', 'zoom_move_flag': '', 'af_flag': '',
    'frame_rate': '', 'tx_mode': '',
    'frame_min_temp': '',
    'frame_max_temp': '',
    'frame_average_temp': '',
    # Data 22 ~ 41
    'roi0_min': '', 'roi0_max': '', 'roi1_min': '', 'roi1_max': '', 'roi2_min': '', 'roi2_max': '',
    'roi3_min': '', 'roi3_max': '', 'roi4_min': '', 'roi4_max': '', 'roi5_min': '', 'roi5_max': '',
    'roi6_min': '', 'roi6_max': '', 'roi7_min': '', 'roi7_max': '', 'roi8_min': '', 'roi8_max': '',
    'roi9_min': '', 'roi9_max': '',
    'colorbar_min': '',
    'colorbar_max': '',
    'emissivity': '',
    'user_temp_offset': '',
    'roi0': '', 'roi1': '', 'roi2': '', 'roi3': '', 'roi4': '', 'roi5': '', 'roi6': '', 'roi7': '',
    'roi8': '', 'roi9': '', 'min_max_en': '', 'mask0': '', 'mask1': '', 'mask2': '',
    'arm0': '', 'arm1': '', 'arm2': '', 'arm3': '', 'arm4': '', 'arm5': '',
    'arm6': '', 'arm7': '', 'arm8': '', 'arm9': '',
    'roi_x_end_pos': '',
    'check_data': ''
}

###################################################### Mini Gimbal Response ###################################################
miniG_response = []
miniG_res_payload = {
    'roll_en_hi': '', 'roll_en_lo': '', 'pitch_en_hi': '', 'pitch_en_lo': '', 'yaw_en_h': '', 'yaw_en_l': '',
    'cam_status': '', 'fan_heater_sta': '', 'motor_bd': '', 'temp': '', 'drift_offset_h': '', 'drift_offset_l': '','stabilizer_mode': '',
    '17': '', 'eo_dzoom': '', 'eo_wdr': '', 'eo_blc': '', 'eo_dis': '', 'eo_dn': '',
    '23': '', '24': '', 'eo_defog': '', 'eo_op_zoom_h': '', 'eo_op_zoom_l': '', 'eo_d_zoom': '', 'eo_bri': '', 'eo_sharp': '',
    'ir_dzoom': '', 'ir_pale': '', 'ir_agc_mode': '', 'ir_dde': '', '35': '', 'fw_h': '', 'fw_l': ''
}

miniG_res_row = [
    'roll_en_hi', 'roll_en_lo', 'pitch_en_hi', 'pitch_en_lo', 'yaw_en_h', 'yaw_en_l',
    'cam_status', 'fan_heater_sta', 'motor_bd', 'temp', 'drift_offset_h', 'drift_offset_l', 'stabilizer_mode',
    '17', 'eo_dzoom', 'eo_wdr', 'eo_blc', 'eo_dis', 'eo_dn',
    '23', '24', 'eo_defog', 'eo_op_zoom_h', 'eo_op_zoom_l', 'eo_d_zoom', 'eo_bri', 'eo_sharp',
    'ir_dzoom', 'ir_pale', 'ir_agc_mode', 'ir_dde', '35', 'fw_h', 'fw_l'
]



# RTSP Information
rtsp_url = ''
ipc_id = ''
ipc_pw = ''

video_player_ch1 = None
video_player_ch2 = None
video_player_ch3 = None
video_player_ch4 = None

# selected ch is one of below ch(ch1_rtsp_info ....)
selected_ch = None
ch1_rtsp_info = {'ch': '', 'model': '', 'ip': '', 'id': '', 'pw': '', 'rtsp_port': '', 'port': '', 'url': '',
                 'x': 0, 'y': 0,
                 'h': cam1_resolution['h'] / 2, 'w': cam1_resolution['w'] / 2
                 }
ch2_rtsp_info = {'ch': '', 'model': '', 'ip': '', 'id': '', 'pw': '', 'rtsp_port': '', 'port': '', 'url': '',
                 'x': ch1_rtsp_info['w'] + 5, 'y': 0,
                 'h': cam1_resolution['h'] / 2, 'w': cam1_resolution['w'] / 2
                 }
ch3_rtsp_info = {'ch': '', 'model': '', 'ip': '', 'id': '', 'pw': '', 'rtsp_port': '', 'port': '', 'url': '',
                 'x': 0, 'y': ch1_rtsp_info['h'] + 5,
                 'h': cam1_resolution['h'] / 2, 'w': cam1_resolution['w'] / 2
                 }
ch4_rtsp_info = {'ch': '', 'model': '', 'ip': '', 'id': '', 'pw': '', 'rtsp_port': '', 'port': '', 'url': '',
                 'x': ch1_rtsp_info['w'] + 5, 'y': ch1_rtsp_info['h'] + 5,
                 'h': cam1_resolution['h'] / 2, 'w': cam1_resolution['w'] / 2
                 }

# PTZ/OSD Toggle Variable
ptz_osd_toggle_flag = False

# (2024.07.12) Uncooled Type Query Data Store
uncooled_normal_q = {'normal': ''}
uncooled_zoom_q = {'zoom': '', 'magnification': ''}
uncooled_focus_q = {'focus': ''}
uncooled_comm_q = {'mode': '', 'add': '', 'baud': '', 'word': '',
                   'stop': '', 'parity': '', 'protocol': ''}
uncooled_lens_q = {'af_trigger': '', 'zoom_spd': '', 'focus_spd': '', 'af_mode': '',
                   'af_interval': '', 'fov_position': '', 'query_mode': ''}
uncooled_image_q = {'dis': '', 'dnr': '', 'flip': '', 'mirror': '',
                    'freeze': '', 'dzoom': '', 'dzoom_position': ''}
uncooled_sensor_q = {'histogram': '', 'brightness': '', 'contrast': '', 'white_hot': '',
                     'pseudo': '', 'edge': ''}
uncooled_cali_q = {'trigger': '', 'mode': '', 'interval': ''}
uncooled_etc_q = {'save': '', 'cvbs': '', 'display': ''}
uncooled_status_q = {'boot': '', 'board_t': '', 'lens_t': '', 'sensor_t': '',
                     'fan': '', 'telemetry': '', 'calibration': '', 'af': ''}
uncooled_version_q = {'sensor': '', 'lens': '', 'main': '', 'main_y': '',
                      'main_m_d': '', 'osd': '', 'osd_y': '', 'osd_m_d': ''}
uncooled_encoder_q = {'zoom_max': '', 'zoom_min': '', 'focus_max': '', 'focus_min': ''}

# (2024.07.16) Uncooled Type Query MSB+LSB Data Store
# position, speed, mode
zoom_msb_lsb = [uncooled_zoom_q['zoom'], uncooled_lens_q['zoom_spd'], uncooled_image_q['dzoom'],
                uncooled_image_q['dzoom_position']]
focus_msb_lsb = [uncooled_focus_q['focus'], uncooled_lens_q['focus_spd'], uncooled_lens_q['af_mode']
                 ]
fov_msb_lsb = [uncooled_lens_q['fov_position']]

# (2024.07.24): NYX Series Query Data Store
# zoom_pos, focus_pos, fov, zoom_spd, focus_spd, dzoom
# lens_pos_q = ['NYX.GET#lens_zpos', 'NYX.GET#lens_fpos', 'NYX.GET#lens_cfov',
#               'NYX.GET#lens_zspd', 'NYX.GET#lens_fspd', 'NYX.GET#isp0_dzen']
cooled_lens_pos_spd = [0, 0, 0, 0, 0, 0, 0]

# User, Model Information
left_label_size = int(WINDOWS_SIZE['x'] * 0.01875)
right_text_fd_size = int(WINDOWS_SIZE['x'] * 0.01875)

# rtsp_ch1_pos = {'x': 0, 'y': 0,
#                 'h': cam1_resolution['h'] / 2, 'w': cam1_resolution['w'] / 2}
# rtsp_ch2_pos = {'x': rtsp_ch1_pos['w'] + 5, 'y': 0,
#                 'h': cam1_resolution['h'] / 2, 'w': cam1_resolution['w'] / 2}
# rtsp_ch3_pos = {'x': 0, 'y': rtsp_ch1_pos['h'] + 5,
#                 'h': cam1_resolution['h'] / 2, 'w': cam1_resolution['w'] / 2}
# rtsp_ch4_pos = {'x': rtsp_ch1_pos['w'] + 5, 'y': rtsp_ch1_pos['h'] + 5,
#                 'h': cam1_resolution['h'] / 2, 'w': cam1_resolution['w'] / 2}

ch1_btn_pos = {'x': info_start_pos['x'] + lbl_size['w'] * 2.5, 'y': info_start_pos['y'] - 20,
               'h': lbl_size['h'], 'w': lbl_size['w'] / 3,
               'bg': my_color['bg'], 'fg': my_color['fg'], 'text': 'CH1'}
ch2_btn_pos = {'x': ch1_btn_pos['x'] + 50, 'y': info_start_pos['y'] - 20,
               'h': lbl_size['h'], 'w': lbl_size['w'] / 3,
               'bg': my_color['bg'], 'fg': my_color['fg'], 'text': 'CH2'}
ch3_btn_pos = {'x': ch2_btn_pos['x'] + 50, 'y': info_start_pos['y'] - 20,
               'h': lbl_size['h'], 'w': lbl_size['w'] / 3,
               'bg': my_color['bg'], 'fg': my_color['fg'], 'text': 'CH3'}
ch4_btn_pos = {'x': ch3_btn_pos['x'] + 50, 'y': info_start_pos['y'] - 20,
               'h': lbl_size['h'], 'w': lbl_size['w'] / 3,
               'bg': my_color['bg'], 'fg': my_color['fg'], 'text': 'CH4'}

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
treeview_pos = {'x': cam1_resolution['w'] + 30, 'y': search_btn['y'] + search_btn['h'] + 10}
tree_view_size = {'w': int((WINDOWS_SIZE['x'] - 1280) / 2.7), 'h': WINDOWS_SIZE['y'] - (lbl_size['h'] * 17) + 7}

# Script Table
script_tb_pos = {'x': cam1_resolution['w'] * 67 / 100, 'y': treeview_pos['y'] + tree_view_size['h'] - 20,
                 'w': int(cam1_resolution['w'] / 3), 'h': WINDOWS_SIZE['y'] - (lbl_size['h'] * 17),
                 'c': int(cam1_resolution['w'] / 8)}
script_column = ['Function', 'Interval']

# Log Field Position and Size
log_txt_fld_info = {'x': 0, 'y': WINDOWS_SIZE['y'] - lbl_size['h'] * 8 - 50,
                    'h': lbl_size['h'] * 8 + 9, 'w': lbl_size['w'] * 6,
                    'bg': my_color['spare_fir'], 'fg': my_color['bg']}

# (2024.07.15): System Information Position and Size
sys_info_tab = {'x': log_txt_fld_info['x'] + log_txt_fld_info['w'] + 5, 'y': log_txt_fld_info['y'] + 8,
                'h': lbl_size['h'] * 8 + 9, 'w': lbl_size['w'] * 3 + 15,
                'bg': 'lightgray', 'fg': my_color['bg']}
# (2024.07.17) System Information Update Button
sys_info_update_btn = {'x': sys_info_tab['x'] + sys_info_tab['w'] - 50, 'y': sys_info_tab['y'] + sys_info_tab['h'] - 50,
                       'h': lbl_size['h'] + 2, 'w': lbl_size['w'] - 7,
                       'bg': my_color['bg'], 'fg': my_color['fg'], 'text': 'Search'}

# (2024.07.10) PTZ/OSD Mode Toggle
ptz_osd_mode_lbl = {'x': info_start_pos['x'], 'y': treeview_pos['y'] + tree_view_size['h'],
                    'h': lbl_size['h'] * 2, 'w': lbl_size['w'] / 2,
                    'bg': my_color['fg'], 'text': 'PTZ\nMode'}
ptz_osd_mode_btn = {'x': ptz_osd_mode_lbl['x'], 'y': ptz_osd_mode_lbl['y'] + ptz_osd_mode_lbl['h'],
                    'h': lbl_size['h'], 'w': lbl_size['w'],
                    'bg': my_color['bg'], 'fg': my_color['fg'], 'text': 'Script Mode'}

############################################## PTZ UI ############################################
ptz_canvas = {'x': info_start_pos['x'], 'y': treeview_pos['y'] + tree_view_size['h'] - 15,
              'w': 160, 'h': 220}

# Size and Text is applied by create_button function of Ptz.py
ptz_btn_size = 45
ptz_up_btn = {'x': ptz_canvas['w'] / 2 + 2, 'y': ptz_canvas['h'] / 3 / 2 + 15,
              'h': ptz_btn_size, 'w': ptz_btn_size,
              'bg': my_color['bg'], 'fg': my_color['fg'], 'text': 'UP'}
ptz_up_left_btn = {'x': ptz_up_btn['x'] - ptz_btn_size, 'y': ptz_up_btn['y'],
                   'h': ptz_btn_size, 'w': ptz_btn_size,
                   'bg': my_color['bg'], 'fg': my_color['fg'], 'text': 'UPPER\nLEFT'}
ptz_up_right_btn = {'x': ptz_up_btn['x'] + ptz_btn_size, 'y': ptz_up_btn['y'],
                    'h': ptz_btn_size, 'w': ptz_btn_size,
                    'bg': my_color['bg'], 'fg': my_color['fg'], 'text': 'UPPER\nRIGHT'}

ptz_down_btn = {'x': ptz_up_btn['x'], 'y': ptz_up_btn['y'] + ptz_btn_size * 2,
                'h': ptz_btn_size, 'w': ptz_btn_size,
                'bg': my_color['bg'], 'fg': my_color['fg'], 'text': 'DOWN'}
ptz_down_left_btn = {'x': ptz_down_btn['x'] - ptz_btn_size, 'y': ptz_down_btn['y'],
                     'h': ptz_btn_size, 'w': ptz_btn_size,
                     'bg': my_color['bg'], 'fg': my_color['fg'], 'text': 'BOTTOM\nLEFT'}
ptz_down_right_btn = {'x': ptz_down_btn['x'] + ptz_btn_size, 'y': ptz_down_btn['y'],
                      'h': ptz_btn_size, 'w': ptz_btn_size,
                      'bg': my_color['bg'], 'fg': my_color['fg'], 'text': 'BOTTOM\nRIGHT'}

ptz_left_btn = {'x': ptz_up_btn['x'] - ptz_btn_size, 'y': ptz_up_btn['y'] + ptz_btn_size,
                'h': ptz_btn_size, 'w': ptz_btn_size,
                'bg': my_color['bg'], 'fg': my_color['fg'], 'text': 'LEFT'}
ptz_right_btn = {'x': ptz_up_btn['x'] + ptz_btn_size, 'y': ptz_left_btn['y'],
                 'h': ptz_btn_size, 'w': ptz_btn_size,
                 'bg': my_color['bg'], 'fg': my_color['fg'], 'text': 'RIGHT'}
ptz_center_btn = {'x': 53, 'y': 50,
                  'h': 50, 'w': 50,
                  'bg': my_color['bg'], 'fg': my_color['fg'], 'text': 'AF'}

# Size and Text is applied by refresh_ptz function of Ptz.py
set_nyx_btn = {'x': ptz_up_btn['x'] + 3, 'y': ptz_up_btn['y'] - ptz_up_btn['h'] + 5,
               'h': 3, 'w': 30,
               'bg': my_color['bg'], 'fg': my_color['fg'], 'text': 'Set'}

############################################## Preset UI ############################################
tour_lists = []

preset_canvas = {'x': ptz_canvas['x'] + ptz_canvas['w'], 'y': ptz_canvas['y'],
                 'w': 130, 'h': 220, 'bg': my_color['bg']}

preset_lbl = {'x': ptz_canvas['x'] + ptz_canvas['w'], 'y': ptz_canvas['y'] + 5,
              'w': 65, 'h': 20, 'bg': my_color['fg']}
tour_lbl = {'x': preset_lbl['x'] + preset_lbl['w'] + 1, 'y': preset_lbl['y'],
            'w': 65, 'h': 20, 'bg': my_color['fg']}

preset_txt_fld = {'x': preset_lbl['x'], 'y': preset_lbl['y'] + preset_lbl['h'] + 1,
                  'w': 65, 'h': 20, 'bg': my_color['fg']}
tour_txt_fld = {'x': preset_txt_fld['x'] + preset_txt_fld['w'] + 1, 'y': preset_txt_fld['y'],
                'w': 65, 'h': 20, 'bg': my_color['fg']}

preset_save_btn = {'x': preset_txt_fld['x'], 'y': preset_txt_fld['y'] + preset_txt_fld['h'] + 1,
                   'w': 32, 'h': 20, 'bg': my_color['bg'], 'text': 'Save'}
preset_call_btn = {'x': preset_save_btn['x'] + preset_save_btn['w'], 'y': preset_save_btn['y'],
                   'w': 32, 'h': 20, 'bg': my_color['bg'], 'text': 'Call'}

tour_save_btn = {'x': tour_txt_fld['x'], 'y': tour_txt_fld['y'] + tour_txt_fld['h'] + 1,
                 'w': 32, 'h': 20, 'bg': my_color['bg'], 'text': 'Save'}
tour_call_btn = {'x': tour_save_btn['x'] + tour_save_btn['w'], 'y': tour_save_btn['y'],
                 'w': 32, 'h': 20, 'bg': my_color['bg'], 'text': 'Call'}
tour_stop_btn = {'x': tour_call_btn['x'], 'y': tour_call_btn['y'] + tour_call_btn['h'] + 1,
                 'w': 32, 'h': 20, 'bg': my_color['bg'], 'text': 'Stop'}

############################################## Script UI ############################################
# Script(Repeat, interval) Position Setting
interval_lbl = {'x': search_btn['x'] - 80, 'y': treeview_pos['y'] + tree_view_size['h'] - 10,
                'h': lbl_size['h'], 'w': lbl_size['w'],
                'bg': my_color['fg'], 'fg': my_color['fg'], 'text': 'Interval(msec)'}
interval_txt_fld = {'x': interval_lbl['x'] + interval_lbl['w'] + 10, 'y': interval_lbl['y'],
                    'h': lbl_size['h'], 'w': lbl_size['w'] - 30,
                    'bg': my_color['spare_fir'], 'fg': my_color['fg']}
interval_add_btn = {'x': interval_txt_fld['x'] + interval_txt_fld['w'] + 5, 'y': interval_txt_fld['y'],
                    'h': lbl_size['h'], 'w': lbl_size['w'] / 3,
                    'bg': my_color['bg'], 'fg': my_color['fg'], 'text': 'Add'}
interval_button = None

repeat_lbl = {'x': interval_lbl['x'], 'y': interval_lbl['y'] + interval_lbl['h'] + 5,
              'h': lbl_size['h'], 'w': lbl_size['w'],
              'bg': my_color['fg'], 'fg': my_color['fg'], 'text': 'Repeat'}
repeat_txt_fld = {'x': repeat_lbl['x'] + repeat_lbl['w'] + 10, 'y': repeat_lbl['y'],
                  'h': lbl_size['h'], 'w': lbl_size['w'] - 30,
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

capture_pos = {'x': ch1_rtsp_info['x'], 'y': ch1_rtsp_info['y'],
               'h': ch1_rtsp_info['h'] * 2, 'w': ch1_rtsp_info['w'] * 2}
capture_path = {'zoom': rf'Capture/Zoom', 'focus': rf'Capture/Focus'}
