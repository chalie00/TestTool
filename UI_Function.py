import threading
import time

from datetime import datetime
from tkinter import ttk
from icecream import ic

import Constant as Cons
import MainFunction as Mf
import Communication as Comm
import Ptz as pt
import Table as tb
import ASYNC_Temp as Async

thread_running = threading.Event()
thread = None


# (2024.07.19): Model Drop Down Menu function
# (2024.09.24): Add Model for FT
# 2025.12.16: model select function modify for finetree
def model_select(event, parent, sel_op):
    current_sel = sel_op.get()
    Cons.model_obj['model_name'] = current_sel
    Cons.selected_model = current_sel

    if current_sel in ['NYX Series', 'DRS', 'Uncooled', 'MiniGimbal', 'Multi', 'CTEC']:
        col_name = Cons.column_array
    else:
        col_name = Cons.column_array_fine_tree
        
    command_data, ft_data = Mf.get_data_from_csv(Cons.cmd_path)
    if current_sel == "FineTree":
        Cons.fine_tree_cmd_data_all = ft_data
        Cons.fine_tree_cmd_data_filtered = ft_data[:]   # ✅ 현재 뷰는 일단 전체
    else:
        Cons.fine_tree_cmd_data_all = []
        Cons.fine_tree_cmd_data_filtered = []

    # ✅ 테이블 재생성 금지, update만
    Mf.update_table(Cons.tv, col_name, Cons.tree_view_size['w'], command_data)

    pt.PTZ(parent).refresh_ptz()
    parent.focus_set()


# Search a protocol which user typed a text
# 2025.12.16: search function modify for finetree
def search_command(event, parent, sear_fld, col_name, col_count, treeview):
    query = sear_fld.get().lower().strip()

    command_data, ft_data = Mf.get_data_from_csv(Cons.cmd_path)
    
    if Cons.selected_model == "FineTree":
        Cons.fine_tree_cmd_data_all = ft_data  # 원본 갱신(엑셀 다시 읽었으니)
        if query:
            paired = [(cmd, ft) for cmd, ft in zip(command_data, ft_data)
                      if query in str(cmd[0]).lower()]
        else:
            paired = list(zip(command_data, ft_data))

        filtered_cmd = [p[0] for p in paired]
        filtered_ft  = [p[1] for p in paired]

        Cons.fine_tree_cmd_data_filtered = filtered_ft  # ✅ 화면용 갱신
        rows_to_show = filtered_cmd
    else:
        rows_to_show = [cmd for cmd in command_data
                        if (not query) or (query in str(cmd[0]).lower())]

    # ✅ update만 호출
    Mf.update_table(treeview, col_name, Cons.tree_view_size['w'], rows_to_show)
    
def interval_add(parent, interval):
    cur_interval = float(int(interval.get()) / 1000)
    Cons.script_itv_arrs.append(cur_interval)
    row_cmd_title = len(Cons.script_cmd_arrs)
    col_interval = len(Cons.script_itv_arrs)

    for i, cmd_list in enumerate(Cons.script_itv_arrs):
        Cons.script_cmd_itv_arrs[i][0] = Cons.script_cmd_titles[i]
        Cons.script_cmd_itv_arrs[i][1] = Cons.script_itv_arrs[i]

    Mf.check_interval_active()
    print(Cons.script_cmd_itv_arrs)
    tb.Table(parent)


# (2024.07.04): Start a thread with a selected script
def start_thread(parent, app, repeat_txt_fld, interval_txt_fld, treeview, script_start_btn, script_stop_btn):
    global thread
    if not thread_running.is_set():
        thread_running.set()
        Cons.data_sending = True
        # target에 함수 이름만 넘기고 인자는 별도로 설정 해야함
        thread = threading.Thread(target=run_script, args=(parent, app, repeat_txt_fld, interval_txt_fld,
                                                           treeview, script_start_btn, script_stop_btn), daemon=True)

        thread.start()
    else:
        ic('[info] script is alerady running')


def stop_script(script_start_btn, script_stop_btn):
    global thread
    thread_running.clear()
    Cons.data_sending = False
    script_start_btn.config(state='normal')
    script_stop_btn.config(state='disabled')
    print('stop script')
    ui_obj = [Cons.model_obj, Cons.network_obj, Cons.etc_obj, Cons.etc_btn_obj]
    set_ui_state(ui_obj, 'normal')

    if thread is not None and thread.is_alive():
        thread.join(timeout=1)  # Allow GUI to process events while waiting
        if thread.is_alive():
            print("[warn] worker thread still alive after join timeout")
        thread = None


def clr_script(parent, script_start_btn, script_stop_btn):
    Cons.data_sending = False
    script_start_btn.config(state='normal')
    script_stop_btn.config(state='normal')
    print('clear script')
    Mf.clr_table_arrays(parent)


