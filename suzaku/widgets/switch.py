import typing

import skia

from ..var import SkBooleanVar
from .switchbox import SkSwitchBox
from .frame import SkFrame
from .text import SkText


class SkSwitch(SkFrame):
    def __init__(
        self,
        *args,
        cursor: typing.Union[str, None] = "hand",
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

        self.switchbox = SkSwitchBox(
            self,
            command=command,
            cursor=cursor,
        )
        self.label = SkText(self, text=text, align="left", cursor=cursor)

        def _(__):
            self.switchbox.invoke()
            self.switchbox.focus_set()

        self.label.bind("click", _)
        self.bind("click", _)

        self.command = command

    def set_attribute(self, **kwargs):
        if "cursor" in kwargs:
            cursor = kwargs.pop("cursor")
            self.attributes["cursor"] = cursor
            self.label.attributes["cursor"] = cursor
            self.switchbox.attributes["cursor"] = cursor
        if "variable" in kwargs:
            self.switchbox.configure(variable=kwargs.pop("variable"))
        super().set_attribute(**kwargs)

    def invoke(self):
        if self.cget("disabled"):
            return
        self.switchbox.invoke()

    @property
    def checked(self):
        return self.switchbox.checked

    def draw_widget(self, canvas: skia.Canvas, rect: skia.Rect) -> None:
        padx = 3
        ipadx = 5
        pady = 7
        width = 2 * (self.height - pady * 2)
        self.switchbox.fixed(
            padx,
            pady,
            width=width,
            height=self.height - pady * 2,
        )
        self.label.fixed(width + ipadx, 0, height=self.height)
