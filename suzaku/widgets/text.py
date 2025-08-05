from typing import Union

import skia

from ..styles.color import SkColor
from ..styles.color_old import color
from .packs import central_text
from .widget import SkWidget
from .window import SkWindow


class SkText(SkWidget):
    def __init__(self, parent: Union[SkWindow, "SkWidget"], text: str = "", style: str = "SkText"):
        super().__init__(parent, style=style)
        self.attributes["text"] = text

    def _draw(self, canvas: skia.Surfaces, rect: skia.Rect):
        """
        :param canvas:
        :param rect:
        :return:
        """
        central_text(canvas, self.cget("text"), color(self.theme.styles[self.style]["fg"]), self.x, self.y, self.width, self.height)
