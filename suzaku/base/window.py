from typing import Any

from .event import EventHanding



class Window(EventHanding):

    _instance_count = 0

    def __init__(self, parent=None, *, title: str = "suzaku", size: tuple[int, int] = (300, 300), id=None, fullscreen=False, opacity: float = 1.0, force_hardware_acceleration: bool = False):
        """Initialize window.

        * parent: Parent, usually "Application"
        * title: Window title
        * size: Window size
        * id: Window ID, auto set if None
        * fullscreen: Whether window is fullscreen (not recommended)
        * opacity: Window opacity
        """

        self.window_attr = {
            "name": "window",
            "parent": None,
            "glfw_window": None,
            "title": "",
            "width": 0,
            "height": 0,
            "x": 0,
            "y": 0,
            "visible": False,
            "id": "",
            "fullscreen": False,
            "opacity": 1.0,

            "mouse_x": 0,
            "mouse_y": 0,
            "mouse_rootx": 0,
            "mouse_rooty": 0,

            "default_cursor": "arrow",
            "cursor": "arrow",
            "focus": True,
            "force_hardware_acceleration": force_hardware_acceleration
        }

        self.evts = {
            "closed": [],
            "move": [],
            "update": [],

            "mouse_motion": [],
            "mouse_pressed": [],
            "mouse_released": [],
            "mouse_enter": [],
            "mouse_leave": [],

            "key_press": [],
            "key_release": [],
            "key_repeat": [],
            "char": [],

            "focus_in": [],
            "focus_out": [],

            "resize": [],
        }

        self.visuals = []

        Window._instance_count += 1

        ### 获取Application示例，并把自己添加进去。 ###
        from .application import Application
        parent = parent if parent is not None else Application.get_instance()
        self.window_attr["parent"] = parent
        if isinstance(parent, Application):
            parent.add_window(self)
        ##########################################

        ### 初始化窗口属性 ###
        self.window_attr["title"] = title

        if not id:
            id = self.window_attr["name"] + "." + str(self.get_instance_count())
        self.window_attr["id"] = id

        self.window_attr["width"] = size[0]
        self.window_attr["height"] = size[1]

        self.window_attr["fullscreen"] = fullscreen

        if self.window_attr["width"] <= 0 or self.window_attr["height"] <= 0:
            raise ValueError("窗口宽度和高度必须为正数")

        self.window_attr["opacity"] = opacity

        ####################

        self.is_mouse_pressed = False

        self.create()

    @classmethod
    def get_instance_count(cls):
        """Get window instance count."""
        return cls._instance_count

    import contextlib

    # 修改窗口类的skia_surface方法
    @contextlib.contextmanager
    def skia_surface(self, window):
        import skia, glfw
        from OpenGL import GL

        # 添加窗口有效性检查
        if not glfw.get_current_context() or glfw.window_should_close(window):
            yield None
            return

        try:
            context = skia.GrDirectContext.MakeGL()
            (fb_width, fb_height) = glfw.get_framebuffer_size(window)
            backend_render_target = skia.GrBackendRenderTarget(
                fb_width, fb_height, 0, 0, skia.GrGLFramebufferInfo(0, GL.GL_RGBA8))
            surface = skia.Surface.MakeFromBackendRenderTarget(
                context, backend_render_target, skia.kBottomLeft_GrSurfaceOrigin,
                skia.kRGBA_8888_ColorType, skia.ColorSpace.MakeSRGB())
            # 将断言改为更友好的错误处理
            if surface is None:
                raise RuntimeError("Failed to create Skia surface")
            yield surface
        finally:
            if 'context' in locals():
                context.releaseResourcesAndAbandonContext()

    def _on_char(self, window, char) -> None:
        """Trigger char event.

        * window: GLFW window
        * char: Character
        """
        from .event import Event
        evt = Event(char=chr(char))
        self.event_generate("char", evt)

    def _on_key(self, window, key, scancode, action, mods) -> None:
        """Trigger key event.

        * window: GLFW window
        * key: Key
        * scancode: Scancode
        * action: Action
        * mods: Modifier keys
        """
        from glfw import PRESS, RELEASE, REPEAT, MOD_CONTROL, MOD_ALT, MOD_SHIFT, MOD_SUPER, MOD_NUM_LOCK, MOD_CAPS_LOCK
        from .event import Event
        from glfw import get_key_name

        keyname: str = get_key_name(key, scancode)  # 获取对应的键名，不同平台scancode不同，因此需要输入scancode来正确转换。有些按键不具备键名
        mods_dict = {
            MOD_CONTROL: "control",
            MOD_ALT: "alt",
            MOD_SHIFT: "shift",
            MOD_SUPER: "super",
            MOD_NUM_LOCK: "num_lock",
            MOD_CAPS_LOCK: "caps_lock",
        }

        try:
            if mods:
                m = mods_dict[mods]
            else:
                m = "none"
        except KeyError:
            m = "none"

        evt = Event(key=key, keyname=keyname, mods=m)

        # 我真尼玛服了啊，改了半天，发现delete键获取不到键名，卡了我半天啊

        if action == PRESS:
            self.event_generate("key_press", evt)
        elif action == RELEASE:
            self.event_generate("key_release", evt)
        elif action == REPEAT:
            self.event_generate("key_repeat", evt)

    def _on_focus(self, window, focused) -> None:
        from .event import Event
        evt = Event()
        if focused:
            self.window_attr["focus"] = True
            self.event_generate("focus_in", evt)
        else:
            self.window_attr["focus"] = False
            self.event_generate("focus_out", evt)

    def _on_framebuffer_size(self, window, width, height, ) -> None:
        if self.draw_func:
            # 确保设置当前窗口上下文
            import glfw
            glfw.make_context_current(window)
            with self.skia_surface(window) as surface:
                with surface as canvas:
                    self.draw_func(canvas)
                surface.flushAndSubmit()
                self.update()

    def _on_resizing(self, window, width, height) -> None:
        """Trigger resize event when window size changes.

        * window: GLFW window
        * width: Width
        * height: Height
        """
        from OpenGL import GL
        GL.glViewport(0, 0, width, height)
        self._on_framebuffer_size(window, width, height)
        self.window_attr["width"] = width
        self.window_attr["height"] = height
        self.event_generate("resize", width, height)
        #self.update()

    def _on_window_pos(self, window, x, y) -> None:
        """Trigger move event when window position changes.

        * window: GLFW window
        * x: Mouse relative y coordinate to window
        * y: Mouse relative x coordinate to window
        """
        self.window_attr["x"] = x
        self.window_attr["y"] = y
        from .event import Event
        self.event_generate("move", Event(x=x, y=y))

    def _on_closed(self, window) -> None:
        """Trigger closed event after window is closed.

        * window: GLFW window
        """
        #from glfw import terminate
        from .event import Event
        self.event_generate("closed", Event())
        #terminate()

    def _on_mouse_button(self, window, arg1, is_pressed: bool, arg2) -> None:
        """Trigger mouse_pressed or mouse_released event.

        * window: GLFW window
        * arg1: Mouse button
        * is_pressed: Whether pressed
        * arg2: Modifier keys
        """
        #print(arg1, arg2)

        from .event import Event
        from glfw import get_cursor_pos
        pos = get_cursor_pos(window)

        if is_pressed:
            self.event_generate("mouse_pressed", Event(x=pos[0], y=pos[1]))
        else:
            self.event_generate("mouse_released", Event(x=pos[0], y=pos[1]))

    def _on_cursor_enter(self, window, is_enter: bool) -> None:
        """Trigger mouse_enter or mouse_leave event.

        * window: GLFW window
        * is_enter: Whether cursor entered window
        """
        from .event import Event
        from glfw import get_cursor_pos
        pos = get_cursor_pos(window)

        if is_enter:
            self.event_generate("mouse_enter", Event(x=pos[0], y=pos[1]))
        else:
            self.event_generate("mouse_leave", Event(x=pos[0], y=pos[1]))

    def _on_cursor_pos(self, window, x, y) -> None:
        """Trigger mouse_motion event when mouse moves in window.

        * window: GLFW window
        * x: Mouse x coordinate
        * y: Mouse y coordinate
        """
        from .event import Event

        self.event_generate("mouse_motion", Event(x=x, y=y))

    def update(self) -> None:
        """Update window."""
        if self.window_attr["visible"]:
            self.event_generate("update")
            from glfw import swap_buffers
            swap_buffers(self.winfo_glfw_window())

    def __str__(self):
        """Get string representation of window."""
        return self.winfo_id()

    def configure(self, **kwargs) -> "Window":
        """Configure window attributes.

        * kwargs: Attributes to set
        """
        self.window_attr.update(kwargs)
        return self

    config = configure  # 别名

    def cget(self, name: str) -> any:
        """Get attribute from window_attr.

        * name: Attribute name
        """
        return self.windowattr[name]

    def cursor(self, cursorname: str = None) -> str | type:

        """
        设置窗口当前的鼠标指针样式

        cursorname:
          None -> 获取当前光标样式名
          其他 -> 设置当前光标样式

        :param cursorname: 光标样式名
        :return: 光标样式名 或者 self
        """

        from glfw import (set_cursor, create_standard_cursor, ARROW_CURSOR, HAND_CURSOR, VRESIZE_CURSOR,
                          RESIZE_NWSE_CURSOR, RESIZE_NS_CURSOR, RESIZE_NESW_CURSOR, RESIZE_EW_CURSOR, RESIZE_ALL_CURSOR,
                          POINTING_HAND_CURSOR, NOT_ALLOWED_CURSOR, NO_CURRENT_CONTEXT, IBEAM_CURSOR, HRESIZE_CURSOR,
                          CROSSHAIR_CURSOR, CENTER_CURSOR)
        if cursorname is None:
            return self.window_attr["cursor"]

        name = cursorname.lower()

        cursorget = vars()[f"{name.upper()}_CURSOR"] # e.g. crosschair -> CROSSHAIR_CURSOR
        if cursorget:
            c = create_standard_cursor(cursorget)
        else:
            return self.window_attr["cursor"]

        self.window_attr["cursor"] = name
        set_cursor(self.winfo_glfw_window(), c)
        return self

    def default_cursor(self, cursorname: str = None) -> str | type:
        """Set or get default cursor style.

        * cursorname: Cursor style name, None to get current
        """
        if cursorname is None:
            return self.window_attr["default_cursor"]
        self.window_attr["default_cursor"] = cursorname
        return self

    def opacity(self, value: float = None) -> float | type:
        """Get or set window opacity.

        * value: Opacity, None to get
        """
        if value is None:
            return self.window_attr["opacity"]
        else:
            self.window_attr["opacity"] = value
            from glfw import set_window_opacity
            set_window_opacity(self.winfo_glfw_window(), value)
        return self

    def visible(self, is_visible: bool = None) -> bool | type:
        """Get or set window visibility.

        * is_visible: None to get, True to show, False to hide
        """
        if is_visible is None:
            return self.window_attr["visible"]
        elif is_visible:
            self.show()
        else:
            self.hide()
        return self

    def show(self) -> "Window":
        """Show window."""
        from glfw import show_window
        show_window(self.winfo_glfw_window())
        self.window_attr["visible"] = True
        return self

    def hide(self) -> "Window":
        """Hide window."""
        from glfw import hide_window
        hide_window(self.winfo_glfw_window())
        self.window_attr["visible"] = False
        return self

    def maximize(self) -> "Window":
        """Maximize window."""
        from glfw import maximize_window
        maximize_window(self.winfo_glfw_window())
        return self

    def restore(self) -> "Window":
        """Restore window (unmaximize)."""
        from glfw import restore_window
        restore_window(self.winfo_glfw_window())
        return self

    def add(self, visual) -> "Window":
        """Add child visual.

        * visual: Child visual
        """
        self.visuals.append(visual)
        return self

    def destroy(self) -> None:
        """Proper window destruction."""
        if self.window_attr["glfw_window"]:
            import glfw
            glfw.destroy_window(self.window_attr["glfw_window"])
            self.window_attr["glfw_window"] = None  # Clear the reference

    def title(self, text: str = None) -> str | type:
        """Get or set window title.

        * text: Title, None to get
        """
        if text is None:
            return self.window_attr["title"]
        else:
            self.window_attr["title"] = text
            from glfw import set_window_title
            set_window_title(self.winfo_glfw_window(), text)
            return self

    def resize(self, width: int = None, height: int = None) -> "Window":
        """Resize window.

        * width: Width
        * height: Height
        """
        if width is None:
            width = self.width
        if height is None:
            height = self.height

        self.window_attr["width"] = width
        self.window_attr["height"] = height

        from glfw import set_window_size
        set_window_size(self.winfo_glfw_window(), width, height)
        self.event_generate("resize", width, height)

        return self

    def move(self, x: int = None, y: int = None) -> "Window":
        """Move window.

        * x: X coordinate
        * y: Y coordinate
        """
        if x is None:
            x = self.x
        if y is None:
            y = self.y
        self.window_attr["x"] = x
        self.window_attr["y"] = y
        from glfw import set_window_pos
        set_window_pos(self.winfo_glfw_window(), x, y)
        self.event_generate("move")

        return self

    def configure(self, **kw) -> "Window":
        """Configure window attributes.

        * **kw: Attribute key-value pairs
        """
        pass
        return self

    config = configure

    def cget(self, key: str) -> any:
        """Get window attribute.

        * key: Attribute name
        """
        return self.window_attr[key]

    def winfo(self) -> dict:
        """Get all window attributes."""
        return self.window_attr

    def winfo_parent(self) -> "Application":
        """Get parent Application."""
        return self.window_attr["parent"]

    def winfo_glfw_window(self) -> any:
        """Get GLFW window."""
        return self.window_attr["glfw_window"]

    def winfo_master_window(self) -> "Window":
        """Get master window (self)."""
        return self

    def set_draw_func(self, func: callable) -> "Window":
        """Set Skia draw function.

        * func: Draw function
        """
        self.draw_func = func
        return self

    def set_application(self, app) -> "Window":
        """Set application instance (for Application use).

        * app: Application instance
        """
        self.application = app
        return self

    def create(self) -> any:
        """Create GLFW window."""

        import glfw

        if hasattr(self, 'application') and self.application:
            if self.window_attr["fullscreen"]:
                monitor = glfw.get_primary_monitor()
            else:
                monitor = None

            import sys
            glfw.window_hint(glfw.STENCIL_BITS, 8)
            # see https://www.glfw.org/faq#macos
            if sys.platform.startswith("darwin"):
                glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
                glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 2)
                glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)
                glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

            # 使用应用程序的GLFW配置
            window = glfw.create_window(
                self.winfo_width(),
                self.winfo_height(),
                self.title(),
                monitor, None
            )
            if not window:
                raise RuntimeError("无法创建GLFW窗口")

            self.window_attr["visible"] = True

            self.window_attr["glfw_window"] = window

            pos = glfw.get_window_pos(window)

            self.window_attr["x"] = pos[0]
            self.window_attr["y"] = pos[1]

            self.cursor(self.default_cursor())

            if self.window_attr["force_hardware_acceleration"]:
                glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, glfw.TRUE)
                glfw.window_hint(glfw.CLIENT_API, glfw.OPENGL_API)
                glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
                glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
                glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

            return window
        else:
            raise RuntimeError("窗口必须先添加到Application实例")

    def create_bind(self) -> None:
        """Bind GLFW window events"""
        window =  self.winfo_glfw_window()
        import glfw
        glfw.make_context_current(window)
        glfw.set_window_size_callback(window, self._on_resizing)
        glfw.set_framebuffer_size_callback(window, self._on_framebuffer_size)
        glfw.set_window_close_callback(window, self._on_closed)
        glfw.set_window_opacity(window, self.window_attr["opacity"])
        glfw.set_mouse_button_callback(window, self._on_mouse_button)
        glfw.set_cursor_enter_callback(window, self._on_cursor_enter)
        glfw.set_cursor_pos_callback(window, self._on_cursor_pos)
        glfw.set_window_pos_callback(window, self._on_window_pos)
        glfw.set_window_focus_callback(window, self._on_focus)
        glfw.set_key_callback(window, self._on_key)
        glfw.set_char_callback(window, self._on_char)


