import skia

from .color import skcolor_to_color, style_to_color
from .theme import SkTheme


class SkDropShadow:
    """A class for handling shadow styles."""

    def draw(self, paint):
        """Set the ImageFilter property of a given `skia.Paint` to draw shadows.

        :param paint:
        :return:
        """
        if self.obj:
            paint.setImageFilter(self.obj)

    def drop_shadow(
        self, paint, config=None, dx=0, dy=0, sigmaX=0, sigmaY=0, color=None, widget=None
    ):
        """Draw a drop shadow using the given paint.

        :param paint: The paint object to use for drawing the shadow.
        :param config: A list of configuration parameters for the shadow.
        :param dx: The offset in the x-direction.
        :param dy: The offset in the y-direction.
        :param sigmaX: The standard deviation in the x-direction.
        :param sigmaY: The standard deviation in the y-direction.
        :param color: The color of the drop shadow.
        :param widget: The widget to use for theming the shadow color.
        :return: None
        """
        if config:
            dx, dy, sigmaX, sigmaY, color = config
        self.set_drop_shadow(dx, dy, sigmaX, sigmaY, color, widget)
        self.draw(paint)

    def set_drop_shadow(self, dx, dy, sigmaX, sigmaY, color, widget=None):
        """Set the drop shadow parameters.

        :param dx: The offset in the x-direction.
        :param dy: The offset in the y-direction.
        :param sigmaX: The standard deviation in the x-direction.
        :param sigmaY: The standard deviation in the y-direction.
        :param color: The color of the drop shadow.
        :return: None
        """
        if widget:
            color = skcolor_to_color(style_to_color(color, widget.theme))
        else:
            color = skcolor_to_color(color)

        self.obj = skia.ImageFilters.DropShadow(
            dx=dx,
            dy=dy,
            sigmaX=sigmaX,
            sigmaY=sigmaY,
            color=color,
        )
