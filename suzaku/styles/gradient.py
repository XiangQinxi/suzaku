from typing import Literal

import skia
from svgwrite.data.pattern import percentage


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

    def get(self):
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

    def set_linear(
        self,
        start: Literal["nw", "n", "ne", "w", "e", "sw", "s", "se"],  # n
        end: Literal["nw", "n", "ne", "w", "e", "sw", "s", "se"],  # s
        points_and_colors: dict[
            str, skia.Color
        ] = None,  # {"0%": Color1, "100%": Color2}
    ):
        """
        Set linear gradient
        :param start: Start position
        :param end: End position
        :param points_and_colors: Points and colors
        :return:
        """

        start_pos = self.get_anchor_pos(start)
        end_pos = self.get_anchor_pos(end)

        points: list[tuple[float, float]] = []
        colors: list[skia.Color] = []

        for percentage, color in points_and_colors.items():
            p = float(percentage.strip("%")) / 100
            points.append(
                (
                    start_pos[0] + (end_pos[0] - start_pos[0]) * p,  # x pos
                    start_pos[1] + (end_pos[1] - start_pos[1]) * p,  # y pos
                )
            )
            colors.append(color)

        return skia.GradientShader.MakeLinear(
            points=points,  # [ (x, y), (x1, y1), (x2, y2) ]
            colors=colors,  # [ Color1, Color2, Color3 ]
            # tileMode=skia.TileMode.CLAMP
        )
