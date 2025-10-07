import typing

import ctypes
import os
import sys
import glfw

if typing.TYPE_CHECKING:
    from . import window


import warnings
warnings.warn(FutureWarning("相亲西给我补docstring"))


class SkMisc:

    def time(self, value: float | None = None):
        if value is not None:
            glfw.set_time(value)
            return self
        else:
            return glfw.get_time()

    def get_program_files(self):
        import winreg

        try:
            with winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion"
            ) as key:
                val, _ = winreg.QueryValueEx(key, "ProgramFilesDir")
                return val
        except Exception:
            return os.environ.get("ProgramFiles", r"C:\\Program Files")

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
        self.window: window.SkWindow
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

    @staticmethod
    def unpack_radius(
        radius:
            tuple[
                tuple[int, int],
                tuple[int, int],
                tuple[int, int],
                tuple[int, int],
            ]
    ) -> tuple[tuple[int, int], ...]:
        """Unpacking the radius"""
        _radius: list[tuple[int, int]] = list(radius)
        for i, r in enumerate(_radius):
            if isinstance(r, int):
                _radius[i] = (r, r)
        result = tuple(_radius)
        return result

    @staticmethod
    def unpack_padx(padx):
        """Unpack padx.
        
        :param padx:
        :return:
        """
        if type(padx) is tuple:
            left = padx[0]
            right = padx[1]
        else:
            left = right = padx
        return left, right

    @staticmethod
    def unpack_pady(pady):
        """Unpack pady.
        【上下】
        :param pady:
        :return:
        """
        if type(pady) is tuple:
            top = pady[0]
            bottom = pady[1]
        else:
            top = bottom = pady
        return top, bottom

    def unpack_padding(self, padx, pady):
        """Unpack padding.
        【左上右下】
        :param padx:
        :param pady:
        :return:
        """
        left, right = self.unpack_padx(padx)
        top, bottom = self.unpack_pady(pady)

        return left, top, right, bottom

    @staticmethod
    def _style(name: str, default, style):
        """"""
        if name in style:
            return style[name]
        else:
            return default
