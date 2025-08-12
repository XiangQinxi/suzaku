from typing import Union

from ..text import SkText


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
            sheets = self.theme.styles["SkButton"][
                f"{"pressed" if self.is_mouse_pressed else "hover"}"
            ]
        else:
            sheets = self.theme.styles["SkButton"][
                f"{"focus" if self.is_focus else "rest"}"
            ]
        if "bg_shader" in sheets:
            bg_shader = sheets["bg_shader"]
        else:
            bg_shader = None

        if "bd_shadow" in sheets:
            bd_shadow = sheets["bd_shadow"]
        else:
            bd_shadow = None
        if "bd_shader" in sheets:
            bd_shader = sheets["bd_shader"]
        else:
            bd_shader = None

        print(self.theme.get_style("SkButton:radius"))

        self._draw_frame(
            canvas,
            rect,
            radius=self.theme.get_style("SkButton", "radius"),
            bg=sheets["bg"],
            width=sheets["width"],
            bd=sheets["bd"],
            bd_shadow=bd_shadow,
            bd_shader=bd_shader,
            bg_shader=bg_shader,
        )
        self._draw_central_text(
            canvas,
            text=self.attributes["text"],
            fg=sheets["fg"],
            canvas_x=self.canvas_x,
            canvas_y=self.canvas_y,
            width=self.width,
            height=self.height,
        )

    # endregion
