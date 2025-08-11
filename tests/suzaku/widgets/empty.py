from .widget import SkWidget


class SkEmpty(SkWidget):
    """
    Empty element, used only as a placeholder in layouts.
    """

    def __init__(self, *args, size=(0, 0), **kwargs) -> None:
        """Initialize empty element.

        :param args: SkWidget arguments
        :param size: Default size
        :param kwargs: SkWidget arguments
        :return: None
        """
        super().__init__(*args, size=size, name="sk_empty", **kwargs)

    def _draw(self, canvas, rect) -> None:
        """Draw method, does nothing.

        :param canvas: skia.Surface to draw on
        :param rect: Rectangle to draw in
        :return: None
        """
        ...
