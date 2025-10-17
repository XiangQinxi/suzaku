import typing

import ctypes
import os
import sys
import glfw

if typing.TYPE_CHECKING:
    from .widgets import window


class SkMisc:
    window: "window.SkWindow"

    def get_widget_with_id(self, widget_id: str) -> "window.SkWidget | None":
        """Get the widget with the given ID.

        :param widget_id: The ID of the widget.
        :return: SkWidget | None: The widget with the given ID, or None if not found.
        """
        for widget in self.window.children:
            if widget.id == widget_id:
                return widget
        return None

    def time(self, value: float | None = None):
        """Get or set the time.

        :param value: The time to set. Defaults to None.

        :return: float | typing.Self: The time if value is None, otherwise self.
        """

        if value is not None:
            glfw.set_time(value)
            return self
        else:
            return glfw.get_time()

    def get_program_files(self):
        """Get the path of the Program Files directory.

        :return: str: The path of the Program Files directory.
        """
        import winreg

        try:
            with winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion",
            ) as key:
                val, _ = winreg.QueryValueEx(key, "ProgramFilesDir")
                return val
        except Exception:
            return os.environ.get("ProgramFiles", r"C:\\Program Files")

    def get_tabtip_path(self):
        """Get the path of the TabTip.exe file.

        :return: str: The path of the TabTip.exe file.
        """
        base = self.get_program_files()
        return os.path.join(
            base, "Common Files", "Microsoft Shared", "ink", "TabTip.exe"
        )

    def _keyboard_open_win32(self):
        """Open the on-screen keyboard on Windows."""
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
        """Get or set the clipboard string.

        :param value: The string to set to clipboard. Defaults to None.
        :return: str | typing.Self: The string if value is None, otherwise self.
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
        """Post an empty event to the event queue."""
        glfw.post_empty_event()

    @staticmethod
    def mods_name(_mods, join: str = "+") -> str:
        """Get the name of the modifier keys.

        :param _mods: The modifier keys.
        :param join: The separator to join the names. Defaults to "+".
        :return: str: The name of the modifier keys.
        """
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
        radius: tuple[
            tuple[int, int],
            tuple[int, int],
            tuple[int, int],
            tuple[int, int],
        ],
    ) -> tuple[tuple[int, int], ...]:
        """Unpack the radius.

        :param radius: The radius to unpack.
        :return: tuple[tuple[int, int], ...]: The unpacked radius.
        """
        _radius: list[tuple[int, int]] = list(radius)
        for i, r in enumerate(_radius):
            if isinstance(r, int):
                _radius[i] = (r, r)
        result = tuple(_radius)
        return result

    @staticmethod
    def unpack_padx(padx: int | tuple[int, int]) -> tuple[int, int]:
        """Unpack padx.

        :param padx:
        :return: tuple[int, int]: The unpacked padx.
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

        :param pady:
        :return: tuple[int, int]: The unpacked pady.
        """
        if type(pady) is tuple:
            top = pady[0]
            bottom = pady[1]
        else:
            top = bottom = pady
        return top, bottom

    def unpack_padding(self, padx, pady):
        """Unpack padding.

        :param padx: The padding to unpack.
        :param pady: The padding to unpack.
        :return: tuple[int, int, int, int]: The unpacked padding. [Left, Top, Right, Bottom]
        """
        left, right = self.unpack_padx(padx)
        top, bottom = self.unpack_pady(pady)

        return left, top, right, bottom

    @staticmethod
    def _style(name: str, default, style):
        """Get the style value.

        :param name: The name of the style.
        :param default: The default value.
        :param style: The style dictionary.
        :return: The value of the style.
        """
        if name in style:
            return style[name]
        else:
            return default

    @staticmethod
    def sk_get_type(obj_or_cls: typing.Any) -> list[str]:
        """
        Returns a list of names of a class/object's parent classes. Written by Google Gemini.

        This is used to prevent circular import caused by loads of isinstance().

        :param obj_or_cls: The class or object to be checked
        :return: A list of names of its parent classes
        """
        # 判斷傳入的是類別還是物件
        if isinstance(obj_or_cls, type):
            # 如果是類別，直接使用它
            cls = obj_or_cls
        else:
            # 如果是物件，使用其 __class__ 屬性獲取類別
            cls = obj_or_cls.__class__

        # 獲取方法解析順序 (MRO)
        mro_tuple = cls.__mro__

        # 建立一個列表，用於儲存父類別的名稱
        parent_names = []

        # 遍歷 MRO 元組，從第二個元素（第一個父類別）開始
        # 並且排除最後一個元素（object），因為它不是我們自定義的類別。
        for parent_cls in mro_tuple[1:-1]:
            parent_names.append(parent_cls.__name__)

        return parent_names
