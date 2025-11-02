import typing
import warnings

import glfw
import skia

from ..event import SkEvent, SkEventHandling
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

    # I don't think OpenGL works here
    # 设置全局GLFW、OpenGL配置

    # import OpenGL

    # OpenGL.ERROR_CHECKING = False

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

    from sdl2 import (
        SDL_GL_CONTEXT_MAJOR_VERSION,
        SDL_GL_CONTEXT_MINOR_VERSION,
        SDL_GL_CONTEXT_PROFILE_MASK,
        SDL_GL_SetAttribute,
    )

    SDL_GL_SetAttribute(SDL_GL_CONTEXT_MAJOR_VERSION, 3)
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_MINOR_VERSION, 3)
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_PROFILE_MASK, 0x0001)  # SDL_GL_CONTEXT_PROFILE_CORE


class SkAppBase(SkEventHandling, SkMisc):
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

        self._event = None
        self.windows: list[SkWindowBase] = (
            []
        )  # Windows that have been added to the event loop. 【被添加进事件循环的SkWindow】
        self.is_always_update: bool | typing.Literal["auto"] = is_always_update
        self.is_get_context_on_focus: bool = is_get_context_on_focus
        self.vsync = vsync
        self.samples = samples
        self.alive: bool = False  # Is the program currently running. 【程序是否正在运行】

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
        """Get the instance of the application."""
        if cls._instance is None:
            raise SkAppInitError("App not initialized")
        return cls._instance

    # endregion

    # region add_window 添加窗口
    def add_window(self, window) -> typing.Self:
        """Add the window to the event loop
        (normally SkWindow automatically adds it during initialization).

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

    def update(self) -> None:
        """Update all windows.

        :param bool redraw: Whether to redraw the window.
        """
        from glfw import poll_events, wait_events

        input_mode: bool = False

        # poll_events()

        for window in self.windows:
            if window.visible and window.alive:
                window.update()
                if window.mode == "input":
                    input_mode = True
                if glfw.get_current_context():
                    glfw.swap_interval(1 if self.vsync else 0)  # 是否启用垂直同步

        if input_mode:
            poll_events()
        else:
            wait_events()

    def run(self) -> None:
        """Run the program (i.e., start the event loop).

        :return:
        """
        self.alive = True

        if not self.windows:
            warnings.warn(
                "At least one window is required to run application!",
                SkAppNotFoundWindow,
            )

        match self.framework:
            case "glfw":
                glfw.window_hint(glfw.SAMPLES, self.samples)
                glfw.set_error_callback(self.error)

        while self.alive:
            if not self.windows:
                self.alive = False
                break
            for window in self.windows:
                if window.can_be_close():
                    window.destroy()

            self.update()

        self.cleanup()

    mainloop = run

    def destroy_window(self, window):
        self.windows.remove(window)

    def cleanup(self) -> None:
        """Clean up resources."""
        match self.framework:
            case "glfw":
                for window in self.windows:
                    glfw.destroy_window(window.the_window)
                glfw.terminate()
            case "sdl2":
                import sdl2

                sdl2.SDL_Quit()
            case _:
                raise SkAppInitError(f"Unknown framework {self.framework}")
        self.quit()

    def quit(self) -> None:
        """Quit application."""
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
