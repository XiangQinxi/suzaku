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

        self.event_generate("changed")

        self.items: list[SkListItem] = []
        self.selected_item: SkListItem | None = None

        for item in items:
            self.append(item)

        self.bind_scroll_event()

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

    def selected(
        self, item: SkListItem | None = None
    ) -> SkListItem | typing.Self | None:
        if item:
            self.selected_item = item
            self.event_trigger("changed", SkEvent(event_type="changed", widget=item))
            return self
        return self.selected_item

    def selected_index(self, index: int) -> typing.Self | int:
        if index:
            self.selected(self.items[index])
            return self
        if self.selected_item is None:
            return -1
        return self.items.index(self.selected_item)

    def append(self, item: SkListItem | str):
        if isinstance(item, SkListItem):
            self.items.append(item)
        elif isinstance(item, str):
            item = SkListItem(self, text=item)
            self.items.append(item)
        self.update_order()
