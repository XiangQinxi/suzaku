import typing

import skia

from .button import SkButton
from .container import SkContainer
from .text import SkText


class SkTextButton(SkButton, SkText):
    """A Button with Text

    :param args:
    :param size: Widget default size
    :param cursor: The style displayed when the mouse hovers over it
    :param command: Triggered when the button is clicked
    :param kwargs:
    """

    def __init__(
        self,
        parent: SkContainer,
        text: str | None | int | float = "",
        *,
        cursor: typing.Union[str, None] = "hand",
        command: typing.Union[typing.Callable, None] = None,
        style: str = "SkButton",
        **kwargs,
    ) -> None:
        SkButton.__init__(self, parent=parent)
        SkText.__init__(
            self, parent=parent, text=text, style=style, cursor=cursor, **kwargs
        )

        self.command = command
        self.focusable = True
        self.ipadx = 10
        self.help_parent_scroll = True

        self.bind("click", lambda _: self.invoke())

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
            _height = self.text_height + 8 + self.ipady * 2
        return _height

    # region Draw

    def draw_widget(
        self, canvas: skia.Canvas, rect: skia.Rect, style_name: str | None = None
    ):
        """Draw the button

        :param canvas:
        :param rect:
        :param style_name:
        :return:
        """
        if style_name is None:
            if not self.cget("disabled"):
                if self.is_mouse_floating:
                    if self.is_mouse_pressed:
                        style_name = f"{self.style}:pressed"
                    else:
                        style_name = f"{self.style}:hover"
                else:
                    if "focus" in self.styles[self.style]:
                        if self.is_focus:
                            style_name = f"{self.style}:focus"
                        else:
                            style_name = self.style
                    else:
                        style_name = self.style
            else:
                style_name = f"{self.style}:disabled"

        style = self.theme.get_style(style_name)

        # Draw the button border
        SkButton.draw_widget(self, canvas, rect, style_name)

        # Draw the button text
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
            align=self.cget("align"),
        )
        canvas.restore()

    # endregion
