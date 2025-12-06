from ..event import SkEvent
from .container import SkContainer
from .frame import SkFrame
from .tabbutton import SkTabButton
from .widget import SkWidget


class SkTabBar(SkFrame):
    """A tab bar"""

    def __init__(
        self,
        parent: SkContainer,
        style: str = "SkTabBar",
        expand: bool = True,
        **kwargs,
    ):
        super().__init__(parent, style=style, **kwargs)

        self.attributes["expand"]: bool = expand

        self.items: list[SkTabButton] = []
        self.selected_item: SkWidget | None = None

    def delete_all(self):
        """Delete all tab buttons"""
        for item in self.items:
            item.layout_forget()
            item.destroy()
        self.items.clear()
        self.selected_item = None

    def delete(self, index: int):
        """Delete a tab button by index

        :param index: The index of the tab button
        :return: None
        """
        self.items.pop(index).layout_forget()
        self.update_order()

    def select(self, index: int):
        """Select item by index

        :param index: The index of the item
        :return: None
        """
        if self.selected_item is not self.items[index]:
            self.selected_item = self.items[index]
            self.trigger(
                "change",
                SkEvent(widget=self, event_type="change", index=index, item=self.selected_item),
            )

    def update_order(self):
        """Update the order of the tab buttons

        :return: None
        """
        for index, item in enumerate(self.items):
            if index == len(self.items) - 1:
                padx = (1, 3)
            elif index == 0:
                padx = (3, 1)
            item.box(side="left", padx=padx, pady=3, expand=self.cget("expand"))

    def add(self, text: str | None = None, widget: SkWidget = None, **kwargs) -> SkTabButton:
        """Add a tab button

        :param text: The text of the tab button
        :param widget: The widget of the tab button
        :param kwargs: The keyword arguments
        :return: The tab button
        """

        button = SkTabButton(self, text=text, **kwargs)
        self.items.append(button)
        self.update_order()
        return button
