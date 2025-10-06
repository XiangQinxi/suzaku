from __future__ import annotations

import typing
import warnings

import skia

from ..styles.theme import SkTheme

if typing.TYPE_CHECKING:
    from ..widgets.widget import SkWidget


ERR_COLOR = (0, 255, 0, 255)


class SkColorWarning(Warning):
    pass


class SkColor:
    """A class for handling colors, encapsulating skia.Color, which will make things much simpler.

    Example
    -------
    .. code-block:: python
        SkColor("#ffffff")  # Supports hex
        SkColor( (255, 255, 255, 255 ) )  # Supports RGBA format
        SkColor("white")  # Supports predefined color names (refer to color parameters in skia)

    Afterward, use `Color().color` to obtain the Skia.Color.

    Of course, if you want to change the color _value, you can use the `set_color` method of `SkColor` to modify it—though generally, you won't need to.

    :param color: Color value, can be hex, rgba, or color name.
    :type color: str | tuple | list | None
    """

    def __init__(self, color: str | tuple | list | None = None) -> None:
        self.color: str | tuple | list | int | None = None
        self.set_color(color)

    def get(self) -> skia.Color:
        """Get the color _value.

        :return: Color _value.
        """
        return self.color

    def set_color(self, color: str | tuple | list) -> SkColor:
        """Set the color of the SkColor."""
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
                    "Color tuple / list must have 3 (RGB) or 4 (RGBA) elements"
                )
        else:
            return self
        return self

    def set_color_name(self, name: str) -> None:
        """Convert color name string to skia color.

        :param name: Color name
        :return skia.Color: Skia color
        :raises ValueError: When color not exists
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

    def set_color_hex(self, _hex: str) -> None:
        """
        转换十六进制颜色字符串为Skia颜色

        Args:
            _hex: 十六进制颜色字符串(支持 #RRGGBB 和 #RRGGBBAA 格式)

        Returns:
            skia.Color: 对应的RGBA颜色对象

        Raises:
            ValueError: 当十六进制格式无效时抛出
        """
        hex_color = _hex.lstrip("#")
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
    """A class for handling gradient styles, returning `skia.GradientShader` to make it easier to use."""

    @staticmethod
    def get_anchor_pos(widget: SkWidget, anchor) -> tuple[int | float, int | float]:
        """Get widget`s anchor position
        (Relative widget position, not absolute position within the window)

        :param widget: The SkWidget
        :param anchor: Anchor position
        :return: Anchor position in widget
        """
        x = widget.canvas_x
        y = widget.canvas_y
        width = widget.width
        height = widget.height
        match anchor:
            case "nw":
                return x, y
            case "n":
                return x + width / 2, y
            case "ne":
                return x + width, y
            case "w":
                return x, y + height / 2
            case "e":
                return x + width, y + height / 2
            case "sw":
                return x, y + height
            case "s":
                return x + width / 2, y + height
            case "se":
                return x + width, y + height
            case "center":
                return x + width / 2, y + height / 2
            case _:
                return 0, 0

    def draw(self, paint: skia.Paint) -> None:
        paint.setShader(self.gradient)

    def linear(
        self,
        paint: skia.Paint,
        config: (
            dict | None
        ) = None,  # {"start_anchor": "n", "end_anchor": "s", "start": "red", "end": "blue"}
        widget=None,
        start_pos: tuple[int | float, int | float] | None = None,
        end_pos: tuple[int | float, int | float] | None = None,
    ):
        self.set_linear(
            config=config, widget=widget, start_pos=start_pos, end_pos=end_pos
        )
        self.draw(paint)

    def set_linear(
        self,
        config: (
            dict | None
        ) = None,  # {"start_anchor": "n", "end_anchor": "s", "start": "red", "end": "blue"}
        widget=None,
        start_pos: tuple[int | float, int | float] | None = None,
        end_pos: tuple[int | float, int | float] | None = None,
    ):
        """Set linear gradient

        .. code-block:: python
            gradient.set_linear(
                {
                    "start_anchor": "n",
                    "end_anchor": "s",
                    "start": "red",
                    "end": "blue"
                }
            )


        :param paint: Paint
        :param widget: Widget
        :param config: Gradient configs
        :param end_pos: End position
        :param start_pos: Start position
        :return: cls
        """
        self.gradient = None
        if config:

            # Convert to a color list recognizable by Skia 【转换成skia能识别的颜色列表】
            colors: list[
                tuple[int | float, int | float, int | float, int | float] | str
            ] = []
            positions: list[float] = []
            for position, color in config["colors"].items():
                position: str  # ["0%", "0.5", "100%"]

                if position.endswith("%"):
                    positions.append(float(position.strip("%")) / 100)
                else:
                    positions.append(float(position))
                colors.append(SkColor(color).color)

            if start_pos is None or end_pos is None:
                if widget:
                    if "start_anchor" in config:
                        start_anchor = config["start_anchor"]
                    else:
                        start_anchor: typing.Literal[
                            "nw", "n", "ne", "w", "e", "sw", "s", "se"
                        ] = "n"
                    if "end_anchor" in config:
                        end_anchor = config["end_anchor"]
                    else:
                        end_anchor: typing.Literal[
                            "nw", "n", "ne", "w", "e", "sw", "s", "se"
                        ] = "s"

            if widget:
                self.gradient = skia.GradientShader.MakeLinear(
                    positions=positions,
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


def style_to_color(
    style_attr_value: list[int] | tuple[int, int, int, int] | dict | str,
    theme: str | SkTheme,
) -> None | SkColor | SkGradient:
    """Returns the color object indicated by the color style attribute _value.

    Example
    -------
    .. code-block:: python
        my_theme = SkTheme()
        background_attr_value = my_theme.get_style_attr("SkButton:hover", "background")
        theme.style_to_color(background_attr_value, my_theme.name)
    This shows getting a color object for the background of a `SkButton` at `hover` state.

    :param style_attr_value: The _value of style attribute
    :param theme: The name of the theme used, or the theme itself
    """
    match style_attr_value:
        case list() | tuple() | str():
            # If is configured to a RGB(A) color tuple of hex string
            return SkColor(style_attr_value)
        case dict():
            # If is configured to something else: color palette, gradient, texture, etc.
            match list(style_attr_value.keys())[0]:
                case "color_palette":
                    # If is set to a color in color palette
                    if type(theme) is str:
                        theme = SkTheme.find_loaded_theme(theme)
                        if theme == False:
                            warnings.warn(
                                "No theme found using given name!", SkColorWarning
                            )
                            return SkColor(ERR_COLOR)
                    return style_to_color(
                        theme.get_preset_color(style_attr_value["color_palette"]), theme
                    )
                case "texture":
                    warnings.warn("Texture is currently not implemented", FutureWarning)
                    NotImplemented
                    return SkColor(ERR_COLOR)
            return None
        case int():
            return style_attr_value
        case _:
            # If invalid, then return green to prevent crash
            warnings.warn(
                message=f"Invalid color configuration in styles! {style_attr_value}",
                category=Warning,
            )
            return SkColor(ERR_COLOR)


def skcolor_to_color(color: int | SkColor | list) -> int:
    """Returns skia.Color received or convert received SkColor into skia.Color

    :param color: SkColor object or skia.Color object
    :return: Color object
    """
    if isinstance(color, SkColor):
        return color.get()
    elif isinstance(color, list):
        return SkColor(color).color
    else:
        return color
