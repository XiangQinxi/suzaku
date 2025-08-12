from .container import SkContainer
from .widget import SkWidget


class SkFrame(SkWidget, SkContainer):
    def __init__(self, *args, border: bool = True, **kwargs) -> None:
        SkWidget.__init__(self, *args, **kwargs)
        SkContainer.__init__(self)

        self.attributes["border"] = border

    # region Draw

    def _draw(self, canvas, rect):
        if self.attributes["border"]:
            sheets = self.theme.styles["SkFrame"]
            if "bd_shadow" in sheets:
                bd_shadow = sheets["bd_shadow"]
            else:
                bd_shadow = False
            if "bd_shader" in sheets:
                bd_shader = sheets["bd_shader"]
            else:
                bd_shader = None
            self._draw_frame(
                canvas,
                rect,
                radius=sheets["radius"],
                bg=sheets["bg"],
                width=sheets["width"],
                bd=sheets["bd"],
                bd_shadow=bd_shadow,
                bd_shader=bd_shader,
            )

    # endregion
