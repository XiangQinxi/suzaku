from .container import SkContainer
from .frame import SkFrame
from .tabbutton import SkTabButton
from .widget import SkWidget


class SkTabBar(SkFrame):
    """A tab bar"""

    def __init__(self, parent: SkContainer, style: str = "SkTabBar", **kwargs):
        super().__init__(parent, style=style, **kwargs)

        self.event_generate("selected")

        self.items = []
        self.selected_item: SkWidget | None = None

    def select(self, index: int):
        """Select item by index

        :param index: The index of the item
        :return: None
        """
        self.selected_item = self.items[index]
        self.event_trigger("selected", index)

    def add(
        self, text: str | None = None, widget: SkWidget = None, **kwargs
    ) -> SkTabButton:
        """Add a tab button

        :param text: The text of the tab button
        :param widget: The widget of the tab button
        :param kwargs: The keyword arguments
        :return: The tab button
        """
        button = SkTabButton(self, text=text, **kwargs)
        button.box(side="left", padx=(3, 0), pady=3)
        self.items.append(button)
        return button
