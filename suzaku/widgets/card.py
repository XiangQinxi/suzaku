import skia

from .container import SkContainer
from .frame import SkFrame


class SkCard(SkFrame):
    """A card widget"""

    def __init__(self, parent: SkContainer, *, style: str = "SkCard", **kwargs):
        super().__init__(parent, style=style, **kwargs)

    def draw_widget(self, canvas: skia.Canvas, rect: skia.Rect) -> None:
        """Draw the Frame border（If self.attributes["border"] is True）

        :param canvas: skia.Canvas
        :param rect: skia.Rect
        :return: None
        """
        style = self.theme.get_style(self.style)
        if "bd_shadow" in style:
            bd_shadow = style["bd_shadow"]
        else:
            bd_shadow = False
        if "bd_shader" in style:
            bd_shader = style["bd_shader"]
        else:
            bd_shader = None
        self._draw_rect(
            canvas,
            rect,
            radius=style["radius"],
            bg=style["bg"],
            width=style["width"],
            bd=style["bd"],
            bd_shadow=bd_shadow,
            bd_shader=bd_shader,
        )
        return None
