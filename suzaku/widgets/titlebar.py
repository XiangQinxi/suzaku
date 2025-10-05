from ..event import SkEvent
from .card import SkCard
from .container import SkContainer
from .text import SkText
from .textbutton import SkTextButton
from .image import SkImage


class SkTitleBar(SkCard):
    def __init__(
        self,
        parent: SkContainer,
        style: str = "SkTitleBar",
        **kwargs,
    ):
        super().__init__(parent, style=style, **kwargs)

        self.icon = SkImage(self, path=self.window.wm_iconpath())
        self.icon.resize(15, 15)
        self.icon.box(side="left", padx=(10, 0))

        self.title = SkText(self, text=self.window.title())
        self.title.box(
            side="left",
        )

        self.close = SkTextButton(self, text="×", command=self.window.destroy)
        # self.close_theme = self.close.theme.special("SkButton:rest", radius=99)
        self.close.box(side="right")

        self.bind("mouse_pressed", self._mouse_pressed)
        self.title.bind("mouse_pressed", self._mouse_pressed)
        self.window.bind("mouse_motion", self._mouse_motion)
        self.window.bind("mouse_released", self._mouse_released)
        self.window.bind("configure", self._window_configure)

        self._x1 = None
        self._y1 = None

    def _window_configure(self, event: SkEvent):
        self.title.configure(text=self.window.title())

    def _mouse_pressed(self, event: SkEvent):
        self._x1 = event.x
        self._y1 = event.y

    def _mouse_motion(self, event: SkEvent):
        if self._x1 and self._x1:
            self.window.move(
                round(event.rootx - self._x1),
                round(event.rooty - self._y1),
            )

    def _mouse_released(self, event: SkEvent):
        self._x1 = None
        self._y1 = None
