import skia

from .frame import SkFrame


class SkCard(SkFrame):
    """A card widget"""

    def _draw(self, canvas: skia.Canvas, rect: skia.Rect) -> None:
        """Draw the Frame border（If self.attributes["border"] is True）

        :param canvas: skia.Canvas
        :param rect: skia.Rect
        :return: None
        """
        style = self.theme.get_style("SkCard")
        if "bd_shadow" in style:
            bd_shadow = style["bd_shadow"]
        else:
            bd_shadow = False
        if "bd_shader" in style:
            bd_shader = style["bd_shader"]
        else:
            bd_shader = None
        self._draw_frame(
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
