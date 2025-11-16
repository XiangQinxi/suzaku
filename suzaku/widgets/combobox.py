import typing

import skia

from ..event import SkEvent
from ..styles.color import skcolor_to_color, style_to_color
from .button import SkButton
from .container import SkContainer
from .lineinput import SkLineInput
from .popupmenu import SkPopupMenu
from .text import SkText
from ..var import SkStringVar


class SkComboBox(SkButton):
    def __init__(
        self,
        parent: SkContainer,
        *,
        text: str = None,
        values: list | None = None,
        style: str = "SkComboBox",
        readonly: bool = False,
        placeholder: str = None,
        textvariable: None | SkStringVar = None,
        **kwargs,
    ):
        super().__init__(parent, style=style, **kwargs)

        if textvariable is None:
            textvariable = SkStringVar(default_value=text)

        self.attributes["textvariable"] = textvariable
        self.attributes["readonly"]: bool = readonly
        self.attributes["values"]: list | None = values
        self.attributes["command"]: None | typing.Callable = None
        self.attributes["placeholder"]: str = placeholder

        self.popupmenu = SkPopupMenu(self.window)
        self.popupmenu.bind_scroll_event()

        if values:
            for value in values:
                self.popupmenu.add_command(value)
        self.input = SkLineInput(
            self, textvariable=textvariable, readonly=readonly, placeholder=placeholder
        )
        self.bind("click", self._on_click)
        self.bind("command", lambda evt: self.cget("textvariable").set(evt["text"]))
        self.parent.bind("scrolled", self._on_parent_scrolled)
        self.popupmenu.bind("command", lambda evt: self.trigger("command", evt))

        self.help_parent_scroll = True

    def _on_parent_scrolled(self, event: SkEvent):
        if self.popupmenu.is_popup:
            self.popup()

    def set_attribute(self, **kwargs):
        if "values" in kwargs:
            values = kwargs.pop("values")
            self.attributes["values"] = values
            self.popupmenu.remove_all()
            for item in values:
                self.popupmenu.add_command(item, command=lambda: self.set)
        if "readonly" in kwargs:
            readonly = kwargs.pop("readonly")
            self.attributes["readonly"] = readonly
            self.input.set_attribute(readonly=readonly)
        if "placeholder" in kwargs:
            placeholder = kwargs.pop("placeholder")
            self.attributes["placeholder"] = placeholder
            self.input.set_attribute(placeholder=placeholder)
        return super().set_attribute(**kwargs)

    def draw_widget(self, canvas, rect, style_selector: str | None = None) -> None:
        style = super().draw_widget(canvas, rect, style_selector)
        arrow_padding = 10
        button_rect: skia.Rect = skia.Rect.MakeLTRB(
            rect.right() - self.height + arrow_padding,
            rect.top() + arrow_padding,
            rect.right() - arrow_padding,
            rect.bottom() - arrow_padding,
        )
        arrow = skcolor_to_color(
            style_to_color(
                self._style("arrow", skia.ColorBLACK, self.theme.select(self.style_name)),
                self.theme,
            )
        )
        button_rect.offset(0, arrow_padding / 4)
        self._draw_arrow(canvas, button_rect, color=arrow, is_press=self.popupmenu.is_popup)
        self.input.fixed(5, 0, self.width - self.height, self.height)

    def set(self, value: str):
        self.cget("textvariable").set(value)

    def get(self) -> str:
        return self.cget("textvariable").get()

    def popup(self):
        if self.cget("values"):
            y = self.canvas_y + self.height
            self.popupmenu.popup(
                x=self.canvas_x,
                y=y,
                width=self.width,
                height=min(self.popupmenu.content_height, self.window.height - y),
            )

    def _on_click(self, event: SkEvent):
        if self.popupmenu and not self.cget("disabled"):
            if self.popupmenu.is_popup:
                self.popupmenu.hide()
            else:
                self.popup()

    @staticmethod
    def _draw_arrow(
        canvas: skia.Canvas,
        rect: skia.Rect,  # 箭头绘制区域
        color: int = skia.ColorBLACK,
        is_press: bool = False,  # 按下状态
    ):
        """
        绘制标准下拉箭头（实心三角形）
        """
        margin = rect.height() * 0.1
        width = rect.width() * 0.6  # 箭头底部宽度
        height = rect.height() * 0.3  # 箭头高度

        # 基础位置（未按下状态朝下）
        if not is_press:
            points = [
                skia.Point(rect.centerX() - width / 2, rect.top() + margin),
                skia.Point(rect.centerX() + width / 2, rect.top() + margin),
                skia.Point(rect.centerX(), rect.top() + margin + height),
            ]
        else:
            # 按下状态：箭头朝上且下移5%
            points = [
                skia.Point(
                    rect.centerX() - width / 2,
                    rect.top() + margin + height + rect.height() * 0.05,
                ),
                skia.Point(
                    rect.centerX() + width / 2,
                    rect.top() + margin + height + rect.height() * 0.05,
                ),
                skia.Point(rect.centerX(), rect.top() + margin + rect.height() * 0.05),
            ]

        path = skia.Path().moveTo(points[0]).lineTo(points[1]).lineTo(points[2]).close()
        paint = skia.Paint(Color=color, Style=skia.Paint.kFill_Style, AntiAlias=True)
        canvas.drawPath(path, paint)
