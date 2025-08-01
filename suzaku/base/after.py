class After:
    def after(self, ms: int, func: callable):
        """
        延迟执行
        (未来将给出ID作为标识符，供解绑)

        Args:
            ms: 延迟执行的毫秒
            func: 延迟执行的函数

        Returns:
            self
        """
        import threading
        timer = threading.Timer(ms / 1000, func)
        timer.start()
        return self
