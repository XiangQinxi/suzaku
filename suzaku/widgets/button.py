import typing

from .. import SkTheme
from .container import SkContainer
from .frame import SkFrame


class SkButton(SkFrame):
    """Button without Label or Icon.

    **Will be re-written in the future.**

    :param args: Passed to SkVisual
    :param text: Button text
    :param size: Default size
    :param cursor: Cursor styles when hovering
    :param styles: Style name
    :param command: Function to run when clicked
    :param **kwargs: Passed to SkVisual
    """

    def __init__(
        self,
        parent: SkContainer,
        *,
        style: str = "SkButton",
        size: tuple[int, int] = (105, 35),
        cursor: typing.Union[str, None] = "hand",
        command: typing.Union[typing.Callable, None] = None,
        **kwargs,
    ) -> None:
        super().__init__(parent, style=style, size=size, **kwargs)

        self.attributes["cursor"] = cursor

        self.command = command
        self.focusable = True

        if command:
            self.bind("click", lambda _: command())

    def draw_widget(self, canvas, rect) -> None:
        """Draw button

        :param canvas: skia.Surface to draw on
        :param rect: Rectangle to draw in

        :return: None
        """
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

        if "width" in style:
            width = style["width"]
        else:
            width = 0
        if "bd" in style:
            bd = style["bd"]
        else:
            bd = None
        if "bg" in style:
            bg = style["bg"]
        else:
            bg = None

        # Draw the button border
        self._draw_frame(
            canvas,
            rect,
            radius=self.theme.get_style(self.style)["radius"],
            bg=bg,
            width=width,
            bd=bd,
            bd_shadow=bd_shadow,
            bd_shader=bd_shader,
            bg_shader=bg_shader,
        )
