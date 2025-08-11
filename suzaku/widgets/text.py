from typing import Union

import skia

from ..styles.color import SkColor, color
from ..styles.font import default_font
from .widget import SkWidget
from .window import SkWindow


class SkText(SkWidget):
    def __init__(self, parent=None, *args, text: str = "", textvariable=None, **kwargs):
        super().__init__(parent=parent, *args, **kwargs)
        self.attributes["textvariable"] = textvariable
        self.attributes["text"] = text
        self.attributes["font"] = default_font

    def get(self):
        if self.attributes["textvariable"]:
            return self.attributes["textvariable"].get()
        else:
            return self.attributes["text"]

    # region Draw

    def _draw(self, canvas: skia.Surfaces, rect: skia.Rect):
        # print(self.get())
        self._draw_central_text(
            canvas,
            text=self.get(),
            fg=self.theme.styles["SkText"]["fg"],
            x=self.x,
            y=self.y,
            width=self.width,
            height=self.height,
        )

    # endregion
