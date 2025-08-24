import skia

from .widget import SkWidget


class SkSeparator(SkWidget):
    def __init__(self, master=None, *, style: str = "SkSeparator", **kwargs):
        super().__init__(master, style=style, **kwargs)

    def draw_widget(self, canvas: skia.Canvas, rect: skia.Rect) -> None:
        self._draw_line(
            canvas,
            x0=rect.left(),
            y0=rect.centerY(),
            x1=rect.right(),
            y1=rect.centerY(),
            fg=self.theme.get_style_attr(self.style, "fg"),
            width=self.theme.get_style_attr(self.style, "width"),
        )
