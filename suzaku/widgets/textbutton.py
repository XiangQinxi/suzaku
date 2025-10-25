import typing

import skia

from ..styles.color import skcolor_to_color, style_to_color
from .button import SkButton
from .container import SkContainer
from .text import SkText


class SkTextButton(SkButton, SkText):
    """A Button with Text

    :param args:
    :param size: Widget default size
    :param cursor: The style displayed when the mouse hovers over it
    :param command: Triggered when the button is clicked
    :param kwargs:
    """

    def __init__(
        self,
        parent: SkContainer,
        text: str | None | int | float = "",
        *,
        cursor: typing.Union[str, None] = "hand",
        command: typing.Union[typing.Callable, None] = None,
        style: str = "SkButton",
        **kwargs,
    ) -> None:
        SkButton.__init__(self, parent=parent)
        SkText.__init__(
            self, parent=parent, text=text, style=style, cursor=cursor, **kwargs
        )
        self.attributes["command"] = command

        self.focusable = True
        self.ipadx = 10
        self.help_parent_scroll = True

        self.bind("click", lambda _: self.invoke())

    def _click(self, event) -> None:
        """
        Check click event (not press)

        :return: None
        """
        if self.button != 1:
            if self.is_mouse_floating:
                self.trigger("click", event)
                time = self.time()

                if self.click_time + self.cget("double_click_interval") > time:
                    self.trigger("double_click", event)
                    self.click_time = 0
                else:
                    self.click_time = time

    @property
    def dwidth(self):
        _width = self.cget("dwidth")
        if _width <= 0:
            _width = self.measure_text(self.get()) + self.ipadx * 2
        return _width

    @property
    def dheight(self):
        _height = self.cget("dheight")
        if _height <= 0:
            _height = self.text_height + 8 + self.ipady * 2
        return _height

    # region Draw

    def draw_widget(
        self, canvas: skia.Canvas, rect: skia.Rect, style_selector: str | None = None
    ):
        """Draw the button

        :param canvas:
        :param rect:
        :param style_selector:
        :return:
        """

        # Draw the button border
        style = SkButton.draw_widget(self, canvas, rect, style_selector)

        # Draw the button text
        canvas.save()
        canvas.clipRect(rect)
        self._draw_text(
            canvas,
            skia.Rect.MakeLTRB(
                rect.left() + self.ipadx,
                rect.top(),
                rect.right() - self.ipadx,
                rect.bottom(),
            ),
            text=self.get(),
            fg=style["fg"],
            align=self.cget("align"),
        )
        canvas.restore()
        return style

    # endregion


class SkCloseButton(SkTextButton):
    def __init__(self, parent: SkContainer, *, style: str = "SkCloseButton", **kwargs):
        super().__init__(parent, style=style, **kwargs)

    def draw_widget(self, canvas, rect, style_selector: str | None = None) -> None:
        """Draw button
        :param canvas: skia.Surface to draw on
        """
        style = super().draw_widget(canvas, rect, style_selector)

        icon_padding = self._style("icon_padding", 10, style)
        icon_width = self._style("icon_width", 1, style)
        fg = skcolor_to_color(
            style_to_color(self._style("fg", None, style), self.theme)
        )

        cross_size = rect.width() * 0.35  # ×大小
        offset_x, offset_y = rect.centerX(), rect.centerY()

        path = skia.Path()
        path.moveTo(offset_x - cross_size / 2, offset_y - cross_size / 2)
        path.lineTo(offset_x + cross_size / 2, offset_y + cross_size / 2)
        path.moveTo(offset_x + cross_size / 2, offset_y - cross_size / 2)
        path.lineTo(offset_x - cross_size / 2, offset_y + cross_size / 2)

        paint = skia.Paint(
            Color=fg,
            Style=skia.Paint.kStroke_Style,
            StrokeWidth=icon_width,
            StrokeCap=skia.Paint.kRound_Cap,
            AntiAlias=self.anti_alias,
        )
        canvas.drawPath(path, paint)


class SkMaximizeButton(SkTextButton):
    def __init__(
        self, parent: SkContainer, *, style: str = "SkMaximizeButton", **kwargs
    ):
        super().__init__(parent, style=style, command=self.toggle_maximize, **kwargs)

    def toggle_maximize(self):
        if self.window.window_attr("maximized"):
            self.window.restore()
        else:
            self.window.maximize()

    def draw_widget(self, canvas, rect, style_selector: str | None = None) -> None:
        """Draw button
        :param canvas: skia.Surface to draw on
        """
        style = super().draw_widget(canvas, rect, style_selector)

        icon_padding = self._style("icon_padding", 10, style)
        icon_width = self._style("icon_width", 1.1, style)
        fg = skcolor_to_color(
            style_to_color(self._style("fg", None, style), self.theme)
        )

        icon_radius = self.theme.get_style_attr(self.style_name, "icon_radius")

        paint = skia.Paint(
            Color=fg,
            Style=skia.Paint.kStroke_Style,
            StrokeWidth=icon_width,
            AntiAlias=self.anti_alias,
        )

        if not self.window.window_attr("maximized"):
            icon_padding = rect.width() * 0.32  # 图标内边距
            icon_rect = rect.makeInset(icon_padding, icon_padding)

            canvas.drawRoundRect(icon_rect, icon_radius, icon_radius, paint)
        else:
            margin = rect.width() * 0.3
            inner_size = rect.width() - margin * 2

            # 右上角矩形（较小）
            right_rect = skia.Rect.MakeXYWH(
                rect.left() + margin * 1.2,
                rect.top() + margin * 0.8,
                inner_size,
                inner_size,
            )

            # 左下角矩形（较大，覆盖右上）
            left_rect = skia.Rect.MakeXYWH(
                rect.left() + margin * 0.8,
                rect.top() + margin * 1.2,
                inner_size,
                inner_size,
            )

            # 绘制设置
            paint = skia.Paint(
                Color=fg,
                Style=skia.Paint.kStroke_Style,
                StrokeWidth=icon_width,
                AntiAlias=True,
            )

            # 1. 先绘制左下矩形（完整）
            canvas.drawRoundRect(left_rect, icon_radius, icon_radius, paint)

            # 2. 设置裁剪区域（关键修正点）
            clip_path = skia.Path()
            clip_path.addRect(left_rect, skia.PathDirection.kCCW)

            canvas.save()
            # 正确调用方式（注意参数顺序）：
            canvas.clipPath(
                clip_path, skia.ClipOp.kDifference, True
            )  # 第三个参数是doAntiAlias
            canvas.drawRoundRect(right_rect, icon_radius, icon_radius, paint)
            canvas.restore()


class SkMinimizeButton(SkTextButton):
    def __init__(
        self, parent: SkContainer, *, style: str = "SkMinimizeButton", **kwargs
    ):
        super().__init__(parent, style=style, command=self.click, **kwargs)

    def click(self):
        self.window.iconify()

    def draw_widget(self, canvas, rect, style_selector: str | None = None) -> None:
        """Draw button
        :param canvas: skia.Surface to draw on
        """
        style = super().draw_widget(canvas, rect, style_selector)

        icon_width = self._style("icon_width", 1, style)
        fg = self._style("fg", None, style)

        self._draw_line(
            canvas,
            rect.left() + rect.width() * 0.32,
            rect.centerY(),
            rect.right() - rect.width() * 0.32,
            rect.centerY(),
            fg=fg,
            width=icon_width,
        )
