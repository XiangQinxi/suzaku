import typing
import warnings

import glfw
import skia

from ..event import SkEvent, SkEventHanding
from ..misc import SkMisc


class SkAppInitError(Exception):
    """Exception when GLFW initialization fails."""

    pass


class SkAppNotFoundWindow(Warning):
    """Warning when no window is found."""

    pass


def init_glfw() -> None:
    """Initialize GLFW module.

    :raises SkAppInitError:
        If GLFW initialization fails
    """
    if not glfw.init():
        raise SkAppInitError("glfw.init() failed")
    # 设置全局GLFW配置
    glfw.window_hint(glfw.STENCIL_BITS, 8)
    glfw.window_hint(glfw.TRANSPARENT_FRAMEBUFFER, True)
    glfw.window_hint(glfw.WIN32_KEYBOARD_MENU, True)
    glfw.window_hint(glfw.COCOA_RETINA_FRAMEBUFFER, True)


def init_sdl2() -> None:
    """Initialize SDL2 module.

    :raises SkAppInitError:
        If SDL2 initialization fails
    """
    import ctypes
    import sys

    import sdl2dll  # 导入pysdl2-dll
    from sdl2 import SDL_INIT_VIDEO, SDL_Init  # 导入pysdl2
    from sdl2.sdlimage import IMG_INIT_JPG, IMG_Init  # 加载图片需要，否则只能加载BMP

    SDL_Init(SDL_INIT_VIDEO)
    IMG_Init(IMG_INIT_JPG)


class SkAppBase(SkEventHanding, SkMisc):
    """Base Application class.

    >>> app = SkAppBase()
    >>> window = SkWindowBase()
    >>> app.run()

    :param bool is_always_update:
        Whether to continuously refresh (if `False`, refresh only when a window event is triggered).
        【是否一直刷新（如果为False，则只有触发窗口事件时才刷新）】
    :param bool is_get_context_on_focus:
        Is the context only obtained when the window gains focus.
        【是否只有在窗口获得焦点时，获得上下文】
    """

    _instance = None  # 实例过SkAppBase

    # region __init__ 初始化

    def __init__(
        self,
        *,
        is_always_update: bool = False,
        is_get_context_on_focus: bool = True,
        framework: typing.Literal["glfw", "sdl2"] = "glfw",
        vsync: bool = True,
        samples: int = 4,
    ) -> None:
        super().__init__()
        from .windowbase import SkWindowBase

        self.windows: list[SkWindowBase] = (
            []
        )  # Windows that have been added to the event loop. 【被添加进事件循环的SkWindow】
        self.is_always_update: bool | typing.Literal["auto"] = is_always_update
        self.is_get_context_on_focus: bool = is_get_context_on_focus
        self.vsync = vsync
        self.samples = samples
        self.alive: bool = (
            False  # Is the program currently running. 【程序是否正在运行】
        )

        SkAppBase.default_application = self

        self.framework = framework
        match framework:
            case "glfw":
                init_glfw()
            case "sdl2":
                init_sdl2()

        if SkAppBase._instance is not None:
            raise RuntimeError("App is a singleton, use App.get_instance()")
        SkAppBase._instance = self

    @classmethod
    def get_instance(cls) -> int:
        """Get the instance of the application. 【获取SkAppBase实例】"""
        if cls._instance is None:
            raise SkAppInitError("App not initialized")
        return cls._instance

    # endregion

    # region add_window 添加窗口
    def add_window(self, window) -> typing.Self:
        """Add the window to the event loop
        (normally SkWindow automatically adds it during initialization).
        【添加窗口进入事件循环（一般情况下SkWindow初始化时就会自动添加）】

        :param SkWindowBase window: The window

        >>> app = SkAppBase()
        >>> win = SkWindowBase(app)
        >>> app.add_window(window)

        """

        self.windows.append(window)
        # 将窗口的GLFW初始化委托给Application
        return self

    # endregion

    # region about mainloop 事件循环相关
    def run(self) -> None:
        """Run the program (i.e., start the event loop).
        【运行程序（即开始事件循环）】

        :return:
        """

        if not self.windows:
            warnings.warn(
                "At least one window is required to run application!",
                SkAppNotFoundWindow,
            )

        match self.framework:
            case "glfw":
                glfw.window_hint(glfw.SAMPLES, self.samples)
                glfw.set_error_callback(self.error)

                if self.is_always_update:
                    deal_event = glfw.poll_events
                else:
                    deal_event = lambda: glfw.wait_events_timeout(0.5)
            case "sdl2":
                from sdl2 import SDL_PollEvent

                deal_event = SDL_PollEvent
            case _:
                raise SkAppInitError(f"Unknown framework {self.framework}")

        self.alive = True
        for window in self.windows:
            window.create_bind()

        # Start event loop
        # 【开始事件循环】
        while self.alive and self.windows:
            # 处理事件
            deal_event()

            # 检查after事件，其中的事件是否到达时间，如到达则执行
            if self._afters:
                for item, config in tuple(self._afters.items()):
                    if config[0] <= self.time():  # Time
                        config[1]()  # Function
                        if config[2]:  # Is Post
                            self.post()
                        del self._afters[item]

            # Create a copy of the window tuple to avoid modifying it while iterating
            # 【创建窗口副本，避免在迭代时修改窗口列表】
            current_windows = set(self.windows)
            for window in current_windows:
                # Make sure the window is created and bound
                # 【确保新窗口绑定事件】
                window.create_bind()
                # Draw window
                # 【绘制窗口】
                if (
                    self.is_get_context_on_focus
                ):  # Only draw the window that has gained focus.
                    if glfw.get_window_attrib(window.glfw_window, glfw.FOCUSED):
                        window.draw()
                else:
                    if glfw.get_window_attrib(window.glfw_window, glfw.VISIBLE):
                        window.draw()
                # Check if the window is valid
                # 【检查窗口是否有效】
                if window.can_be_close():
                    window.event_trigger(
                        "delete_window",
                        SkEvent(event_type="delete_window", window=window),
                    )
                    # print(window.id)
                    if window.can_be_close():
                        glfw.destroy_window(window.glfw_window)
                        window.draw_func = None
                        window.glfw_window = None  # Clear the reference
                        for child in window.children:
                            child.destroy()
                        self.destroy_window(window)
                        del window
                        continue
            del current_windows
            if glfw.get_current_context():
                glfw.swap_interval(1 if self.vsync else 0)  # 是否启用垂直同步

        self.cleanup()  # 【清理资源】

    mainloop = run

    def destroy_window(self, window):
        window.event_trigger("closed", SkEvent(event_type="closed", window=window))
        self.windows.remove(window)

    def cleanup(self) -> None:
        """Clean up resources.【清理资源】"""
        for window in self.windows:
            glfw.destroy_window(window.glfw_window)
        glfw.terminate()
        self.quit()

    def quit(self) -> None:
        """Quit application.【退出应用】"""
        self.alive = False

    # endregion
    # region error 错误处理
    @staticmethod
    def error(error_code: typing.Any, description: bytes):
        """
        处理GLFW错误

        :param error_code: 错误码
        :param description: 错误信息
        :return: None
        """
        print(f"GLFW Error {error_code}: {description.decode()}")

    # endregion
