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
