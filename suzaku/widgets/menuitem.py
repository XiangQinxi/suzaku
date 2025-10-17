from ..event import SkEvent
from .container import SkContainer
from .textbutton import SkTextButton


class SkMenuItem(SkTextButton):
    def __init__(
        self,
        parent: SkContainer,
        text: str = "",
        *,
        style="SkMenu",
        align="left",
        **kwargs,
    ):
        super().__init__(parent, text=text, style=style, align=align, **kwargs)

        self.focusable = True

        self.bind("click", self._on_click)
        self.help_parent_scroll = True

    def _on_click(self, event: SkEvent):
        if "hide" in self.parent.events:
            self.parent.trigger("hide", SkEvent(event_type="hide"))
