from typing import Union, Literal

import skia

from suzaku.base.drawbase import set_drop_shadow, set_rainbow_shader

from ..base.container import SkContainer
from ..styles.color import SkColor
from ..styles.color_old import color
from .widget import SkWidget


class SkFrame(SkWidget, SkContainer):
    def __init__(self, *args, **kwargs) -> None:
        SkWidget.__init__(self, *args, **kwargs)
        SkContainer.__init__(self)

    def _draw(self, canvas, rect):
        sheets = self.theme.styles["SkFrame"]
        if "bd_shadow" in sheets:
            bd_shadow = sheets["bd_shadow"]
        else:
            bd_shadow = False
        if "bd_shader" in sheets:
            bd_shader = sheets["bd_shader"]
        else:
            bd_shader = None
        self._draw_skframe(
            canvas, rect, radius=sheets["radius"],
            bg=sheets["bg"], width=sheets["width"],
            bd=sheets["bd"], bd_shadow=bd_shadow, bd_shader=bd_shader
        )

    def _draw_skframe(self, canvas: any, rect: any, radius: int, bg: str, width: int, bd: str, bd_shadow: bool = True, bd_shader: None | Literal["rainbow"] = "rainbow"):
        # 绘制背景
        rect_paint = skia.Paint(
            AntiAlias=True,
            Style=skia.Paint.kStrokeAndFill_Style,
        )

        rect_paint.setColor(color(bg))
        rect_paint.setStrokeWidth(width)

        canvas.drawRoundRect(rect, radius, radius, rect_paint)

        # 绘制边框
        # 绘制阴影
        if bd_shadow:
            set_drop_shadow(rect_paint, dx=3, dy=3, sigmaX=10, sigmaY=10, color=color(bd)) # TODO: color is deprecated

        # 彩虹边框效果
        if bd_shader:
            if bd_shader.lower() == "rainbow":
                set_rainbow_shader(rect_paint, rect)

        rect_paint.setColor(color(bd))
        rect_paint.setStyle(skia.Paint.kStroke_Style)

        canvas.drawRoundRect(rect, radius, radius, rect_paint)
