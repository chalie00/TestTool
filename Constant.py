import MainFunction as Mf
import Constant_Script as Test_Script
import Constant_Net_OBJ as Net_Obj_Con
import Constant_Query as Qry

# =====================================================   Constant Script =====================================================
capture_title = Test_Script.capture_title
script_cmd_arrs = Test_Script.script_cmd_arrs
script_cmd_titles = Test_Script.script_cmd_titles
script_itv_arrs = Test_Script.script_itv_arrs
script_cmd_itv_arrs = Test_Script.script_cmd_itv_arrs

# =====================================================   Constant Network =====================================================
selected_model = Net_Obj_Con.selected_model
model_option = Net_Obj_Con.model_option
selected_ch = Net_Obj_Con.selected_ch
FW_NODE = Net_Obj_Con.FW_NODE
FW_BAUD = Net_Obj_Con.FW_BAUD
FW_DBITS = Net_Obj_Con.FW_DBITS
FW_SBITS = Net_Obj_Con.FW_SBITS
FW_PARITY = Net_Obj_Con.FW_PARITY
READ_MAX_BYTES = Net_Obj_Con.READ_MAX_BYTES
RECV_WAIT_SEC = Net_Obj_Con.RECV_WAIT_SEC
PRE_SEND_DELAY = Net_Obj_Con.PRE_SEND_DELAY
POST_SEND_DELAY = Net_Obj_Con.POST_SEND_DELAY
model_obj = Net_Obj_Con.model_obj
channel_buttons = Net_Obj_Con.channel_buttons
network_obj = Net_Obj_Con.network_obj
etc_obj = Net_Obj_Con.etc_obj
etc_btn_obj = Net_Obj_Con.etc_btn_obj
res_log_obj = Net_Obj_Con.res_log_obj
rtsp_url = Net_Obj_Con.rtsp_url
ipc_id = Net_Obj_Con.ipc_id
ipc_pw = Net_Obj_Con.ipc_pw
video_player_ch1 = None
video_player_ch2 = None
video_player_ch3 = None
video_player_ch4 = None
start_time = Net_Obj_Con.start_time
only_socket = Net_Obj_Con.only_socket
fine_tree_cmd_data = Net_Obj_Con.fine_tree_cmd_data
finetree_parms_arrays = Net_Obj_Con.finetree_parms_arrays
ptz_osd_toggle_flag = Net_Obj_Con.ptz_osd_toggle_flag
tour_lists = Net_Obj_Con.tour_lists
interval_button = Net_Obj_Con.interval_button

# =====================================================   Constant Query =====================================================
uncooled_normal_q = Qry.uncooled_normal_q
uncooled_zoom_q = Qry.uncooled_zoom_q
uncooled_focus_q = Qry.uncooled_focus_q
uncooled_comm_q =  Qry.uncooled_comm_q
uncooled_lens_q = Qry.uncooled_lens_q
uncooled_image_q = Qry.uncooled_image_q
uncooled_sensor_q = Qry.uncooled_sensor_q
uncooled_cali_q = Qry.uncooled_cali_q
uncooled_etc_q =Qry.uncooled_etc_q
uncooled_status_q = Qry.uncooled_status_q
uncooled_version_q = Qry.uncooled_version_q
uncooled_encoder_q = Qry.uncooled_encoder_q
zoom_msb_lsb = Qry.zoom_msb_lsb
focus_msb_lsb = Qry.focus_msb_lsb
fov_msb_lsb = Qry.fov_msb_lsb
cooled_lens_pos_spd = Qry.cooled_lens_pos_spd

# =======================================================  Table ==================================================================
# Command File Path
cmd_path = rf'Command/Command.xlsx'

# Log File Path
log_path = rf'Log/'

# Table Data
column_array = ['Function', 'Command']
column_array_fine_tree = ['Function', 'Parameter']

# Command from CSV File
command_array = Mf.get_data_from_csv(cmd_path)

# =======================================================  UI  ==================================================================
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
pt_drv_info = {'ch': '', 'model': '', 'ip': '', 'port': '', 'drv': False}  # Default Port :1470

# User, Model Information
left_label_size = int(WINDOWS_SIZE['x'] * 0.01875)
right_text_fd_size = int(WINDOWS_SIZE['x'] * 0.01875)

