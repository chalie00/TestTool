import threading
import time
from datetime import datetime

import Constant as Cons
import MainFunction as Mf
import Communication as Comm
import Ptz as pt
import Table as tb

thread_running = threading.Event()
thread = None


# (2024.07.19): Model Drop Down Menu function
# (2024.09.24): Add Model for FT
def model_select(event, parent, sel_op):
    col_name = []
    current_sel = sel_op.get()
    Cons.model_obj['model_name'] = current_sel
    print(current_sel)
    if current_sel in ['NYX Series', 'DRS', 'Uncooled', 'MiniGimbal']:
        col_name = Cons.column_array
    elif current_sel in ['FineTree']:
        col_name = Cons.column_array_fine_tree

    Cons.selected_model = current_sel
    Comm.find_ch()
    col_count = len(col_name)
    command_data = Mf.get_data_from_csv(Cons.cmd_path)

    Mf.make_table(parent, col_count, Cons.tree_view_size['w'], col_name,
                  Cons.treeview_pos['x'], Cons.treeview_pos['y'], command_data)

    pt.PTZ(parent).refresh_ptz()


# Search a protocol which user typed text
def search_command(event, parent, sear_fld, col_name, col_count):
    query = sear_fld.get().lower()
    selected_item = []
    command_data = Mf.get_data_from_csv(Cons.cmd_path)
    for item in command_data:
        if query in item[0].lower():
            selected_item.append(item)

    Mf.make_table(parent, col_count, Cons.tree_view_size['w'], col_name,
                  Cons.treeview_pos['x'], Cons.treeview_pos['y'], selected_item)


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


# (2024.07.04): Start thread with selected script
def start_thread(parent, app, repeat_txt_fld, interval_txt_fld, treeview, script_start_btn, script_stop_btn):
    global thread
    if not thread_running.is_set():
        thread_running.set()
        # target에 함수 이름만 넘기고 인자는 별도로 설정 해야함
        thread = threading.Thread(target=run_script, args=(parent, app, repeat_txt_fld, interval_txt_fld,
                                                           treeview, script_start_btn, script_stop_btn))
        Cons.data_sending = True

        thread.start()


def stop_script(script_start_btn, script_stop_btn):
    global thread
    Cons.data_sending = False
    script_start_btn.config(state='normal')
    script_stop_btn.config(state='disabled')
    print('stop script')

    # thread_running.clear()
    # if thread and thread.is_alive():
    #     thread.join(timeout=1)  # Allow GUI to process events while waiting
    #     thread = None
    thread_running.clear()

    if thread is not None and thread.is_alive():
        thread.join(timeout=1)  # Allow GUI to process events while waiting
        thread = None


def clr_script(parent, script_start_btn, script_stop_btn):
    Cons.data_sending = False
    script_start_btn.config(state='normal')
    script_stop_btn.config(state='normal')
    print('clear script')
    Mf.clr_table_arrays(parent)


# (2024.07.04): Start thread with selected script
# (2024.10.18): Add a Finetree for script
# (2024.10.18): modify threading for repeat
def run_script(parent, app, repeat_txt_fld, interval_txt_fld, treeview, script_start_btn, script_stop_btn) -> []:
    current_time = datetime.now()
    time_str = current_time.strftime('%Y-%m-%d-%H-%M-%S')
    response_file_name = rf'{Cons.log_path}_{time_str}.txt'
    repeat = int(repeat_txt_fld.get())

    try:
        script_start_btn.config(state='disabled')
        script_stop_btn.config(state='normal')

        for i in range(repeat):
            print(rf'Repeat {i + 1}')
            if not Cons.data_sending:
                return

            if not thread_running.is_set():
                thread_running.set()

            if Cons.script_toggle_flag:
                execute_model_logic(app, parent, response_file_name)
            else:
                handle_custom_protocol_logic(parent, treeview, interval_txt_fld)

            time.sleep(0.1)

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

    if Cons.selected_model in ['Uncooled', 'DRS']:
        Comm.send_cmd_to_ucooled_with_interval(interval, script, titles, parent)
    elif Cons.selected_model == 'NYX Series':
        Comm.send_cmd_to_nyx_with_interval(app, parent, titles, script, interval, res_file_name)
    elif Cons.selected_model == 'FineTree':
        print('Finetree Script Run')
        for i, cmd_data in enumerate(Cons.finetree_parms_arrays):
            Comm.fine_tree_send_cgi(cmd_data[0], cmd_data[1])
            file_name = rf'{Cons.capture_path["zoom"]}/{titles[i]}.png'
            Mf.capture_image(parent, file_name)
    elif Cons.selected_model == 'MiniGimbal':
        Comm.send_to_mini_with_interval(Cons.only_socket, titles, script, interval)


def handle_custom_protocol_logic(parent, treeview, interval_txt_fld):
    protocol_str_arr = [treeview.set(id)[2] for id in treeview.get_checked()]
    hex_protocol = [Mf.convert_str_to_hex(protocol) for protocol in protocol_str_arr]
    interval = float(int(interval_txt_fld.get()) / 1000)
    titles = Cons.script_cmd_titles
    Comm.send_cmd_to_ucooled_with_interval(interval, hex_protocol, titles, parent)
