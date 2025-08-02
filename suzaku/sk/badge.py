from .widget import SkWidget

class SkBadge(SkWidget):
    def __init__(self, *args, text: str = "SkBadge", style = "SkBadge", **kwargs) -> None:
        super().__init__(*args, style=style, name="sk_badge", **kwargs)

        self.visual_attr["text"] = text
        self.visual_attr["name"] = "sk_badge"


    def draw(self, canvas, rect) -> None:
        import skia
        rect_paint = skia.Paint(
            AntiAlias=True,
            Style=skia.Paint.kStrokeAndFill_Style,
        )

        from ..style.color import color

        theme = self.theme.get_theme()[self.winfo_style()]

        radius = theme["radius"]
        rect_paint.setColor(color(theme["bg"]))
        rect_paint.setStrokeWidth(theme["width"])

        canvas.drawRoundRect(rect, radius, radius, rect_paint)

        rect_paint.setStyle(skia.Paint.kStroke_Style)
        rect_paint.setColor(color(theme["border"]))

        canvas.drawRoundRect(rect, radius, radius, rect_paint)

        text_paint = skia.Paint(
            AntiAlias=True,
            Color=color(theme["fg"])
        )

        from suzaku.style.font import default_font
        font = default_font()

        # canvas.drawTextBlob(text, self.winfo_x(), self.winfo_y()+self.winfo_height()/2, paint2)

        # 计算位置，绘制文本居中
        text_width = font.measureText(self.visual_attr["text"])
        metrics = font.getMetrics()

        draw_x = self.winfo_x() + self.winfo_width() / 2 - text_width / 2
        draw_y = self.winfo_y() + self.winfo_height() / 2 - (metrics.fAscent + metrics.fDescent) / 2

        canvas.drawSimpleText(self.visual_attr["text"], draw_x, draw_y, font, text_paint)
