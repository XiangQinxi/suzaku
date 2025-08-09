from typing import Any, Literal, Union

import skia

from ..styles.color_old import color as _color


class SkColor:
    def __init__(self, color: str) -> None:
        self.color = None
        self.set_color(color)

    def set_color(self, color) -> None:
        typec = type(color)
        if typec is str:
            if color.startswith("#"):
                self.set_color_hex(color)
            self.set_color_name(color)
        elif typec is tuple or typec is list:
            if len(color) == 3:
                self.set_color_rgba(color[0], color[1], color[2])
            elif len(color) == 4:
                self.set_color_rgba(color[0], color[1], color[2], color[3])
            else:
                raise ValueError(
                    "Color tuple/list must have 3 (RGB) or 4 (RGBA) elements"
                )
        return None

    def set_color_name(self, name: str) -> None:
        """Convert color name string to skia color.

        :param name: Color name
        :return skia.Color: Skia color
        :raise ValueError: When color not exists
        """
        try:
            self.color = getattr(skia, f"Color{name.upper()}")
        except:
            raise ValueError(f"Unknown color name: {name}")

    def set_color_rgba(self, r, g, b, a=255):
        """
        转换RGB/RGBA值为Skia颜色

        Args:
            r: 红色通道 (0-255)
            g: 绿色通道 (0-255)
            b: 蓝色通道 (0-255)
            a: 透明度通道 (0-255, 默认255)

        Returns:
            skia.Color: 对应的RGBA颜色对象
        """
        self.color = skia.Color(r, g, b, a)

    def set_color_hex(self, hex: str) -> None:
        """
        转换十六进制颜色字符串为Skia颜色

        Args:
            hex: 十六进制颜色字符串(支持 #RRGGBB 和 #RRGGBBAA 格式)

        Returns:
            skia.Color: 对应的RGBA颜色对象

        Raises:
            ValueError: 当十六进制格式无效时抛出
        """
        hex_color = hex.lstrip("#")
        if len(hex_color) == 6:  # RGB 格式，默认不透明(Alpha=255)
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            self.color = skia.ColorSetRGB(r, g, b)  # 返回不透明颜色
        elif len(hex_color) == 8:  # RGBA 格式(含 Alpha 通道)
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            a = int(hex_color[6:8], 16)
            self.color = skia.ColorSetARGB(a, r, g, b)  # 返回含透明度的颜色
        else:
            raise ValueError("HEX 颜色格式应为 #RRGGBB 或 #RRGGBBAA")


class SkGradient:
    def __init__(self):
        """Initialize gradient

        :param widget: Widget
        """
        # self.widget = widget
        self.gradient: skia.GradientShader | None = None

    def draw(self, paint: skia.Paint) -> skia.Paint:
        """Draw gradient

        :param paint: Paint
        :return: None
        """
        if self.gradient is None:
            return None
        paint.setShader(self.gradient)
        return paint

    def get(self) -> skia.GradientShader:
        """Get gradient shader

        :return: Gradient shader
        """
        return self.gradient

    @staticmethod
    def get_anchor_pos(widget: "SkWidget", anchor) -> tuple[int, int]:
        """Get widget`s anchor position(Relative widget position, not absolute position within the
        window)

        :param widget: The SkWidget
        :param anchor: Anchor position
        :return: Anchor position in widget
        """
        width = widget.width
        height = widget.height
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
        config: (
            dict | None
        ) = None,  # {"start_anchor": "n", "end_anchor": "s", "start": "red", "end": "blue"}
        widget=None,
        start_pos: tuple[int, int] = None,
        end_pos: tuple[int, int] = None,
    ):
        """Set linear gradient

        ## Example
        `gradient.set_linear({"start_anchor": "n", "end_anchor": "s",
        "start": "red", "end": "blue"})`

        :param end_pos: End position
        :param start_pos: Start position
        :param widget: Widget
        :param config: Gradient configs
        :return: cls
        """

        if config:
            if start_pos is None or end_pos is None:
                if widget:
                    if "start_anchor" in config:
                        start_anchor = config["start_anchor"]
                        del config["start_anchor"]
                    else:
                        start_anchor: Literal[
                            "nw", "n", "ne", "w", "e", "sw", "s", "se"
                        ] = "n"
                    if "end_anchor" in config:
                        end_anchor = config["end_anchor"]
                        del config["end_anchor"]
                    else:
                        end_anchor: Literal[
                            "nw", "n", "ne", "w", "e", "sw", "s", "se"
                        ] = "s"

            colors = []
            for color in config["colors"]:
                colors.append(_color(color))

            if widget:
                self.gradient = skia.GradientShader.MakeLinear(
                    points=[
                        tuple(self.get_anchor_pos(widget, start_anchor)),
                        tuple(self.get_anchor_pos(widget, end_anchor)),
                    ],  # [ (x, y), (x1, y1) ]
                    colors=colors,  # [ Color1, Color2, Color3 ]
                )
            else:
                self.gradient = skia.GradientShader.MakeLinear(
                    points=[start_pos, end_pos],  # [ (x, y), (x1, y1) ]
                    colors=colors,  # [ Color1, Color2, Color3 ]
                )

            return self
        else:
            return None
