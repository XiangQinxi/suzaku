from .card import SkCard
from .container import SkContainer
from ..event import SkEvent
from .window import SkWindow


class SkPopup(SkCard):
    def __init__(self, parent: SkWindow | SkContainer, **kwargs):
        super().__init__(parent, **kwargs)

        self.focusable = True

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
