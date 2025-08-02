from typing import Any

from .event import EventHanding



class Window(EventHanding):

    _instance_count = 0

    def __init__(self, parent=None, *, title: str = "suzaku", size: tuple[int, int] = (300, 300), id=None, fullscreen=False, opacity: float = 1.0, force_hardware_acceleration: bool = False, name="window"):

        """
        初始化窗口

        :param parent: 父类 一般为"Application"
        :param title: 窗口标题
        :param size: 窗口大小
        :param id: 窗口ID，如果为None将自动设置ID
        :param fullscreen: 窗口是否全屏(有点问题，暂时不要使用)
        :param opacity: 窗口透明度
        """

        from .application import Application
        parent = parent if parent is not None else Application.get_instance()
        self.parent = parent
        if isinstance(parent, Application):
            self.application = parent
        else:
            self.application = parent.application
        if isinstance(parent, Application):
            parent.add_window(self)

        self.name = name

        if not id:
            id = self.name + "." + str(self.get_instance_count())
        self.id = id

        self.x = 0
        self.y = 0
        self.width = size[0]
        self.height = size[1]
        self.glfw_window = None
        self.visible = False
        self.id = id
        self.mouse_x = 0
        self.mouse_y = 0
        self.mouse_rootx = 0
        self.mouse_rooty = 0

        self.new_cursor = "arrow"
        self.focus = True

        self.attributes = {
            "title": title,
            "opacity": 1.0,
            "cursor": "arrow",  # default cursor
            "force_hardware_acceleration": force_hardware_acceleration
        }

        self.events = {
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

        Window._instance_count += 1

        self.width = size[0]
        self.height = size[1]

        self.attributes["fullscreen"] = fullscreen

        if self.width <= 0 or self.height <= 0:
            raise ValueError("窗口宽度和高度必须为正数")

        self.attributes["opacity"] = opacity

        ####################

        self.is_mouse_pressed = False

        self.create()

    @classmethod
    def get_instance_count(cls):
        """
        获取窗口实例数量
        :return: 窗口实例数量
        """
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
        """
        触发字符事件

        Args:
            window: GLFW窗口
            char: 字符

        Returns:
            None
        """
        from .event import Event
        self.event_generate("char", Event(event_type="char", char=chr(char)))

    def _on_key(self, window, key, scancode, action, mods) -> None:
        """
        触发键盘事件

        Args:
            window: GLFW窗口
            key: 按键
            scancode: 扫描码
            action: 动作
            mods: 修饰键

        Returns:

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

        # 我真尼玛服了啊，改了半天，发现delete键获取不到键名，卡了我半天啊

        if action == PRESS:
            self.event_generate("key_press", Event(event_type="key_press", key=key, keyname=keyname, mods=m))
        elif action == RELEASE:
            self.event_generate("key_release", Event(event_type="key_release", key=key, keyname=keyname, mods=m))
        elif action == REPEAT:
            self.event_generate("key_repeat", Event(event_type="key_repeat", key=key, keyname=keyname, mods=m))

    def _on_focus(self, window, focused) -> None:
        from .event import Event
        if focused:
            self.attributes["focus"] = True
            self.event_generate("focus_in", Event(event_type="focus_in"))
        else:
            self.attributes["focus"] = False
            self.event_generate("focus_out", Event(event_type="focus_out"))

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
        """
        触发resize事件(窗口大小改变时触发)

        :param window: GLFW窗口
        :param width: 宽度
        :param height: 高度
        :return: None
        """
        from OpenGL import GL
        GL.glViewport(0, 0, width, height)
        self._on_framebuffer_size(window, width, height)
        self.width = width
        self.height = height
        from .event import Event
        self.event_generate("resize", Event(event_type="resize", width=width, height=height))
        #self.update()

    def _on_window_pos(self, window, x, y) -> None:
        """
        触发move事件(窗口位置改变时触发)

        :param window:
        :param x: 传遍鼠标相对窗口的Y坐标
        :param y: 传递鼠标相对窗口的X坐标
        :return: None
        """
        self.x = x
        self.y = y
        from .event import Event
        self.event_generate("move", Event(event_type="move", x=x, y=y))

    def _on_closed(self, window) -> None:
        """
        触发closed事件(窗口关闭后触发)

        :param window: GLFW窗口
        :return: None
        """
        #from glfw import terminate
        from .event import Event
        self.event_generate("closed", Event(event_type="closed"))
        #terminate()

    def _on_mouse_button(self, window, arg1, is_press: bool, arg2) -> None:
        """
        触发mouse_pressed事件(鼠标按下时触发)或mouser_released事件(鼠标松开时触发)

        is_pressed:
          True  -> 鼠标按键按下时触发`window_mouse_press`事件
          False -> 鼠标按键松开时触发`window_mouse_release`事件

        :param window: GLFW窗口
        :param arg1: 按键
        :param is_press: 是否按下
        :param arg2: 修饰键
        :return: None
        """
        #print(arg1, arg2)

        from .event import Event
        from glfw import get_cursor_pos
        pos = get_cursor_pos(window)
        self.mouse_x = pos[0]
        self.mouse_y = pos[1]
        self.mouse_rootx = pos[0] + self.x
        self.mouse_rooty = pos[1] + self.y

        if is_press:
            self.event_generate("mouse_press", Event(event_type="mouse_press", x=pos[0], y=pos[1], rootx=self.mouse_rootx, rooty=self.mouse_rooty))
        else:
            self.event_generate("mouse_release", Event(event_type="mouse_release", x=pos[0], y=pos[1], rootx=self.mouse_rootx, rooty=self.mouse_rooty))

    def _on_cursor_enter(self, window, is_enter: bool) -> None:
        """
        触发mouse_enter事件(鼠标进入窗口时触发)或mouser_leave事件(鼠标离开窗口时触发)

        is_enter:
          True  -> 鼠标进入窗口时触发`window_mouse_enter`事件
          False -> 鼠标离开窗口时触发`window_mouse_leave`事件
        :param window: GLFW窗口
        :param is_enter: 是否进入窗口
        :return: None
        """

        from .event import Event
        from glfw import get_cursor_pos
        pos = get_cursor_pos(window)
        self.mouse_x = pos[0]
        self.mouse_y = pos[1]
        self.mouse_rootx = pos[0] + self.x
        self.mouse_rooty = pos[1] + self.y

        if is_enter:
            self.event_generate("mouse_enter", Event(event_type="mouse_enter", x=pos[0], y=pos[1], rootx=self.mouse_rootx, rooty=self.mouse_rooty))
        else:
            self.event_generate("mouse_leave", Event(event_type="mouse_leave", x=pos[0], y=pos[1], rootx=self.mouse_rootx, rooty=self.mouse_rooty))

    def _on_cursor_pos(self, window, x, y) -> None:
        """
        触发mouse_motion事件(鼠标进入窗口并移动时触发)

        :param window: GLFW窗口
        :param x: 鼠标x坐标
        :param y: 鼠标y坐标
        :return: None
        """

        from .event import Event

        self.mouse_x = x
        self.mouse_y = y
        self.mouse_rootx = x
        self.mouse_rooty = y

        self.event_generate("mouse_motion", Event(event_type="mouse_motion", x=x, y=y, rootx=self.mouse_rootx, rooty=self.mouse_rooty))

    def update(self) -> None:
        """
        更新窗口
        :return: None
        """
        if self.visible:
            from .event import Event
            self.event_generate("update", Event(event_type="update"))
            from glfw import swap_buffers
            swap_buffers(self.glfw_window)

    def __str__(self):
        """
        获取窗口字符串表示
        :return: 窗口字符串表示
        """
        return self.id

    def configure(self, **kwargs) -> "Window":
        """
        配置attributes中的属性

        :param kwargs: 需要设置的属性
        :return: self
        """
        self.attributes.update(kwargs)
        if "opacity" in kwargs:
            from glfw import set_window_opacity
            set_window_opacity(self.glfw_window, kwargs.pop("opacity"))
        return self

    config = configure  # 别名

    def cget(self, name: str) -> any:
        """
        获取attributes中的属性

        :param name: 需要获取属性的名称
        :return: any
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
            return self.new_cursor

        name = cursorname.lower()

        cursorget = vars()[f"{name.upper()}_CURSOR"] # e.g. crosschair -> CROSSHAIR_CURSOR
        if cursorget:
            c = create_standard_cursor(cursorget)
        else:
            return self.new_cursor

        self.new_cursor = name
        set_cursor(self.glfw_window, c)
        return self

    def default_cursor(self, cursorname: str = None) -> str | type:
        """
        设置窗口的默认光标样式

        cursorname:
          None -> 获取窗口默认光标样式
          其他 -> 设置窗口默认光标样式

        :param cursorname: 光标样式名
        :return: 光标吗
        """
        if cursorname is None:
            return self.new_cursor
        self.new_cursor = cursorname
        return self

    def visible(self, is_visible: bool = None) -> bool | type:
        """
        获取或设置窗口可见性

        is_visible:
          None -> 获取窗口可见性
          True -> 显示窗口
          False -> 隐藏窗口

        :param is_visible:
        :return: self
        """
        if is_visible is None:
            return self.visible
        elif is_visible:
            self.show()
        else:
            self.hide()
        return self

    def show(self) -> "Window":
        """
        显示窗口
        :return: self
        """
        from glfw import show_window
        show_window(self.glfw_window)
        self.visible = True
        return self

    def hide(self) -> "Window":
        """
        隐藏窗口
        :return: self
        """
        from glfw import hide_window
        hide_window(self.glfw_window)
        self.visible = False
        return self

    def maximize(self) -> "Window":
        """
        最大化窗口
        :return: self
        """
        from glfw import maximize_window
        maximize_window(self.glfw_window)
        return self

    def restore(self) -> "Window":
        """
        恢复窗口(取消窗口最大化)
        :return: self
        """
        from glfw import restore_window
        restore_window(self.glfw_window)
        return self

    def add(self, visual) -> "Window":
        """
        添加子元素
        :param visual: 子元素
        :return: self
        """
        self.visuals.append(visual)
        return self

    def destroy(self) -> None:
        """Proper window destruction"""
        if self.glfw_window:
            import glfw
            glfw.destroy_window(self.glfw_window)
            self.glfw_window = None  # Clear the reference

    def title(self, text: str = None) -> str | type:
        """
        获取或设置窗口标题

        text:
        None -> 获取窗口标题
        其他 -> 设置窗口标题

        :param text: 标题
        :return: self
        """
        if text is None:
            return self.attributes["title"]
        else:
            self.attributes["title"] = text
            from glfw import set_window_title
            set_window_title(self.glfw_window, text)
            return self

    def resize(self, width: int = None, height: int = None) -> "Window":
        """
        调整窗口大小
        :param width: 宽度
        :param height: 高度
        :param animation_s: 动画持续时间(秒)，0表示无动画
        :return: self
        """
        if width is None:
            width = self.width
        if height is None:
            height = self.height

        self.width = width
        self.height = height

        from glfw import set_window_size
        set_window_size(self.glfw_window, width, height)
        from .event import Event
        self.event_generate("resize", Event(event_type="resize", width=width, height=height))

        return self

    def move(self, x: int = None, y: int = None) -> "Window":
        """
        移动窗口
        :param x: x坐标
        :param y: y坐标
        :return: self
        """
        if x is None:
            x = self.x
        if y is None:
            y = self.y
        self.x = x
        self.y = y
        from glfw import set_window_pos
        set_window_pos(self.glfw_window, x, y)
        from .event import Event
        self.event_generate("move", Event(event_type="move", x=x, y=y))

        return self

    def configure(self, **kw) -> "Window":
        """
        配置窗口属性

        :param kw: 属性名-属性值对
        :return: self
        """
        pass
        return self

    config = configure

    def cget(self, key: str) -> any:
        """
        获取窗口属性

        :param key: 属性名
        :return: 属性值
        """
        return self.attributes[key]
    
    def get_attribute(self, attribute_name: str) -> Any:
        """
        获取窗口的全部属性
        :return: 窗口属性
        """
        return self.attributes[attribute_name]

    def set_attribute(self, **kwargs):
        self.attributes.update(**kwargs)

    def set_draw_func(self, func: callable) -> "Window":
        """
        处理Skia绘制事件
        param func: 绘制函数
        return: self
        """
        self.draw_func = func
        return self

    def create(self) -> any:
        """
        创建GLFW窗口

        Returns:
            any: GLFW窗口
        """

        import glfw

        if hasattr(self, 'application') and self.application:
            if self.attributes["fullscreen"]:
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
                self.width,
                self.height,
                self.title(),
                monitor, None
            )
            if not window:
                raise RuntimeError("无法创建GLFW窗口")

            self.visible = True

            self.glfw_window = window

            pos = glfw.get_window_pos(window)

            self.x = pos[0]
            self.y = pos[1]

            self.cursor(self.default_cursor())

            if self.attributes["force_hardware_acceleration"]:
                glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, glfw.TRUE)
                glfw.window_hint(glfw.CLIENT_API, glfw.OPENGL_API)
                glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
                glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
                glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

            return window
        else:
            raise RuntimeError("窗口必须先添加到Application实例")

    def create_bind(self) -> None:
        """
        绑定GLFW窗口事件

        Returns:
            None
        """
        window =  self.glfw_window
        import glfw
        glfw.make_context_current(window)
        glfw.set_window_size_callback(window, self._on_resizing)
        glfw.set_framebuffer_size_callback(window, self._on_framebuffer_size)
        glfw.set_window_close_callback(window, self._on_closed)
        glfw.set_window_opacity(window, self.attributes["opacity"])
        glfw.set_mouse_button_callback(window, self._on_mouse_button)
        glfw.set_cursor_enter_callback(window, self._on_cursor_enter)
        glfw.set_cursor_pos_callback(window, self._on_cursor_pos)
        glfw.set_window_pos_callback(window, self._on_window_pos)
        glfw.set_window_focus_callback(window, self._on_focus)
        glfw.set_key_callback(window, self._on_key)
        glfw.set_char_callback(window, self._on_char)


