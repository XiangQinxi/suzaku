from ..con import Orient
from .card import SkCard
from .container import SkContainer
from .frame import SkFrame
from .separator import SkSeparator
from .tabbar import SkTabBar


class SkTabs(SkCard):
    def __init__(self, parent: SkContainer, style: str = "SkTabs", **kwargs) -> None:
        super().__init__(parent, style=style, **kwargs)

        self.tabs = []
        self.selected: SkFrame | None = None
        self.tabbar: SkTabBar = SkTabBar(self)
        self.tabbar.box(side="top", padx=2, pady=2)
        self.tabbar.bind("selected", self._select)
        self.separator = SkSeparator(self, orient=Orient.H)
        self.separator.box(side="top", padx=0, pady=0)

    def select(self, index: int) -> None:
        self.tabbar.select(index)

    def _select(self, index: int) -> None:
        if self.tabbar.items[index] == self.selected:
            return
        if self.selected:
            self.selected.layout_forget()
        self.selected = self.tabs[index]
        self.selected.box(side="bottom", expand=True, padx=0, pady=(5, 2))

    def add(self, tab: SkContainer, text: str | None = "") -> None:
        self.tabs.append(tab)
        self.tabbar.add(text)
