from .widget import SkWidget
from typing import Union


class SkFrame(SkWidget):
    def __init__(self, parent: Union[SkWidget, "SkWindow"]) -> None:
        super().__init__(parent)

        pass