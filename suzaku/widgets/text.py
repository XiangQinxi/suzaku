import skia

from .widget import SkWidget
from typing import Union
from .window import SkWindow


class SkText(SkWidget):
    def __init__(self, parent: Union[SkWindow, "SkWidget"], text: str = "", style: str = "SkText"):
        super().__init__(parent, style=style)
        self.attributes["text"] = text

    def draw(self, canvas: skia.Surfaces, rect: skia.Rect):
        """

        
        :param canvas:
        :param rect:
        :return:
        """
        from .packs import central_text
        from ..styles.color import color
        central_text(canvas, self.cget("text"), color(self.theme.styles[self.style]["fg"]), self.x, self.y, self.width, self.height)
