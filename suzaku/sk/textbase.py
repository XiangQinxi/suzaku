from .visual import SkVisual
from typing import Union


class SkTextBase(SkVisual):

    from .window import SkWindow

    def __init__(self, parent: Union[SkWindow, "SkVisual"], text: str = "", size: tuple[int, int] = (100, 30), style: str = "", id: str = None) -> None:
        super().__init__(parent, size, style, id)
        self.text = text
