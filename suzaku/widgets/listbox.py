import skia

from .card import SkCard
from .container import SkContainer
from .listitem import SkListItem


class SkListBox(SkCard):
    def __init__(
        self,
        parent: SkContainer,
        style: str = "SkListBox",
        lists: list[str] | None = None,
        **kwargs,
    ):
        super().__init__(parent, style=style, **kwargs)

        self.lists: list[SkListItem] = [] if lists is None else lists
        self.selected_item: SkListItem | None = None
        for item in self.lists:
            if isinstance(item, SkListBox):
                self.lists.append(item)
            if isinstance(item, str):
                self.lists.append(SkListItem(self, text=item))
            self.lists[-1].box(side="top", padx=3, pady=2)

    def append(self, item: SkListItem):
        self.lists.append(item)
