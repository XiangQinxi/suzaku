import copy
import typing

import glfw
import skia

from ..base.windowbase import SkWindowBase
from ..event import SkEvent
from ..styles.color import style_to_color
from ..styles.theme import SkTheme, default_theme
from .app import SkApp
from .container import SkContainer


class SkWindow(SkWindowBase, SkContainer):
    # region __init__ 初始化

    def __init__(
        self,
        parent: typing.Self | SkApp = None,
        *args,
        theme: SkTheme = None,
        size: tuple[int, int] = (300, 300),
        anti_alias: bool = True,
        **kwargs,
    ) -> None:
        """SkWindow, inherited from SkWindowBase

        :param args: SkWindowBase Args
        :param theme: Theme
        :param kwargs: SkWindowBase Kwargs
        """
        SkWindowBase.__init__(self, parent=parent, *args, size=size, **kwargs)
        SkContainer.__init__(self)

        self.theme: SkTheme | None = None
        self.styles: dict | None = None

        if isinstance(self.parent, SkWindow):
            self.apply_theme(self.parent.theme if self.parent.theme else theme)
        else:
            if theme is None:
                theme = default_theme
            self.apply_theme(theme)

        self.focus_widget = self
        self.draws: list[typing.Callable] = []

        self.window: SkWindow = self
        self._anti_alias: bool = anti_alias

        self.previous_widget = None
        self.esc_to_close = True

        self.entered_widgets = []

        self.set_draw_func(self._draw)
        self.bind("mouse_motion", self._motion, add=True)
        self.bind("mouse_pressed", self._mouse)
        self.bind("mouse_released", self._mouse_released)

        self.bind("focus_loss", self._leave)
        self.bind("mouse_leave", self._leave)

        self.bind("char", self._char)

        self.bind("key_pressed", self._key_pressed)
        self.bind("key_repeated", self._key_repected)
        self.bind("key_released", self._key_released)

        self.bind("scroll", self._scroll)

    # endregion

    # region Theme related 主题相关

    @property
    def anti_alias(self) -> bool:
        return self._anti_alias

    @anti_alias.setter
    def anti_alias(self, value: bool):
        self._anti_alias = value
        for child in self.children:
            child.anti_alias = value

    def apply_theme(self, new_theme: SkTheme):
        """Apply theme to the window and its children.

        :param new_theme:
        :return:
        """
        self.theme = new_theme
        self.styles = self.theme.styles
        for child in self.children:
            child.apply_theme(new_theme)

    # endregion

    # region Event handlers 事件处理

    def destroy(self) -> None:
        super().destroy()

    def _key_pressed(self, event: SkEvent):
        """Key press event for SkWindow.

        :param event: SkEvent
        :return:
        """
        # print(cls.cget("focus_widget"))
        if self.esc_to_close:
            if event.key == glfw.KEY_ESCAPE:
                if self.focus_widget is not self:
                    pass
                    # self.focus_set()
                else:
                    self.destroy()
        if self.focus_get() is not self:
            self.focus_get().event_trigger("key_pressed", event)
        del event

    def _scroll(self, event: SkEvent) -> None:
        if self.focus_get() is not self:
            self.focus_get().event_trigger("scroll", event)

    def _key_repected(self, event: SkEvent) -> None:
        if self.focus_get() is not self:
            self.focus_get().event_trigger("key_repeated", event)
        del event

    def _key_released(self, event: SkEvent) -> None:
        if self.focus_get() is not self:
            self.focus_get().event_trigger("key_released", event)
        del event

    def _char(self, event: SkEvent) -> None:
        # print(12)
        if self.focus_get() is not self:
            self.focus_get().event_trigger("char", event)
        del event

    def _leave(self, event: SkEvent) -> None:
        event = SkEvent(
            event_type="mouse_leave",
            x=event.x,
            y=event.y,
            rootx=event.rootx,
            rooty=event.rooty,
        )
        children = self.visible_children
        children.reverse()
        for widget in children:
            widget.is_mouse_pressed = False
            widget.event_trigger("mouse_leave", event)
        del event

    @staticmethod
    def is_entered_widget_bounds(widget, event: SkEvent) -> bool:
        """Check if within the widget's bounds.
        【检查是否进入组件范围（即使超出父组件，其超出部分进入仍判定为True）】
        :param widget: SkWidget
        :param event: SkEvent
        :return bool:
        """
        if widget.visible:
            cx, cy = widget.canvas_x, widget.canvas_y
            x, y = event.x, event.y
            width, height = widget.width, widget.height
            return cx <= x <= cx + width and cy <= y <= cy + height
        return False

    def is_entered_widget(self, widget, event: SkEvent) -> bool:
        """Check if within the widget.
        【检查是否进入组件】
        :param widget: SkWidget
        :param event: SkEvent
        :return bool:
        """
        if self.is_entered_widget_bounds(widget, event):
            is_parents = []
            parent = widget.parent
            while parent:
                if isinstance(parent, (SkWindow, SkApp)):
                    break
                is_parents.append(self.is_entered_widget_bounds(parent, event))
                parent = parent.parent
            return all(is_parents)
        return False

    def _mouse(self, event: SkEvent) -> None:
        children = self.visible_children
        children.reverse()
        for widget in children:
            if self.is_entered_widget(widget, event):
                widget.is_mouse_floating = True
                if widget.focusable:
                    widget.focus_set()
                widget.is_mouse_pressed = True
                widget.button = event.button
                names = [
                    "mouse_pressed",
                    f"button{event.button+1}_pressed",
                    f"b{event.button + 1}_pressed",
                ]
                for name in names:
                    widget.event_trigger(name, event)
                break

    def _motion(self, event: SkEvent) -> None:
        """Mouse motion event for SkWindow.

        :param event: SkEvent
        :return:
        """
        current_widget = None
        event = SkEvent(
            event_type="mouse_motion",
            button=self.button,
            x=event.x,
            y=event.y,
            rootx=event.rootx,
            rooty=event.rooty,
        )

        # 找到当前鼠标所在的视觉元素
        children = self.visible_children
        children.reverse()

        for widget in reversed(children):
            if self.is_entered_widget(widget, event):
                current_widget = widget

        # 处理上一个元素的离开事件
        if self.previous_widget and self.previous_widget != current_widget:
            event.event_type = "mouse_leave"
            self.cursor(self.default_cursor())
            self.previous_widget.event_trigger("mouse_leave", event)
            self.previous_widget.is_mouse_floating = False

        # 处理当前元素的进入和移动事件
        if current_widget:
            if current_widget.visible:
                if not current_widget.is_mouse_floating:
                    event.event_type = "mouse_enter"
                    self.cursor(current_widget.attributes["cursor"])
                    current_widget.is_floating = True
                    current_widget.event_trigger("mouse_enter", event)
                    current_widget.is_mouse_floating = True
                else:
                    event.event_type = "mouse_motion"
                    if self.button >= 0:
                        names = [
                            "mouse_motion",
                            f"button{self.button+1}_motion",
                            f"b{self.button+1}_motion",
                        ]

                        for name in names:
                            current_widget.event_trigger(name, event)
                    else:
                        current_widget.event_trigger("mouse_motion", event)
                    self.cursor(current_widget.attributes["cursor"])
                    current_widget.is_floating = True
                self.previous_widget = current_widget
        else:
            self.previous_widget = None
        del current_widget, event

    def _draw(self, canvas: skia.Canvas) -> None:
        # print(style_to_color())
        bg = self.theme.get_style("SkWindow")["bg"]
        canvas.clear(style_to_color(bg, self.theme).color)
        # canvas.clear(skia.ColorTRANSPARENT)

        self.draw_children(canvas)

        return None

    def _mouse_released(self, event: SkEvent) -> None:
        """Mouse release event for SkWindow.

        :param event:
        :return:
        """
        button = self.button
        names = [
            "mouse_released",
            f"button{button+1}_released",
            f"b{button+1}_released",
        ]

        _widget = None
        for widget in self.visible_children:
            if widget.is_mouse_pressed:
                _widget = widget

        if _widget:
            if button >= 0:
                for name in names:
                    event = SkEvent(
                        event_type=name,
                        button=button,
                        x=event.x,
                        y=event.y,
                        rootx=self.mouse_rootx,
                        rooty=self.mouse_rooty,
                    )
                    if _widget:
                        _widget.is_mouse_pressed = False
                        _widget.event_trigger(name, event)
        return None

    # endregion

    # region Focus related 焦点相关

    def focus_get(self):
        """Get the current widget as the focus

        :return:
        """
        return self.focus_widget

    def focus_set(self):
        """Set the current widget as the focus

        :return:
        """
        if self.focus_widget is not self:
            self.focus_widget.focus = False
            self.focus_widget.event_trigger(
                "focus_loss", SkEvent(event_type="focus_loss")
            )
            self.focus_widget = self
        glfw.focus_window(self.the_window)

    # endregion
