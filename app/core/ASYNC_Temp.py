# 2025.11.20 Creating for async templet
import threading
import os
import logging


from app.config import Constant as Cons
from app.services import Communication as Comm

from datetime import datetime

# 2025.11.20 Async Templet
def run_in_worker(fn, *, root_view=None, on_done=None, on_error=None, desc="worker"):
    """
    fn: Blocking function to run in a worker thread.
    root_view: Tk root used to schedule UI updates with `after`.
    on_done: Callback invoked on the UI thread with the worker result.
    on_error: Callback invoked on the UI thread when an exception occurs.
    desc: Label used in log messages.
    """
    if not callable(fn):
        ex = TypeError(f"{desc} expected callable fn, got {type(fn).__name__}")
        logging.error("ERROR before worker start: %s", ex)
        if root_view is not None and on_error is not None:
            root_view.after(0, lambda err=ex: on_error(err))
        return None

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
    return t  # Return the thread so callers can track it if needed.


# 2025.11.20 NYX Series Async Function
def async_send(fn, title=None, root_view=None, log_name=None):
    def done_func(rx):
        # if isinstance(rx, (bytes, bytearray)):
        #     response_raw = binascii.hexlify(rx).decode('utf-8')
        # else:
        #     response_raw = str(rx)
        logging.info("async_send done title=%s rx=%r", title, rx)

        if rx is None:
            return

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
            # if Cons.res_log_obj is not None:
            #     Cons.res_log_obj.dis_response_text()
            if Cons.selected_model == 'DRS':
                if Cons.res_log_obj is not None:
                    Cons.res_log_obj.dis_response_text()
            elif Cons.selected_model == 'Multi':
                if Cons.res_log_obj is not None:
                    Cons.res_log_obj.multi_response(rx)
            elif Cons.selected_model == 'CMJ_PT':
                if Cons.res_log_obj is not None:
                    Cons.res_log_obj.multi_response(rx)
        root_view.after(0, _update_ui)

    def on_error(ex: Exception):
        logging.error('[NYX ERR] [%s] %s', title, ex)

    return run_in_worker(fn, root_view=root_view, on_done=done_func, on_error=on_error, desc=f'nyx: {title}')

