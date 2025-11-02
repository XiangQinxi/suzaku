import typing

import skia

from ..var import SkVar
from .frame import SkFrame
from .radiobox import SkRadioBox
from .text import SkText


class SkRadioItem(SkFrame):
    """Not yet completed"""

    def __init__(
        self,
        *args,
        cursor: typing.Union[str, None] = "arrow",
        command: typing.Union[typing.Callable, None] = None,
        text: str | None = None,
        style: str = "SkRadioItem",
        border: bool = False,
        value: bool | int | float | str | None = None,
        variable: SkVar | None = None,
        **kwargs,
    ) -> None:
        super().__init__(*args, style=style, **kwargs)

        self.attributes["cursor"] = cursor
        self.attributes["border"] = border

        self.focusable = True
        self.help_parent_scroll = True

        self.radiobox = SkRadioBox(
            self, command=command, cursor=cursor, value=value, variable=variable
        )
        # self.checkbox.box(side="left", padx=2, pady=2)
        self.label = SkText(self, text=text, align="left", cursor=cursor)
        # self.label.box(side="right", expand=True, padx=2, pady=2)

        def _(__):
            self.radiobox.invoke()
            self.radiobox.focus_set()

        self.label.bind("click", _)
        self.bind("click", _)

        self.command = command

    def set_attribute(self, **kwargs):
        if "cursor" in kwargs:
            self.attributes["cursor"] = kwargs.pop("cursor")
            self.label.attributes["cursor"] = kwargs.pop("cursor")
            self.radiobox.attributes["cursor"] = kwargs.pop("cursor")
        if "value" in kwargs:
            self.radiobox.config(value=kwargs.pop("value"))
        if "variable" in kwargs:
            self.radiobox.config(variable=kwargs.pop("variable"))
        super().set_attribute(**kwargs)

    def invoke(self):
        pass

    @property
    def checked(self):
        return self.radiobox.checked

    def draw_widget(self, canvas: skia.Canvas, rect: skia.Rect) -> None:
        padx = 3
        ipadx = 5
        pady = 7
        self.radiobox.fixed(padx, pady, width=self.height - pady * 2, height=self.height - pady * 2)
        self.label.fixed(self.height - pady * 2 + ipadx, 0, height=self.height)
