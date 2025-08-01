from .visual import SkVisual

from typing import Union
from typing import Any


class SkButton(SkVisual):

    def __init__(self, *args, text: str = "SkButton", size: tuple[int, int] = (105, 35),
                 cursor: Union[str, None] = "hand", style="SkButton",
                 command: Union[callable, None] = None, id: Union[str, None] = None, **kwargs) -> None:

        """
        Button Component.

        按钮组件。

        **Will be re-written in future. 将被重写。**

        Args:
            *args:
                Passed to `SkVisual`.

                `SkVisual`参数。

            text (str):
                Button text.

                标签文本。

            size (tuple[int, int]):
                Default size.

                默认大小。

            cursor (str | None):
                Cursor style when floating.

                鼠标放上去的光标样式。

            command (function | None):
                Function to run when clicked

                触发点击按钮时，执行的函数（无回调）。

            id (str | None):
                Identification code (Optional).

                可选ID标识码

            **kwargs:
                Passed to `SkVisual`

                `SkVisual`参数。

        Returns:
            None
        """

        super().__init__(*args, size=size, style=style, **kwargs)

        self.evts["click"] = []
        self.visual_attr["name"] = "sk_button"
        self.visual_attr["text"] = text

        self.visual_attr["cursor"] = cursor

        self.command = command

        if command:
            self.bind("click", lambda evt: command())

        """self.bind("mouse_enter", lambda evt: print("enter"))
        self.bind("mouse_leave", lambda evt: print("leave"))
        self.bind("mouse_motion", lambda evt: print("motion"))"""

        #self.bind("mouse_pressed", lambda evt: print("pressed"))
        self.bind("mouse_released", self._click)

    def _click(self, evt) -> None:
        """
        Check click event (not pressed).

        判断点击事件，而非按下事件。

        :return: None
        """
        if self.is_mouse_enter:
            self.event_generate("click", evt)

    def draw(self, canvas, rect) -> None:
        """
        绘制按钮方法。

        :param canvas: 传入的skia.Surface
        :param rect: 给出的矩形
        :return:
        """
        import skia
        rect_paint = skia.Paint(
            AntiAlias=True,
            Style=skia.Paint.kStrokeAndFill_Style,
        )

        from ..style.color import color

        if self.is_mouse_enter:
            if self.is_mouse_pressed:
                sheets = self.theme.get_theme()[self.winfo_style()]["pressed"]
            else:
                sheets = self.theme.get_theme()[self.winfo_style()]["hover"]
        else:
            if self.focus_get() is self and "focus" in self.theme.get_theme()[self.winfo_style()]:
                sheets = self.theme.get_theme()[self.winfo_style()]["focus"]
            else:
                sheets = self.theme.get_theme()[self.winfo_style()]["rest"]

        radius = self.theme.get_theme()[self.winfo_style()]["radius"]
        rect_paint.setColor(color(sheets["bg"]))
        rect_paint.setStrokeWidth(sheets["width"])

        canvas.drawRoundRect(rect, radius, radius, rect_paint)

        rect_paint.setStyle(skia.Paint.kStroke_Style)
        rect_paint.setColor(color(sheets["border"]))

        canvas.drawRoundRect(rect, radius, radius, rect_paint)

        text_paint = skia.Paint(
            AntiAlias=True,
            Color=color(sheets["fg"])
        )

        from ..base.font import default_font
        font = default_font()

        #canvas.drawTextBlob(text, self.winfo_x(), self.winfo_y()+self.winfo_height()/2, paint2)

        # 计算位置，绘制文本居中
        text_width = font.measureText(self.visual_attr["text"])
        metrics = font.getMetrics()

        draw_x = self.winfo_x() + self.winfo_width() / 2 - text_width / 2
        draw_y = self.winfo_y() + self.winfo_height() / 2 - (metrics.fAscent + metrics.fDescent) / 2

        canvas.drawSimpleText(self.visual_attr["text"], draw_x, draw_y, font, text_paint)
