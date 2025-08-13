from typing import Union

from ..widgets.text import SkText


class SkTextButton(SkText):
    def __init__(
        self,
        *args,
        size: tuple[int, int] = (105, 35),
        cursor: Union[str, None] = "hand",
        command: Union[callable, None] = None,
        **kwargs,
    ) -> None:
        super().__init__(*args, size=size, **kwargs)

        self.attributes["cursor"] = cursor

        self.command = command

        self.focusable = True

        if command:
            self.bind("click", lambda _: command())

    # region Draw

    def _draw(self, canvas, rect):
        sheets = None
        if self.is_mouse_floating:
            if self.is_mouse_pressed:
                stylename = "SkButton:pressed"
            else:
                stylename = "SkButton:hover"
        else:
            if self.is_focus:
                stylename = "SkButton:focus"
            else:
                stylename = "SkButton"

        style = self.theme.get_style(stylename)

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
        self._draw_central_text(
            canvas,
            text=self.attributes["text"],
            fg=style["fg"],
            canvas_x=self.canvas_x,
            canvas_y=self.canvas_y,
            width=self.width,
            height=self.height,
        )

    # endregion
