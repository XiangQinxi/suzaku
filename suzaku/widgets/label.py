import skia

from .text import SkText


class SkLabel(SkText):
    """(A SkText with border and background"""

    def __init__(self, parent, text: str | None = None, *, style: str = "SkLabel", **kwargs):
        super().__init__(parent, text=text, style=style, **kwargs)

    def draw_widget(self, canvas: skia.Canvas, rect: skia.Rect) -> None:
        bg_shader = self._style2(self.theme, self.style_name, "bg_shader", None)
        bd_shadow = self._style2(self.theme, self.style_name, "bd_shadow", None)
        bd_shader = self._style2(self.theme, self.style_name, "bd_shader", None)
        radius = self._style2(self.theme, self.style_name, "radius", 0)
        width = self._style2(self.theme, self.style_name, "width", 0)
        bd = self._style2(self.theme, self.style_name, "bd", None)
        bg = self._style2(self.theme, self.style_name, "bg", None)

        # Draw the button border
        self._draw_rect(
            canvas,
            rect,
            radius=radius,
            bg=bg,
            width=width,
            bd=bd,
            bd_shadow=bd_shadow,
            bd_shader=bd_shader,
            bg_shader=bg_shader,
        )
        super().draw_widget(canvas, rect)
