import typing

import skia

from ..styles.color import style_to_color
from ..styles.font import default_font
from ..var import SkStringVar
from .container import SkContainer
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
        parent: SkContainer,
        text: str | None | int | float = "",
        *,
        align="center",
        style: str = "SkText",
        textvariable: SkStringVar = None,
        **kwargs,
    ):
        super().__init__(parent=parent, style_name=style, **kwargs)
        self.attributes["textvariable"]: SkStringVar = textvariable
        self.attributes["text"]: str | None = str(text)
        self.attributes["font"]: skia.Font = default_font
        self.attributes["align"] = align
        self.help_parent_scroll = True

    def set(self, text: str) -> typing.Self:
        """Set the text"""
        if self.attributes["textvariable"]:
            self.attributes["textvariable"].set(text)
        else:
            self.attributes["text"] = text
        if not self.cget("dwidth") or not self.cget("dheight"):
            self.parent.update_layout()
        return self

    def get(self) -> str:
        """Get the text"""
        if self.attributes["textvariable"]:
            return self.attributes["textvariable"].get()
        else:
            return self.attributes["text"]

    @property
    def dwidth(self):
        _width = self.cget("dwidth")
        if _width <= 0:
            _width = self.measure_text(self.get()) + self.ipadx * 2
        return _width

    @property
    def dheight(self):
        _height = self.cget("dheight")
        if _height <= 0:
            _height = self.text_height + self.ipady * 2
        return _height

    # region Draw

    def draw_widget(self, canvas: skia.Canvas, rect: skia.Rect):
        style = self.theme.select(self.style_name)
        canvas.save()
        canvas.clipRect(rect)
        self._draw_text(
            canvas,
            skia.Rect.MakeLTRB(
                rect.left() + self.ipadx,
                rect.top(),
                rect.right() - self.ipadx,
                rect.bottom(),
            ),
            text=self.get(),
            fg=style["fg"],
            font=self.attributes["font"],
            align=self.cget("align"),
        )
        canvas.restore()

    # endregion
