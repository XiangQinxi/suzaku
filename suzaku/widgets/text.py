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
        self._draw_sklabel(canvas, rect, fg=self.theme.styles["SkText"]["fg"])

    def _draw_sklabel(self, canvas: skia.Surfaces, rect: skia.Rect, fg: SkColor):
        """
        :param canvas:
        :param rect:
        :return:
        """
        self._draw_central_text(
            canvas,
            self.cget("text"),
            color(fg),
            self.x,
            self.y,
            self.width,
            self.height,
        )

    # endregion
