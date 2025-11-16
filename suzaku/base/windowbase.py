import contextlib
import os
import os.path
import sys
import typing
import warnings

import glfw
import skia

from ..event import SkEvent, SkEventHandling
from ..misc import SkMisc
from . import SkAppBase


class _GLFW_IMAGE:
    def __init__(self, path: str):
        self.path = path
        self.image: skia.Image = skia.Image.open(fp=self.path)
        self.image.convert()

    @property
    def size(self):
        return self.image.width(), self.image.height()

    def convert(self):
        self.image.convert(colorType=skia.ColorType.kRGBA_8888_ColorType)


class SkWindowBase(SkEventHandling, SkMisc):
    """Base Window class

    Example:
    >>> window = SkWindowBase()

    :param parent:
        Window parent class (if a window class is specified,
        the child window will close when the parent window closes)
    :param title: Window title
    :param size: Window size
    :param fullscreen: Window fullscreen
    :param opacity: Window opacity
    :param border: Whether it has border and titlebar
    """

    _instance_count = 0

    # region __init__ 初始化

    def __init__(
        self,
        parent: SkAppBase | None = None,
        *,
        title: str = "suzaku",
        size: tuple[int, int] = (300, 300),
        fullscreen=False,
        opacity: float = 1.0,
        minsize: tuple[int, int] = (80, 80),
        force_hardware_acceleration: bool = False,
    ):
        # glfw.default_window_hints()

        self.id = self.__class__.__name__ + str(self._instance_count + 1)
        self.children = []

        SkEventHandling.__init__(self)
        self.parent: SkAppBase | typing.Self | int = (
            parent if parent is not None else SkAppBase.get_instance()
        )
        if self.parent is None:
            raise ValueError("parent must be not None")
        if isinstance(self.parent, SkAppBase):  # parent=SkAppBase
            self.application = self.parent
            self.parent.add_window(self)
        elif isinstance(self.parent, SkWindowBase):  # parent=SkWindowBase
            self.application = self.parent.application
            self.parent.application.add_window(self)

            def _closed(_):
                if self.the_window:
                    self.destroy()

            self.parent.bind("closed", _closed)
        else:
            raise TypeError("parent must be SkAppBase or SkWindowBase")
        self.framework = self.parent.framework

        self._event_init = False  #
        self._cursor = None
        self.cursors = {}
        self.mode: typing.Literal["normal", "input"] = "normal"

        # Always is 0
        self.x: int | float = 0
        self.y: int | float = 0
        self.canvas_x: int | float = 0
        self.canvas_y: int | float = 0
        # Window position
        self.root_x: int | float = 0
        self.root_y: int | float = 0
        # Window size
        self.width: int | float = size[0]
        self.height: int | float = size[1]

        self.button = -1

        # 添加DPI相关属性
        self.dpi_scale = 1.0
        self.physical_width = size[0]
        self.physical_height = size[1]

        self.the_window = None
        self.visible = False
        self.mouse_x = 0
        self.mouse_y = 0
        self.mouse_rootx = 0
        self.mouse_rooty = 0

        self.focus = True

        self.attributes = {
            "title": title,
            "opacity": opacity,
            "cursor": "arrow",  # default cursor
            "force_hardware_acceleration": force_hardware_acceleration,
            "minsize": minsize,
        }

        [
            self.EVENT_TYPES.append(event_type)
            for event_type in [
                "drop",
                "maximize",
                "iconify",
                "dpi_change",
                "delete_window",
                "closed",
                "move",
            ]
        ]

        buttons = [
            "button1",
            "button2",
            "button3",
            "b1",
            "b2",
            "b3",
        ]  # Left Right Middle
        button_states = ["press", "release", "motion", "move"]

        for button in buttons:
            for state in button_states:
                self.trigger(f"button_{state}[{button}]")

        SkWindowBase._instance_count += 1

        self.draw_func = None
        self.context = None
        self.surface = None
        self.attributes["fullscreen"] = fullscreen
        self.is_mouse_floating = False
        self.is_mouse_press = False

        if self.width <= 0 or self.height <= 0:
            raise ValueError("The window size must be positive")

        ####################

        self.the_window = self.create()
        self.alive = True
        self.create_bind()

        # self.cursor(self.default_cursor())

        self.icon1_path = os.path.abspath(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "..",
                "resources",
                "imgs",
                "icon.ico",
            )
        )

        self.attributes["iconpath"] = self.icon1_path

        self.wm_iconpath(self.icon1_path)
        # icon: skia.Image = skia.Image.open(self.icon1_path)

        # info = skia.ImageInfo.MakeN32Premul(icon.width(), icon.height())
        # pixels = bytearray(icon.width() * icon.height() * 4)
        # print(pixels)

        # self.icon = (
        #     icon.width(),
        #     icon.height(),
        #     pixels,
        # )

        # glfw.set_window_icon(self.the_window, 1, self.icon)

    @classmethod
    def get_instance_count(cls) -> int:
        """Get instance count.

        >>> print(SkWindowBase.get_instance_count())

        :return: Instance count
        """
        return cls._instance_count

    def create(self) -> typing.Any:
        """Create the glfw window.

        :return: cls
        """

        if hasattr(self, "application") and self.application:
            match self.framework:
                case "glfw":
                    if self.cget("fullscreen"):
                        monitor = glfw.get_primary_monitor()
                    else:
                        monitor = None

                    glfw.window_hint(
                        glfw.CONTEXT_RELEASE_BEHAVIOR, glfw.RELEASE_BEHAVIOR_NONE
                    )  # mystery optimize
                    glfw.window_hint(glfw.STENCIL_BITS, 8)
                    glfw.window_hint(glfw.COCOA_RETINA_FRAMEBUFFER, glfw.TRUE)  # macOS
                    glfw.window_hint(glfw.SCALE_TO_MONITOR, glfw.TRUE)  # Windows/Linux

                    # see https://www.glfw.org/faq#macos
                    if sys.platform.startswith("darwin"):
                        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
                        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 2)
                        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)
                        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
                    else:
                        if self.cget("force_hardware_acceleration"):
                            glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)
                            glfw.window_hint(glfw.CLIENT_API, glfw.OPENGL_API)
                            glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
                            glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
                            glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

                    window = glfw.create_window(
                        self.width, self.height, self.cget("title"), monitor, None
                    )
                    if not window:
                        raise RuntimeError("无法创建GLFW窗口")

                    self.visible = True

                    pos = glfw.get_window_pos(window)

                    self.root_x = pos[0]
                    self.root_y = pos[1]

                    glfw.set_window_opacity(window, self.cget("opacity"))

                    # _glfw.glfwSetWindowIcon(window, 1, [self.icon1])

                    # 初始化DPI缩放
                    if monitor:
                        self._update_dpi_scale()
                case "sdl2":
                    import sdl2

                    window = sdl2.SDL_CreateWindow(
                        self.cget("title").encode("utf-8"),
                        sdl2.SDL_WINDOWPOS_CENTERED,
                        sdl2.SDL_WINDOWPOS_CENTERED,
                        self.width,
                        self.height,
                        sdl2.SDL_WINDOW_OPENGL | sdl2.SDL_WINDOW_SHOWN | sdl2.SDL_WINDOW_RESIZABLE,
                    )

                    self.visible = True
            return window
        else:
            raise RuntimeError("The window must be added to the Application instance first")

    def create_bind(self) -> None:
        """Binding glfw window events.

        :return: None
        """
        if not self._event_init:
            window = self.the_window
            match self.framework:
                case "glfw":
                    glfw.make_context_current(window)
                    glfw.set_window_size_callback(window, self._on_resizing)
                    glfw.set_framebuffer_size_callback(window, self._on_framebuffer_size)
                    glfw.set_window_close_callback(window, self._on_closed)
                    glfw.set_mouse_button_callback(window, self._on_mouse_button)
                    glfw.set_cursor_enter_callback(window, self._on_cursor_enter)
                    glfw.set_cursor_pos_callback(window, self._on_cursor_pos)
                    glfw.set_window_pos_callback(window, self._on_window_pos)
                    glfw.set_window_focus_callback(window, self._on_focus)
                    glfw.set_key_callback(window, self._on_key)
                    glfw.set_char_callback(window, self._on_char)
                    glfw.set_window_refresh_callback(window, self._on_refresh)
                    glfw.set_window_maximize_callback(window, self._on_maximize)
                    glfw.set_drop_callback(window, self._on_drop)
                    glfw.set_window_iconify_callback(window, self._on_iconify)
                    glfw.set_scroll_callback(window, self._on_scroll)
                    glfw.set_window_content_scale_callback(window, self._on_dpi_change)
                case "sdl2":
                    print("TODO: implement sdl2 `create_bind`")
            self._event_init = True

    # endregion

    # region Draw 绘制相关

    def update(self, redraw: bool = False) -> None:
        """Update window.

        :param bool redraw: Whether to redraw the window.
        """
        if self.visible:
            self.trigger("update", SkEvent(event_type="update"))

            if self.mode == "input" or redraw:
                self.draw()
            else:
                if all([not child.need_redraw for child in self.children]):
                    return
                self.draw()
            # self.update_layout: typing.Callable
            # self.post()

    @contextlib.contextmanager
    def skia_surface(self, arg: typing.Any) -> skia.Surface:
        """Create a Skia surface for the window.

        :param arg: GLFW or SDL2 Window/Surface
        :return: Skia Surface
        """
        match self.framework:
            case "glfw":
                from OpenGL import GL

                if not glfw.get_current_context() or glfw.window_should_close(arg):
                    yield None
                    return

                self.context = skia.GrDirectContext.MakeGL()
                fb_width, fb_height = glfw.get_framebuffer_size(arg)
                backend_render_target = skia.GrBackendRenderTarget(
                    fb_width, fb_height, 0, 0, skia.GrGLFramebufferInfo(0, GL.GL_RGBA8)
                )
                surface: skia.Surface = skia.Surface.MakeFromBackendRenderTarget(
                    self.context,
                    backend_render_target,
                    skia.kBottomLeft_GrSurfaceOrigin,
                    skia.kRGBA_8888_ColorType,
                    skia.ColorSpace.MakeSRGB(),
                )
                self.context.setResourceCacheLimit(16 * 1024 * 1024)

                if surface is None:
                    raise RuntimeError("Failed to create Skia surface")

                yield surface

            case "sdl2":
                import ctypes

                import sdl2

                width, height = arg.w, arg.h
                pixels_ptr = arg.pixels
                pitch = arg.pitch

                # SDL 像素包装成 buffer
                buf_type = ctypes.c_uint8 * (pitch * height)
                buf = buf_type.from_address(pixels_ptr)

                imageinfo = skia.ImageInfo.MakeN32Premul(width, height)
                surface = skia.Surface.MakeRasterDirect(imageinfo, buf, pitch)

                if surface is None:
                    raise RuntimeError("Failed to create Skia surface")

                yield surface  # ⚠️ 必须用 yield，不要 return

    def draw(self, event: SkEvent = None) -> None:
        if self.visible:
            # Set the current context for each arg
            # 【为该窗口设置当前上下文】
            match self.framework:
                case "glfw":
                    glfw.make_context_current(self.the_window)

                    # Create a Surface and hand it over to this arg.
                    # 【创建Surface，交给该窗口】
                    with self.skia_surface(self.the_window) as self.surface:
                        if self.surface:
                            with self.surface as canvas:
                                # Determine and call the drawing function of this arg.
                                # 【判断并调用该窗口的绘制函数】
                                if self.draw_func:
                                    self.draw_func(canvas)

                            self.surface.flushAndSubmit()
                            self.trigger(
                                "redrawing", SkEvent(self, "redrawing", surface=self.surface)
                            )

                    glfw.swap_buffers(self.the_window)
                case "sdl2":
                    import sdl2

                    surface = sdl2.SDL_GetWindowSurface(self.the_window).contents

                    with self.skia_surface(surface) as sk_surface:
                        if sk_surface:
                            with sk_surface as canvas:
                                if self.draw_func:
                                    self.draw_func(canvas)

                    sdl2.SDL_UpdateWindowSurface(self.the_window)
        if self.context:
            self.context.freeGpuResources()
            self.context.releaseResourcesAndAbandonContext()
        for child in self.children:
            child.need_redraw = False
        self.trigger("redraw", SkEvent(self, "redraw"))

    def save(self, path: str = "snapshot.png", _format: str = "png"):
        """Save a snapshot of the window.

        :param path: Path to save the snapshot
        :param _format: Format of the snapshot, default is "png"
        :return: Whether the snapshot is saved successfully
        """
        if _format == "png":
            _format = skia.kPNG
        elif _format == "jpg":
            _format = skia.kJPEG
        elif _format == "webp":
            _format = skia.kWEBP

        self.image_snapshot = None

        def _(evt):
            self.image_snapshot = evt["surface"].makeImageSnapshot()
            if self.surface:
                snapshot = self.surface.makeImageSnapshot()
                if snapshot:
                    return snapshot.save(path, _format)
                else:
                    warnings.warn("Cannot save snapshot")
            else:
                warnings.warn("No surface to save")
            return None

        task_id = self.bind("redrawing", _)
        self.draw(None)
        self.unbind(task_id)

    snapshot = save

    def set_draw_func(self, func: typing.Callable) -> "SkWindowBase":
        """Set the draw function.

        :param func: Draw function
        :return: cls
        """
        self.draw_func = func
        return self

    # endregion

    # region Event handling 事件处理

    def can_be_close(self, value: bool | None = None) -> typing.Self | bool:
        """Set whether the window can be closed.

        Prevent users from closing the window, which can be used in conjunction with prompts like "Save before closing?"

        >>> def delete(_: SkEvent):
        >>>     window.can_be_close(False)
        >>> window.bind("delete_window", delete)


        :param value: Whether the window can be closed
        :return: None
        """
        if value is not None:
            glfw.set_window_should_close(self.the_window, value)
            return self
        else:
            if self.the_window:
                return glfw.window_should_close(self.the_window)
            else:
                return False

    def _on_char(self, window: typing.Any, char: int) -> None:
        """Trigger text input event

        :param window: GLFW Window
        :param char: Unicode character
        """

        self.trigger("char", SkEvent(event_type="char", char=chr(char), glfw_window=window))
        self.update()
        # self.update(redraw=True)

    def _on_key(self, window: typing.Any, key: str, scancode: str, action: str, mods: int) -> None:
        """
        触发键盘事件

        :param window: GLFW Window
        :param key: Key
        :param scancode: Scan code
        :param action: Action
        :param mods: Modifiers
        """
        from glfw import PRESS, RELEASE, REPEAT, get_key_name

        keyname: str = get_key_name(
            key, scancode
        )  # 获取对应的键名，不同平台scancode不同，因此需要输入scancode来正确转换。有些按键不具备键名
        # print(self.mods_name(mods))
        # 我真尼玛服了啊，改了半天，发现delete键获取不到键名，卡了我半天啊

        if action == PRESS:
            name = "key_press"
        elif action == RELEASE:
            name = "key_release"
        elif action == REPEAT:
            name = "key_repeat"
        else:
            name = "key"
        self.ime(100, 1000)
        self.trigger(
            name,
            SkEvent(
                event_type=name,
                key=key,
                keyname=keyname,
                mods=self.mods_name(mods),
                mods_key=mods,
                glfw_window=window,
            ),
        )
        self.update()

    def _on_focus(self, window, focused) -> None:
        """Triggers the focus event (triggered when the window gains or loses focus).

        :param window: GLFW Window
        :param focused: Focused
        :return: None
        """
        if focused:
            self.configure(focus=True)
            self.trigger("focus_gain", SkEvent(event_type="focus_gain", glfw_window=window))
            self.update(redraw=True)
        else:
            self.configure(focus=False)
            self.trigger("focus_loss", SkEvent(event_type="focus_loss", glfw_window=window))

    def _on_refresh(self, window: typing.Any):
        self.update(True)

    def _on_scroll(self, window, x_offset, y_offset):
        """Trigger scroll event (triggered when the mouse scroll wheel is scrolled).

        :param window: GLFW Window
        :param x_offset: X offset
        :param y_offset: Y offset
        :return: None
        """
        self.trigger(
            "scroll",
            SkEvent(
                event_type="scroll",
                x_offset=x_offset,
                y_offset=y_offset,
                glfw_window=window,
            ),
        )

    def _on_framebuffer_size(self, window: typing.Any, width: int, height: int) -> None:
        self.update()

    def _on_resizing(self, window, width: int, height: int) -> None:
        """Trigger resize event (triggered when the window size changes).

        :param window: GLFW Window
        :param width: Window width
        :param height: Window height
        :return: None
        """
        # GL.glViewport(0, 0, width, height)
        self._on_framebuffer_size(window, width, height)
        self.width = width
        self.height = height

        # 更新物理尺寸
        self.physical_width = int(width * self.dpi_scale)
        self.physical_height = int(height * self.dpi_scale)

        event = SkEvent(event_type="resize", width=width, height=height, dpi_scale=self.dpi_scale)
        self.trigger("resize", event)
        for child in self.children:
            child.trigger("resize", event)
        self.update(True)
        # cls.update()

    def _on_window_pos(self, window: typing.Any, x: int, y: int) -> None:
        """Trigger move event (triggered when the window position changes).

        :param window: GLFW Window
        :param x: Window X position
        :param y: Window Y position
        :return: None
        """
        self.root_x = x
        self.root_y = y
        self.trigger("move", SkEvent(event_type="move", x=x, y=y, glfw_window=window))

    def _on_closed(self, window: typing.Any) -> None:
        """Trigger closed event (triggered when the window is closed).
        (Note: This method is deprecated. Triggering the closed event has been delegated to the destroy method.)
        :param window: GLFW Window
        :return: None
        """
        # self.trigger("closed", SkEvent(event_type="closed", the_window=window))

    def _on_mouse_button(
        self,
        window: typing.Any,
        button: typing.Literal[0, 1, 2],
        is_press: bool,
        mods: int,
    ) -> None:
        """Trigger mouse button event (triggered when the mouse button is press or release).

        :param window: GLFW Window
        :param int button: Button
        :param is_press: Whether press
        :param mods: Modifiers
        :return: None
        """
        # print(arg1, arg2)

        self.mouse_x, self.mouse_y = self.mouse_pos()
        self.mouse_rootx, self.mouse_rooty = self.mouse_root_pos()

        if is_press:
            self.is_mouse_press = True
            state = "press"
        else:
            self.is_mouse_press = False
            state = "release"
            self.button = -1

        names = [
            f"mouse_{state}",
            f"mouse_{state}[button{button+1}]",
            f"mouse_{state}[b{button+1}]",
        ]

        self.button = button

        for name in names:
            self.trigger(
                name,
                SkEvent(
                    event_type=name,
                    x=self.mouse_x,
                    y=self.mouse_y,
                    rootx=self.mouse_rootx,
                    rooty=self.mouse_rooty,
                    button=button,
                    mods=self.mods_name(mods),
                ),
            )

    def _on_cursor_enter(self, window: typing.Any, is_enter: bool) -> None:
        """Trigger mouse enter event (triggered when the mouse enters the window) or mouse leave event (triggered when the mouse leaves the window).

        :param window: GLFW Window
        :param is_enter: Whether entered
        :return: None
        """
        self.mouse_x, self.mouse_y = self.mouse_pos()
        self.mouse_rootx, self.mouse_rooty = self.mouse_root_pos()

        if is_enter:
            self.is_mouse_floating = True
            self.trigger(
                "mouse_enter",
                SkEvent(
                    event_type="mouse_enter",
                    x=self.mouse_x,
                    y=self.mouse_y,
                    rootx=self.mouse_rootx,
                    rooty=self.mouse_rooty,
                ),
            )
        else:
            self.is_mouse_floating = False
            self.trigger(
                "mouse_leave",
                SkEvent(
                    event_type="mouse_leave",
                    x=self.mouse_x,
                    y=self.mouse_y,
                    rootx=self.mouse_rootx,
                    rooty=self.mouse_rooty,
                ),
            )

    def _on_cursor_pos(self, window: typing.Any, x: int, y: int) -> None:
        """Trigger mouse motion event (triggered when the mouse enters the window and moves).

        :param window: GLFW Window
        :param x: Mouse X position
        :param y: Mouse Y position
        :return: None
        """

        self.mouse_x = x
        self.mouse_y = y
        window_pos = self.window_pos()
        self.mouse_rootx = x + window_pos[0]
        self.mouse_rooty = y + window_pos[1]

        button = self.button
        if button >= 0:
            names = [
                "mouse_motion",
                f"mouse_motion[button{button+1}]",
                f"mouse_motion[b{button+1}]",
            ]

            for name in names:
                self.trigger(
                    name,
                    SkEvent(
                        event_type=name,
                        x=self.mouse_x,
                        y=self.mouse_y,
                        rootx=self.mouse_rootx,
                        rooty=self.mouse_rooty,
                        glfw_window=window,
                    ),
                )
        self.trigger(
            "mouse_move",
            SkEvent(
                event_type="mouse_move",
                x=self.mouse_x,
                y=self.mouse_y,
                rootx=self.mouse_rootx,
                rooty=self.mouse_rooty,
                glfw_window=window,
            ),
        )

    def _on_maximize(self, window, maximized: bool):
        self.trigger(
            "maximize",
            SkEvent(event_type="maximize", maximized=maximized, glfw_window=window),
        )

    def _on_drop(self, window: typing.Any, paths):
        self.trigger("drop", SkEvent(event_type="drop", paths=paths, glfw_window=window))

    def _on_iconify(self, window: typing.Any, iconified: bool):
        self.trigger(
            "iconify",
            SkEvent(event_type="iconify", iconified=iconified, glfw_window=window),
        )

    # endregion

    # region Configure 属性配置

    # TODO: wtf function name and docstring
    def ime(self, x: int = 9, y: int = 0):
        return
        if sys.platform == "win32":
            import ctypes
            from ctypes import wintypes

            user32 = ctypes.WinDLL("user32", use_last_error=True)
            imm32 = ctypes.WinDLL("imm32", use_last_error=True)

            # 类型定义
            HWND = wintypes.HWND
            HIMC = wintypes.HANDLE
            DWORD = wintypes.DWORD
            LONG = wintypes.LONG

            class POINT(ctypes.Structure):
                _fields_ = [("x", LONG), ("y", LONG)]

            class RECT(ctypes.Structure):
                _fields_ = [
                    ("left", LONG),
                    ("top", LONG),
                    ("right", LONG),
                    ("bottom", LONG),
                ]

            class CANDIDATEFORM(ctypes.Structure):
                _fields_ = [
                    ("dwIndex", DWORD),
                    ("dwStyle", DWORD),
                    ("ptCurrentPos", POINT),
                    ("rcArea", RECT),
                ]

            # 函数声明
            imm32.ImmGetContext.restype = HIMC
            imm32.ImmGetContext.argtypes = [HWND]

            imm32.ImmReleaseContext.restype = wintypes.BOOL
            imm32.ImmReleaseContext.argtypes = [HWND, HIMC]

            imm32.ImmSetCandidateWindow.restype = wintypes.BOOL
            imm32.ImmSetCandidateWindow.argtypes = [HIMC, ctypes.POINTER(CANDIDATEFORM)]

            # 常量
            CFS_CANDIDATEPOS = 0x40  # 直接指定候选框位置
            CFS_EXCLUDE = 0x80  # 排除区域

            def set_candidate_pos(hwnd, x, y):
                himc = imm32.ImmGetContext(hwnd)
                if not himc:
                    return False

                form = CANDIDATEFORM()
                form.dwIndex = 0
                form.dwStyle = CFS_CANDIDATEPOS
                form.ptCurrentPos = POINT(x, y)
                form.rcArea = RECT(0, 0, 0, 0)

                ok = imm32.ImmSetCandidateWindow(himc, ctypes.byref(form))
                imm32.ImmReleaseContext(hwnd, himc)
                return bool(ok)

            hwnd = user32.GetForegroundWindow()
            return set_candidate_pos(hwnd, 100, 200)

    def geometry(self, spec: str | None = None) -> str | typing.Self:
        """Get or set the geometry of the window.

        :param spec: Geometry specification string, such as "100x100+100+100"
        :return: Geometry string if no argument is given, otherwise self
        """
        if spec is None:
            return f"{self.width}x{self.height}+{self.root_x}+{self.root_y}"

        width, height = None, None
        x, y = None, None

        if "x" in spec:
            wh, _, rest = spec.partition("+")
            width, height = map(int, wh.split("x"))
            if rest:
                x, y = map(int, rest.split("+"))
        elif spec.startswith("+"):
            x, y = map(int, spec[1:].split("+"))

        if width and height:
            self.resize(width, height)
        if x is not None and y is not None:
            self.move(x, y)
        return self

    @property
    def window_frame_size(self) -> tuple[int, int, int, int]:
        """Get the size of the window frame.

        :return: Window frame size (left, top, right, bottom)
        """
        return glfw.get_window_frame_size(self.the_window)

    @property
    def monitor(self):
        return glfw.get_window_monitor(self.the_window)

    @property
    def monitor_name(self) -> str:
        return glfw.get_monitor_name(self.monitor)

    @property
    def work_area(self):
        """The area of a monitor not occupied by global task bars or menu bars is the work area. This is specified in screen coordinates

        :return:
        """
        return glfw.get_monitor_workarea(self.monitor)

    def wm_ask_notice(self) -> None:
        """Request window attention

        This method will request the window to gain focus and display the window icon in the taskbar.


        >>> window.hongwen()
        >>> window.ask_notice()

        :return: None
        """
        glfw.request_window_attention(self.the_window)

    ask_notice = ask_focus = wm_ask_notice

    def wm_iconpath(self, path: str | None = None) -> str | None:
        if path:
            try:
                import PIL
                from PIL import Image

                icon = Image.open(path)
                if self.framework == "glfw":
                    from glfw import set_window_icon

                    set_window_icon(self.the_window, 1, icon)
            except ImportError:
                pass
            else:
                self.configure(iconpath=path)
        else:
            return self.cget("iconpath")

    iconpath = wm_iconpath

    def wm_maxsize(self, width: int | float | None = None, height: int | float | None = None):
        if width is None:
            width = glfw.DONT_CARE
        if height is None:
            height = glfw.DONT_CARE
        glfw.set_window_size_limits(self.the_window, glfw.DONT_CARE, glfw.DONT_CARE, width, height)

    maxsize = wm_maxsize

    def wm_minsize(
        self, width: int | None = None, height: int | None = None
    ) -> tuple[int | None, int | None]:
        if width is None and height is None:
            size = self.cget("minsize")
            if size[0] is None:
                w = 0
            else:
                w = size[0]
            if size[1] is None:
                h = 0
            else:
                h = size[1]
            return w, h
        else:
            self.configure(minsize=(width, height))
            if width is None:
                width = glfw.DONT_CARE
            if height is None:
                height = glfw.DONT_CARE

            glfw.set_window_size_limits(
                self.the_window, width, height, glfw.DONT_CARE, glfw.DONT_CARE
            )
            return self

    minsize = wm_minsize

    def wm_resizable(self, value: bool | None = None) -> bool | typing.Self:
        return self.window_attr("resizable", value)

    resizable = wm_resizable

    def window_attr(
        self,
        name: typing.Literal[
            "topmost",
            "focused",
            "hovered",
            "auto_iconify",
            "focus_on_show",
            "resizable",
            "visible",
            "border",
            "maximized",
        ],
        value: typing.Any = None,
    ) -> typing.Any:

        attrib_names = {
            "topmost": glfw.FLOATING,
            "focused": glfw.FOCUSED,
            "hovered": glfw.HOVERED,
            "auto_iconify": glfw.AUTO_ICONIFY,
            "focus_on_show": glfw.FOCUS_ON_SHOW,
            "resizable": glfw.RESIZABLE,
            "visible": glfw.VISIBLE,
            "border": glfw.DECORATED,
            "maximized": glfw.MAXIMIZED,
        }

        if name in attrib_names:
            attrib_name = attrib_names[name]
        else:
            attrib_name = name

        if value is not None:
            glfw.set_window_attrib(self.the_window, attrib_name, value)
            return self
        else:
            return glfw.get_window_attrib(self.the_window, attrib_name)

    def wm_cursor(
        self,
        cursor_name: (
            typing.Literal[
                "arrow",
                "center",
                "ibeam",
                "hresize",
                "yresize",
                "not_allowed",
                "crosshair",
                "hand",
                "arrow",
            ]
            | None
            | str
        ),
        custom_cursor: tuple[typing.Any, int, int] | None = None,
    ) -> typing.Self | str:
        """Set the mouse pointer style of the window.

        cursor_name:
          None -> Get the current cursor style name
          Other -> Set the current cursor style

        :param cursor_name: Cursor style name
        :param custom_cursor: Custom cursor，e.g. (image, x, y)
        :return: Cursor style name or cls
        """

        from glfw import create_standard_cursor, set_cursor

        if cursor_name is None:
            return self._cursor

        name = cursor_name.upper()

        if name not in self.cursors:
            if custom_cursor is not None:
                # 【自定义光标样式】
                cursor = glfw.create_cursor(custom_cursor[0], custom_cursor[1], custom_cursor[2])
            else:
                cursor_get = getattr(
                    __import__("glfw", fromlist=[f"{name}_CURSOR"]), f"{name}_CURSOR"
                )  # e.g. crosschair -> CROSSHAIR_CURSOR

                if cursor_get is None:
                    raise ValueError(f"Cursor {name} not found")

                cursor = create_standard_cursor(cursor_get)
            set_cursor(self.the_window, cursor)
            self.cursors[name] = cursor
        else:
            set_cursor(self.the_window, self.cursors[name])
        return self

    cursor = wm_cursor

    def default_cursor(self, cursor_name: str | None = None) -> typing.Union[str, "SkWindowBase"]:
        """Set the default cursor style of the window.

        cursor_name:
          None -> Get the default cursor style name
          Other -> Set the default cursor style

        :param cursor_name: Cursor style name
        :return: Cursor style name or cls
        """
        if cursor_name is None:
            return self.cget("cursor")
        self.configure(cursor=cursor_name)
        return self

    def wm_visible(self, is_visible: bool | None = None) -> typing.Union[bool, "SkWindowBase"]:
        """Get or set the visibility of the window.

        is_visible:
          None -> Get the visibility of the window
          True -> Show the window
          False -> Hide the window

        :param is_visible: Visibility
        :return: cls
        """
        if type(is_visible) is not bool:
            return self.visible

        if is_visible:
            self.show()
        else:
            self.hide()

        self.visible = is_visible
        return self

    visible = wm_visible

    def wm_show(self) -> "SkWindowBase":
        """Show the window.

        :return: cls
        """
        self.visible = True
        if hasattr(self, "update_layout"):
            self.update_layout()  # 添加初始布局更新
        glfw.show_window(self.the_window)
        self.update(True)  # 添加初始绘制触发
        return self

    show = wm_show

    def wm_hide(self) -> "SkWindowBase":
        """Hide the window.

        :return: cls
        """
        from glfw import hide_window

        hide_window(self.the_window)
        self.visible = False
        return self

    hide = withdraw = wm_withdraw = wm_hide

    def wm_maximize(self) -> "SkWindowBase":
        """Maximize the window.

        :return: cls
        """
        from glfw import maximize_window

        maximize_window(self.the_window)
        return self

    maximize = wm_maximize

    def wm_iconify(self) -> "SkWindowBase":
        """Iconify the window.

        :return: cls
        """
        from glfw import iconify_window

        iconify_window(self.the_window)
        return self

    iconify = wm_iconify

    def wm_restore(self) -> "SkWindowBase":
        """Restore the window (cancel window maximization).

        :return: cls
        """
        from glfw import restore_window

        restore_window(self.the_window)
        return self

    restore = wm_restore

    def wm_destroy(self) -> None:
        """Destroy the window.

        :return: None
        """
        # self._event_init = False
        # print(self.id)
        self.application.destroy_window(self)
        glfw.destroy_window(self.the_window)

        self.alive = False
        self.draw_func = None
        self.the_window = None  # Clear the reference

        for child in self.children:
            child.destroy()

    destroy = wm_destroy

    def wm_title(self, text: str | None = None) -> typing.Union[str, "SkWindowBase"]:
        """Get or set the window title.

        text:
        None -> Get the window title
        Other -> Set the window title

        :param text: Title
        :return: cls
        """
        if text is None:
            return self.cget("title")
        else:
            self.configure(title=text)
            from glfw import set_window_title

            set_window_title(self.the_window, text)

        return self

    title = wm_title

    def resize(self, width: int | None = None, height: int | None = None) -> "SkWindowBase":
        """Resize the window.

        :param width: Width
        :param height: Height
        :return: cls
        """
        if width is None:
            width = self.width
        if height is None:
            height = self.height

        self.width = width
        self.height = height

        from glfw import set_window_size

        set_window_size(self.the_window, round(width), round(height))
        self.trigger("resize", SkEvent(event_type="resize", width=width, height=height))

        return self

    def move(self, x: int | None = None, y: int | None = None) -> "SkWindowBase":
        """Move the window.

        :param x: x position
        :param y: y position
        :return: cls
        """
        if x is None:
            x = self.root_x
        if x < -self.width / 2:
            x = round(-self.width / 2)
        if y is None:
            y = self.root_y
        if y < -self.height / 2:
            y = round(-self.height / 2)
        self.root_x = x
        self.root_y = y
        from glfw import set_window_pos

        set_window_pos(self.the_window, round(x), round(y))
        self.trigger("move", SkEvent(event_type="move", rootx=x, rooty=y))

        return self

    def window_pos(self):
        return glfw.get_window_pos(self.the_window)

    def mouse_pos(self):
        return glfw.get_cursor_pos(self.the_window)

    def mouse_root_pos(self):
        pos = self.mouse_pos()
        window_pos = self.window_pos()
        return pos[0] + window_pos[0], pos[1] + window_pos[1]

    def get_attribute(self, attribute_name: str) -> typing.Any:
        """Get the window attribute with attribute name.

        :param attribute_name: Attribute name
        :return: Attribute _value
        """
        if attribute_name == "opacity":
            if not hasattr(self, "the_window") or not self.the_window:
                return 1.0
            from glfw import get_window_opacity

            return get_window_opacity(self.the_window)
        return self.attributes[attribute_name]

    cget = get_attribute

    def set_attribute(self, **kwargs):
        """Set the window attribute with attribute name.

        :param kwargs: Attribute name and _value
        :return: cls
        """
        if "opacity" in kwargs:

            if not hasattr(self, "the_window") or not self.the_window:
                return self

            opacity = kwargs.pop("opacity")
            if not isinstance(opacity, (float, int)) or not 0.0 <= opacity <= 1.0:
                raise ValueError("Opacity must be a float between 0.0 and 1.0")

            try:
                from glfw import set_window_opacity

                set_window_opacity(self.the_window, float(opacity))
            except Exception as e:
                print(f"[ERROR] Failed to set opacity: {e}")

        self.attributes.update(kwargs)
        self.trigger("configure", SkEvent(event_type="configure", widget=self))
        return self

    config = configure = set_attribute

    @property
    def window_id(self):
        if sys.platform == "win32":
            return glfw.get_win32_window(self.the_window)
        elif sys.platform.startswith("linux"):
            try:
                return glfw.get_wayland_window(self.the_window)
            except Exception:
                return glfw.get_x11_window(self.the_window)
        elif sys.platform == "darwin":
            return glfw.get_cocoa_window(self.the_window)
        else:
            return None

    # endregion

    # region DPI缩放相关
    # 添加DPI缩放相关方法
    def _update_dpi_scale(self) -> None:
        """Update DPI scale based on current monitor"""
        if not self.monitor:
            self.dpi_scale = 1.0
            return

        # 获取显示器的物理尺寸和分辨率
        video_mode = glfw.get_video_mode(self.monitor)
        if not video_mode:
            self.dpi_scale = 1.0
            return

        # 计算DPI缩放因子 (假设标准DPI为96)
        if hasattr(glfw, "get_monitor_physical_size"):
            width_mm, height_mm = glfw.get_monitor_physical_size(self.monitor)
            if width_mm > 0 and height_mm > 0:
                # 计算每毫米的像素数
                pixels_per_mm = video_mode.size[0] / (width_mm / 25.4)  # 转换为英寸
                self.dpi_scale = pixels_per_mm / 96.0  # 标准DPI为96
        elif sys.platform == "win32":
            # Windows平台特定的DPI获取方式
            try:
                import ctypes

                user32 = ctypes.windll.user32
                user32.SetProcessDPIAware()
                self.dpi_scale = user32.GetDpiForWindow(self.hwnd) / 96.0
            except:
                self.dpi_scale = 1.0
        else:
            # 回退方案
            self.dpi_scale = 1.0

        # 触发DPI变化事件
        self.trigger("dpi_change", SkEvent(event_type="dpi_change", dpi_scale=self.dpi_scale))

    def _on_dpi_change(self, window, xscale, yscale) -> None:
        """Handle DPI change event

        :param window: GLFW Window
        :param xscale: X scale factor
        :param yscale: Y scale factor
        """
        # 更新DPI缩放因子
        self.dpi_scale = (xscale + yscale) / 2.0

        # 触发DPI变化事件
        self.trigger(
            "dpi_change",
            SkEvent(event_type="dpi_change", dpi_scale=self.dpi_scale, glfw_window=window),
        )

        # 更新窗口物理尺寸
        self.physical_width = int(self.width * self.dpi_scale)
        self.physical_height = int(self.height * self.dpi_scale)

        # 触发重绘
        # self.update()

    # 添加获取DPI缩放因子的方法
    def get_dpi_scale(self) -> float:
        """Get current DPI scale factor

        :return: DPI scale factor
        """
        return self.dpi_scale

    # 添加设置DPI缩放因子的方法
    def set_dpi_scale(self, scale: float) -> "SkWindowBase":
        """Set DPI scale factor

        :param scale: DPI scale factor
        :return: cls
        """
        if scale <= 0:
            raise ValueError("DPI scale must be positive")

        self.dpi_scale = scale
        self.physical_width = int(self.width * scale)
        self.physical_height = int(self.height * scale)

        # 触发DPI变化事件
        self.trigger("dpi_change", SkEvent(event_type="dpi_change", dpi_scale=scale))

        self.update(True)

    # endregion
