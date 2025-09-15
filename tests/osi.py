import subprocess


import psutil


def is_osk_running():
    for proc in psutil.process_iter(["name"]):
        if proc.info["name"] and proc.info["name"].lower() in ("osk.exe", "tabtip.exe"):
            return True
    return False


print("软键盘是否运行:", is_osk_running())


import subprocess
import os


import ctypes
import os


def show_keyboard():
    tabtip = r"C:\Program Files\Common Files\Microsoft Shared\ink\TabTip.exe"
    if not os.path.exists(tabtip):
        tabtip = "osk.exe"  # 兜底

    # ShellExecuteW(hwnd, operation, file, parameters, directory, show_cmd)
    ctypes.windll.shell32.ShellExecuteW(None, "open", tabtip, None, None, 1)


show_keyboard()
