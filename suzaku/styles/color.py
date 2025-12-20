from __future__ import annotations

import math
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
        self.color: str | tuple | list | int | skia.Color | None = None
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
            else:
                self.set_color_name(color)
        elif typec is tuple or typec is list:
            if len(color) == 3:
                self.set_color_rgba(color[0], color[1], color[2])
            elif len(color) == 4:
                self.set_color_rgba(color[0], color[1], color[2], color[3])
            else:
                raise ValueError("Color tuple / list must have 3 (RGB) or 4 (RGBA) elements")
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
        if isinstance(a, float):
            if 0 <= a <= 1:
                a = int(a * 255)
            else:
                a = round(a)
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


anchor_angle_map = {
    "n": 90,
    "s": 270,
    "e": 0,
    "w": 180,
    "nw": 135,
    "ne": 45,
    "sw": 225,
    "se": 315,
}


class SkGradient:
    """A class for handling gradient styles, returning `skia.GradientShader` to make it easier to use."""

    gradient: skia.GradientShader | None

    @staticmethod
    def line_rect_intersection(
        w: float | int,
        h: float | int,
        x: float | int = 0,
        y: float | int = 0,
        angle_deg: float = None,
        slope: float = None,
    ) -> typing.List[typing.Tuple[float, float]]:
        """
        计算经过矩形中心的直线与矩形的交点

        Parameters:
            w: 矩形宽度
            h: 矩形高度
            angle_deg: 直线角度（度），0度为水平向右，90度为垂直向上
            slope: 直线斜率（k），如果提供angle_deg，则忽略slope

        Returns:
            交点列表，通常有2个点（直线穿过矩形）
        """
        # 矩形中心
        center_x = w / 2
        center_y = h / 2

        # 计算斜率
        if angle_deg is not None:
            # 角度转弧度
            angle_rad = math.radians(angle_deg)

            # 处理垂直情况（角度为90度或270度）
            if abs(angle_deg % 180 - 90) < 1e-10:
                slope = float("inf")  # 无穷大，表示垂直线
            else:
                slope = math.tan(angle_rad)
        elif slope is None:
            raise ValueError("Must provide angle_deg or slope parameter")

        intersections = []

        # 情况1：垂直线 (x = center_x)
        if slope == float("inf"):
            # 与上下边相交
            intersections.append((center_x + x, 0 + y))  # 上边
            intersections.append((center_x + x, h + y))  # 下边
            return intersections

        # 情况2：水平线 (y = center_y)
        if abs(slope) < 1e-10:
            # 与左右边相交
            intersections.append((0 + x, center_y + y))  # 左边
            intersections.append((w + x, center_y + y))  # 右边
            return intersections

        # 情况3：一般斜线
        # 直线方程: y = slope * (x - center_x) + center_y

        # 1. 与左边相交 (x = 0)
        y_left = slope * (0 - center_x) + center_y
        if 0 <= y_left <= h:
            intersections.append((0 + x, y_left + y))

        # 2. 与右边相交 (x = w)
        y_right = slope * (w - center_x) + center_y
        if 0 <= y_right <= h:
            intersections.append((w + x, y_right + y))

        # 3. 与上边相交 (y = 0)
        # 从方程解x: 0 = slope * (x - center_x) + center_y
        x_top = center_x - center_y / slope
        if 0 <= x_top <= w:
            intersections.append((x_top + x, 0 + y))

        # 4. 与下边相交 (y = h)
        x_bottom = center_x + (h - center_y) / slope
        if 0 <= x_bottom <= w:
            intersections.append((x_bottom + x, h + y))

        # 确保只有2个交点（直线穿过矩形）
        if len(intersections) > 2:
            # 按x坐标排序，取第一个和最后一个
            intersections.sort(key=lambda p: p[0])
            return [intersections[0], intersections[-1]]

        return intersections

    @staticmethod
    def get_anchor_pos(widget: SkWidget, anchor) -> tuple[int | float, int | float]:
        """Get widget's anchor position
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
        self.set_linear(config=config, widget=widget, start_pos=start_pos, end_pos=end_pos)
        self.draw(paint)

    def sweep(
        self,
        paint: skia.Paint,
        config: dict | None = None,
        widget=None,
        center_pos: tuple[int | float, int | float] | None = None,
    ):
        self.set_sweep(config=config, widget=widget, center_pos=center_pos)
        self.draw(paint)

    def set_linear(
        self,
        config: (
            dict | None
        ) = None,  # {"start_anchor": "n", "end_anchor": "s", "colors": {"0%": "red", "50%": "blue", "100%": "green"}}
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
            opacity = config.get("opacity", 1.0)
            # Convert to a color list recognizable by Skia 【转换成skia能识别的颜色列表】
            colors: list[tuple[int | float, int | float, int | float, int | float] | str] = []
            positions: list[float] = []
            for position, color in config["colors"].items():
                position: str  # ["0%", "0.5", "100%"]

                if position.endswith("%"):
                    positions.append(float(position.strip("%")) / 100)
                else:
                    positions.append(float(position))
                if widget:
                    _color = skcolor_to_color(style_to_color(color, widget.theme))
                    skia.ColorSetA(_color, int(skia.ColorGetA(_color) * opacity))
                    colors.append(_color)
                else:
                    _color = SkColor(color).color
                    skia.ColorSetA(_color, int(skia.ColorGetA(_color) * opacity))
                    colors.append(_color)

            if all(((start_pos is None or end_pos is None), widget)):
                if "start_anchor" in config or "end_anchor" in config:
                    if "start_anchor" in config:
                        start_anchor = config["start_anchor"]
                    else:
                        start_anchor: typing.Literal[
                            "nw", "n", "ne", "w", "e", "sw", "s", "se", "center"
                        ] = "n"
                    if "end_anchor" in config:
                        end_anchor = config["end_anchor"]
                    else:
                        end_anchor: typing.Literal[
                            "nw", "n", "ne", "w", "e", "sw", "s", "se", "center"
                        ] = "s"
                    start_pos = tuple(self.get_anchor_pos(widget, start_anchor))
                    end_pos = tuple(self.get_anchor_pos(widget, end_anchor))
                elif "direction" in config:
                    direction = config["direction"]
                    if isinstance(direction, int | float):
                        angle = direction
                    elif isinstance(direction, str):
                        if direction in anchor_angle_map:
                            angle = anchor_angle_map[direction]
                        else:
                            raise ValueError(f"invalid direction: {direction}")
                    else:
                        raise ValueError(f"invalid direction: {direction}")
                    start_pos, end_pos = self.line_rect_intersection(
                        widget.width,
                        widget.height,
                        widget.canvas_x,
                        widget.canvas_y,
                        angle_deg=angle,
                    )

                else:
                    raise ValueError("must provide direction or start_anchor and end_anchor")

            self.gradient = skia.GradientShader.MakeLinear(
                positions=positions,
                points=[
                    start_pos,
                    end_pos,
                ],  # [ (x, y), (x1, y1) ]
                colors=colors,  # [ Color1, Color2, Color3 ]
            )

            return self
        else:
            return None

    def set_sweep(
        self,
        config: dict | None = None,
        widget=None,
        center_pos: tuple[int | float, int | float] | None = None,
    ):
        self.gradient = None
        if config:
            opacity = config.get("opacity", 1.0)
            # Convert to a color list recognizable by Skia 【转换成skia能识别的颜色列表】
            colors: list[tuple[int | float, int | float, int | float, int | float] | str] = []
            positions: list[float] = []
            for position, color in config["colors"].items():
                position: str  # ["0%", "0.5", "100%"]

                if position.endswith("%"):
                    positions.append(float(position.strip("%")) / 100)
                else:
                    positions.append(float(position))
                if widget:
                    _color = skcolor_to_color(style_to_color(color, widget.theme))
                    skia.ColorSetA(_color, int(skia.ColorGetA(_color) * opacity))
                    colors.append(_color)
                else:
                    _color = SkColor(color).color
                    skia.ColorSetA(_color, int(skia.ColorGetA(_color) * opacity))
                    colors.append(_color)

            if center_pos is None:
                if widget:
                    if "center_anchor" in config:
                        center_anchor = config["center_anchor"]
                    else:
                        center_anchor: typing.Literal[
                            "nw", "n", "ne", "w", "e", "sw", "s", "se", "center"
                        ] = "center"
            if widget:
                _center_pos = self.get_anchor_pos(widget, center_anchor)
                self.gradient = skia.GradientShader.MakeSweep(
                    cx=_center_pos[0],
                    cy=_center_pos[1],
                    positions=positions,
                    colors=colors,  # [ Color1, Color2, Color3 ]
                )
            else:
                self.gradient = skia.GradientShader.MakeSweep(
                    cx=center_pos[0],
                    cy=center_pos[1],
                    positions=positions,
                    colors=colors,  # [ Color1, Color2, Color3 ]
                )

            return self
        else:
            return None


def style_to_color(
    style_attr_value: list[int] | tuple[int, int, int, int] | dict | str,
    theme: str | SkTheme,
) -> None | SkColor | SkGradient | typing.Any:
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
                        if not theme:
                            warnings.warn("No theme found using given name!", SkColorWarning)
                            return SkColor(ERR_COLOR)
                    return style_to_color(
                        theme.get_preset_color(style_attr_value["color_palette"]), theme
                    )
                case "texture":
                    if type(theme) is str:
                        theme: SkTheme = SkTheme.find_loaded_theme(theme)
                        if not theme:
                            warnings.warn("No theme found using given name!", SkColorWarning)
                            return SkColor(ERR_COLOR)
                    return theme.get_preset_color(style_attr_value["texture"]), theme
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
