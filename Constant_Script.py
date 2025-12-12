# Script Variable
script_toggle_flag = None

# script_cmd_arrs = []
# script_cmd_titles = []
# script_itv_arrs = []
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
#     'IR D-Zoom x8', 'DN Auto', 'White', 'Brightness 0', 'Black',
#     'Brightness 5', 'Rainbow', 'Brightness 10', 'Rainbow HC', 'Sharpness 0',
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
#     ['IR D-Zoom x8', 0.5], ['DN Auto', 0.5], ['White', 0.5], ['Brightness 0', 0.5], ['Black', 0.5],
#     ['Brightness 5', 0.5], ['Rainbow', 0.5], ['Brightness 10', 0.5], ['Rainbow HC', 0.5], ['Sharpness 0', 0.5],
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
# script_cmd_arrs = [
#     [255, 1, 0, 64, 0, 0, 65], [255, 1, 0, 0, 0, 0, 1], [255, 1, 160, 17, 0, 0, 178],
#     [255, 1, 0, 0, 0, 0, 0],
#     [255, 1, 0, 128, 0, 0, 129], [255, 1, 0, 0, 0, 0, 1], [255, 1, 160, 17, 0, 0, 178],
#     [255, 1, 0, 0, 0, 0, 0],
#     [255, 1, 1, 0, 0, 0, 2], [255, 1, 0, 0, 0, 0, 1], [255, 1, 160, 17, 0, 0, 178],
#     [255, 1, 0, 0, 0, 0, 0],
#     [255, 1, 0, 32, 0, 0, 33], [255, 1, 0, 0, 0, 0, 1], [255, 1, 160, 17, 0, 0, 178],
#     [255, 1, 0, 0, 0, 0, 0],
#     [255, 1, 0, 128, 0, 0, 129], [255, 1, 0, 0, 0, 0, 1], [255, 1, 160, 17, 0, 0, 178],
#     [255, 1, 0, 0, 0, 0, 0],
#     [255, 1, 1, 0, 0, 0, 2], [255, 1, 0, 0, 0, 0, 1], [255, 1, 160, 17, 0, 0, 178],
#     [255, 1, 0, 0, 0, 0, 0]
# ]
#
#
# script_cmd_titles = [
#     'Zoom Out', 'All Stop', 'Out AF', 'ScreenShot',
#     'Far', 'All Stop', ' Far AF', 'ScreenShot',
#     'Near', 'All Stop', 'Near AF', 'ScreenShot',
#     'Zoom In', 'All Stop', 'In AF', 'ScreenShot',
#     'Far', 'All Stop', 'Far AF', 'ScreenShot',
#     'Near', 'All Stop', 'Near AF', 'ScreenShot'
# ]
# script_itv_arrs = [
#     2.0, 0.3, 15.0, 1.0,
#     2.0, 0.3, 15.0, 1.0,
#     2.0, 0.3, 15.0, 1.0,
#     2.0, 0.3, 15.0, 1.0,
#     2.0, 0.3, 15.0, 1.0,
#     2.0, 0.3, 15.0, 1.0
# ]
# script_cmd_itv_arrs = [
#     ['Zoom Out', 2.0], ['All Stop', 0.3], ['Out AF', 15.0], ['ScreenShot', 1.0],
#     ['Far', 2.0], ['All Stop', 0.3], ['Far AF', 15.0], ['ScreenShot', 1.0],
#     ['Near', 2.0], ['All Stop', 0.3], ['Near AF', 15.0], ['ScreenShot', 1.0],
#     ['Zoom In', 2.0], ['All Stop', 0.3], ['In AF', 15.0], ['ScreenShot', 1.0],
#     ['Far', 2.0], ['All Stop', 0.3], ['Far AF', 15.0], ['ScreenShot', 1.0],
#     ['Near', 2.0], ['All Stop', 0.3], ['Near AF', 15.0], ['ScreenShot', 1.0]
# ]

