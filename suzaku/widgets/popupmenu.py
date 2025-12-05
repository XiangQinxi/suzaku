import typing

from .checkitem import SkCheckItem
from .container import SkContainer
from .menuitem import SkMenuItem
from .popup import SkPopup
from .radioitem import SkRadioItem
from .separator import SkSeparator
from .switch import SkSwitch
from .window import SkWindow
from .. import SkEvent


class SkPopupMenu(SkPopup):

    def __init__(self, parent: SkWindow | SkContainer, *, style: str = "SkPopup", **kwargs):
        super().__init__(parent, style=style, **kwargs)

        self.items: list[SkMenuItem | SkSeparator | SkCheckItem | SkRadioItem | SkSwitch] = []

    def add(
        self,
        item: SkMenuItem | SkCheckItem | SkSeparator | SkRadioItem | SkSwitch,
        index: int = -1,
    ) -> None:
        """Add a menu item."""
        if index == -1:
            self.items.append(item)
        else:
            self.items.insert(index, item)
        self.update_order()

    def index(self, item: SkMenuItem | SkCheckItem | SkSeparator | SkRadioItem | SkSwitch) -> int:
        """Get the index of a menu item."""
        return self.items.index(item)

    def update_order(self):
        """Update the order of the menu items."""
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

    def add_command(self, text: str | None = None, **kwargs):
        if "command" in kwargs:
            command = kwargs.pop("command")

            def command_wrapper():
                command()
                self.trigger(
                    "command",
                    SkEvent(button, "command", text=text, index=button.index),
                )

        else:

            def command_wrapper():
                self.trigger(
                    "command",
                    SkEvent(button, "command", text=text, index=button.index),
                )

        button = SkMenuItem(self, text=text, command=command_wrapper, **kwargs)
        self.add(button)
        button.index = self.index(button)
        return button.id

    def add_cascade(self):
        pass

    def add_checkitem(self, text: str | None = None, **kwargs):
        checkitem = SkCheckItem(self, text=text, **kwargs)
        self.add(checkitem)
        return checkitem.id

    add_checkbutton = add_checkitem

    def add_switch(self, text: str | None = None, **kwargs):
        switch = SkSwitch(self, text=text, **kwargs)
        self.add(switch)
        return switch.id

    def add_radioitem(self, text: str | None = None, **kwargs):
        radioitem = SkRadioItem(self, text=text, **kwargs)
        self.add(radioitem)
        return radioitem.id

    add_radiobutton = add_radioitem

    def add_separator(self, **kwargs):
        separator = SkSeparator(self, **kwargs)
        self.add(separator)
        return separator.id

    def remove_item(self, _id):
        for item in self.items:
            if item.id == _id:
                self.items.remove(item)

    def configure_item(self, _id, **kwargs):
        """Configure attributes of the item with id"""
        for item in self.items:
            if item.id == _id:
                self.items[_id].configure(**kwargs)

    config_item = configure_item
