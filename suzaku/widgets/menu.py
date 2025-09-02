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
        **kwargs,
    ):
        super().__init__(parent, text=text, **kwargs)

        self.attributes["popupmenu"] = menu
        self.bind("click", self._on_click)
        self.help_parent_scroll = True

    def _on_click(self, event: SkEvent):
        if self.cget("popupmenu"):
            self.cget("popupmenu").popup(x=self.x, y=self.y + self.height + 10)
            """from tkinter import Menu

            Menu.add_cascade()"""
