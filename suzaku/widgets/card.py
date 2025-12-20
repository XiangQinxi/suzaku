import skia

from .container import SkContainer
from .frame import SkFrame


class SkCard(SkFrame):
    """A frame with border and background"""

    def __init__(
        self,
        parent: SkContainer,
        *,
        style: str = "SkCard",
        styles: dict | None = None,
        **kwargs,
    ):
        super().__init__(parent, style=style, **kwargs)

        self.attributes["styles"] = styles

    def draw_widget(self, canvas: skia.Canvas, rect: skia.Rect) -> None:
        """Draw the Frame border（If self.attributes["border"] is True）

        :param canvas: skia.Canvas
        :param rect: skia.Rect
        :return: None
        """
        radius = self._style2(self.theme, self.style_name, "radius", 0)
        bd_shadow = self._style2(self.theme, self.style_name, "bd_shadow", None)
        width = self._style2(self.theme, self.style_name, "width", 0)
        bd = self._style2(self.theme, self.style_name, "bd", None)
        bg = self._style2(self.theme, self.style_name, "bg", None)

        self._draw_rect(
            canvas,
            rect,
            radius=radius,
            bg=bg,
            width=width,
            bd=bd,
            bd_shadow=bd_shadow,
        )
        return None
