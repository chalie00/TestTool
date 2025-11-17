# -*- coding: utf-8 -*-

import tkinter as tk
import threading

import UI_Init as UI_init
import Constant as Cons
import KeyBind
import MainFunction as Mf
import Communication as Comm
import Table as tb
import Response as Res
import System_Info as SysInfo
import TTL_Communication as ttl


import ssl, hashlib, binascii, time
import requests
from requests.adapters import HTTPAdapter
from requests.auth import HTTPDigestAuth
from urllib3.util.ssl_ import create_urllib3_context


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

        # ======================================== Set Command Table ===========================================
        column_name = Cons.column_array
        column_count = len(column_name)
        cmd_data = Cons.command_array

        treeview = Mf.make_table(parent, column_count, Cons.tree_view_size['w'], column_name,
                                 Cons.treeview_pos['x'], Cons.treeview_pos['y'], cmd_data)

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
