import typing

import skia

from ..const import Orient
from ..event import SkEvent
from .card import SkCard
from .container import SkContainer
from .listitem import SkListItem
from .separator import SkSeparator


class SkListBox(SkCard):
    def __init__(
        self,
        parent: SkContainer,
        style: str = "SkListBox",
        items: list[str] | None = None,
        **kwargs,
    ):
        super().__init__(parent, style=style, **kwargs)

        self.items: list[SkListItem] = []
        self.selected_item: SkListItem | None = None

        for item in items:
            self.append(item)

        self.bind_scroll_event()

    def item(self, index: int) -> SkListItem:
        """Get the item with the specified index.【获取指定索引的项】

        :param int index: Item index.【项索引】
        :return: Item.【项】
        """
        return self.items[index]

    def index(self, item: SkListItem) -> int:
        return self.items.index(item)

    def update_order(self):
        for index, item in enumerate(self.items):
            padx = 0
            pady = 0
            ipadx = 10
            if isinstance(item, SkSeparator):
                pady = 2
            else:
                padx = 3
                if index != len(self.items) - 1:
                    pady = (2, 0)
                elif ipadx == 0:
                    pady = (0, 2)
                else:
                    pady = (2, 4)
            item.box(side="top", padx=padx, pady=pady, ipadx=ipadx)

    def select(
        self, item: SkListItem | None = None, index: int | None = None
    ) -> int | typing.Self | None:
        if item:
            self.selected_item = item
            self.trigger("changed", self.items.index(item))
            return self
        if index:
            self.selected_item = self.item(index)
            self.trigger("changed", index)
            return self
        return self.index(self.selected_item) if self.selected_item else None

    def append(self, item: SkListItem | str):
        if isinstance(item, SkListItem):
            self.items.append(item)
        elif isinstance(item, str):
            item = SkListItem(self, text=item)
            self.items.append(item)
        self.update_order()
