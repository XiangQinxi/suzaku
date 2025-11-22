from .container import SkContainer
from .widget import SkWidget


class SkEmpty(SkWidget):
    """Empty element, used only as a placeholder in layouts."""

    def __init__(self, parent: SkContainer, **kwargs) -> None:
        """Initialize empty element.

        :param args: SkWidget arguments
        :param size: Default size
        :param kwargs: SkWidget arguments
        :return: None
        """
        super().__init__(parent, **kwargs)
        self.help_parent_scroll = True

    @property
    def dwidth(self):
        """Get default width.

        :return: Default width
        """
        return 0

    @property
    def dheight(self):
        """Get default height.

        :return: Default height
        """
        return 0

    def draw_widget(self, canvas, rect) -> None:
        """Draw method, does nothing.

        :param canvas: skia.Surface to draw on
        :param rect: Rectangle to draw in
        :return: None
        """
        ...