# NYX Series Zoom In/Out AF Test Code
# For Test Arrays (Zoom Out -> All Stop -> AF -> Zoom In -> All Stop -> AF)
capture_title = 'Capture NYX'
# # ============================================ Rebooting was added ========================================================= 
# script_cmd_arrs = [
#     'NYX.SET#lens_zctl=wide', 'NYX.SET#lens_zctl=stop', 'NYX.SET#lens_afex=execute', 'Capture NYX',
#     'NYX.SET#syst_exec=reboot',
#     'NYX.SET#lens_zctl=narrow', 'NYX.SET#lens_zctl=stop', 'NYX.SET#lens_afex=execute', 'Capture NYX',
#     'NYX.SET#syst_exec=reboot',
#     'NYX.SET#lens_fctl=near', 'NYX.SET#lens_fctl=stop', 'NYX.SET#lens_afex=execute', 'Capture NYX',
#     'NYX.SET#syst_exec=reboot',
#     'NYX.SET#lens_fctl=far', 'NYX.SET#lens_fctl=stop', 'NYX.SET#lens_afex=execute', 'Capture NYX',
#     'NYX.SET#syst_exec=reboot',
# ]
# script_cmd_titles = ['zoom narrow', 'zoom stop', 'af execute', 'Capture NYX', 'reboot',
#                      'zoom wide', 'zoom stop', 'af execute', 'Capture NYX', 'reboot',
#                      'focus near', 'focus stop', 'af execute', 'Capture NYX', 'reboot',
#                      'focus far', 'focus stop', 'af execute', 'Capture NYX', 'reboot'
#                      ]
# script_itv_arrs = [2.0, 1.0, 4.0, 2.0, 2.0,
#                    2.0, 1.0, 4.0, 2.0, 2.0,
#                    2.0, 1.0, 4.0, 2.0, 2.0,
#                    2.0, 1.0, 4.0, 2.0, 2.0,
#                    ]
# script_cmd_itv_arrs = [
#     ['zoom narrow', 2.0], ['zoom stop', 1.0], ['af execute', 4.0], ['Capture NYX', 2.0], ['reboot', 2.0],
#     ['zoom wide', 2.0], ['zoom stop', 1.0], ['af execute', 4.0], ['Capture NYX', 2.0], ['reboot', 2.0],
#     ['focus near', 2.0], ['focus stop', 1.0], ['af execute', 4.0], ['Capture NYX', 2.0], ['reboot', 2.0],
#     ['focus far', 2.0], ['focus stop', 1.0], ['af execute', 4.0], ['Capture NYX', 2.0], ['reboot', 2.0],
# ]
script_cmd_arrs = [
    'NYX.SET#lens_zctl=wide', 'NYX.SET#lens_zctl=stop', 'NYX.SET#lens_afex=execute', 'Capture NYX',
    'NYX.SET#lens_zctl=narrow', 'NYX.SET#lens_zctl=stop', 'NYX.SET#lens_afex=execute', 'Capture NYX',
    'NYX.SET#lens_fctl=near', 'NYX.SET#lens_fctl=stop', 'NYX.SET#lens_afex=execute', 'Capture NYX',
    'NYX.SET#lens_fctl=far', 'NYX.SET#lens_fctl=stop', 'NYX.SET#lens_afex=execute', 'Capture NYX',
]
script_cmd_titles = [
    'zoom wide', 'zoom stop', 'af execute', 'Capture NYX',
    'zoom narrow', 'zoom stop', 'af execute', 'Capture NYX',
    'focus near', 'focus stop', 'af execute', 'Capture NYX',
    'focus far', 'focus stop', 'af execute', 'Capture NYX',
]
script_itv_arrs = [2.0, 1.0, 4.0, 3.0,
                   2.0, 1.0, 4.0, 3.0,
                   2.0, 1.0, 4.0, 3.0,
                   2.0, 1.0, 4.0, 3.0,
                   ]
script_cmd_itv_arrs = [
    ['zoom wide', 2.0], ['zoom stop', 1.0], ['af execute', 4.0], ['Capture NYX', 3.0],
    ['zoom narrow', 2.0], ['zoom stop', 1.0], ['af execute', 4.0], ['Capture NYX', 3.0],
    ['focus near', 2.0], ['focus stop', 1.0], ['af execute', 4.0], ['Capture NYX', 3.0],
    ['focus far', 2.0], ['focus stop', 1.0], ['af execute', 4.0], ['Capture NYX', 3.0],
]

# =================================================== DRS Response =====================================================
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

# ======================================== Mini Gimbal Response ========================================================
miniG_response = []
miniG_res_payload = {
    'roll_en_hi': '', 'roll_en_lo': '', 'pitch_en_hi': '', 'pitch_en_lo': '', 'yaw_en_h': '', 'yaw_en_l': '',
    'cam_status': '', 'fan_heater_sta': '', 'motor_bd': '', 'temp': '', 'drift_offset_h': '', 'drift_offset_l': '',
    'stabilizer_mode': '',
    '17': '', 'eo_dzoom': '', 'eo_wdr': '', 'eo_blc': '', 'eo_dis': '', 'eo_dn': '',
    '23': '', '24': '', 'eo_defog': '', 'eo_op_zoom_h': '', 'eo_op_zoom_l': '', 'eo_d_zoom': '', 'eo_bri': '',
    'eo_sharp': '',
    'ir_dzoom': '', 'ir_pale': '', 'ir_agc_mode': '', 'ir_dde': '', '35': '', 'fw_h': '', 'fw_l': ''
}

miniG_res_row = [
    'roll_en_hi', 'roll_en_lo', 'pitch_en_hi', 'pitch_en_lo', 'yaw_en_h', 'yaw_en_l',
    'cam_status', 'fan_heater_sta', 'motor_bd', 'temp', 'drift_offset_h', 'drift_offset_l', 'stabilizer_mode',
    '17', 'eo_dzoom', 'eo_wdr', 'eo_blc', 'eo_dis', 'eo_dn',
    '23', '24', 'eo_defog', 'eo_op_zoom_h', 'eo_op_zoom_l', 'eo_d_zoom', 'eo_bri', 'eo_sharp',
    'ir_dzoom', 'ir_pale', 'ir_agc_mode', 'ir_dde', '35', 'fw_h', 'fw_l'
]
