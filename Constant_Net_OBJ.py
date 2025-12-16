
# (2024.07.19): Model Flag (Uncooled, NTX Series)
#  !import (2025.04.29): When was selected FineTree at first, It will be crash,
#   because FineTree needs to collect another arrays

selected_model = 'Multi'
model_option = ['Uncooled', 'DRS', 'FineTree', 'NYX Series', 'MiniGimbal', 'Multi', 'CTEC']

# ====================================================  NETWORK ==================================================================
# Network Information form User Input
data_sending = True
host_ip: str = ""
port: int = 0  # Default 32000
rtsp_port: int = 0
buf_size = 4096

# RTSP Information
rtsp_url = ''
ipc_id = ''
ipc_pw = ''

video_player_ch1 = None
video_player_ch2 = None
video_player_ch3 = None
video_player_ch4 = None

# the selected ch is one of below ch(ch1_rtsp_info ....)
# 2025.06.30 Added Muilti Sensor PT Drv
selected_ch = None

# for Seyeon TTL
# 확정된 파라미터
FW_NODE = "ttyS1"
FW_BAUD = {
    'Uncooled': 38400,
    'NYX Series': 57600,
}.get(selected_model, 38400)
FW_DBITS = 8
FW_SBITS = 1
FW_PARITY = "n"  # 소문자

# 수신 루프 설정
READ_MAX_BYTES = 8192
RECV_WAIT_SEC = 3.0  # 최대 대기
PRE_SEND_DELAY = 0.30  # 헤더 보낸 뒤 터널 준비 시간
POST_SEND_DELAY = 0.30  # 송신 직후 첫 수신까지 지연


# ====================================================  OBJECT ==================================================================
# validator_txt, model_txt, fw_txt
model_obj = {'model_name': selected_model}

# CH Object
channel_buttons = {}

# ip_txt, port_txt, rtsp_txt, ipc_id_txt, ipc_pw_txt
network_obj = {}

# inter_txt, repe_txt
etc_obj = {}

# etc Button
etc_btn_obj = {'drop_down': None, 'script_clear': None}

# log Obj
res_log_obj = None

# =======================================================  ETC   ==================================================================
start_time = None
only_socket = None

# 0: parameter, 1: value, 2: BaseUrl
fine_tree_cmd_data = []
finetree_parms_arrays = []

# PTZ/OSD Toggle Variable
ptz_osd_toggle_flag = False
tour_lists = []

interval_button = None