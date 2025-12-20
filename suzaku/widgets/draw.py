import typing
from functools import cache

import skia

from ..styles.color import SkColor, skcolor_to_color, style_to_color
from ..styles.drop_shadow import SkDropShadow

gradient_names = ["linear", "sweep", "radial"]
gradients = []
for gradient_name in gradient_names:
    gradients.append(f"{gradient_name}_gradient")
    gradients.append(f"{gradient_name[0]}g")


class SkDraw:

    @staticmethod
    def _blur(style: skia.BlurStyle | None = None, sigma: float = 5.0):
        """Create a blur mask filter"""
        if not style:
            style = skia.kNormal_BlurStyle
        return skia.MaskFilter.MakeBlur(style, sigma)

    def _draw_blur(self, paint: skia.Paint, style=None, sigma=None):
        paint.setMaskFilter(self._blur(style, sigma))

    def _draw_text(
        self,
        canvas: skia.Canvas,
        rect: skia.Rect,
        text: str | None = "",
        bg: None | str | int | SkColor = None,
        fg: None | str | int | SkColor = None,
        radius: float | int = 3,
        align: typing.Literal["center", "right", "left"] = "center",
        font: skia.Font = None,
    ) -> None:
        """Draw central text

        .. note::
            >>> self._draw_text(canvas, "Hello", skia.ColorBLACK, 0, 0, 100, 100)

        :param canvas: The canvas
        :param rect: The skia Rect
        :param text: The text
        :param fg: The color of the text
        :return: None
        """
        if not font:
            font = self.attributes["font"]

        # bg = skia.ColorBLACK

        text = str(text)

        # 绘制字体
        @cache
        def cache_paint(anti_alias, fg_):
            return skia.Paint(AntiAlias=anti_alias, Color=fg_)

        text_paint = cache_paint(self.anti_alias, skcolor_to_color(style_to_color(fg, self.theme)))

        text_width = self.measure_text(text)

        if align == "center":
            draw_x = rect.left() + (rect.width() - text_width) / 2
        elif align == "right":
            draw_x = rect.left() + rect.width() - text_width
        else:  # left
            draw_x = rect.left()

        metrics = self.metrics
        draw_y = rect.top() + rect.height() / 2 - (metrics.fAscent + metrics.fDescent) / 2

        if bg:
            bg = skcolor_to_color(style_to_color(bg, self.theme))
            bg_paint = skia.Paint(AntiAlias=self.anti_alias, Color=bg)
            canvas.drawRoundRect(
                rect=skia.Rect.MakeLTRB(
                    draw_x,
                    rect.top(),
                    draw_x + text_width,
                    rect.bottom(),
                ),
                rx=radius,
                ry=radius,
                paint=bg_paint,
            )

        canvas.drawSimpleText(text, draw_x, draw_y, font, text_paint)

        return draw_x, draw_y

    def _draw_styled_text(
        self,
        canvas: skia.Canvas,
        rect: skia.Rect,
        bg: None | str | int | SkColor = None,
        fg: None | str | int | SkColor = None,
        radius: float | int = 3,
        # [ "Content", {"start": 5, "end": 10, "fg": skia.ColorRED, "bg": skia.ColorBLACK, "font": skia.Font} ]
        text: tuple[str, dict[str, str | int | SkColor | skia.Font]] = ("",),
        font: skia.Font = None,
    ):
        """Draw styled text

        :param canvas: The canvas
        :param rect: The skia Rect
        :param bg: The background color
        :param fg: The foreground color
        :param text: The text
        :param font: The font
        :return: None
        """
        if isinstance(text, str):
            _text = text
            return None
        else:
            _text = text[0]
        self._draw_text(
            canvas=canvas,
            text=_text,
            rect=rect,
            bg=bg,
            fg=fg,
            align="left",
            font=font,
        )
        if isinstance(text, str):
            return None

        for item in text:
            if "font" in item:
                font = item["font"]
            if "fg" in item:
                fg = item["fg"]
            if "bg" in item:
                bg = item["bg"]
            if isinstance(item, dict):

                _rect = skia.Rect.MakeLTRB(
                    rect.left() + self.measure_text(_text[: item["start"]]),
                    rect.top(),
                    rect.right(),
                    rect.bottom(),
                )
                self._draw_text(
                    canvas=canvas,
                    rect=_rect,
                    text=_text[item["start"] : item["end"]],
                    bg=bg,
                    fg=fg,
                    radius=radius,
                    align="left",
                    font=font,
                )
        return None

    @staticmethod
    def _is_shader(arg):
        """
        e.g. bg: ["linear_gradient", {...}]
        """

        if isinstance(arg, list):
            if arg[0] in gradients:
                return True
        return False

    def _draw_rect(
        self,
        canvas: skia.Canvas,
        rect: skia.Rect,
        radius: int | tuple[int, int, int, int] = 0,
        bg: str | SkColor | int | None | tuple[int, int, int, int] = None,
        bd: str | SkColor | int | None | tuple[int, int, int, int] = None,
        width: int | float = 0,
        bd_shadow: None | tuple[int | float, int | float, int | float, int | float, str] = None,
        bd_shader: None | typing.Literal["linear_gradient"] = None,
        bg_shader: None | typing.Literal["linear_gradient"] = None,
    ):
        """Draw the frame

        :param canvas: The skia canvas
        :param rect: The skia rect
        :param radius: The radius of the rect
        :param bg: The background
        :param width: The width
        :param bd: The color of the border
        :param bd_shadow: The border_shadow switcher
        :param bd_shader: The shader of the border

        """
        radius = self.unpack_radius(radius)
        rrect = skia.RRect()
        rrect.setRectRadii(
            skia.Rect.MakeLTRB(*rect),
            [
                skia.Point(*radius[0]),  # 左上
                skia.Point(*radius[1]),  # 右上
                skia.Point(*radius[2]),  # 右下
                skia.Point(*radius[3]),  # 左下
            ],
        )
        if bg:
            bg_paint = skia.Paint(
                AntiAlias=self.anti_alias,
                Style=skia.Paint.kStrokeAndFill_Style,
            )
            bg = skcolor_to_color(style_to_color(bg, self.theme))

            # Background
            bg_paint.setStrokeWidth(width)
            bg_paint.setColor(bg)
            if bd_shadow:
                self.drop_shadow.drop_shadow(widget=self, config=bd_shadow, paint=bg_paint)
            if bg_shader:
                if isinstance(bg_shader, dict):
                    if "linear_gradient" in bg_shader:
                        self.gradient.linear(
                            widget=self,
                            config=bg_shader["linear_gradient"],
                            paint=bg_paint,
                        )
                    if "lg" in bg_shader:
                        self.gradient.linear(
                            widget=self,
                            config=bg_shader["lg"],
                            paint=bg_paint,
                        )
                    if "sweep_gradient" in bg_shader:
                        self.gradient.sweep(
                            widget=self,
                            config=bg_shader["sweep_gradient"],
                            paint=bg_paint,
                        )
                    if "sg" in bg_shader:
                        self.gradient.sweep(
                            widget=self,
                            config=bg_shader["sg"],
                            paint=bg_paint,
                        )
            canvas.drawRRect(rrect, bg_paint)
        if bd and width > 0:
            bd_paint = skia.Paint(
                AntiAlias=self.anti_alias,
                Style=skia.Paint.kStroke_Style,
            )
            bd = skcolor_to_color(style_to_color(bd, self.theme))

            # Border
            bd_paint.setStrokeWidth(width)
            bd_paint.setColor(bd)
            if bd_shader:
                if isinstance(bd_shader, dict):
                    if "linear_gradient" in bd_shader:
                        self.gradient.linear(
                            widget=self,
                            config=bd_shader["linear_gradient"],
                            paint=bd_paint,
                        )
                    if "lg" in bd_shader:
                        self.gradient.linear(
                            widget=self,
                            config=bd_shader["lg"],
                            paint=bd_paint,
                        )
                    if "sweep_gradient" in bd_shader:
                        self.gradient.sweep(
                            widget=self,
                            config=bd_shader["sweep_gradient"],
                            paint=bd_paint,
                        )
                    if "sg" in bd_shader:
                        self.gradient.sweep(
                            widget=self,
                            config=bd_shader["sg"],
                            paint=bd_paint,
                        )
            canvas.drawRRect(rrect, bd_paint)
        return rrect

    def _draw_circle(
        self,
        canvas: skia.Canvas,
        cx: float | int,
        cy: float | int,
        radius: int | float = 0,
        bg: str | SkColor | int | None | tuple[int, int, int, int] = None,
        bd: str | SkColor | int | None | tuple[int, int, int, int] = None,
        width: int | float = 0,
        bd_shadow: None | tuple[int | float, int | float, int | float, int | float, str] = None,
        bd_shader: None | typing.Literal["linear_gradient"] = None,
        bg_shader: None | typing.Literal["linear_gradient"] = None,
    ):
        """Draw the circle

        :param canvas: The skia canvas
        :param cx: The x coordinate of the center
        :param cy: The y coordinate of the center
        :param radius: The radius of the circle
        :param bg: The background
        :param width: The width
        :param bd: The color of the border
        :param bd_shadow: The border_shadow switcher
        :param bd_shader: The shader of the border
        """

        if bg:
            bg_paint = skia.Paint(
                AntiAlias=self.anti_alias,
                Style=skia.Paint.kStrokeAndFill_Style,
            )
            bg = skcolor_to_color(style_to_color(bg, self.theme))

            # Background
            bg_paint.setStrokeWidth(width)
            bg_paint.setColor(bg)
            if bd_shadow:
                self.drop_shadow.drop_shadow(widget=self, config=bd_shadow, paint=bg_paint)
            if bg_shader:
                if isinstance(bg_shader, dict):
                    if "linear_gradient" in bg_shader:
                        self.gradient.linear(
                            widget=self,
                            config=bg_shader["linear_gradient"],
                            paint=bg_paint,
                        )
                    if "lg" in bg_shader:
                        self.gradient.linear(
                            widget=self,
                            config=bg_shader["lg"],
                            paint=bg_paint,
                        )
                    if "sweep_gradient" in bg_shader:
                        self.gradient.sweep(
                            widget=self,
                            config=bg_shader["sweep_gradient"],
                            paint=bg_paint,
                        )
                    if "sg" in bg_shader:
                        self.gradient.sweep(
                            widget=self,
                            config=bg_shader["sg"],
                            paint=bg_paint,
                        )
            canvas.drawCircle(cx, cy, radius, bg_paint)
        if bd and width > 0:
            bd_paint = skia.Paint(
                AntiAlias=self.anti_alias,
                Style=skia.Paint.kStroke_Style,
            )
            bd = skcolor_to_color(style_to_color(bd, self.theme))

            # Border
            bd_paint.setStrokeWidth(width)
            bd_paint.setColor(bd)
            if bd_shader:
                if isinstance(bd_shader, dict):
                    if "linear_gradient" in bd_shader:
                        self.gradient.linear(
                            widget=self,
                            config=bd_shader["linear_gradient"],
                            paint=bd_paint,
                        )
                    if "lg" in bd_shader:
                        self.gradient.linear(
                            widget=self,
                            config=bd_shader["lg"],
                            paint=bd_paint,
                        )
                    if "sweep_gradient" in bd_shader:
                        self.gradient.sweep(
                            widget=self,
                            config=bd_shader["sweep_gradient"],
                            paint=bd_paint,
                        )
                    if "sg" in bd_shader:
                        self.gradient.sweep(
                            widget=self,
                            config=bd_shader["sg"],
                            paint=bd_paint,
                        )
            canvas.drawCircle(cx, cy, radius, bd_paint)

    def _draw_rect_new(
        self,
        canvas: skia.Canvas,
        rect: typing.Any,
        radius: int = 0,
        bg: str | SkColor | int | None | tuple[int, int, int, int] = None,
        # bg: {"color": "white", "linear_gradient(lg)": ...}
        bd: str | SkColor | int | None | tuple[int, int, int, int] = None,
        width: int | float = 0,
    ):
        return
        shadow = SkDropShadow(config_list=bd_shadow)
        shadow.draw(bg_paint)
        if bg:
            bg_paint = skia.Paint(
                AntiAlias=self.anti_alias,
                Style=skia.Paint.kStrokeAndFill_Style,
            )
            bg_paint.setStrokeWidth(width)
            match bg:
                case dict():
                    for key, value in bg.items():
                        match key.lower():
                            case "color":
                                _bg = skcolor_to_color(style_to_color(value, self.theme))
                                bg_paint.setColor(_bg)
                            case "lg" | "linear_gradient":
                                self.gradient.linear(
                                    widget=self,
                                    config=value,
                                    paint=bg_paint,
                                )
                case None:
                    pass

            canvas.drawRoundRect(rect, radius, radius, bg_paint)

    def _draw_line(
        self,
        canvas: skia.Canvas,
        x0,
        y0,
        x1,
        y1,
        fg=skia.ColorGRAY,
        width: int = 1,
        shader: None | typing.Literal["linear_gradient"] = None,
        shadow: None | tuple[int | float, int | float, int | float, int | float, str] = None,
    ):
        fg = skcolor_to_color(style_to_color(fg, self.theme))
        paint = skia.Paint(Color=fg, StrokeWidth=width)
        if shader:
            if isinstance(shader, dict):
                if "linear_gradient" in shader:
                    self.gradient.linear(
                        widget=self,
                        config=shader["linear_gradient"],
                        paint=paint,
                    )
                if "lg" in shader:
                    self.gradient.linear(
                        widget=self,
                        config=shader["lg"],
                        paint=paint,
                    )
                if "sweep_gradient" in shader:
                    self.gradient.sweep(
                        widget=self,
                        config=shader["sweep_gradient"],
                        paint=paint,
                    )
                if "sg" in shader:
                    self.gradient.sweep(
                        widget=self,
                        config=shader["sg"],
                        paint=paint,
                    )
        if shadow:
            _ = SkDropShadow(config_list=shadow)
            _.draw(paint)
        canvas.drawLine(x0, y0, x1, y1, paint)

    @staticmethod
    def _draw_image_rect(canvas: skia.Canvas, rect: skia.Rect, image: skia.Image) -> None:
        canvas.drawImageRect(image, rect, skia.SamplingOptions(), skia.Paint())

    @staticmethod
    def _draw_image(canvas: skia.Canvas, image: skia.Image, x, y) -> None:
        canvas.drawImage(image, left=x, top=y)
