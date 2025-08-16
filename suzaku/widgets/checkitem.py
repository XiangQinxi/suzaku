from typing import Union

from suzaku.widgets.checkbox import SkCheckBox
from suzaku.widgets.frame import SkFrame
from suzaku.widgets.text import SkText


class SkCheckItem(SkFrame):
    """Not yet completed"""

    def __init__(
        self,
        *args,
        size: tuple[int, int] = (105, 35),
        cursor: Union[str, None] = "hand",
        command: Union[callable, None] = None,
        text: str = "",
        **kwargs,
    ) -> None:
        super().__init__(*args, size=size, **kwargs)

        self.attributes["cursor"] = cursor

        self.focusable = True

        self.checkbox = SkCheckBox(self)
        self.checkbox.box(side="left", padx=2, pady=2)
        self.label = SkText(self, text=text)
        self.label.box(side="left", padx=2, pady=2)

        if command:
            self.bind("click", lambda _: command())
