from typing import Any

from .widget import SkWidget


class SkImage(SkWidget):
    """Just a Image widget

    :param image: path of image file
    :param size: size of image
    """

    def __init__(
        self, parent, path: str, x: int, y: int, width: int, height: int
    ) -> None:
        super().__init__(parent, (width, height))
        self.parent = parent
        self.width: int = width
        self.height: int = height
        self.path = path
        self.x: int = x
        self.y: int = y

    def draw_widget(self, canvas, rect) -> None:
        """Draw image

        :param canvas: skia.Surface to draw on
        :param rect: not needed (defined in SkWidget._draw_image)

        :return: None
        """
        if self.path:
            path = self.path
        else:
            path = None
        self._draw_image(canvas, path=path, uri=None, rect=rect)
