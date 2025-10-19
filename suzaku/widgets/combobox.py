import skia

from ..event import SkEvent
from ..styles.color import skcolor_to_color, style_to_color
from .button import SkButton
from .container import SkContainer
from .lineinput import SkLineInput
from .popupmenu import SkPopupMenu
from .text import SkText


class SkComboBox(SkButton):
    def __init__(
        self,
        parent: SkContainer,
        style: str = "SkComboBox",
        editable: bool = True,
        **kwargs,
    ):
        super().__init__(parent, style=style, **kwargs)

        self.attributes["editable"]: bool = editable

        self.popupmenu = SkPopupMenu(self.parent)
        self.popupmenu.add_command("asdf1")
        self.input = SkLineInput(self)
        self.text = SkText(
            self,
        )
        self.bind("click", self._on_click)

        self.help_parent_scroll = True

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
                self._style(
                    "arrow", skia.ColorBLACK, self.theme.select(self.style_name)
                ),
                self.theme,
            )
        )
        button_rect.offset(0, arrow_padding / 4)
        self._draw_arrow(
            canvas, button_rect, color=arrow, is_press=self.popupmenu.is_popup
        )
        if self.cget("editable"):
            self.input.fixed(0, 0, self.width - self.height, self.height)
        else:
            self.input.layout_forget()

    def _on_click(self, event: SkEvent):
        print(1243)
        if self.popupmenu and not self.cget("disabled"):
            if self.popupmenu.is_popup:
                self.popupmenu.hide()
            else:
                self.popupmenu.popup(
                    x=self.x - self.parent.x_offset,
                    y=self.y - self.parent.y_offset + self.height + 5,
                    width=self.width,
                )

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
