import typing

from .checkitem import SkCheckItem
from .radioitem import SkRadioItem
from .container import SkContainer
from .menuitem import SkMenuItem
from .popup import SkPopup
from .separator import SkSeparator
from .window import SkWindow


class SkPopupMenu(SkPopup):

    def __init__(self, parent: SkWindow | SkContainer, **kwargs):
        super().__init__(parent, **kwargs)

        self.items: list[SkMenuItem | SkSeparator | SkCheckItem | SkRadioItem] = []

    def add(self, item: SkMenuItem | SkCheckItem | SkSeparator | SkRadioItem):
        self.items.append(item)

    def add_command(self, text: str | None = None, **kwargs):
        button = SkMenuItem(self, text=text, **kwargs)
        button.box(side="top", padx=5, pady=(1, 3), ipadx=10)
        self.add(button)
        return button.id

    def add_cascade(self):
        pass

    def add_checkitem(self, text: str | None = None, **kwargs):
        checkitem = SkCheckItem(self, text=text, **kwargs)
        checkitem.box(side="top", padx=5, pady=(1, 3), ipadx=10)
        self.add(checkitem)
        return checkitem.id

    add_checkbutton = add_checkitem

    def add_radioitem(self, text: str | None = None, **kwargs):
        radioitem = SkRadioItem(self, text=text, **kwargs)
        radioitem.box(side="top", padx=5, pady=(1, 3), ipadx=10)
        self.add(radioitem)
        return radioitem.id

    add_radiobutton = add_radioitem

    def add_separator(self, **kwargs):
        separator = SkSeparator(self, **kwargs)
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
