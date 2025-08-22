import typing

import skia

from .button import SkButton
from .container import SkContainer
from .text import SkText


class SkTextButton(SkText):
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
        text: str | None = "",
        *,
        cursor: typing.Union[str, None] = "hand",
        command: typing.Union[typing.Callable, None] = None,
        style: str = "SkButton",
        **kwargs,
    ) -> None:
        super().__init__(parent=parent, text=text, style=style, **kwargs)

        self.attributes["cursor"] = cursor

        self.command = command

        self.focusable = True

        if command:
            self.bind("click", lambda _: command())

    @property
    def dwidth(self):
        _width = self.cget("dwidth")
        if _width <= 0:
            _width = self.measure_text(self.get()) + 8
        return _width

    @property
    def dheight(self):
        _height = self.cget("dheight")
        if _height <= 0:
            _height = self.text_height + 8
        return _height

    # region Draw

    def draw_widget(self, canvas: skia.Canvas, rect: skia.Rect):
        """Draw the button

        :param canvas:
        :param rect:
        :return:
        """
        if self.is_mouse_floating:
            if self.is_mouse_pressed:
                style_name = self.style + ":pressed"
            else:
                style_name = self.style + ":hover"
        else:
            if self.is_focus:
                style_name = self.style + ":focus"
            else:
                style_name = self.style

        style = self.theme.get_style(style_name)

        if "bg_shader" in style:
            bg_shader = style["bg_shader"]
        else:
            bg_shader = None

        if "bd_shadow" in style:
            bd_shadow = style["bd_shadow"]
        else:
            bd_shadow = None
        if "bd_shader" in style:
            bd_shader = style["bd_shader"]
        else:
            bd_shader = None

        # Draw the button border
        self._draw_frame(
            canvas,
            rect,
            radius=self.theme.get_style(self.style)["radius"],
            bg=style["bg"],
            width=style["width"],
            bd=style["bd"],
            bd_shadow=bd_shadow,
            bd_shader=bd_shader,
            bg_shader=bg_shader,
        )

        # Draw the button text
        self._draw_text(
            canvas,
            rect=rect,
            text=self.get(),
            fg=style["fg"],
        )

    # endregion