# (2024.07.04): Start thread with a selected script
# (2024.10.18): Add a Finetree for a script
# (2024.10.18): modify threading for repeat
def run_script(parent, app, repeat_txt_fld, interval_txt_fld, treeview, script_start_btn, script_stop_btn) -> []:
    current_time = datetime.now()
    time_str = current_time.strftime('%Y-%m-%d-%H-%M-%S')
    response_file_name = rf'{Cons.log_path}_{time_str}.txt'
    repeat = int(repeat_txt_fld.get() or '1')
    ui_obj = [Cons.model_obj, Cons.network_obj, Cons.etc_obj, Cons.etc_btn_obj]
    # 2025.05.28: Disable some UI(model, network, etc), but must be modified PTZ, Preset, Tour, Script Stop
    set_ui_state(ui_obj, 'disable')

    try:
        script_start_btn.config(state='disabled')
        script_stop_btn.config(state='normal')

        for i in range(repeat):
            if not thread_running.is_set():
                break

            ic(rf'Repeat {i + 1}')
            if not Cons.data_sending:
                break

            if Cons.script_toggle_flag:
                execute_model_logic(app, parent, response_file_name)
            else:
                handle_custom_protocol_logic(parent, treeview, interval_txt_fld)

            time.sleep(0.1)

        set_ui_state(ui_obj, 'normal')

    except Exception as e:
        print(f"Error: {e}")

    finally:
        thread_running.clear()
        script_start_btn.config(state='normal')
        script_stop_btn.config(state='disabled')
        Cons.data_sending = False
        print('Finally stop script')


def execute_model_logic(app, parent, res_file_name):
    interval = Cons.script_itv_arrs
    script = Cons.script_cmd_arrs
    titles = Cons.script_cmd_titles
    print(script)

    if Cons.selected_model in ['Uncooled', 'DRS', 'Multi']:
        # Comm.send_cmd_to_ucooled_with_interval(interval, script, titles, parent)
        file_name = f"{Cons.selected_model}_{Cons.start_time}.txt"
        Async.async_send(Comm.send_cmd_to_ucooled_with_interval(interval, script, titles, parent), root_view=parent, log_name=file_name)
    elif Cons.selected_model == 'NYX Series':
        file_name = f"NYX Script_{Cons.start_time}.txt"
        Comm.send_cmd_to_nyx_with_interval(app, parent, titles, script, interval, file_name)
    elif Cons.selected_model == 'FineTree':
        print('Finetree Script Run')
        file_name = f"{Cons.selected_model}_{Cons.start_time}.txt"
        for i, cmd_data in enumerate(Cons.finetree_parms_arrays):
            Comm.fine_tree_send_cgi(cmd_data[0], cmd_data[1])
            Async.async_send(Comm.fine_tree_send_cgi(cmd_data[0], cmd_data[1]), root_view=parent, log_name=file_name)
            file_name_cap = rf'{Cons.capture_path["zoom"]}/{titles[i]}.png'
            Mf.capture_image(parent, file_name_cap)
    elif Cons.selected_model == 'MiniGimbal':
        Comm.send_to_mini_with_interval(Cons.only_socket, titles, script, interval)


def handle_custom_protocol_logic(parent, treeview, interval_txt_fld):
    protocol_str_arr = [treeview.set(id)[2] for id in treeview.get_checked()]
    hex_protocol = [Mf.convert_str_to_hex(protocol) for protocol in protocol_str_arr]
    interval = float(int(interval_txt_fld.get()) / 1000)
    titles = Cons.script_cmd_titles
    Comm.send_cmd_to_ucooled_with_interval(interval, hex_protocol, titles, parent)


# 2025.05.28: Disable some UI
def set_ui_state(ui_obj, state):
    print('State')
    for ui_array in ui_obj:
        for ui_item in ui_array.values():
            try:
                if isinstance(ui_item, str):
                    continue
                if isinstance(ui_item, ttk.Combobox):
                    ui_item.config(state='disabled' if state == 'disable' else 'normal')
                ui_item.config(state=state)
            except Exception as e:
                print(rf'Failed to change the {ui_item}: {e}')


# 2025.06.30: pushed_PT_Drv Button
def pushed_pt_drv():
    info = getattr(Cons, 'pt_drv_info')
    if info['drv']:
        info.update({
            'ch': '',
            'model': '',
            'ip': '',
            'port': '',
            'drv': False,
        })
        Cons.channel_buttons['pt_drv'].config(bg=Cons.pt_drv_btn_pos['bg'])
        for i in range(3, 5):
            Cons.channel_buttons[f'CH{i}'].config(state='normal')
    else:
        info.update({
            'ch': 'pt_drv',
            'model': Cons.model_obj['model_name'],
            'ip': Cons.network_obj['ip_txt'].get(),
            'port': Cons.network_obj['port_txt'].get(),
            'drv': True,
        })
        Cons.channel_buttons['pt_drv'].config(bg='green')
        for i in range(3, 5):
            Cons.channel_buttons[f'CH{i}'].config(state='disabled')

