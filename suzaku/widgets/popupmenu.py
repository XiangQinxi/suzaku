import typing

from .checkitem import SkCheckItem
from .container import SkContainer
from .menuitem import SkMenuItem
from .popup import SkPopup
from .separator import SkSeparator
from .window import SkWindow


class SkPopupMenu(SkPopup):

    def __init__(self, parent: SkWindow | SkContainer, **kwargs):
        super().__init__(parent, **kwargs)

        self.items: list[SkMenuItem | SkSeparator] = []

    def add(self, item: SkMenuItem | SkCheckItem):
        self.items.append(item)

    def add_command(self, text: str = None, command: typing.Callable = None):
        button = SkMenuItem(self, text=text, command=command)
        button.box(side="top", padx=5, pady=(1, 3), ipadx=10)
        self.add(button)
        return button.id

    def add_cascade(self):
        pass

    def add_checkitem(self, text: str = None, command: typing.Callable = None):
        checkitem = SkCheckItem(self, text=text, command=command)
        checkitem.box(side="top", padx=5, pady=(1, 3), ipadx=10)
        self.add(checkitem)
        return checkitem.id

    def add_separator(self):
        separator = SkSeparator(self)
        separator.box(side="top", padx=0, pady=0, ipadx=10)
        self.add(separator)
        return separator.id

    def remove_item(self, _id):
        for item in self.items:
            if item.id == _id:
                self.items.remove(item)

    def configure_item(self, _id, **kwargs):
        for item in self.items:
            if item.id == _id:
                self.items[_id].configure(**kwargs)

    config_item = configure_item
