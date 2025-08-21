import typing

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
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        self.attributes["cursor"] = cursor

        self.focusable = True

        self.checkbox = SkCheckBox(self)
        self.checkbox.box(side="left", padx=2, pady=2)
        self.label = SkText(self, text=text)
        self.label.box(side="left", padx=2, pady=2)

        if command:
            self.bind("click", lambda _: command())
