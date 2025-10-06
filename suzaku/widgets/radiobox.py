import typing

import skia

from ..event import SkEvent
from ..styles.color import skcolor_to_color, style_to_color
from ..var import SkVar
from .widget import SkWidget


class SkRadioBox(SkWidget):
    def __init__(
        self,
        *args,
        cursor: str | None = "hand",
        command: typing.Callable | None = None,
        selected: bool = False,
        style: str = "SkRadioBox",
        value: bool | int | float | str | None = None,
        variable: SkVar | None = None,
        **kwargs,
    ):
        super().__init__(*args, cursor=cursor, style=style, **kwargs)
        self.attributes["selected"] = selected
        self.attributes["value"] = value
        self.attributes["variable"]: SkVar = variable

        self.focusable = True
        self.help_parent_scroll = True
        self.command = command
        self.bind("click", lambda _: self.invoke())

    @property
    def checked(self) -> bool:
        if self.cget("variable"):
            return self.cget("variable").get() == self.cget("value")
        else:
            return False

    def invoke(self):
        if self.attributes["variable"] is not None:
            self.attributes["variable"].set(self.cget("value"))
        if self.command:
            self.command()

    def _on_click(self, event: SkEvent):
        self.invoke()

    def draw_widget(self, canvas: skia.Canvas, rect: skia.Rect):
        """if self.is_mouse_floating:
            if self.is_mouse_pressed:
                style_selector = "SkCheckBox:pressed"
            else:
                style_selector = "SkCheckBox:hover"
        else:
            if self.is_focus:
                style_selector = "SkCheckBox:focus"
            else:"""
        if self.checked:
            style_name = f"{self.style}:checked"
        else:
            style_name = f"{self.style}:unchecked"
        if self.is_mouse_floating:
            style_name = style_name + "-hover"
        else:
            """if self.is_focus:
                style_selector = style_selector + "-focus"
            else:
                style_selector = style_selector + "-rest"""
            style_name = style_name + "-rest"

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
            width: int | float = style["width"]
        else:
            width: int | float = 0
        if "inner_width" in style:
            inner_width: int | float = style["inner_width"]
        else:
            inner_width: int | float = 3
        if "bd" in style:
            bd = style["bd"]
        else:
            bd = None
        if "bg" in style:
            bg = style["bg"]
        else:
            bg = None
        if "fg" in style:
            fg = style["fg"]
        else:
            fg = None
        _ = min(rect.width(), rect.height())
        self._draw_circle(
            canvas,
            rect.centerX(),
            rect.centerY(),
            radius=_ / 2,
            bg=bg,
            width=width,
            bd=bd,
            bd_shadow=bd_shadow,
            bd_shader=bd_shader,
            bg_shader=bg_shader,
        )

        if self.checked:
            self._draw_circle(
                canvas,
                rect.centerX(),
                rect.centerY(),
                radius=_ / 2 - inner_width,
                bg=fg,
                width=0,
                bg_shader=bg_shader,
            )
