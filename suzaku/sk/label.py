from .visual import SkVisual


class SkLabel(SkVisual):
    def __init__(self, *args, text: str = "SkLabel", style="SkLabel", **kwargs) -> None:
        """
        初始化标签

        :param args: SkVisual参数
        :param text: 标签文本
        :param kwargs: SkVisual参数
        """
        super().__init__(*args, style=style, **kwargs)
        self.visual_attr["text"] = text
        self.visual_attr["name"] = "sk_label"

    def draw(self, canvas, rect) -> None:
        """
        绘制标签

        :param canvas: 传入的skia.Surface
        :param rect: 给出的矩形
        :return: None
        """
        import skia
        from ..style.color import color
        rect_paint = skia.Paint(
            Style=skia.Paint.kFill_Style,
            Color=color(self.theme.get_theme()[self.winfo_style()]["bg"]),
        )

        canvas.drawRect(rect, rect_paint)

        text_paint = skia.Paint(
            AntiAlias=True,
            Color=color(self.theme.get_theme()[self.winfo_style()]["fg"])
        )

        from ..base.font import default_font

        font = default_font()

        text_width = font.measureText(self.visual_attr["text"])
        metrics = font.getMetrics()

        draw_x = self.winfo_x() + self.winfo_width() / 2 - text_width / 2
        draw_y = self.winfo_y() + self.winfo_height() / 2 - (metrics.fAscent + metrics.fDescent) / 2

        canvas.drawSimpleText(self.visual_attr["text"], draw_x, draw_y, font, text_paint)
