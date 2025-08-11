import threading


class SkAfter:
    def after(self, ms: int, func: callable):
        """Execute a function after a delay (an ID will be provided in the future for unbinding).

        * `ms`: Delay in milliseconds
        * `func`: Function to execute after delay
        """
        timer = threading.Timer(ms / 1000, func)
        timer.start()
        return self
