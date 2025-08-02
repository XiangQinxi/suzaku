from .widget import SkWidget


class SkLabel(SkWidget):

    from ..base.var import Var

    def __init__(self, *args, text: str = "SkLabel", style="SkLabel", textvariable: Var = None, **kwargs) -> None:
        """
        初始化标签

        :param args: SkVisual参数
        :param text: 标签文本
        :param kwargs: SkVisual参数
        """
        super().__init__(*args, style=style, name="sk_visual", **kwargs)

        if textvariable is not None:
            self.visual_attr["text"] = textvariable.get()
            textvariable.bind("change", self._textvariable)
        else:
            self.visual_attr["text"] = text
        self.visual_attr["textvariable"] = textvariable
        self.bind("textvariable", self._textvariable)

    def _textvariable(self, evt):
        self.visual_attr["text"] = self.visual_attr["textvariable"].get()

    def draw(self, canvas, rect) -> None:
        """
        绘制标签

        :param canvas: 传入的skia.Surface
        :param rect: 给出的矩形
        :return: None
        """
        import skia
        from ..style.color import color
        rect_paint = skia.Paint(
            Style=skia.Paint.kFill_Style,
            Color=color(self.theme.get_theme()[self.winfo_style()]["bg"]),
        )

        canvas.drawRect(rect, rect_paint)

        from .packs import central_text

        central_text(canvas, self.cget("text"), color(self.theme.get_theme()[self.winfo_style()]["fg"]), self.winfo_x(), self.winfo_y(), self.winfo_width(), self.winfo_height())

