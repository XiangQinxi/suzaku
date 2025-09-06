import typing

import skia

from .checkbox import SkCheckBox
from .frame import SkFrame
from .text import SkText


class SkCheckItem(SkFrame):
    """Not yet completed"""

    def __init__(
        self,
        *args,
        cursor: typing.Union[str, None] = "hand",
        command: typing.Union[typing.Callable, None] = None,
        text: str = "",
        style: str = "SkCheckItem",
        **kwargs,
    ) -> None:
        super().__init__(*args, style=style, **kwargs)

        self.attributes["cursor"] = cursor

        self.focusable = True
        self.help_parent_scroll = True

        self.checkbox = SkCheckBox(self)
        # self.checkbox.box(side="left", padx=2, pady=2)
        self.label = SkText(self, text=text, align="left", cursor="hand")
        # self.label.box(side="right", expand=True, padx=2, pady=2)

        def _(__):
            self.checkbox.invoke()
            self.checkbox.focus_set()

        self.label.bind("b1_pressed", _)

        if command:
            self.label.bind("b1_pressed", lambda _: command())

    def draw_widget(self, canvas: skia.Canvas, rect: skia.Rect) -> None:
        self.checkbox.fixed(2, 5, width=self.height - 10, height=self.height - 10)
        self.label.fixed(
            self.height - 5, 0, width=self.width - self.height, height=self.height
        )
