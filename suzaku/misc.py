import threading
import typing
import os, ctypes, sys

import glfw


class SkMisc:
    def time(self, value: float = None):
        if value is not None:
            glfw.set_time(value)
            return self
        else:
            return glfw.get_time()

    def get_program_files(self):
        import winreg

        try:
            with winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion"
            ) as key:
                val, _ = winreg.QueryValueEx(key, "ProgramFilesDir")
                return val
        except Exception:
            return os.environ.get("ProgramFiles", r"C:\Program Files")

    def get_tabtip_path(self):
        base = self.get_program_files()
        return os.path.join(
            base, "Common Files", "Microsoft Shared", "ink", "TabTip.exe"
        )

    def _keyboard_open_win32(self):
        tabtip = (
            self.get_tabtip_path()
        )  # r"C:\Program Files\Common Files\Microsoft Shared\ink\TabTip.exe"
        if not os.path.exists(tabtip):
            tabtip = "osk.exe"  # 兜底
        # ShellExecuteW(hwnd, operation, file, parameters, directory, show_cmd)
        ctypes.windll.shell32.ShellExecuteW(None, "open", tabtip, None, None, 1)

    def keyboard_open(self):
        return
        if sys.platform == "win32":
            self._keyboard_open_win32()

    def clipboard(self, value: str | None = None) -> str | typing.Self:
        """Get string from clipboard

        anti images
        """
        if value is not None:
            glfw.set_clipboard_string(self.window.the_window, value)
            return self
        else:
            try:
                return glfw.get_clipboard_string(self.window.the_window).decode("utf-8")
            except AttributeError:
                return ""

    @staticmethod
    def post():
        """
        发送一个空事件，用于触发事件循环
        """
        glfw.post_empty_event()

    @staticmethod
    def mods_name(_mods, join: str = "+"):
        keys = []
        flags = {
            "control": glfw.MOD_CONTROL,
            "shift": glfw.MOD_SHIFT,
            "alt": glfw.MOD_ALT,
            "super": glfw.MOD_SUPER,
            "caps_lock": glfw.MOD_CAPS_LOCK,
            "num_lock": glfw.MOD_NUM_LOCK,
        }

        for name, value in flags.items():
            if _mods & value == value:
                keys.append(name)

        return join.join(keys)
