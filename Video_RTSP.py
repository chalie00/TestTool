import threading
import icecream as ic

import Constant as Cons
import Communication as Comm
import VideoPlayer as Vp


def open_video_window():
    Cons.selected_model = Cons.model_obj['model_name']
    Comm.find_ch()
    # Cons.selected_model = Cons.selected_ch['model']
    Cons.selected_model = Cons.selected_ch['model'] if Cons.selected_ch else 'UNKNOWN_MODEL'
    # print(Cons.selected_model)
    # Create only one socket for Minigimbal
    if Cons.selected_model == 'MiniGimbal':
        threading.Thread(target=handle_minigimbal, daemon=True).start()

    for i in range(1, 5):
        Cons.channel_buttons[f'CH{i}'].config(bg=Cons.ch1_btn_pos['bg'])

    videos = [
        Cons.video_player_ch1,
        Cons.video_player_ch2,
        Cons.video_player_ch3,
        Cons.video_player_ch4
    ]

    threading.Thread(target=start_videos, args=(videos,)).start()


def start_videos(videos):
    for video in videos:
        if video:
            print(f"Starting video player: {video}")
            video.start_video()
        else:
            print("Video player is None")


def handle_minigimbal():
    Cons.only_socket = Comm.create_socket()
    try:
        while True:
            data = Cons.only_socket.recv(39)
            hex_value = [f'{bytes:02x}' for bytes in data]
            # print(rf'{datetime.now()}: {hex_value}')
            Comm.update_res_to_cons(hex_value)
            # Comm.save_res_from_miniG_Text(data)
            # Comm.save_res_from_miniG_CSV(data)
            if not data:
                print('No data is being sent from MiniGimbal')
                break
    except KeyboardInterrupt:
        print('Keyboard interrupt received, shutting down')
    except Exception as e:
        print(f"Error: {e}")
    finally:
        Cons.only_socket.close()


def pushed_ch_btn(parent, ch_name):
    info = get_rtsp_info(ch_name)
    info['url'] = generate_rtsp_url(info)

    if info['url'] == 'Invalid model':
        print(f"Invalid model selected for {ch_name}")
        return

    Cons.channel_buttons[ch_name].config(bg='green')
    start_video_player(parent, ch_name, info)


def get_rtsp_info(ch_name):
    info = getattr(Cons, f'{ch_name.lower()}_rtsp_info')
    info.update({
        'ch': ch_name.lower(),
        'model': Cons.model_obj['model_name'],
        'ip': Cons.network_obj['ip_txt'].get(),
        'id': Cons.network_obj['ipc_id_txt'].get(),
        'pw': Cons.network_obj['ipc_pw_txt'].get(),
        'rtsp_port': Cons.network_obj['rtsp_txt'].get(),
        'port': Cons.network_obj['port_txt'].get(),
    })
    return info


def generate_rtsp_url(info):
    url_patterns = {
        'NYX Series': rf'rtsp://{info["id"]}:{info["pw"]}@{info["ip"]}:{info["rtsp_port"]}/test',
        'Uncooled': rf'rtsp://{info["id"]}:{info["pw"]}@{info["ip"]}:{info["rtsp_port"]}/cam0_0',
        'DRS': rf'rtsp://{info["id"]}:{info["pw"]}@{info["ip"]}:{info["rtsp_port"]}/cam0_0',
        'FineTree': rf'rtsp://{info["id"]}:{info["pw"]}@{info["ip"]}:{info["rtsp_port"]}/media/1/1',
        # MiniGimbal cannot display rtsp stream in currently
        'MiniGimbal': rf'',
        # EO Video Port: 20100, IR Video Port: 30100
        'TMS_20_EO': rf'rtsp://{info["id"]}:{info["pw"]}@{info["ip"]}/net0',
        'TMS_20_IR': rf'rtsp://{info["id"]}:{info["pw"]}@{info["ip"]}/net1',
        #  2025.06.25 Added a CTEC EO Camera
        # rtsp://192.168.100.160:554/AVStream1_1
        'CTEC': rf'rtsp://{info["id"]}:{info["pw"]}@{info["ip"]}/AVStream1_1',
    }
    return url_patterns.get(info['model'], 'Invalid model')


def start_video_player(parent, ch_name, info):
    if ch_name.lower() == 'ch1':
        ch_info = Cons.ch1_rtsp_info
        pos = {'x': ch_info['x'], 'y': ch_info['y'], 'h': ch_info['h'], 'w': ch_info['w']}
        Cons.video_player_ch1 = Vp.VideoPlayer(parent, info['url'], pos, ch_name)
    elif ch_name.lower() == 'ch2':
        ch_info = Cons.ch2_rtsp_info
        pos = {'x': ch_info['x'], 'y': ch_info['y'], 'h': ch_info['h'], 'w': ch_info['w']}
        Cons.video_player_ch2 = Vp.VideoPlayer(parent, info['url'], pos, ch_name)
    elif ch_name.lower() == 'ch3':
        ch_info = Cons.ch3_rtsp_info
        pos = {'x': ch_info['x'], 'y': ch_info['y'], 'h': ch_info['h'], 'w': ch_info['w']}
        Cons.video_player_ch3 = Vp.VideoPlayer(parent, info['url'], pos, ch_name)
    elif ch_name.lower() == 'ch4':
        ch_info = Cons.ch4_rtsp_info
        pos = {'x': ch_info['x'], 'y': ch_info['y'], 'h': ch_info['h'], 'w': ch_info['w']}
        Cons.video_player_ch4 = Vp.VideoPlayer(parent, info['url'], pos, ch_name)
