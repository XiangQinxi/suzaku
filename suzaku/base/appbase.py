import warnings

import glfw


class SkAppInitError(Exception):
    """Exception when GLFW initialization fails."""

    pass


class SkAppNotFoundWindow(Warning):
    """Warning when no window is found."""

    pass


def init_glfw() -> None:
    """Initialize GLFW module."""
    if not glfw.init():
        raise SkAppInitError("glfw.init() failed")
    # 设置全局GLFW配置
    glfw.window_hint(glfw.STENCIL_BITS, 8)


class SkAppBase:

    _instance = None

    # region __init__ 初始化

    def __init__(self, window_event_wait: bool = False) -> None:
        """Base Application class.

        :param window_event_wait: Whether to wait for window events
        """

        from .windowbase import SkWindowBase

        self.windows: list[SkWindowBase] = []
        self.window_event_wait: bool = window_event_wait
        self.running: bool = False
        init_glfw()
        if SkAppBase._instance is not None:
            raise RuntimeError("App is a singleton, use App.get_instance()")
        SkAppBase._instance = self

    # 这里用这个可以使`SkWindowBase`的初始化更加简单，可以不选择填`parent=App`
    @classmethod
    def get_instance(cls) -> int:
        """Get instance count."""
        if cls._instance is None:
            raise SkAppInitError("App not initialized")
        return cls._instance

    # endregion

    # region add_window 添加窗口
    def add_window(self, window) -> "SkAppBase":
        """Add a window.

        :param window: The window
        """

        self.windows.append(window)
        # 将窗口的GLFW初始化委托给Application
        return self

    # endregion

    # region about mainloop 事件循环相关
    def run(self) -> None:
        """Run the application."""
        if not self.windows:
            warnings.warn(
                "At least one window is required to run application!",
                SkAppNotFoundWindow,
            )
        self.running = True
        for window in self.windows:
            window.create_bind()

        glfw.swap_interval(1)

        # Event loop
        if self.window_event_wait:
            deal_event = glfw.wait_events
        else:
            deal_event = glfw.poll_events
        while self.running and self.windows:
            deal_event()

            # Create a copy of the window list to avoid modifying it while iterating
            current_windows = self.windows

            for window in current_windows:
                # Check if the window is valid
                if not window.glfw_window or glfw.window_should_close(
                    window.glfw_window
                ):
                    window.destroy()
                    self.windows.remove(window)
                    continue

                # Only draw visible windows
                if window.visible and glfw.get_window_attrib(window.glfw_window, glfw.FOCUSED):
                    # Set the current context for each window
                    glfw.make_context_current(window.glfw_window)
                    with window.skia_surface(window.glfw_window) as surface:
                        if surface:
                            with surface as canvas:
                                if hasattr(window, "draw_func") and window.draw_func:
                                    window.draw_func(canvas)
                            surface.flushAndSubmit()
                            glfw.swap_buffers(window.glfw_window)

        self.cleanup()

    def cleanup(self) -> None:
        """Clean up resources."""
        for window in self.windows:
            glfw.destroy_window(window.glfw_window)
        glfw.terminate()
        self.running = False

    def quit(self) -> None:
        """Quit application."""
        self.running = False

    # endregion
