from .container import SkContainer
from .widget import SkWidget


class SkFrame(SkWidget, SkContainer):
    def __init__(self, *args, size: tuple[int, int] = (100, 100), border: bool = False, **kwargs) -> None:
        SkWidget.__init__(self, *args, size=size, **kwargs)
        SkContainer.__init__(self)

        self.attributes["border"] = border

    # region Draw

    def _draw(self, canvas, rect):
        style = self.theme.get_style("SkFrame")
        if self.attributes["border"]:
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

    # endregion
