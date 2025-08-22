import threading
import typing

import glfw


class SkMisc:
    def time(self, value: float = None):
        if value is not None:
            glfw.set_time(value)
            return self
        else:
            return glfw.get_time()

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
