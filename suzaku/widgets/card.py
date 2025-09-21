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
        styles = self.theme.get_style(self.style)
        if self.cget("styles") is not None:
            styles = self.cget("styles")
        radius = self._style("radius", 0, styles)
        bg_shader = self._style("bg_shader", None, styles)
        bd_shadow = self._style("bd_shadow", None, styles)
        bd_shader = self._style("bd_shader", None, styles)
        width = self._style("width", 0, styles)
        bd = self._style("bd", None, styles)
        bg = self._style("bg", None, styles)

        self._draw_rect(
            canvas,
            rect,
            radius=radius,
            bg=bg,
            width=width,
            bd=bd,
            bg_shader=bg_shader,
            bd_shadow=bd_shadow,
            bd_shader=bd_shader,
        )
        return None
