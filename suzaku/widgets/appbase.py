def init_glfw() -> None:
    """Initialize GLFW module."""
    import glfw
    if not glfw.init():
        raise RuntimeError('glfw.init() failed')
    # 设置全局GLFW配置
    glfw.window_hint(glfw.STENCIL_BITS, 8)


class SkAppBase:

    """
    SkAppBase
    """

    _instance = None

    def __init__(self, window_event_wait: bool = False) -> None:
        """
        SkAppBase.

        应用程式。
        """

        self.windows = []
        self.window_event_wait = window_event_wait
        self.running = False
        init_glfw()
        if SkAppBase._instance is not None:
            raise RuntimeError("App is a singleton, use App.get_instance()")
        SkAppBase._instance = self

    # 这里用这个可以使`SkWindowBase`的初始化更加简单，可以不选择填`parent=App`
    @classmethod
    def get_instance(cls) -> int:
        """Get instance count."""
        if cls._instance is None:
            raise RuntimeError("App not initialized")
        return cls._instance

    from .windowbase import SkWindowBase

    def add_window(self, window: SkWindowBase) -> "SkAppBase":
        """Add a window.

        * `window`: The window
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
            if self.window_event_wait:
                glfw.wait_events()
            else:
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
        """Clean up resources."""
        import glfw
        for window in self.windows:
            glfw.destroy_window(window.glfw_window)
        glfw.terminate()
        self.running = False

    def quit(self) -> None:
        """Quit application."""
        self.running = False
        self.running = False