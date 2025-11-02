import typing

import skia

from ..event import SkEvent
from ..styles.color import skcolor_to_color, style_to_color
from ..var import SkBooleanVar
from .widget import SkWidget


class SkCheckBox(SkWidget):

    def __init__(
        self,
        *args,
        cursor: str | None = "arrow",
        command: typing.Callable | None = None,
        # selected: bool = False,
        style: str = "SkCheckBox",
        variable: SkBooleanVar | None = None,
        default: bool = False,
        **kwargs,
    ):
        super().__init__(*args, cursor=cursor, style_name=style, **kwargs)
        # self.attributes["selected"] = selected
        self.attributes["variable"] = variable
        self.attributes["command"] = command

        self.focusable = True
        self._checked: bool = default
        self.help_parent_scroll = True

        self.bind("click", self._on_click)

    @property
    def checked(self) -> bool:
        """【获取当前复选框的选中状态】"""
        if self.cget("variable"):
            return self.cget("variable").get()
        return self._checked

    def invoke(self):
        """【切换复选框的选中状态】"""
        self._checked = not self.checked
        if self.cget("variable"):
            self.cget("variable").set(self._checked)
        if self.cget("command"):
            self.cget("command")()

    def _on_click(self, event: SkEvent):
        """【处理点击事件，切换复选框的选中状态】"""
        self.invoke()

    def _draw_checkmark(self, canvas: skia.Canvas, rect: skia.Rect, fg: skia.Color):
        """【绘制复选框的选中标记】"""
        left, top = rect.left(), rect.top()
        width, height = rect.width(), rect.height()

        points = [
            (0.2, 0.6),  # 起点
            (0.4, 0.8),  # 中间拐点
            (0.8, 0.2),  # 终点
        ]

        # 转换为实际坐标
        real_points = [(left + p[0] * width, top + p[1] * height) for p in points]

        paint = skia.Paint(
            Color=skcolor_to_color(style_to_color(fg, self.theme)),
            StrokeWidth=2,  # 动态线条粗细
            Style=skia.Paint.kStroke_Style,
            AntiAlias=self.anti_alias,
        )

        # 分段绘制线条
        canvas.drawLine(*real_points[0], *real_points[1], paint)  # 左下到中间
        canvas.drawLine(*real_points[1], *real_points[2], paint)  # 中间到右上

    def draw_widget(self, canvas: skia.Canvas, rect: skia.Rect):
        """【绘制复选框】"""
        if self.checked:
            style_name = f"{self.style_name}:checked"
        else:
            style_name = f"{self.style_name}:unchecked"
        if self.is_mouse_floating:
            style_name = style_name + "-hover"
        else:
            """if self.is_focus:
                style_selector = style_selector + "-focus"
            else:
                style_selector = style_selector + "-rest"""
            style_name = style_name + "-rest"

        style = self.theme.select(style_name)

        if "bg_shader" in style:
            bg_shader = style["bg_shader"]
        else:
            bg_shader = None
        if "bd_shadow" in style:
            bd_shadow = style["bd_shadow"]
        else:
            bd_shadow = None
        if "bd_shader" in style:
            bd_shader = style["bd_shader"]
        else:
            bd_shader = None

        if "width" in style:
            width = style["width"]
        else:
            width = 0
        if "bd" in style:
            bd = style["bd"]
        else:
            bd = None
        if "bg" in style:
            bg = style["bg"]
        else:
            bg = None
        if "fg" in style:
            fg = style["fg"]
        else:
            fg = None

        self._draw_rect(
            canvas,
            rect,
            radius=self.theme.select(self.style_name)["radius"],
            bg=bg,
            width=width,
            bd=bd,
            bd_shadow=bd_shadow,
            bd_shader=bd_shader,
            bg_shader=bg_shader,
        )

        if self.checked:
            self._draw_checkmark(canvas, rect, fg)
