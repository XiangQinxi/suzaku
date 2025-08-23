import typing

from ..event import SkEvent
from .card import SkCard
from .container import SkContainer
from .menuitem import SkMenuItem
from .window import SkWindow


class SkPopupMenu(SkCard):

    def __init__(self, parent: SkWindow | SkContainer, **kwargs):
        super().__init__(parent, **kwargs)

        self.focusable = True

        self.items: list[SkMenuItem] = []
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
            width = self.content_width
        if "height" in kwargs:
            height = kwargs.pop("height")
        else:
            height = self.content_height
        self.fixed(**kwargs, width=width, height=height)

    def _mouse_released(self, event: SkEvent):
        if not self.is_focus:
            self.hide()

    def _hide(self, event: SkEvent):
        if self.skip:
            self.skip = False
            return
        self.hide()

    def add_command(self, text: str = None, command: typing.Callable = None):
        button = SkMenuItem(self, text=text, command=command)
        button.box(side="top", padx=5, pady=(5, 0))
        self.items.append(button)
        return button.id

    def remove_item(self, _id):
        for item in self.items:
            if item.id == _id:
                self.items.remove(item)

    def configure_item(self, _id, **kwargs):
        for item in self.items:
            if item.id == _id:
                self.items[_id].configure(**kwargs)

    config_item = configure_item
