from .widget import SkWidget
from .elements.border import ElBorder
from typing import Union


class SkFrame(SkWidget):
    def __init__(self, parent: Union[SkWidget, "SkWindow"]) -> None:
        super().__init__(parent)

        self.border = ElBorder(self)
        self.border.fill()

        self.elements.append(self.border)
