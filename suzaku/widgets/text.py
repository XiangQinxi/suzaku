from typing import Union

import skia

from ..base.drawbase import central_text
from ..styles.color import SkColor
from ..styles.color_old import color
from .widget import SkWidget
from .window import SkWindow


class SkText(SkWidget):
    def __init__(self, *args, text: str = "", **kwargs):
        super().__init__(*args, **kwargs)
        self.attributes["text"] = text

    def _draw(self, canvas: skia.Surfaces, rect: skia.Rect):
        self._draw_sklabel(canvas, rect, fg=self.theme.styles["SkText"]["fg"])

    def _draw_sklabel(self, canvas: skia.Surfaces, rect: skia.Rect, fg):
        """
        :param canvas:
        :param rect:
        :return:
        """
        central_text(
            canvas,
            self.cget("text"),
            color(fg),
            self.x,
            self.y,
            self.width,
            self.height,
        )
