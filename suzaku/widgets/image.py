import typing

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
        fill: typing.Literal["both", "x", "y"] | None = None,
        anchor: typing.Literal[
            "nw", "n", "ne", "e", "se", "s", "sw", "w", "center"
        ] = "center",
        **kwargs,
    ) -> None:
        super().__init__(parent, **kwargs)
        self.path: str = path
        self.image: skia.Image | None

        self.attributes["fill"] = fill
        self.attributes["anchor"] = anchor
        self.attributes["width"] = None
        self.attributes["height"] = None

        if path:
            self.image: skia.Image = skia.Image.open(path)
        else:
            self.image = None

    def resize(self, width: int, height: int) -> None:
        """Resize image to width and height"""
        self.image.resize(width, height)
        self.configure(width=width, height=height)

    @property
    def image_width(self):
        return self.image.width()

    @property
    def image_height(self):
        return self.image.height()

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
            if self.cget("width"):
                _width = self.cget("width")
            else:
                _width = self.image_width
        else:
            _width = 0
        return _width

    @property
    def dheight(self):
        if self.image:
            if self.cget("height"):
                _height = self.cget("height")
            else:
                _height = self.image_height
        else:
            _height = 0
        return _height

    def draw_widget(self, canvas, rect) -> None:
        """Draw image

        :param canvas: skia.Surface to draw on
        :param rect: not needed (defined in SkWidget._draw_image)

        :return: None
        """

        x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()

        match self.cget("fill"):
            case "both":
                pass
            case "x":
                h = self.dheight
            case "y":
                w = self.dwidth
            case None:
                w, h = self.dwidth, self.dheight
                x, y = rect.centerX() - w / 2, rect.centerY() - h / 2

        rect = skia.Rect.MakeXYWH(x, y, w, h)

        self._draw_image_rect(canvas, rect, self.image)