pt_drv_btn_pos = {'x': info_start_pos['x'] + 50, 'y': info_start_pos['y'] - 20,
                  'h': lbl_size['h'], 'w': lbl_size['w'] / 3 + 15,
                  'bg': my_color['bg'], 'fg': my_color['fg'], 'text': 'PT Drv'}

ch1_btn_pos = {'x': pt_drv_btn_pos['x'] + lbl_size['w'] + 60, 'y': info_start_pos['y'] - 20,
               'h': lbl_size['h'], 'w': lbl_size['w'] / 3,
               'bg': my_color['bg'], 'fg': my_color['fg'], 'text': 'CH1'}
ch2_btn_pos = {'x': ch1_btn_pos['x'] + 40, 'y': info_start_pos['y'] - 20,
               'h': lbl_size['h'], 'w': lbl_size['w'] / 3,
               'bg': my_color['bg'], 'fg': my_color['fg'], 'text': 'CH2'}
ch3_btn_pos = {'x': ch2_btn_pos['x'] + 40, 'y': info_start_pos['y'] - 20,
               'h': lbl_size['h'], 'w': lbl_size['w'] / 3,
               'bg': my_color['bg'], 'fg': my_color['fg'], 'text': 'CH3'}
ch4_btn_pos = {'x': ch3_btn_pos['x'] + 40, 'y': info_start_pos['y'] - 20,
               'h': lbl_size['h'], 'w': lbl_size['w'] / 3,
               'bg': my_color['bg'], 'fg': my_color['fg'], 'text': 'CH4'}

test_btn = {'x': ch4_btn_pos['x'] + 40, 'y': info_start_pos['y'] - 20,
            'h': lbl_size['h'], 'w': lbl_size['w'] / 3,
            'bg': my_color['bg'], 'fg': my_color['fg'], 'text': 'TEST'}

save_btn = {'x': test_btn['x'] + 40, 'y': info_start_pos['y'] - 20,
            'h': lbl_size['h'], 'w': lbl_size['w'] / 3,
            'bg': my_color['bg'], 'fg': my_color['fg'], 'text': 'Save'}

arrow_left_btn = {'pos1_x': save_btn['x'] + 35, 'pos1_y': info_start_pos['y'] - 20 + lbl_size['h']/2,
                  'pos2_x': save_btn['x'] + 80, 'pos2_y': info_start_pos['y'] - 20,
                  'pos3_x': save_btn['x'] + 80, 'pos3_y': info_start_pos['y'] - 20 + lbl_size['h'],
                  'bg': my_color['bg'], 'fg': my_color['fg'], 'text': ''}

arrow_right_btn = {'pos1_x': arrow_left_btn['pos2_x'] + 25, 'pos1_y': arrow_left_btn['pos2_x'] - 20 + lbl_size['h']/2,
                   'pos2_x': arrow_left_btn['pos2_x'] + 5, 'pos2_y': arrow_left_btn['pos2_x'] - 20,
                   'pos3_x': arrow_left_btn['pos2_x'] + 40, 'pos3_y': arrow_left_btn['pos2_x'] - 20 + lbl_size['h'],
                   'bg': my_color['bg'], 'fg': my_color['fg'], 'text': ''}

validator_lbl = {'x': info_start_pos['x'], 'y': info_start_pos['y'],
                 'h': lbl_size['h'], 'w': lbl_size['w'],
                 'bg': my_color['fg'], 'text': 'Validator', 'type': 'Label'}
validator_txt_fld = {'x': validator_lbl['x'] + validator_lbl['w'], 'y': validator_lbl['y'],
                     'h': validator_lbl['h'], 'w': validator_lbl['w'] * 1.5, 'bg': my_color['spare_fir'],
                     'type': 'Entry'}

model_lbl = {'x': validator_lbl['x'], 'y': validator_lbl['y'] + validator_lbl['h'],
             'h': validator_lbl['h'], 'w': validator_lbl['w'],
             'bg': my_color['fg'], 'text': 'Model', 'type': 'Label'}
