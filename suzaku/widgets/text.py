from typing import Union

import skia

from ..styles.color import SkColor
from ..styles.color_old import color
from ..styles.font import default_font
from .widget import SkWidget
from .window import SkWindow


class SkText(SkWidget):
    def __init__(self, *args, text: str = "", textvariable=None, **kwargs):
        super().__init__(*args, **kwargs)
        if textvariable is not None:
            self.attributes["textvariable"] = textvariable
            self.attributes["text"] = textvariable.get()
            textvariable.bind("change", self._textvariable)
        else:
            self.attributes["text"] = text
        self.attributes["font"] = default_font

    def _textvariable(self, evt):
        self.attributes["text"] = self.attributes["textvariable"].get()

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
