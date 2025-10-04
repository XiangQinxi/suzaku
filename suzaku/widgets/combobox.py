from ..event import SkEvent
from .container import SkContainer
from .popupmenu import SkPopupMenu
from .textbutton import SkTextButton


class SkComboBox(SkTextButton):
    def __init__(
        self,
        parent: SkContainer,
        text: str = "",
        style: str = "SkComboBox",
        **kwargs,
    ):
        super().__init__(parent, text=text, style=style, **kwargs)
        self.popupmenu = SkPopupMenu(self.parent)
        self.bind("click", self._on_click)
        self.help_parent_scroll = True

    def _on_click(self, event: SkEvent):
        if self.popupmenu and not self.cget("disabled"):
            if self.popupmenu.is_popup:
                self.popupmenu.hide()
            else:
                self.popupmenu.popup(
                    x=self.x - self.parent.x_offset,
                    y=self.y - self.parent.y_offset + self.height + 10,
                )
