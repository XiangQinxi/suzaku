from ..event import SkEvent
from .container import SkContainer
from .popupmenu import SkPopupMenu
from .lineinput import SkLineInput
from .button import SkButton
from .text import SkText


class SkComboBox(SkButton):
    def __init__(
        self,
        parent: SkContainer,
        style: str = "SkComboBox",
        editable: bool = True,
        **kwargs,
    ):
        super().__init__(
            parent, style=style, command=lambda _=None: self._on_click(_), **kwargs
        )

        self.attributes["editable"]: bool = editable

        self.popupmenu = SkPopupMenu(self.parent)
        self.popupmenu.add_command("asdf1")
        self.input = SkLineInput(self)
        self.text = SkText(
            self,
        )

        self.help_parent_scroll = True

    def draw_widget(self, canvas, rect, style_name: str | None = None) -> None:
        style = super().draw_widget(canvas, rect, style_name)
        if self.cget("editable"):
            self.input.fixed(0, 0, self.width - self.height, self.height)
        else:
            self.input.layout_forget()

    def _on_click(self, event: SkEvent):
        if self.popupmenu and not self.cget("disabled"):
            if self.popupmenu.is_popup:
                self.popupmenu.hide()
            else:
                self.popupmenu.popup(
                    x=self.x - self.parent.x_offset,
                    y=self.y - self.parent.y_offset + self.height + 5,
                    width=self.width,
                )
