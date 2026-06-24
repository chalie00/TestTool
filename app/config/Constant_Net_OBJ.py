# (2024.07.19): Model Flag (Uncooled, NTX Series)
# Important (2025.04.29): Selecting FineTree first used to crash because it
# needs additional arrays to be initialized before use.

selected_model = 'Multi'
model_option = ['Uncooled', 'UncooledTTL', 'DRS',
                'FineTree', 'CTEC', 'NYX Series',
                'Multi', 'CMJ_PT',
                'MiniGimbal']

# ====================================================  NETWORK ==================================================================
# Network information from user input.
data_sending = True
host_ip: str = ""
port: int = 0  # Default 32000
rtsp_port: int = 0
buf_size = 4096

# RTSP information.
rtsp_url = ''
ipc_id = ''
ipc_pw = ''

video_player_ch1 = None
video_player_ch2 = None
video_player_ch3 = None
video_player_ch4 = None

# The selected channel points to one of the chX_rtsp_info objects.
# 2025.06.30: Added Multi Sensor PT Drv.
# The CH button initializes both the object and Constant.chX_rtsp_info.
selected_ch = None

# Seyeon TTL serial parameters.
# Fixed serial parameters.
FW_NODE = "ttyS1"
FW_BAUD = {
    'Uncooled': 38400,
    'UncooledTTL': 38400,
    'NYX Series': 57600,
}.get(selected_model, 38400)
FW_DBITS = 8
FW_SBITS = 1
FW_PARITY = "n"  # Lowercase as expected by the device.

# Receive loop settings.
READ_MAX_BYTES = 8192
RECV_WAIT_SEC = 3.0  # Maximum receive wait time.
PRE_SEND_DELAY = 0.30  # Delay after the header while the tunnel becomes ready.
POST_SEND_DELAY = 0.30  # Delay before the first receiver after sending.

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
fine_tree_cmd_data_filtered = []
finetree_parms_arrays = []

# PTZ/OSD Toggle Variable
ptz_osd_toggle_flag = False
tour_lists = []

interval_button = None
