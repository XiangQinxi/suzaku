from typing import Union

import skia

from ..styles.color import SkColor
from ..styles.color_old import color
from ..base.drawbase import central_text
from .widget import SkWidget
from .window import SkWindow


class SkText(SkWidget):
    def __init__(self, parent: Union[SkWindow, "SkWidget"], text: str = "", style: str = "SkText"):
        super().__init__(parent, style=style)
        self.attributes["text"] = text

    def _draw(self, canvas: skia.Surfaces, rect: skia.Rect):
        self._draw_sklabel(canvas, rect, fg=self.theme.styles[self.style]["fg"])

    def _draw_sklabel(self, canvas: skia.Surfaces, rect: skia.Rect, fg):
        """
        :param canvas:
        :param rect:
        :return:
        """
        central_text(canvas, self.cget("text"), color(fg), self.x, self.y, self.width, self.height)
