from .card import SkCard
from .container import SkContainer


class SkComboBox(SkCard):
    def __init__(self, parent: SkContainer, **kwargs):
        super().__init__(parent, **kwargs)
