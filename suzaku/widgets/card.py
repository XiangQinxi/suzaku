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
        if "radius" not in styles:
            radius = 0
        else:
            radius = styles["radius"]
        if "bg_shader" in styles:
            bg_shader = styles["bg_shader"]
        else:
            bg_shader = None

        if "bd_shadow" in styles:
            bd_shadow = styles["bd_shadow"]
        else:
            bd_shadow = None
        if "bd_shader" in styles:
            bd_shader = styles["bd_shader"]
        else:
            bd_shader = None

        if "width" in styles:
            width = styles["width"]
        else:
            width = 0
        if "bd" in styles:
            bd = styles["bd"]
        else:
            bd = None
        if "bg" in styles:
            bg = styles["bg"]
        else:
            bg = None
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
