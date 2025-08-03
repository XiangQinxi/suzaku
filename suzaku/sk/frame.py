from .widget import SkWidget
from .container import SkContainer
from typing import Union


class SkFrame(SkWidget, SkContainer):
    def __init__(self, parent: Union[SkWidget, "SkWindow"], style="SkFrame", **kwargs) -> None:
        super().__init__(parent, style=style, **kwargs)

    def draw(self, canvas, rect):
        from ..style.color import color

        sheets = self.theme.styles[self.style]

        radius = sheets["radius"]

        # 绘制背景
        import skia
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
                from .packs import set_drop_shadow
                set_drop_shadow(rect_paint, color(sheets["bd"]))

        # Rainbow Border Effect
        if "bd_shader" in sheets:
            if sheets["bd_shader"].lower() == "rainbow":
                from .packs import set_rainbow_shader
                set_rainbow_shader(rect_paint, rect)

        rect_paint.setColor(color(sheets["bd"]))

        canvas.drawRoundRect(rect, radius, radius, rect_paint)

    def put(self, margin=(0,0,0,0)):
        """相对布局快捷方法"""
        self.put_configure(margin)