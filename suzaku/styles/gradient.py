from typing import Literal

import skia
from .color_old import color

def linear_gradient(widget, paint, *args, **kwargs):
    gradient = SkGradient(widget)
    gradient.set_linear(*args, **kwargs)
    gradient.set_gradient(paint=paint)


class SkGradient:
    def __init__(self, widget):
        """Initialize gradient
        :param widget: Widget
        """
        self.widget = widget
        self.gradient: skia.GradientShader | None = None

    def draw(self, paint):
        """Draw gradient
        :param paint: Paint
        :return: None
        """
        if self.gradient is None:
            return
        paint.setShader(self.gradient)

    def get(self) -> skia.GradientShader:
        """Get gradient shader
        :return: Gradient shader
        """
        return self.gradient

    def get_anchor_pos(self, anchor):
        """Get widget`s anchor position(Relative widget position, not absolute position within the window)
        相对组件位置，非窗口中的绝对位置

        :param anchor: Anchor position
        :return: Anchor position in widget
        """
        width = self.widget.width
        height = self.widget.height
        match anchor:
            case "nw":
                return 0, 0
            case "n":
                return width / 2, 0
            case "ne":
                return width, 0
            case "w":
                return 0, height / 2
            case "e":
                return width, height / 2
            case "sw":
                return 0, height
            case "s":
                return width / 2, height
            case "se":
                return width, height
            case _:
                return 0, 0

    def set_gradient(self, paint: skia.Paint):
        paint.setShader(self.get())

    def set_linear(
        self,
        configs=None,  # {"start_anchor": "n", "end_anchor": "s", "start": "red", "end": "blue"}
    ):
        """Set linear gradient

        Example:
            >>> gradient.set_linear({"start_anchor": "n", "end_anchor": "s", "start": "red", "end": "blue"})

        :param configs: Gradient configs
        :return: cls
        """

        if configs:

            if "start_anchor" in configs:
                start_anchor = configs["start_anchor"]
                del configs["start_anchor"]
            else:
                start_anchor: Literal["nw", "n", "ne", "w", "e", "sw", "s", "se"] = "n"
            if "end_anchor" in configs:
                end_anchor = configs["end_anchor"]
                del configs["end_anchor"]
            else:
                end_anchor: Literal["nw", "n", "ne", "w", "e", "sw", "s", "se"] = "s"

            colors = []
            for colr in configs["colors"]:
                colors.append(color(colr))

            self.gradient = skia.GradientShader.MakeLinear(
                points=[
                    tuple(self.get_anchor_pos(start_anchor)),
                    tuple(self.get_anchor_pos(end_anchor))
                ],  # [ (x, y), (x1, y1) ]
                colors=colors,  # [ Color1, Color2, Color3 ]
            )
            return self
        else:
            return None