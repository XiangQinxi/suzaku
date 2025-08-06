from typing import Union

import skia

from ..styles.color import SkColor
from ..styles.color_old import color
from .widget import SkWidget
from .window import SkWindow


class SkText(SkWidget):
    def __init__(self, *args, text: str = "", **kwargs):
        super().__init__(*args, **kwargs)
        self.attributes["text"] = text

    # region Draw

    def _draw(self, canvas: skia.Surfaces, rect: skia.Rect):
        self._draw_central_text(
            canvas,
            text=self.attributes["text"],
            fg=self.theme.styles["SkText"]["fg"],
            x=self.x,
            y=self.y,
            width=self.width,
            height=self.height,
        )

    # endregion
