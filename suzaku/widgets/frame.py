from typing import Union

from ..base.container import SkContainer
from .widget import SkWidget
import skia
from ..styles.color import color

from suzaku.widgets.packs import set_drop_shadow
from suzaku.widgets.packs import set_rainbow_shader

class SkFrame(SkWidget, SkContainer):
    def __init__(self, parent: Union[SkWidget, "SkWindow"], style="SkFrame", **kwargs) -> None:
        super().__init__(parent, style=style, **kwargs)

    def draw(self, canvas, rect):
        sheets = self.theme.styles[self.style]

        radius = sheets["radius"]

        # 绘制背景

        rect_paint = skia.Paint(
            AntiAlias=True,
            Style=skia.Paint.kStrokeAndFill_Style,
        )

        rect_paint.setColor(color(sheets["bg"]))
        rect_paint.setStrokeWidth(sheets["width"])

        canvas.drawRoundRect(rect, radius, radius, rect_paint)

        # 绘制边框
        rect_paint.setStyle(skia.Paint.kStroke_Style)

        # 绘制阴影
        if "bd_shadow" in sheets:
            if "bd_shadw":
                set_drop_shadow(rect_paint, color(sheets["bd"]))

        # Rainbow Border Effect
        if "bd_shader" in sheets:
            if sheets["bd_shader"].lower() == "rainbow":
                set_rainbow_shader(rect_paint, rect)

        rect_paint.setColor(color(sheets["bd"]))

        canvas.drawRoundRect(rect, radius, radius, rect_paint)
