from .container import SkContainer
from .frame import SkFrame


class SkTabBar(SkFrame):
    def __init__(self, parent: SkContainer, **kwargs):
        super().__init__(parent, **kwargs)
