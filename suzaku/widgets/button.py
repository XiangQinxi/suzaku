import typing

from ..event import SkEvent
from .container import SkContainer
from .frame import SkFrame


class SkButton(SkFrame):
    """Button without Label or Icon.

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
        cursor: typing.Union[str, None] = "arrow",
        command: typing.Union[typing.Callable, None] = None,
        **kwargs,
    ) -> None:
        super().__init__(parent, style=style, **kwargs)

        self.attributes["cursor"] = cursor
        self.attributes["command"] = command

        self.focusable = True
        self.help_parent_scroll = True

        self.bind("click", lambda _: self.invoke)

    def _click(self, event) -> None:
        """
        Check click event (not press)

        :return: None
        """
        if self.button != 1:
            if self.is_mouse_floating:

                self.trigger("click", event)
                self.invoke()
                time = self.time()

                if self.click_time + self.cget("double_click_interval") > time:
                    self.trigger("double_click", event)
                    self.click_time = 0
                else:
                    self.click_time = time

    def invoke(self) -> None:
        """Trigger button click event"""
        if self.cget("command") and not self.cget("disabled"):
            self.cget("command")()

    def draw_widget(self, canvas, rect, style_selector: str | None = None) -> str:
        """Draw button

        :param canvas: skia.Surface to draw on
        :param rect: Rectangle to draw in
        :param style_selector: Style name

        :return: None
        """
        if style_selector is None:
            if not self.cget("disabled"):
                if self.is_mouse_floating:
                    if self.is_mouse_press:
                        style_selector = f"{self.style_name}:press"
                    else:
                        style_selector = f"{self.style_name}:hover"
                else:
                    if self.is_focus:
                        style_selector = f"{self.style_name}:focus"
                    else:
                        style_selector = self.style_name
            else:
                style_selector = f"{self.style_name}:disabled"

        bg_shader = self.theme.get_style_attr(style_selector, "bg_shader")
        if not bg_shader:
            bg_shader = None
        # bd_shadow = self.theme.get_style_attr(style_selector, "bd_shadow")
        bd_shadow = self.theme.get_style_attr(style_selector, "bd_shadow")
        if not bd_shadow:
            bd_shadow = None
        bd_shader = self.theme.get_style_attr(style_selector, "bd_shader")
        if not bd_shader:
            bd_shader = None
        width = self.theme.get_style_attr(style_selector, "width")
        if not width:
            width = 0
        # bd = self.theme.get_style_attr(style_selector, "bd")
        bd = self.theme.get_style_attr(style_selector, "bd")
        if not bd:
            bd = None
        # bg = self.theme.get_style_attr(style_selector, "bg")
        bg = self.theme.get_style_attr(style_selector, "bg")
        if not bg:
            bg = None

        # Draw the button border
        self._draw_rect(
            canvas,
            rect,
            radius=self.theme.get_style_attr(self.style_name, "radius"),
            bg=bg,
            width=width,
            bd=bd,
            bd_shadow=bd_shadow,
            bd_shader=bd_shader,
            bg_shader=bg_shader,
        )

        """rest_style = self.theme.get_style(self.style)
        hover_style = self.theme.get_style(self.style + ":hover")
        if "bg" in hover_style:
            bg = hover_style["bg"]
        else:
            bg = rest_style["bg"]"""

        return style_selector
