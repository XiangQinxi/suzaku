import copy

import glfw
import skia

import typing
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
        parent: typing.Self | SkApp = None,
        *args,
        theme: SkTheme = None,
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

        self.attributes["enabled_radius"]: bool = False
        self.attributes["resizable_margin"] = 8

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

        self._x1 = None
        self._y1 = None
        self._anchor = None

        self.set_draw_func(self._draw)
        self.bind("mouse_move", self._move)
        self.bind("mouse_motion", self._motion)
        self.bind("mouse_press", self._mouse)
        self.bind("mouse_released", self._mouse_released)

        self.bind("focus_loss", self._leave)
        self.bind("mouse_leave", self._leave)

        self.bind("char", self._char)

        self.bind("key_pressed", self._key_pressed)
        self.bind("key_repeated", self._key_repected)
        self.bind("key_released", self._key_released)

        self.bind("scroll", self._scroll)

        self.bind("update", self.update)

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

    def update(self):
        SkContainer.update(self)

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
            self.focus_get().trigger("key_pressed", event)
        del event

    def _scroll(self, event: SkEvent) -> None:
        if self.focus_get() is not self:
            self.focus_get().trigger("scroll", event)

    def _key_repected(self, event: SkEvent) -> None:
        if self.focus_get() is not self:
            self.focus_get().trigger("key_repeated", event)
        del event

    def _key_released(self, event: SkEvent) -> None:
        if self.focus_get() is not self:
            self.focus_get().trigger("key_released", event)
        del event

    def _char(self, event: SkEvent) -> None:
        # print(12)
        if self.focus_get() is not self:
            self.focus_get().trigger("char", event)
        del event

    def _leave(self, event: SkEvent) -> None:
        event = SkEvent(
            event_type="mouse_leave",
            x=event["x"],
            y=event["y"],
            rootx=event["rootx"],
            rooty=event["rooty"],
        )
        children = self.visible_children
        children.reverse()
        for widget in children:
            widget.is_mouse_pressed = False
            widget.trigger("mouse_leave", event)
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
            x, y = event["x"], event["y"]
            width, height = widget.width, widget.height
            return cx <= x <= cx + width and cy <= y <= cy + height
        return False

    def is_entered_widget(self, widget, event: SkEvent) -> bool:
        """Check if within the widget.

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
        if self.window.resizable():
            # assert event["x"] is int
            # assert event["y"] is int
            self._anchor = self.mouse_anchor(event["x"], event["y"])
        else:
            self._anchor = None
        if self._anchor:
            self._x1 = event["x"]
            self._y1 = event["y"]
            self._rootx1 = self.root_x
            self._rooty1 = self.root_y
            self._width1 = self.window.width
            self._height1 = self.window.height
            self._right = self.root_x + self.width
            self._bottom = self.root_y + self.height
        children = self.visible_children
        children.reverse()
        for widget in children:
            if self.is_entered_widget(widget, event):
                widget.is_mouse_floating = True
                if widget.focusable:
                    widget.focus_set()
                widget.is_mouse_pressed = True
                widget.button = event["button"]
                names = [
                    "mouse_press",
                    f"mouse_press[button{event["button"] + 1}]",
                    f"mouse_press[b{event["button"] + 1}]",
                ]
                for name in names:
                    widget.trigger(name, event)
                break

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

    def _move(self, event: SkEvent) -> None:
        """Mouse move event for SkWindow.

        :param event: SkEvent
        :return:
        """
        current_widget = None
        event = SkEvent(
            widget=self,
            event_type="mouse_motion",
            button=self.button,
            x=event["x"],
            y=event["y"],
            rootx=event["rootx"],
            rooty=event["rooty"],
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
            self.previous_widget.trigger("mouse_leave", event)
            self.previous_widget.is_mouse_floating = False

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
                self.previous_widget = current_widget
        else:
            self.previous_widget = None

        if (
            not self.window_attr("border")
            and not self.window_attr("maximized")
            and self.window.resizable()
        ):
            match self.mouse_anchor(event.x, event.y):
                case "e" | "w":
                    self.cursor("hresize")
                case "s" | "n":
                    self.cursor("vresize")
                case "se" | "nw":
                    self.cursor("resize_nwse")
                case "sw" | "ne":
                    self.cursor("resize_nesw")
                case _:
                    if not self.previous_widget:
                        self.cursor("arrow")

    def _motion(self, event: SkEvent) -> None:
        self._anchor: str
        if self._anchor and not self.window_attr("maximized"):
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

    def _mouse_released(self, event: SkEvent) -> None:
        """Mouse release event for SkWindow.

        :param event:
        :return:
        """

        self._x1 = None
        self._y1 = None

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
                        _widget.trigger(name, event)
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
            self.focus_widget.trigger(
                "focus_loss", SkEvent(event_type="focus_loss")
            )
            self.focus_widget: SkWindow | SkWidget = self
        glfw.focus_window(self.the_window)

    # endregion

    # region Draw 绘制

    def _rect_path(
        self,
        rect: skia.Rect,
        radius: int | tuple[int, int, int, int] = 0,
    ):
        rrect: skia.RRect = skia.RRect.MakeRect(skia.Rect.MakeLTRB(*rect))
        radii: tuple[
            tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]
        ] = self.unpack_radius(radius)
        # 设置每个角的半径（支持X/Y不对称）
        rrect.setRectRadii(
            skia.Rect.MakeLTRB(*rect),
            [
                skia.Point(*radii[0]),  # 左上
                skia.Point(*radii[1]),  # 右上
                skia.Point(*radii[2]),  # 右下
                skia.Point(*radii[3]),  # 左下
            ],
        )

        path = skia.Path()
        path.addRRect(rrect)
        return path

    def _draw(self, canvas: skia.Canvas) -> None:
        # print(style_to_color())
        style = self.theme.select(self.style)
        self.rect = skia.Rect.MakeLTRB(0, 0, self.width, self.height)

        radius = self._style("radius", 0, style)
        if self.window_attr("maximized"):
            radius = (0, 0, 0, 0)

        _ = not self.window_attr("border") and "radius" in style
        if _:
            radii: tuple[
                tuple[int, int], tuple[int, int], tuple[int, int], tuple[int, int]
            ] = self.unpack_radius(radius)
            rrect: skia.RRect = skia.RRect.MakeRectXY(self.rect, 0, 0)
            rrect.setRectRadii(
                self.rect,
                [
                    skia.Point(*radii[0]),  # 左上
                    skia.Point(*radii[1]),  # 右上
                    skia.Point(*radii[2]),  # 右下
                    skia.Point(*radii[3]),  # 左下
                ],
            )
            canvas.clipRRect(
                rrect,
                self.anti_alias,
            )
        canvas.clear(
            style_to_color(self._style("bg", skia.ColorWHITE, style), self.theme).color
        )
        # canvas.clear(skia.ColorTRANSPARENT)

        self.draw_children(canvas)

        if _:
            bd = style_to_color(
                self._style("bd", skia.ColorBLACK, style), self.theme
            ).color
            width = self._style("width", 2, style)

            path = self._rect_path(self.rect, radius)

            if bd and width > 0:
                bd_paint = skia.Paint(
                    AntiAlias=self.anti_alias,
                    Style=skia.Paint.kStroke_Style,
                )
                bd = skcolor_to_color(style_to_color(bd, self.theme))
                bd_paint.setStrokeWidth(width)
                bd_paint.setColor(bd)
                canvas.drawPath(path, bd_paint)
        return None

    # endregion
