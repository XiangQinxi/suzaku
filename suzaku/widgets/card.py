import skia

from .. import styles
from .container import SkContainer
from .frame import SkFrame


class SkCard(SkFrame):
    """A card widget"""

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
        if "bd_shadow" in styles:
            bd_shadow = styles["bd_shadow"]
        else:
            bd_shadow = False
        if "bd_shader" in styles:
            bd_shader = styles["bd_shader"]
        else:
            bd_shader = None
        self._draw_rect(
            canvas,
            rect,
            radius=styles["radius"],
            bg=styles["bg"],
            width=styles["width"],
            bd=styles["bd"],
            bd_shadow=bd_shadow,
            bd_shader=bd_shader,
        )
        return None
