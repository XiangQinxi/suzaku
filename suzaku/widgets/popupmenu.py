import typing

from ..event import SkEvent
from .card import SkCard
from .checkitem import SkCheckItem
from .container import SkContainer
from .menubutton import SkMenuButton
from .separator import SkSeparator
from .window import SkWindow


class SkPopupMenu(SkCard):

    def __init__(self, parent: SkWindow | SkContainer, **kwargs):
        super().__init__(parent, **kwargs)

        self.focusable = True

        self.items: list[SkMenuButton | SkSeparator] = []
        self.event_generate("hide")
        self.bind("hide", self._hide)

        # 【来检查是否需要关闭改弹出菜单】
        self.window.bind("mouse_released", self._mouse_released)

        self.skip = False

    def popup(self, **kwargs):
        self.focus_set()
        if "width" in kwargs:
            width = kwargs.pop("width")
        else:
            width = None
        if "height" in kwargs:
            height = kwargs.pop("height")
        else:
            height = None
        self.fixed(**kwargs, width=width, height=height)

    def _mouse_released(self, event: SkEvent):
        if not self.is_focus:
            self.hide()

    def _hide(self, event: SkEvent):
        if self.skip:
            self.skip = False
            return
        self.hide()

    def add(self, item: SkMenuButton | SkCheckItem):
        self.items.append(item)

    def add_command(self, text: str = None, command: typing.Callable = None):
        button = SkMenuButton(self, text=text, command=command)
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
