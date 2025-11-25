# 2025.11.20 Creating for async templet
import threading
import os
import logging


import Constant as Cons
import Communication as Comm

from datetime import datetime

# 2025.11.20 Async Templet
def run_in_worker(fn, *, root_view=None, on_done=None, on_error=None, desc="worker"):
    """
    fn        : 실제로 오래 걸리는 동기 함수 (blocking)
    root_view : Tk root (UI 업데이트용). 없으면 콘솔/로그만.
    on_done   : fn 이 성공했을 때, 결과를 받아 UI를 갱신하는 콜백(result) -> None
    on_error  : 에러 발생 시 UI를 갱신하는 콜백(ex) -> None
    desc      : 로그용 설명 텍스트
    """
    def worker():
        try:
            result = fn()
        except Exception as ex:
            logging.exception("ERROR in %s: %s", desc, ex)
            if root_view is not None and on_error is not None:
                err = ex
                root_view.after(0, lambda err=err: on_error(err))
            return

        if root_view is not None and on_done is not None:
            root_view.after(0, lambda: on_done(result))

    t = threading.Thread(target=worker, daemon=True)
    t.start()
    return t   # 필요하면 thread 리턴, 필요없으면 무시해도 됨


# 2025.11.20 NYX Series Async Function
def nyx_series_async(fn, cmd=None, title=None, root_view=None, log_name=None):
    def done_func(rx):
        # if isinstance(rx, (bytes, bytearray)):
        #     response_raw = binascii.hexlify(rx).decode('utf-8')
        # else:
        #     response_raw = str(rx)
        logging.info(title, rx)

        current_time = datetime.now()
        time_str = current_time.strftime('%Y-%m-%d-%H-%M-%S')

        print(f"Received response: {rx}")
        response_with_time = fr'{time_str} : {rx}'
        Cons.response_txt.append(response_with_time)
        # 2025.11.25 New Log Function to create text file was applied
        Comm.log_control(response_with_time, file_name=log_name)

        if root_view is None:
            return

        def _update_ui():
            # log_pos = Cons.log_txt_fld_info
            # log_fld = Res.Response(root_view, log_pos)
            if Cons.res_log_obj is not None:
                Cons.res_log_obj.dis_response_text()

        root_view.after(0, _update_ui)

    def on_error(ex: Exception):
        logging.error('[NYX ERR] [%s] %s', title, ex)

    return run_in_worker(fn, root_view=root_view, on_done=done_func, on_error=on_error, desc=f'nyx: {title}')
