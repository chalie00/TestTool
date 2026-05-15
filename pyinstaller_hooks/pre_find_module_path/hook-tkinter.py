def pre_find_module_path(hook_api):
    # Keep the standard library tkinter package discoverable even when
    # PyInstaller's Tcl/Tk probe fails in this environment.
    return
