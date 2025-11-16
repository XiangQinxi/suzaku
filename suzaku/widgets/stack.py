from .card import SkCard
from .container import SkContainer
from .frame import SkFrame


class SkStack(SkFrame):
    """A stack widget"""

    def __init__(
        self,
        parent: SkContainer,
        *,
        style: str = "SkStack",
        **kwargs,
    ) -> None:
        super().__init__(parent, style=style, **kwargs)

        self.containers: list[SkContainer] = []
        self.selected: SkFrame | None = None

    def select(self, index) -> None:
        """Select a tab by index
        :param index: The tab index
        :return: None
        """
        if self.containers[index] == self.selected:
            return
        if self.selected:
            self.selected.layout_forget()
        self.selected = self.containers[index]
        self.selected.box(side="top", expand=True, padx=0, pady=(0, 0))

    def add(self, container: SkContainer) -> int:
        """Add a tab
        :param container: The container
        :return: The tab widget
        """
        self.containers.append(container)
        return self.containers.index(container)
