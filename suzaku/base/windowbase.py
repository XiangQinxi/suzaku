import contextlib
import sys
from typing import Any, Union

import glfw
import skia
from OpenGL import GL

from ..event import SkEvent, SkEventHanding
from .appbase import SkAppBase


class SkWindowBase(SkEventHanding):

    _instance_count = 0

    # region __init__ 初始化

    def __init__(
        self,
        parent=None,
        *,
        title: str = "suzaku",
        size: tuple[int, int] = (300, 300),
        fullscreen=False,
        opacity: float = 1.0,
        force_hardware_acceleration: bool = False,
        name="window",
    ):
        """Base Window class

        :param parent: window parent
        :param title: window title
        :param size: window size
        :param fullscreen: window fullscreen
        :param opacity: window opacity
        """

        self.children = []

        super().__init__()

        self.parent: SkAppBase | "SkWindowBase" = (
            parent if parent is not None else SkAppBase.get_instance()
        )
        if isinstance(parent, SkAppBase):  # parent=SkAppBase
            self.application = parent
            parent.add_window(self)
        elif isinstance(parent, self.__class__):  # parent=SkWindowBase
            self.application = parent.application
            parent.application.add_window(self)
            parent.bind("closed", lambda _: self.destroy())
        else:
            raise TypeError("parent must be SkAppBase or SkWindowBase")

        self.name = name

        self.x: int | float = 0
        self.y: int | float = 0
        self.width: int | float = size[0]
        self.height: int | float = size[1]
        self.glfw_window = None
        self.visible = False
        self.mouse_x = 0
        self.mouse_y = 0
        self.mouse_rootx = 0
        self.mouse_rooty = 0

        self.new_cursor = "arrow"
        self.focus = True

        self.attributes = {
            "title": title,
            "opacity": opacity,
            "cursor": "arrow",  # default cursor
            "force_hardware_acceleration": force_hardware_acceleration,
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
            "key_pressed": [],
            "key_released": [],
            "key_repeated": [],
            "char": [],
            "focus_gain": [],
            "focus_loss": [],
            "resize": [],
        }

        SkWindowBase._instance_count += 1

        self.width = size[0]
        self.height = size[1]

        self.attributes["fullscreen"] = fullscreen

        if self.width <= 0 or self.height <= 0:
            raise ValueError("The window size must be positive")

        ####################

        self.is_mouse_pressed = False

        self.glfw_window = self.create()

        self.cursor(self.default_cursor())

    @classmethod
    def get_instance_count(cls) -> int:
        """Get instance count.

        :return: Instance count
        """
        return cls._instance_count

    def create(self) -> any:
        """Create the glfw window.

        :return: cls
        """
        if hasattr(self, "application") and self.application:
            if self.attributes["fullscreen"]:
                monitor = glfw.get_primary_monitor()
            else:
                monitor = None

            glfw.window_hint(glfw.STENCIL_BITS, 8)
            # see https://www.glfw.org/faq#macos
            if sys.platform.startswith("darwin"):
                glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
                glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 2)
                glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)
                glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

            window = glfw.create_window(
                self.width, self.height, self.attributes["title"], monitor, None
            )
            if not window:
                raise RuntimeError("无法创建GLFW窗口")

            self.visible = True

            pos = glfw.get_window_pos(window)

            self.x = pos[0]
            self.y = pos[1]

            if self.attributes["force_hardware_acceleration"]:
                glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, glfw.TRUE)
                glfw.window_hint(glfw.CLIENT_API, glfw.OPENGL_API)
                glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
                glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
                glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

            glfw.set_window_opacity(window, self.cget("opacity"))

            return window
        else:
            raise RuntimeError("窗口必须先添加到Application实例")

    # endregion

    # region Draw 绘制相关

    @contextlib.contextmanager
    def skia_surface(self, window: any) -> skia.Surface | None:
        """Create a Skia surface for the window.

        :param window: GLFW Window
        :return: Skia Surface
        """
        # 添加窗口有效性检查
        if not glfw.get_current_context() or glfw.window_should_close(window):
            yield None
            return None

        try:
            context = skia.GrDirectContext.MakeGL()
            (fb_width, fb_height) = glfw.get_framebuffer_size(window)
            backend_render_target = skia.GrBackendRenderTarget(
                fb_width, fb_height, 0, 0, skia.GrGLFramebufferInfo(0, GL.GL_RGBA8)
            )
            surface = skia.Surface.MakeFromBackendRenderTarget(
                context,
                backend_render_target,
                skia.kBottomLeft_GrSurfaceOrigin,
                skia.kRGBA_8888_ColorType,
                skia.ColorSpace.MakeSRGB(),
            )
            # 将断言改为更友好的错误处理
            if surface is None:
                raise RuntimeError("Failed to create Skia surface")
            yield surface
        finally:
            if "context" in locals():
                context.releaseResourcesAndAbandonContext()

    def set_draw_func(self, func: callable) -> "SkWindowBase":
        """Set the draw function.

        :param func: Draw function
        :return: cls
        """
        self.draw_func = func
        return self

    def update(self) -> None:
        """Update window.

        :return: None
        """
        if self.visible:
            self.event_generate("update", SkEvent(event_type="update"))
            glfw.swap_buffers(self.glfw_window)
            if hasattr(self, "update_layout"):
                self.update_layout()

    # endregion

    # region Event handling 事件处理

    def _on_char(self, window: any, char: int) -> None:
        """Trigger text input event

        :param window: GLFW Window
        :param char: Unicode character
        """

        self.event_generate("char", SkEvent(event_type="char", char=chr(char)))

    def _on_key(
        self, window: any, key: str, scancode: str, action: str, mods: int
    ) -> None:
        """
        触发键盘事件

        :param window: GLFW Window
        :param key: Key
        :param scancode: Scan code
        :param action: Action
        :param mods: Modifiers
        """
        from glfw import (MOD_ALT, MOD_CAPS_LOCK, MOD_CONTROL, MOD_NUM_LOCK,
                          MOD_SHIFT, MOD_SUPER, PRESS, RELEASE, REPEAT,
                          get_key_name)

        keyname: str = get_key_name(
            key, scancode
        )  # 获取对应的键名，不同平台scancode不同，因此需要输入scancode来正确转换。有些按键不具备键名
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
            self.event_generate(
                "key_pressed",
                SkEvent(event_type="key_pressed", key=key, keyname=keyname, mods=m),
            )
        elif action == RELEASE:
            self.event_generate(
                "key_released",
                SkEvent(event_type="key_released", key=key, keyname=keyname, mods=m),
            )
        elif action == REPEAT:
            self.event_generate(
                "key_repeated",
                SkEvent(event_type="key_repeated", key=key, keyname=keyname, mods=m),
            )

    def _on_focus(self, window, focused) -> None:
        """Triggers the focus event (triggered when the window gains or loses focus).

        :param window: GLFW Window
        :param focused: Focused
        :return: None
        """
        if focused:
            self.attributes["focus"] = True
            self.event_generate("focus_gain", SkEvent(event_type="focus_gain"))
        else:
            self.attributes["focus"] = False
            self.event_generate("focus_loss", SkEvent(event_type="focus_loss"))

    def _on_framebuffer_size(self, window: any, width: int, height: int) -> None:
        if self.draw_func:
            # 确保设置当前窗口上下文
            glfw.make_context_current(window)
            with self.skia_surface(window) as surface:
                with surface as canvas:
                    self.draw_func(canvas)
                surface.flushAndSubmit()
                self.update()

    def _on_resizing(self, window, width: int, height: int) -> None:
        """Trigger resize event (triggered when the window size changes).

        :param window: GLFW Window
        :param width: Window width
        :param height: Window height
        :return: None
        """
        GL.glViewport(0, 0, width, height)
        self._on_framebuffer_size(window, width, height)
        self.width = width
        self.height = height
        event = SkEvent(event_type="resize", width=width, height=height)
        self.event_generate("resize", event)
        for child in self.children:
            child.event_generate("resize", event)
        # cls.update()

    def _on_window_pos(self, window: any, x: int, y: int) -> None:
        """Trigger move event (triggered when the window position changes).

        :param window: GLFW Window
        :param x: Window X position
        :param y: Window Y position
        :return: None
        """
        self.x = x
        self.y = y
        self.event_generate("move", SkEvent(event_type="move", x=x, y=y))

    def _on_closed(self, window: any) -> None:
        """Trigger closed event (triggered when the window is closed).

        :param window: GLFW Window
        :return: None
        """
        self.event_generate("closed", SkEvent(event_type="closed"))

    def _on_mouse_button(
        self, window: any, arg1: any, is_pressed: bool, arg2: any
    ) -> None:
        """Trigger mouse button event (triggered when the mouse button is pressed or released).

        :param window: GLFW Window
        :param arg1: Button
        :param is_pressed: Whether pressed
        :param arg2: Modifiers
        :return: None
        """
        # print(arg1, arg2)

        from glfw import get_cursor_pos

        pos = get_cursor_pos(window)
        self.mouse_x = pos[0]
        self.mouse_y = pos[1]
        self.mouse_rootx = pos[0] + self.x
        self.mouse_rooty = pos[1] + self.y

        if is_pressed:
            self.event_generate(
                "mouse_pressed",
                SkEvent(
                    event_type="mouse_pressed",
                    x=pos[0],
                    y=pos[1],
                    rootx=self.mouse_rootx,
                    rooty=self.mouse_rooty,
                ),
            )
        else:
            self.event_generate(
                "mouse_released",
                SkEvent(
                    event_type="mouse_released",
                    x=pos[0],
                    y=pos[1],
                    rootx=self.mouse_rootx,
                    rooty=self.mouse_rooty,
                ),
            )

    def _on_cursor_enter(self, window: any, is_enter: bool) -> None:
        """Trigger mouse enter event (triggered when the mouse enters the window) or mouse leave event (triggered when the mouse leaves the window).

        :param window: GLFW Window
        :param is_enter: Whether entered
        :return: None
        """

        from glfw import get_cursor_pos

        pos = get_cursor_pos(window)
        self.mouse_x = pos[0]
        self.mouse_y = pos[1]
        self.mouse_rootx = pos[0] + self.x
        self.mouse_rooty = pos[1] + self.y

        if is_enter:
            self.event_generate(
                "mouse_enter",
                SkEvent(
                    event_type="mouse_enter",
                    x=pos[0],
                    y=pos[1],
                    rootx=self.mouse_rootx,
                    rooty=self.mouse_rooty,
                ),
            )
        else:
            self.event_generate(
                "mouse_leave",
                SkEvent(
                    event_type="mouse_leave",
                    x=pos[0],
                    y=pos[1],
                    rootx=self.mouse_rootx,
                    rooty=self.mouse_rooty,
                ),
            )

    def _on_cursor_pos(self, window: any, x: int, y: int) -> None:
        """Trigger mouse motion event (triggered when the mouse enters the window and moves).

        :param window: GLFW Window
        :param x: Mouse X position
        :param y: Mouse Y position
        :return: None
        """

        self.mouse_x = x
        self.mouse_y = y
        self.mouse_rootx = x
        self.mouse_rooty = y

        self.event_generate(
            "mouse_motion",
            SkEvent(
                event_type="mouse_motion",
                x=x,
                y=y,
                rootx=self.mouse_rootx,
                rooty=self.mouse_rooty,
            ),
        )

    def create_bind(self) -> None:
        """Binding glfw window events.

        :return: None
        """
        window = self.glfw_window
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

    # endregion

    # region Attributes config 属性配置

    def cursor(self, cursor_name: Union[str, None] = None) -> "SkWindowBase":
        """Set the mouse pointer style of the window.

        cursor_name:
          None -> Get the current cursor style name
          Other -> Set the current cursor style

        :param cursor_name: Cursor style name
        :return: Cursor style name or cls
        """

        from glfw import create_standard_cursor, set_cursor

        if cursor_name is None:
            return self.new_cursor

        name = cursor_name.upper()

        # cursor_get = vars()[f"{name.upper()}_CURSOR"] # e.g. cross chair -> CROSSHAIR_CURSOR
        cursor_get = getattr(
            __import__("glfw", fromlist=[f"{name}_CURSOR"]), f"{name}_CURSOR"
        )
        if cursor_get is None:
            raise ValueError(f"Cursor {name} not found")

        self.new_cursor = name
        if self.glfw_window:
            set_cursor(self.glfw_window, create_standard_cursor(cursor_get))
        return self

    def default_cursor(self, cursor_name: str = None) -> Union[str, "SkWindowBase"]:
        """Set the default cursor style of the window.

        cursor_name:
          None -> Get the default cursor style name
          Other -> Set the default cursor style

        :param cursor_name: Cursor style name
        :return: Cursor style name or cls
        """
        if cursor_name is None:
            return self.attributes["cursor"]
        self.attributes["cursor"] = cursor_name
        return self

    def visible(self, is_visible: bool = None) -> Union[bool, "SkWindowBase"]:
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

    def show(self) -> "SkWindowBase":
        """Show the window.

        :return: cls
        """
        self.visible = True
        if hasattr(self, "update_layout"):
            self.update_layout()  # 添加初始布局更新
        glfw.show_window(self.glfw_window)
        self.update()  # 添加初始绘制触发
        return self

    def hide(self) -> "SkWindowBase":
        """Hide the window.

        :return: cls
        """
        from glfw import hide_window

        hide_window(self.glfw_window)
        self.visible = False
        return self

    def maximize(self) -> "SkWindowBase":
        """Maximize the window.

        :return: cls
        """
        from glfw import maximize_window

        maximize_window(self.glfw_window)
        return self

    def restore(self) -> "SkWindowBase":
        """Restore the window (cancel window maximization).

        :return: cls
        """
        from glfw import restore_window

        restore_window(self.glfw_window)
        return self

    def destroy(self) -> None:
        """Destroy the window.

        :return: None
        """
        if self.glfw_window:
            glfw.destroy_window(self.glfw_window)
            self.event_generate("closed", SkEvent(event_type="closed"))
            self.glfw_window = None  # Clear the reference

    def title(self, text: str = None) -> Union[str, "SkWindowBase"]:
        """Get or set the window title.

        text:
        None -> Get the window title
        Other -> Set the window title

        :param text: Title
        :return: cls
        """
        if text is None:
            return self.attributes["title"]
        else:
            self.attributes["title"] = text
            from glfw import set_window_title

            set_window_title(self.glfw_window, text)

        return self

    def resize(self, width: int = None, height: int = None) -> "SkWindowBase":
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

        set_window_size(self.glfw_window, width, height)
        self.event_generate(
            "resize", SkEvent(event_type="resize", width=width, height=height)
        )

        return self

    def move(self, x: int = None, y: int = None) -> "SkWindowBase":
        """Move the window.

        :param x: x position
        :param y: y position
        :return: cls
        """
        if x is None:
            x = self.x
        if y is None:
            y = self.y
        self.x = x
        self.y = y
        from glfw import set_window_pos

        set_window_pos(self.glfw_window, x, y)
        self.event_generate("move", SkEvent(event_type="move", x=x, y=y))

        return self

    def mouse_pos(self):
        return glfw.get_cursor_pos(self.glfw_window)

    def get_attribute(self, attribute_name: str) -> Any:
        """Get the window attribute with attribute name.

        :param attribute_name: Attribute name
        :return: Attribute value
        """
        if attribute_name == "opacity":
            if not hasattr(self, "glfw_window") or not self.glfw_window:
                return 1.0
            from glfw import get_window_opacity

            return get_window_opacity(self.glfw_window)
        return self.attributes[attribute_name]

    cget = get_attribute

    def set_attribute(self, **kwargs):
        """Set the window attribute with attribute name.

        :param kwargs: Attribute name and value
        :return: cls
        """
        if "opacity" in kwargs:

            if not hasattr(self, "glfw_window") or not self.glfw_window:
                return self

            opacity = kwargs.pop("opacity")
            if not isinstance(opacity, (float, int)) or not 0.0 <= opacity <= 1.0:
                raise ValueError("Opacity must be a float between 0.0 and 1.0")

            try:
                from glfw import set_window_opacity

                set_window_opacity(self.glfw_window, float(opacity))
            except Exception as e:
                print(f"[ERROR] Failed to set opacity: {e}")

        self.attributes.update(kwargs)
        return self

    config = configure = set_attribute

    # endregion
