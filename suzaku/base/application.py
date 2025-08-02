class Application:

    """
    应用程序
    """

    _instance = None

    def __init__(self) -> None:
        """
        Application.

        应用程式。
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
        Get instance count.

        获取实例的数量。

        Returns:
            self._instance (int): 实例数量
        """

        if self._instance is None:
            raise RuntimeError("App not initialized")
        return self._instance

    def init_glfw(self) -> None:
        """
        Initialize GLFW module.

        初始化glfw库。

        Returns:
            None
        """

        import glfw
        if not glfw.init():
            raise RuntimeError('glfw.init() failed')
        # 设置全局GLFW配置
        glfw.window_hint(glfw.STENCIL_BITS, 8)

    from .window import Window

    def add_window(self, window: Window) -> "Application":
        """
        Add a window.

        添加窗口。

        Args:
            window (Window): 
                The window.

                窗口

        Returns:
            self
        """
        self.windows.append(window)
        # 将窗口的GLFW初始化委托给Application
        return self

    # 修改Application类的run方法
    def run(self) -> None:
        import glfw
        if not self.windows:
            raise RuntimeError('At least one window is required to run application!')

        self.running = True
        for window in self.windows:
            window.create_bind()

        # 主事件循环
        while self.running and self.windows:
            glfw.poll_events()

            # 创建窗口列表副本避免迭代时修改
            current_windows = list(self.windows)

            for window in current_windows:
                # 检查窗口有效性
                if not window.glfw_window or glfw.window_should_close(window.glfw_window):
                    window.destroy()
                    self.windows.remove(window)
                    continue

                # 仅绘制可见窗口
                if window.visible:
                    # 为每个窗口设置当前上下文
                    glfw.make_context_current(window.glfw_window)
                    with window.skia_surface(window.glfw_window) as surface:
                        if surface:
                            with surface as canvas:
                                if hasattr(window, 'draw_func') and window.draw_func:
                                    window.draw_func(canvas)
                            surface.flushAndSubmit()
                            glfw.swap_buffers(window.glfw_window)

        self.cleanup()

    def cleanup(self) -> None:
        """
        Clean up resources.

        清理资源。

        Returns:
            None
        """
        import glfw
        for window in self.windows:
            glfw.destroy_window(window.glfw_window)
        glfw.terminate()
        self.running = False

    def quit(self) -> None:
        """
        Quit application.

        退出应用程序。

        Returns:
            None
        """
        self.running = False
        self.running = False