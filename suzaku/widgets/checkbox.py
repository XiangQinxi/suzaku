import typing

import skia

from .widget import SkWidget


class SkCheckBox(SkWidget):
    def __init__(
        self,
        *args,
        cursor: typing.Union[str, None] = "hand",
        command: typing.Union[typing.Callable, None] = None,
        selected: bool = False,
        **kwargs,
    ):
        super().__init__(*args, cursor=cursor, **kwargs)
        self.attributes["selected"] = selected
        self.focusable = True

        if command:
            self.bind("click", lambda _: command())

    def draw_widget(self, canvas: skia.Canvas, rect: skia.Rect):
        """if self.is_mouse_floating:
            if self.is_mouse_pressed:
                style_name = "SkCheckBox:pressed"
            else:
                style_name = "SkCheckBox:hover"
        else:
            if self.is_focus:
                style_name = "SkCheckBox:focus"
            else:
                style_name = "SkCheckBox"

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

        self._draw_frame(canvas, rect)"""