model_txt_fld = {'x': model_lbl['x'] + model_lbl['w'], 'y': model_lbl['y'],
                 'h': model_lbl['h'], 'w': model_lbl['w'] * 1.5, 'bg': my_color['spare_fir'], 'type': 'Entry'}

fw_lbl = {'x': model_lbl['x'], 'y': model_lbl['y'] + model_lbl['h'],
          'h': model_lbl['h'], 'w': model_lbl['w'],
          'bg': my_color['fg'], 'text': 'FW Info', 'type': 'Label'}
fw_txt_fld = {'x': fw_lbl['x'] + fw_lbl['w'], 'y': fw_lbl['y'],
              'h': fw_lbl['h'], 'w': fw_lbl['w'] * 1.5, 'bg': my_color['spare_fir'], 'type': 'Entry'}

# Network Information
ip_lbl_info = {'x': validator_txt_fld['x'] + validator_txt_fld['w'], 'y': validator_txt_fld['y'],
               'h': lbl_size['h'], 'w': lbl_size['w'],
               'bg': my_color['fg'], 'text': 'IP Address', 'type': 'Label'}
ip_txt_fld_info = {'x': ip_lbl_info['x'] + ip_lbl_info['w'], 'y': ip_lbl_info['y'],
                   'h': lbl_size['h'], 'w': lbl_size['w'] * 1.5, 'bg': my_color['spare_fir'], 'type': 'Entry'}

port_lbl_info = {'x': ip_lbl_info['x'], 'y': ip_lbl_info['y'] + ip_lbl_info['h'],
                 'h': lbl_size['h'], 'w': lbl_size['w'],
                 'bg': my_color['fg'], 'text': 'Port No', 'type': 'Label'}
port_txt_fld_info = {'x': ip_txt_fld_info['x'], 'y': ip_txt_fld_info['y'] + ip_txt_fld_info['h'],
                     'h': lbl_size['h'], 'w': lbl_size['w'] * 1.5, 'bg': my_color['spare_fir'], 'type': 'Entry'}

rtsp_lbl_info = {'x': port_lbl_info['x'], 'y': port_lbl_info['y'] + port_lbl_info['h'],
                 'h': lbl_size['h'], 'w': lbl_size['w'],
                 'bg': my_color['fg'], 'text': 'RTSP Port', 'type': 'Label'}
rtsp_txt_fld_info = {'x': port_txt_fld_info['x'], 'y': port_txt_fld_info['y'] + port_txt_fld_info['h'],
                     'h': lbl_size['h'], 'w': lbl_size['w'] * 1.5, 'bg': my_color['spare_fir'], 'type': 'Entry'}

# Camera ID, PW Information
ipc_id_info = {'x': fw_lbl['x'], 'y': fw_lbl['y'] + fw_lbl['h'] + 10,
               'h': lbl_size['h'], 'w': lbl_size['w'], 'bg': my_color['fg'], 'text': 'Camera ID', 'type': 'Label'}
ipc_id_txt_fld_info = {'x': ipc_id_info['x'] + ipc_id_info['w'], 'y': ipc_id_info['y'],
                       'h': lbl_size['h'], 'w': lbl_size['w'], 'bg': my_color['spare_fir'], 'type': 'Entry',
                       'security': True}

ipc_pw_info = {'x': ipc_id_txt_fld_info['x'] + ipc_id_txt_fld_info['w'] + 2,
               'y': rtsp_lbl_info['y'] + rtsp_txt_fld_info['h'] + 10,
               'h': lbl_size['h'], 'w': lbl_size['w'], 'bg': my_color['fg'], 'text': 'Camera PW', 'type': 'Label'}
ipc_pw_txt_fld_info = {'x': ipc_pw_info['x'] + ipc_pw_info['w'], 'y': ipc_pw_info['y'],
                       'h': lbl_size['h'], 'w': lbl_size['w'], 'bg': my_color['spare_fir'], 'type': 'Entry',
                       'security': True}

register_btn = {'x': ipc_pw_txt_fld_info['x'] + ipc_pw_txt_fld_info['w'] + 5, 'y': ipc_id_info['y'] - 2,
                'h': lbl_size['h'] + 2, 'w': lbl_size['w'] - 7,
                'bg': my_color['bg'], 'text': 'Register'}

