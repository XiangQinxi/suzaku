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
        self.attributes["command"] = command

        self.focusable = True
        self.help_parent_scroll = True

        self.bind("click", lambda _: self.invoke)

    def _click(self, event) -> None:
        """
        Check click event (not pressed)

        :return: None
        """
        if self.button != 1:
            if self.is_mouse_floating:

                self.event_trigger("click", event)
                self.invoke()
                time = self.time()

                if self.click_time + self.cget("double_click_interval") > time:
                    self.event_trigger("double_click", event)
                    self.click_time = 0
                else:
                    self.click_time = time

    def invoke(self) -> None:
        """【触发按钮的点击事件】"""
        if self.cget("command") and self.cget("disabled") is False:
            self.cget("command")()

    def draw_widget(self, canvas, rect, style_selector: str | None = None) -> None:
        """Draw button

        :param canvas: skia.Surface to draw on
        :param rect: Rectangle to draw in
        :param style_selector: Style name

        :return: None
        """
        if style_selector is None:
            if not self.cget("disabled"):
                if self.is_mouse_floating:
                    if self.is_mouse_pressed:
                        style_selector = f"{self.style}:pressed"
                    else:
                        style_selector = f"{self.style}:hover"
                else:
                    if "focus" in self.styles[self.style]:
                        if self.is_focus:
                            style_selector = f"{self.style}:focus"
                        else:
                            style_selector = self.style
                    else:
                        style_selector = self.style
            else:
                style_selector = f"{self.style}:disabled"

        style = self.theme.get_style(style_selector)
        bg_shader = self._style("bg_shader", None, style)
        # bd_shadow = self.theme.get_style_attr(style_selector, "bd_shadow")
        bd_shadow = self._style("bd_shadow", None, style)
        bd_shader = self._style("bd_shader", None, style)
        width = self.theme.get_style_attr(style_selector, "width")
        # self._style("width", 0, style)
        # bd = self.theme.get_style_attr(style_selector, "bd")
        bd = self._style("bd", None, style)
        # bg = self.theme.get_style_attr(style_selector, "bg")
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

        """rest_style = self.theme.get_style(self.style)
        hover_style = self.theme.get_style(self.style + ":hover")
        if "bg" in hover_style:
            bg = hover_style["bg"]
        else:
            bg = rest_style["bg"]"""

        return style
