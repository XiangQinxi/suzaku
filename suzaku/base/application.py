class Application:

    """
    应用程序
    """

    _instance = None

    def __init__(self) -> None:
        """
        初始化
        """

        self.windows = []
        self.running = False
        self.init_glfw()
        if Application._instance is not None:
            raise RuntimeError("App is a singleton, use App.get_instance()")
        Application._instance = self

    # 这里用这个可以使`Window`的初始化更加简单，可以不选择填`parent=App`
    @classmethod
    def get_instance(self) -> int:
        """
        获取实例的数量

        :return: 示例数量
        """

        if self._instance is None:
            raise RuntimeError("App not initialized")
        return self._instance

    def init_glfw(self) -> None:
        """
        初始化glfw库

        :return: None
        """

        import glfw
        if not glfw.init():
            raise RuntimeError('glfw.init() failed')
        # 设置全局GLFW配置
        glfw.window_hint(glfw.STENCIL_BITS, 8)

    from .window import Window

    def add_window(self, window: Window) -> "Application":
        """
        添加窗口

        :param window: 窗口
        :return self
        """
        self.windows.append(window)
        # 将窗口的GLFW初始化委托给Application
        window.set_application(self)
        return self

    def run(self) -> None:
        """
        运行应用程序

        :return: None
        """
        import glfw
        if not self.windows:
            raise RuntimeError('至少需要添加一个窗口才能运行应用程序')

        self.running = True
        for window in self.windows:
            window.create_bind()

        # 主事件循环
        while self.running and not any(glfw.window_should_close(win.winfo_glfw_window()) for win in self.windows):
            glfw.poll_events()

            for window in self.windows:
                if window.visible():
                    with window.skia_surface(window.winfo_glfw_window()) as surface:
                        with surface as canvas:
                            if hasattr(window, 'draw_func') and window.draw_func:
                                window.draw_func(canvas)
                        surface.flushAndSubmit()
                    glfw.swap_buffers(window.winfo_glfw_window())

        self.cleanup()

    def cleanup(self) -> None:
        """
        清理资源

        :return: None
        """
        import glfw
        for window in self.windows:
            glfw.destroy_window(window.winfo_glfw_window())
        glfw.terminate()
        self.running = False

    def quit(self) -> None:
        """
        退出应用程序

        :return None
        """
        self.running = False