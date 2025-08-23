import typing

from ..event import SkEvent
from .container import SkContainer
from .window import SkWindow
from .textbutton import SkTextButton
from .card import SkCard


class SkMenuItem(SkTextButton):
    def __init__(self, parent: SkContainer, text: str = "", **kwargs):
        super().__init__(parent, text=text, **kwargs)

        self.bind("click", self._on_click)

    def _on_click(self, event: SkEvent):
        self.parent.event_trigger("hide", SkEvent(event_type="hide"))


class SkPopupMenu(SkCard):
    def __init__(self, parent: SkWindow = None, **kwargs):
        super().__init__(parent, **kwargs)

        self.focusable = True

        self.items: list[SkMenuItem] = []
        self.event_generate("hide")
        self.bind("hide", self._hide)

        # 【来检查是否需要关闭改弹出菜单】
        self.window.bind("mouse_released", self._mouse_released)

        self.skip = False

    def popup(
        self,
        x: int,
        y: int,
    ):
        self.focus_set()
        self.fixed(x, y, width=self.content_width, height=self.content_height)

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


class SkMenuButton(SkTextButton):
    def __init__(
        self, parent: SkContainer, menu: SkPopupMenu, text: str = "", **kwargs
    ):
        super().__init__(parent, text=text, **kwargs)

        self.popupmenu = menu
        self.bind("click", self._on_click)

    def _on_click(self, event: SkEvent):
        self.popupmenu.popup(self.canvas_x, self.canvas_y + self.height)
