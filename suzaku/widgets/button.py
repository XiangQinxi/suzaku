import typing

from ..event import SkEvent
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
        cursor: typing.Union[str, None] = "hand",
        command: typing.Union[typing.Callable, None] = None,
        **kwargs,
    ) -> None:
        super().__init__(parent, style=style, **kwargs)

        self.attributes["cursor"] = cursor

        self.command = command
        self.focusable = True
        self.help_parent_scroll = True

        self.bind("click", lambda _: self.invoke)

    def invoke(self) -> None:
        """【触发按钮的点击事件】"""
        if self.command and self.cget("disabled") is False:
            self.command()

    def draw_widget(self, canvas, rect, style_name: str | None = None) -> None:
        """Draw button

        :param canvas: skia.Surface to draw on
        :param rect: Rectangle to draw in
        :param style_name: Style name

        :return: None
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
        bg_shader = self._style("bg_shader", None, style)
        bd_shadow = self._style("bd_shadow", None, style)
        bd_shader = self._style("bd_shader", None, style)
        width = self._style("width", 0, style)
        bd = self._style("bd", None, style)
        bg = self._style("bg", None, style)

        # Draw the button border
        self._draw_rect(
            canvas,
            rect,
            radius=self.theme.get_style_attr(self.style, "radius"),
            bg=bg,
            width=width,
            bd=bd,
            bd_shadow=bd_shadow,
            bd_shader=bd_shader,
            bg_shader=bg_shader,
        )
