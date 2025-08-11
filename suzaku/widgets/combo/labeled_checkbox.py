from typing import Union

from ..checkbox import SkCheckBox
from ..frame import SkFrame
from ..text import SkText


class SkLabeledCheckbox(SkFrame):
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
        self.checkbox.box(side="left", expand=True, padx=2, pady=2)
        self.label = SkText(self, text=text)
        self.label.box(side="left", expand=True, padx=2, pady=2)
