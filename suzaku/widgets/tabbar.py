from .widget import SkWidget
from .container import SkContainer
from .frame import SkFrame
from .tabbutton import SkTabButton


class SkTabBar(SkFrame):
    def __init__(self, parent: SkContainer, **kwargs):
        super().__init__(parent, **kwargs)

        self.event_generate("selected")

        self.items = []
        self.selected_item: SkWidget | None = None

    def select(self, index: int):
        self.selected_item = self.items[index]
        self.event_trigger("selected", index)

    def add(self, text: str | None = None, **kwargs) -> None:
        button = SkTabButton(self, text=text, **kwargs)
        button.box(side="left", padx=(3, 0), pady=3)
        self.items.append(button)