# Searching UI element position and size
search_txt_fld_info = {'x': info_start_pos['x'], 'y': register_btn['y'] + register_btn['h'] + 10,
                       'h': lbl_size['h'], 'w': lbl_size['w'] * 4,
                       'bg': my_color['spare_fir'], 'type': 'Entry'}

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
                    'bg': my_color['spare_fir'], 'fg': my_color['bg'], 'type': 'Entry'}

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
                    'bg': my_color['fg'], 'text': 'PTZ\nMode', 'type': 'Label'}
ptz_osd_mode_btn = {'x': ptz_osd_mode_lbl['x'], 'y': ptz_osd_mode_lbl['y'] + ptz_osd_mode_lbl['h'],
                    'h': lbl_size['h'], 'w': lbl_size['w'],
                    'bg': my_color['bg'], 'fg': my_color['fg'], 'text': 'Script Mode'}


# =============================================== PTZ UI ===============================================================
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

# ==================================================== Preset UI =======================================================
preset_canvas = {'x': ptz_canvas['x'] + ptz_canvas['w'], 'y': ptz_canvas['y'],
                 'w': 130, 'h': 220, 'bg': my_color['bg']}

preset_lbl = {'x': ptz_canvas['x'] + ptz_canvas['w'], 'y': ptz_canvas['y'] + 5,
              'w': 65, 'h': 20, 'bg': my_color['fg'], 'type': 'Label'}
tour_lbl = {'x': preset_lbl['x'] + preset_lbl['w'] + 1, 'y': preset_lbl['y'],
            'w': 65, 'h': 20, 'bg': my_color['fg'], 'type': 'Label'}

preset_txt_fld = {'x': preset_lbl['x'], 'y': preset_lbl['y'] + preset_lbl['h'] + 1,
                  'w': 65, 'h': 20, 'bg': my_color['fg'], 'type': 'Entry'}
tour_txt_fld = {'x': preset_txt_fld['x'] + preset_txt_fld['w'] + 1, 'y': preset_txt_fld['y'],
                'w': 65, 'h': 20, 'bg': my_color['fg'], 'type': 'Entry'}

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

# ======================================================== Script UI ===================================================
# Script(Repeat, interval) Position Setting
interval_lbl = {'x': search_btn['x'] - 80, 'y': treeview_pos['y'] + tree_view_size['h'] - 10,
                'h': lbl_size['h'], 'w': lbl_size['w'],
                'bg': my_color['fg'], 'fg': my_color['fg'], 'text': 'Interval(msec)', 'type': 'Label'}
interval_txt_fld = {'x': interval_lbl['x'] + interval_lbl['w'] + 10, 'y': interval_lbl['y'],
                    'h': lbl_size['h'], 'w': lbl_size['w'] - 30,
                    'bg': my_color['spare_fir'], 'fg': my_color['fg'], 'type': 'Entry'}
interval_add_btn = {'x': interval_txt_fld['x'] + interval_txt_fld['w'] + 5, 'y': interval_txt_fld['y'],
                    'h': lbl_size['h'], 'w': lbl_size['w'] / 3,
                    'bg': my_color['bg'], 'fg': my_color['fg'], 'text': 'Add'}

repeat_lbl = {'x': interval_lbl['x'], 'y': interval_lbl['y'] + interval_lbl['h'] + 5,
              'h': lbl_size['h'], 'w': lbl_size['w'],
              'bg': my_color['fg'], 'fg': my_color['fg'], 'text': 'Repeat', 'type': 'Label'}
repeat_txt_fld = {'x': repeat_lbl['x'] + repeat_lbl['w'] + 10, 'y': repeat_lbl['y'],
                  'h': lbl_size['h'], 'w': lbl_size['w'] - 30,
                  'bg': my_color['spare_fir'], 'fg': my_color['fg'], 'type': 'Entry'}

script_mode_lbl = {'x': repeat_lbl['x'], 'y': repeat_lbl['y'] + repeat_lbl['h'] + 5,
                   'h': lbl_size['h'], 'w': lbl_size['w'],
                   'bg': my_color['fg'], 'fg': my_color['fg'], 'text': 'Script Mode', 'type': 'Label'}
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
