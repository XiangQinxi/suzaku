import typing

import skia

from ..styles.color import style_to_color
from ..styles.font import default_font
from ..var import SkStringVar
from .widget import SkWidget


class SkText(SkWidget):
    """A text component used to display a single line of text

    >>> var = SkStringVar(default_value="I`m a Text")
    >>> text = SkText(parent, textvariable=var)
    >>> text2 = SkText(parent, textvariable=var)

    :param parent: Parent widget or window
    :param str text: The text to be displayed
    :param textvariable: Bind to SkVar. When the SkVar value changes, its own text will also update accordingly.
    """

    def __init__(
        self,
        parent=None,
        *args,
        text: str | None = "",
        textvariable: SkStringVar = None,
        **kwargs,
    ):
        super().__init__(parent=parent, *args, **kwargs)
        self.attributes["textvariable"]: SkStringVar = textvariable
        self.attributes["text"]: str | None = text
        self.attributes["font"]: skia.Font = default_font

    def set(self, text: str) -> typing.Self:
        """Set the text"""
        if self.attributes["textvariable"]:
            self.attributes["textvariable"].set(text)
        else:
            self.attributes["text"] = text
        return self

    def get(self) -> str:
        """Get the text"""
        if self.attributes["textvariable"]:
            return self.attributes["textvariable"].get()
        else:
            return self.attributes["text"]

    # region Draw

    def _draw(self, canvas: skia.Surfaces, rect: skia.Rect):
        self._draw_text(
            canvas,
            text=self.get(),
            fg=self.theme.get_style_attr("SkText", "fg"),
            canvas_x=self.canvas_x,
            canvas_y=self.canvas_y,
            width=self.width,
            height=self.height,
            font=self.attributes["font"],
        )

    # endregion
