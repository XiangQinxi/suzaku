from .visual import SkVisual


class SkEntry(SkVisual):

    """
    按钮组件
    """

    def __init__(self, *args, placeholder: str = "", size=(105, 35), cursor="ibeam", style="SkEntry", id=None, **kwargs) -> None:

        """

        :param args: SkVisual参数
        :param text: 标签文本
        :param size: 默认大小
        :param cursor: 鼠标放上去的光标样式
        :param command: 触发点击按钮时，执行的函数（无回调）
        :param id: 可选ID标识码
        :param kwargs: SkVisual参数
        """

        super().__init__(*args, size=size, style=style, **kwargs)

        self.evts["click"] = []
        self.visual_attr["name"] = "sk_button"
        self.visual_attr["placeholder"] = placeholder
        self.visual_attr["text"] = ""

        self.visual_attr["cursor"] = cursor

        self.bind("key_pressed", self._key_pressed)

    def _key_pressed(self, evt):
        if evt.key == "BackSpace":
            print(123)
            self.visual_attr["text"] = self.visual_attr["text"][:-1]

    def draw(self, canvas, rect) -> None:
        """
        绘制输入框方法。

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
            if self.is_focus:
                sheets = self.theme.get_theme()[self.winfo_style()]["focus"]
            else:
                sheets = self.theme.get_theme()[self.winfo_style()]["hover"]
        elif self.is_focus:
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

        if not self.is_focus:
            if self.visual_attr["placeholder"] and not self.visual_attr["text"]:
                text_width = font.measureText(self.visual_attr["placeholder"])
                metrics = font.getMetrics()

                draw_x = self.winfo_x() + sheets["width"] * 2
                draw_y = self.winfo_y() + self.winfo_height() / 2 - (metrics.fAscent + metrics.fDescent) / 2

                canvas.drawSimpleText(self.visual_attr["placeholder"], draw_x, draw_y, font, text_paint)
        else:
            text_width = font.measureText(self.visual_attr["text"])
            metrics = font.getMetrics()

            draw_x = self.winfo_x() + sheets["width"] * 2
            draw_y = self.winfo_y() + self.winfo_height() / 2 - (metrics.fAscent + metrics.fDescent) / 2

            canvas.drawSimpleText(self.visual_attr["text"], draw_x, draw_y, font, text_paint)

            canvas.drawSimpleText("|", draw_x+5, draw_y, font, text_paint)
