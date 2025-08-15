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

    afters = {}  # {"*id": ["time": *s, "func": *func]}
    _after = 0

    def after(self, s: int | float, func: callable):
        """Execute a function after a delay (an ID will be provided in the future for unbinding).

        :param s: Delay in seconds
        :param func: Function to execute after delay
        :return: ID of the timer
        """
        _id = "after." + str(self._after)
        self.afters[_id] = {"time": self.time() + s, "func": func}
        self._after += 1
        return _id

    def after_cancel(self, _id: str) -> typing.Self:
        """Cancel a timer.

        :param _id: ID of the timer
        """
        del self.afters[_id]
        return self

    def after2(self, s: int | float, func: callable) -> threading.Timer:
        """Execute a function after a delay (an ID will be provided in the future for unbinding).

        :param s: Delay in seconds
        :param func: Function to execute after delay
        """
        timer = threading.Timer(s, func)
        timer.start()
        return timer
