from typing import Any

import skia

from .container import SkContainer
from .widget import SkWidget


class SkImage(SkWidget):
    """Just a Image widget

    :param image: path of image file
    :param size: size of image
    """

    def __init__(
        self,
        parent: SkContainer,
        path: str | None = None,
        **kwargs,
    ) -> None:
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.path = path
        if path:
            self.image: skia.Image = skia.Image.open(path)
        else:
            self.image = None

    def path(self, filename: str | None = None) -> str | None:
        if filename:
            self.path = filename
            if self.image:
                self.image.close()
            self.image: skia.Image = skia.Image.open(filename)
        else:
            return self.path
        return self.path

    @property
    def dwidth(self):
        if self.image:
            _width = self.image.width()
        else:
            _width = 0
        return _width

    @property
    def dheight(self):
        if self.image:
            _height = self.image.height()
        else:
            _height = 0
        return _height

    def draw_widget(self, canvas, rect) -> None:
        """Draw image

        :param canvas: skia.Surface to draw on
        :param rect: not needed (defined in SkWidget._draw_image)

        :return: None
        """
        self._draw_image(canvas, rect, self.image)
