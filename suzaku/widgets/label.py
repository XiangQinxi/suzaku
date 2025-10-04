import skia

from .text import SkText


class SkLabel(SkText):
    """(A SkText with border and background"""

    def __init__(
        self, parent, text: str | None = None, *, style: str = "SkLabel", **kwargs
    ):
        super().__init__(parent, text=text, style=style, **kwargs)

    def draw_widget(self, canvas: skia.Canvas, rect: skia.Rect) -> None:
        style = self.theme.get_style(self.style)

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
        if "radius" in style:
            radius = style["radius"]
        else:
            radius = 0
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
