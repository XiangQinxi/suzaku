from ..event import SkEvent
from .container import SkContainer
from .popupmenu import SkPopupMenu
from .textbutton import SkTextButton


class SkMenu(SkTextButton):
    def __init__(
        self,
        parent: SkContainer,
        text: str = "",
        menu: SkPopupMenu = None,
        style: str = "SkMenu",
        **kwargs,
    ):
        super().__init__(parent, text=text, style=style, **kwargs)

        self.attributes["popupmenu"] = menu
        self.bind("click", self._on_click)
        self.help_parent_scroll = True

    def _on_click(self, event: SkEvent):
        popupmenu: SkPopupMenu = self.cget("popupmenu")
        if popupmenu and not self.cget("disabled"):
            if popupmenu.is_popup:
                popupmenu.hide()
            else:
                self.cget("popupmenu").popup(
                    x=self.x - self.parent.x_offset,
                    y=self.y - self.parent.y_offset + self.height + 10,
                )
