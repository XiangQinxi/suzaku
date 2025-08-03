from .element import Element


class ElBorder(Element):


    def draw(self, canvas, rect, theme):
        self.update_layout()

        from ...style.color import color
        import skia
        rect_paint = skia.Paint(
            AntiAlias=True,
            Style=skia.Paint.kStrokeAndFill_Style,
        )

        rect_paint.setColor(color("black"))
        rect_paint.setStrokeWidth(1)

        canvas.drawRoundRect(rect, 6, 6, rect_paint)
