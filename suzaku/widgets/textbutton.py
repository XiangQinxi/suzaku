import typing

import skia

from .button import SkButton
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
        *args,
        size: tuple[int, int] = (105, 35),
        cursor: typing.Union[str, None] = "hand",
        command: typing.Union[typing.Callable, None] = None,
        **kwargs,
    ) -> None:
        super().__init__(*args, size=size, **kwargs)

        self.attributes["cursor"] = cursor

        self.command = command

        self.focusable = True

        if command:
            self.bind("click", lambda _: command())

    # region Draw

    def _draw(self, canvas: skia.Canvas, rect: skia.Rect):
        """Draw the button

        :param canvas:
        :param rect:
        :return:
        """
        if self.is_mouse_floating:
            if self.is_mouse_pressed:
                style_name = "SkButton:pressed"
            else:
                style_name = "SkButton:hover"
        else:
            if self.is_focus:
                style_name = "SkButton:focus"
            else:
                style_name = "SkButton"

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
            radius=self.theme.get_style("SkButton")["radius"],
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
            text=self.get(),
            fg=style["fg"],
            canvas_x=self.canvas_x,
            canvas_y=self.canvas_y,
            width=self.width,
            height=self.height,
        )

    # endregion
