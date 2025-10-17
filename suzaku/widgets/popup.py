from ..event import SkEvent
from .card import SkCard
from .container import SkContainer
from .window import SkWindow


class SkPopup(SkCard):
    def __init__(self, parent: SkWindow | SkContainer, **kwargs):
        super().__init__(parent, **kwargs)

        self.focusable = True

        self.bind("hide", self._hide)

        # 【来检查是否需要关闭改弹出菜单】
        self.window.bind("mouse_released", self._mouse_released)
        self.hide()

        self.skip = False
        self.visible = False

    @property
    def is_popup(self):
        return self.visible

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

    def _mouse_released(self, event: SkEvent = None):
        if not self.is_focus:
            self.hide()

    def _hide(self, event: SkEvent = None):
        if self.skip:
            self.skip = False
            return
        self.hide()
