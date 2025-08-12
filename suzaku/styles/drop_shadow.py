import skia

from .color import make_color


class SkDropShadow:
    """A class for handling shadow styles.

    :param dx: The offset in the x-direction.
    :param dy: The offset in the y-direction.
    :param sigmaX: The standard deviation in the x-direction.
    :param sigmaY: The standard deviation in the y-direction.
    :param colr: The color of the drop shadow.
    """

    def __init__(self, dx=0, dy=0, sigmaX=0, sigmaY=0, colr=None, config_list=None):
        if config_list:
            self.dx = config_list[0]
            self.dy = config_list[1]
            self.sigmaX = config_list[2]
            self.sigmaY = config_list[3]
            self.colr = config_list[4]
        else:
            self.dx = dx
            self.dy = dy
            self.sigmaX = sigmaX
            self.sigmaY = sigmaY
            self.colr = colr

    def draw(self, paint):
        """Set the ImageFilter property of a given `skia.Paint` to draw shadows.

        :param paint:
        :return:
        """
        paint.setImageFilter(self.get())

    def set(self, dx, dy, sigmaX, sigmaY, colr):
        """Set the drop shadow parameters.

        :param dx: The offset in the x-direction.
        :param dy: The offset in the y-direction.
        :param sigmaX: The standard deviation in the x-direction.
        :param sigmaY: The standard deviation in the y-direction.
        :param colr: The color of the drop shadow.
        :return: None
        """
        self.dx = dx
        self.dy = dy
        self.sigmaX = sigmaX
        self.sigmaY = sigmaY
        self.colr = colr

    def get(self):
        """
        Get the drop shadow filter.

        :return: The drop shadow filter.
        """
        if self.colr is None:
            return None
        return skia.ImageFilters.DropShadow(
            dx=self.dx,
            dy=self.dy,
            sigmaX=self.sigmaX,
            sigmaY=self.sigmaY,
            color=make_color(self.colr),
        )
