# -*- coding: utf-8 -*-

import os
import sys
import tkinter as tk
import threading
import logging


def configure_vlc_runtime():
    base_dir = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    libvlc_path = os.path.join(base_dir, "libvlc.dll")
    plugins_path = os.path.join(base_dir, "plugins")

    if os.path.exists(libvlc_path):
        os.environ["PYTHON_VLC_LIB_PATH"] = libvlc_path
        os.environ["PYTHON_VLC_MODULE_PATH"] = plugins_path
        os.environ["VLC_PLUGIN_PATH"] = plugins_path
        if hasattr(os, "add_dll_directory"):
            os.add_dll_directory(base_dir)


configure_vlc_runtime()


def configure_runtime_logging():
    log_dir = os.path.join(os.getcwd(), "Log")
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "runtime_debug.log")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[
            logging.FileHandler(log_path, encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
        force=True,
    )
    logging.info("runtime logging initialized")
    logging.info("cwd=%s", os.getcwd())
    logging.info("meipass=%s", getattr(sys, "_MEIPASS", ""))


configure_runtime_logging()

from app.ui import UI_Init as UI_init
from app.config import Constant as Cons
from app.ui import KeyBind
from app.services import Communication as Comm
from app.ui import Table as tb
from app.ui import Response as Res
from app.ui import System_Info as SysInfo


def configure_runtime_paths():
    bundle_dir = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    runtime_dir = os.path.dirname(sys.executable) if getattr(sys, "frozen", False) else os.getcwd()

    Cons.cmd_path = os.path.join(bundle_dir, "Command", "Command.xlsx")
    Cons.log_path = os.path.join(runtime_dir, "Log")
    Cons.capture_path = {
        "zoom": os.path.join(runtime_dir, "Capture", "Zoom"),
        "focus": os.path.join(runtime_dir, "Capture", "Focus"),
    }

    os.makedirs(Cons.log_path, exist_ok=True)
    os.makedirs(Cons.capture_path["zoom"], exist_ok=True)
    os.makedirs(Cons.capture_path["focus"], exist_ok=True)

    logging.info("command workbook path=%s", Cons.cmd_path)
    logging.info("runtime log path=%s", Cons.log_path)


configure_runtime_paths()


class TestTool(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.setup_main_window()

        self.thread_running = threading.Event()
        self.thread = None
        self.video_players = {}

        # ================================================ UI Layout ============================================
        ui_initializer = UI_init.UIInit(root, parent, self)

        # ========================================== Log Text Field ============================================
        log_pos = Cons.log_txt_fld_info
        Cons.res_log_obj = Res.Response(parent, log_pos)

        # ========================================== System Information  ============================================
        sys_info_pos = Cons.sys_info_tab
        sys_info = SysInfo.SysInfo(parent, sys_info_pos)

        # ========================================= Set Script Table ===========================================
        script_tb = tb.Table(parent)

        # Set a bind system keyboard for PTZ and Preset in FT
        KeyBind.bind_system_kbd(parent)

    def setup_main_window(self):
        # Set Title
        self.parent.title('Test Tool')
        self.parent.geometry(f'{Cons.WINDOWS_SIZE["x"]}x{Cons.WINDOWS_SIZE["y"]}+'
                             f'{Cons.WINDOWS_POSITION["x"]}+{Cons.WINDOWS_POSITION["y"]}')
        self.parent.config(padx=15, pady=15)


# TODO: Script File Import Function
# TODO: Searching App link for FT

if __name__ == '__main__':
    root = tk.Tk()
    ptz_ins = KeyBind.initialize_ptz(root)
    app = TestTool(root)

    app.pack()
    Comm.click_register_button(app)

    root.focus_set()

    root.mainloop()
