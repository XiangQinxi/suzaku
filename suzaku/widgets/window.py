import copy
import typing

import glfw
import skia

if typing.TYPE_CHECKING:
    from . import SkWidget

from ..base.windowbase import SkWindowBase
from ..event import SkEvent
from ..styles.color import SkColor, skcolor_to_color, style_to_color
from ..styles.drop_shadow import SkDropShadow
from ..styles.theme import SkTheme, default_theme
from .app import SkApp
from .container import SkContainer


class SkWindow(SkWindowBase, SkContainer):
    # region __init__ 初始化

    def __init__(
        self,
        parent: typing.Self | SkApp | None = None,
        *args,
        theme: SkTheme | None = None,
        style: str = "SkWindow",
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
        self.style = style

        self.attributes["enabled_radius"] = False
        self.attributes["resizable_margin"] = 8

        if isinstance(self.parent, SkWindow):
            self.theme = self.parent.theme if self.parent.theme else theme
        if theme is None:
            theme = default_theme
        self.apply_theme(theme)

        self.focus_widget = self
        self.draws: list[typing.Callable] = []

        self.window: SkWindow = self
        self._anti_alias: bool = anti_alias

        # self.previous_widget = None
        self.esc_to_close = True

        self.entered_widgets = []
        self.pressing_widget: SkWidget | None = None
        self.last_entered_widget: SkWidget | None = None

        self._x1 = None
        self._y1 = None
        self._anchor = None

        self.set_draw_func(self._draw)
        self.bind("mouse_move", self._mouse_move)
        self.bind("mouse_motion", self._mouse_motion)
        self.bind("mouse_press", self._mouse_press)
        self.bind("mouse_release", self._mouse_release)
        self.bind("mouse_leave", self._mouse_leave)

        # self.bind("focus_loss", self._leave)

        self.bind("char", self._char)

        self.bind("key_press", self._key_press)
        self.bind("key_repeat", self._key_repeat)
        self.bind("key_release", self._key_release)

        self.bind("scroll", self._scroll)

        self.bind("resize", self._resize)

    # endregion

    # region Theme related 主题相关

    def _resize(self, event: SkEvent = None) -> None:
        if hasattr(self, "update_layout"):
            self.update_layout()

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

        self.update(True)

    # endregion

    # region Event handlers 事件处理

    def destroy(self) -> None:
        super().destroy()

    def _scroll(self, event: SkEvent) -> None:
        if self.focus_get() is not self:
            self.focus_get().trigger("scroll", event)

    def _key_press(self, event: SkEvent):
        """Key press event for SkWindow.

        :param event: SkEvent
        :return:
        """
        # print(cls.cget("focus_widget"))
        if self.esc_to_close:
            if event["key"] == glfw.KEY_ESCAPE:
                if self.focus_widget is not self:
                    pass
                    # self.focus_set()
                else:
                    self.destroy()
        if self.focus_get() is not self:
            self.focus_get().trigger("key_press", event)

    def _key_repeat(self, event: SkEvent) -> None:
        if self.focus_get() is not self:
            self.focus_get().trigger("key_repeat", event)

    def _key_release(self, event: SkEvent) -> None:
        if self.focus_get() is not self:
            self.focus_get().trigger("key_release", event)

    def _char(self, event: SkEvent) -> None:
        # print(12)
        if self.focus_get() is not self:
            self.focus_get().trigger("char", event)

    def is_widget_mouse_floating(self, widget, event: SkEvent) -> bool:
        """Check if within the widget.

        :param widget: SkWidget
        :param event: SkEvent
        :return bool:
        """
        if widget.is_entered(event["x"], event["y"]):
            is_parents = []
            parent = widget.parent
            while parent:
                if isinstance(parent, (SkWindow, SkApp)):
                    break
                is_parents.append(parent.is_entered(event["x"], event["y"]))
                parent = parent.parent
            return all(is_parents)
        return False

    def mouse_anchor(self, x, y) -> str:
        anchor = ""
        resizable_margin = self.cget("resizable_margin")

        if x >= self.width - resizable_margin:
            anchor = "e"
        elif x <= resizable_margin:
            anchor = "w"
        if y >= self.height - resizable_margin:
            anchor = "s" + anchor
        elif y <= resizable_margin:
            anchor = "n" + anchor
        return anchor

    def _mouse_press(self, event: SkEvent) -> None:
        # 判定鼠标位于窗口哪个角落
        if self.window.resizable():
            # assert event["x"] is int
            # assert event["y"] is int
            self._anchor = self.mouse_anchor(event["x"], event["y"])
        else:
            self._anchor = None
        if self._anchor:
            # print(event["x"])
            self._x1 = event["x"]
            self._y1 = event["y"]
            self._rootx1 = self.root_x
            self._rooty1 = self.root_y
            self._width1 = self.window.width
            self._height1 = self.window.height
            self._right = self.root_x + self.width
            self._bottom = self.root_y + self.height
        children = self.visible_children
        # children.reverse()
        for widget in reversed(children):
            if self.is_widget_mouse_floating(widget, event):
                if widget.focusable and not widget.cget("disabled"):
                    widget.focus_set()
                self.pressing_widget = widget
                widget.is_mouse_floating = True
                widget.button = event["button"]
                names = [
                    "mouse_press",
                    f"mouse_press[button{event["button"] + 1}]",
                    f"mouse_press[b{event["button"] + 1}]",
                ]
                for name in names:
                    widget.trigger(name, event)
                break

    def _mouse_move(self, event: SkEvent) -> None:
        """Mouse move event for SkWindow.

        :param event: SkEvent
        :return:
        """

        button = self.button
        x = event["x"]
        y = event["y"]
        rootx = event["rootx"]
        rooty = event["rooty"]

        motion_event = SkEvent(
            widget=self,
            event_type="mouse_motion",
            button=self.button,
            x=x,
            y=y,
            rootx=rootx,
            rooty=rooty,
        )

        children = self.visible_children

        # 找到当前鼠标所在的组件
        current_widget = None
        for widget in children:
            if self.is_widget_mouse_floating(widget, event):
                current_widget = widget

        # 处理上一个元素的离开事件
        if self.last_entered_widget and self.last_entered_widget != current_widget:
            event = SkEvent(
                widget=self,
                event_type="mouse_leave",
                button=self.button,
                x=x,
                y=y,
                rootx=rootx,
                rooty=rooty,
            )
            self.cursor(self.default_cursor())
            self.last_entered_widget.trigger("mouse_leave", event)
            self.last_entered_widget.is_mouse_floating = False

        # 处理当前元素的进入和移动事件
        if current_widget:
            if current_widget.visible:
                if not current_widget.is_mouse_floating:
                    event.event_type = "mouse_enter"
                    self.cursor(current_widget.attributes["cursor"])
                    current_widget.is_floating = True
                    current_widget.trigger("mouse_enter", event)
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
                            current_widget.trigger(name, event)
                    else:
                        current_widget.trigger("mouse_motion", event)
                    self.cursor(current_widget.attributes["cursor"])
                    current_widget.is_floating = True
            self.last_entered_widget = current_widget
        else:
            self.last_entered_widget = None

        if (
            not self.window_attr("border")
            and not self.window_attr("maximized")
            and self.window.resizable()
        ):
            match self.mouse_anchor(event["x"], event["y"]):
                case "e" | "w":
                    self.cursor("hresize")
                case "s" | "n":
                    self.cursor("vresize")
                case "se" | "nw":
                    self.cursor("resize_nwse")
                case "sw" | "ne":
                    self.cursor("resize_nesw")
                case _:
                    if not self.last_entered_widget:
                        self.cursor("arrow")

    def _mouse_motion(self, event: SkEvent) -> None:
        if not self.window_attr("border"):
            self._anchor: str
            if all(
                [
                    self._anchor,
                    not self.window_attr("maximized"),
                    self.window.resizable(),
                    self._x1,
                    self._y1,
                ]
            ):
                x, y = None, None
                width, height = None, None
                minwidth, minheight = self.wm_minsize()
                if self._anchor.startswith("s"):
                    height = max(minheight, self._height1 + event["y"] - self._y1)
                if self._anchor.startswith("n"):
                    height = max(minheight, self._bottom - (event["rooty"] - self._y1))
                    y = min(self.root_y + self.height - minheight, event["rooty"] - self._y1)
                if self._anchor.endswith("e"):
                    width = max(minwidth, self._width1 + event["x"] - self._x1)
                if self._anchor.endswith("w"):
                    width = max(minwidth, self._right - event["rootx"] - self._x1)
                    x = min(self.root_x + self.width - minwidth, event["rootx"] - self._x1)
                self.window.resize(width, height)
                self.window.move(x, y)

    def _mouse_release(self, event: SkEvent) -> None:
        """Mouse release event for SkWindow.

        :param event:
        :return:
        """

        self._x1 = None
        self._y1 = None

        button = self.button
        names = [
            "mouse_release",
            f"mouse_release[button{button+1}]",
            f"mouse_release[b{button+1}]",
        ]

        """_widget = None

        for widget in self.visible_children:
            if widget.is_mouse_floating:
                _widget = widget
                print()"""

        if button >= 0:
            for name in names:
                event = SkEvent(
                    event_type=name,
                    button=button,
                    x=event["x"],
                    y=event["y"],
                    rootx=self.mouse_rootx,
                    rooty=self.mouse_rooty,
                )
                if self.pressing_widget and not self.pressing_widget.cget("disabled"):
                    self.pressing_widget.trigger(name, event)
                    self.pressing_widget = None
        return None

    def _mouse_leave(self, event: SkEvent) -> None:
        if self.last_entered_widget:
            event = SkEvent(
                event_type="mouse_leave",
                x=event["x"],
                y=event["y"],
                rootx=event["rootx"],
                rooty=event["rooty"],
            )
            self.last_entered_widget.is_mouse_floating = False
            self.last_entered_widget.trigger("mouse_leave", event)
        """children = self.visible_children
        children.reverse()
        for widget in children:
            widget.is_mouse_floating = False
            widget.trigger("mouse_leave", event)
        """

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
            self.focus_widget.trigger("focus_loss", SkEvent(event_type="focus_loss"))
            self.focus_widget: SkWindow | SkWidget = self
        glfw.focus_window(self.the_window)

    # endregion

    # region Draw 绘制

    def _rrect(self, rect: skia.Rect, radius: int | tuple[int, int, int, int] = 0):
        radius = self.unpack_radius(radius)
        rrect = skia.RRect()
        rrect.setRectRadii(
            skia.Rect.MakeLTRB(*rect),
            [
                skia.Point(*radius[0]),  # 左上
                skia.Point(*radius[1]),  # 右上
                skia.Point(*radius[2]),  # 右下
                skia.Point(*radius[3]),  # 左下
            ],
        )
        return rrect

    def _draw(self, canvas: skia.Canvas) -> None:
        # print(style_to_color())
        self.rect = skia.Rect.MakeLTRB(0, 0, self.width, self.height)

        radius = self.theme.get_style_attr(self.style, "radius")
        if not radius:
            radius = 0
        if self.window_attr("maximized"):
            radius = 0
        rrect = self._rrect(self.rect, radius)

        _ = not self.window_attr("border") and radius
        if _:
            canvas.clipRRect(
                rrect,
                self.anti_alias,
            )

        bg = self.theme.get_style_attr(self.style, "bg")
        if not bg:
            bg = skia.ColorWHITE

        canvas.clear(style_to_color(bg, self.theme).color)
        # canvas.clear(skia.ColorTRANSPARENT)

        self.draw_children(canvas)

        if _:
            bd = self.theme.get_style_attr(self.style, "bd")
            if not bd:
                bd = None
            width = self.theme.get_style_attr(self.style, "width")
            if not width:
                width = 2
            bd_shader = self.theme.get_style_attr(self.style, "bd_shader")
            if not bd_shader:
                bd_shader = None

            bd_paint = skia.Paint(
                AntiAlias=self.anti_alias,
                Style=skia.Paint.kStroke_Style,
            )
            bd = skcolor_to_color(style_to_color(bd, self.theme))

            if bd and width > 0:
                bd_paint.setStrokeWidth(width)
                bd_paint.setColor(bd)
                if bd_shader:
                    if isinstance(bd_shader, dict):
                        if "linear_gradient" in bd_shader:
                            self.gradient.linear(
                                widget=self,
                                config=bd_shader["linear_gradient"],
                                paint=bd_paint,
                            )
                            # print(bd_shader["linear_gradient"])
                canvas.drawRRect(rrect, bd_paint)
        return None

    # endregion
