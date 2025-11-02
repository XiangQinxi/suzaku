import typing

import skia

from ..var import SkBooleanVar
from .checkbox import SkCheckBox
from .frame import SkFrame
from .text import SkText


class SkCheckItem(SkFrame):
    """Not yet completed"""

    def __init__(
        self,
        *args,
        cursor: typing.Union[str, None] = "arrow",
        command: typing.Union[typing.Callable, None] = None,
        text: str | None = None,
        style: str = "SkCheckItem",
        border: bool = False,
        variable: SkBooleanVar | None = None,
        **kwargs,
    ) -> None:
        super().__init__(*args, style=style, **kwargs)

        self.attributes["cursor"] = cursor
        self.attributes["border"] = border

        self.focusable = True
        self.help_parent_scroll = True

        self.checkbox = SkCheckBox(self, command=command, cursor=cursor, variable=variable)
        # self.checkbox.box(side="left", padx=2, pady=2)
        self.label = SkText(self, text=text, align="left", cursor=cursor)
        # self.label.box(side="right", expand=True, padx=2, pady=2)

        def _(__):
            self.checkbox.invoke()
            self.checkbox.focus_set()

        self.label.bind("click", _)
        self.bind("click", _)

        self.command = command

    def set_attribute(self, **kwargs):
        if "cursor" in kwargs:
            cursor = kwargs.pop("cursor")
            self.attributes["cursor"] = cursor
            self.label.attributes["cursor"] = cursor
            self.checkbox.attributes["cursor"] = cursor
        if "variable" in kwargs:
            self.checkbox.configure(variable=kwargs.pop("variable"))
        super().set_attribute(**kwargs)

    def invoke(self):
        if self.cget("disabled"):
            return
        self.checkbox.invoke()

    @property
    def checked(self):
        return self.checkbox.checked

    def draw_widget(self, canvas: skia.Canvas, rect: skia.Rect) -> None:
        padx = 3
        ipadx = 5
        pady = 7
        self.checkbox.fixed(padx, pady, width=self.height - pady * 2, height=self.height - pady * 2)
        self.label.fixed(self.height - pady * 2 + ipadx, 0, height=self.height)
