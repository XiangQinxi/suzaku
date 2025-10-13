import skia

from ..event import SkEvent
from ..styles.color import skcolor_to_color, style_to_color
from .container import SkContainer
from .widget import SkWidget


class SkSizeGrip(SkWidget):
    def __init__(
        self,
        parent: SkContainer,
        *,
        style: str = "SkSizeGrip",
        cursor: str = "resize_nwse",
        **kwargs,
    ):

        super().__init__(parent=parent, style_name=style, cursor=cursor, **kwargs)

        self.bind("mouse_pressed", self._mouse_pressed)
        self.window.bind("mouse_motion", self._mouse_motion)
        self.window.bind("mouse_released", self._mouse_released)

        self._x1 = None
        self._y1 = None

    def _mouse_pressed(self, event: SkEvent):
        if not self.window.window_attr("maximized"):
            self._x1 = event.x
            self._y1 = event.y
            self._width1 = self.window.width
            self._height1 = self.window.height

    def _mouse_motion(self, event: SkEvent):
        minwidth, minheight = self.window.wm_minsize()
        if self._x1 and self._x1 and self.window.resizable():
            width = max(minwidth, self._width1 + round(event.x - self._x1))
            height = max(minheight, self._height1 + round(event.y - self._y1))

            self.window.resize(width, height)

    def _mouse_released(self, event: SkEvent):
        self._x1 = None
        self._y1 = None

    def draw_widget(self, canvas: skia.Canvas, rect: skia.Rect) -> None:
        style = self.theme.select(self.style_name)

        canvas.save()
        canvas.clipRect(rect)

        fg = self._style("fg", skia.ColorGRAY, style)

        match style["grip_style"]:
            case "dotted":
                dot_size = self._style("dot_size", 2, style)
                dot_spacing = self._style("dot_spacing", 5, style)
                self._draw_dotted_size_grip(
                    canvas,
                    rect,
                    grip_size=self.dheight,
                    color=fg,
                    dot_size=dot_size,
                    spacing=dot_spacing,
                )
            case _:
                self._draw_size_grip(
                    canvas,
                    rect,
                    grip_size=self.dheight,
                    color=fg,
                )

        canvas.restore()

    def _draw_size_grip(
        self, canvas: skia.Canvas, rect: skia.Rect, grip_size=16, color=skia.ColorBLACK
    ):
        """
        在矩形右下角绘制斜线风格的 SizeGrip
        Args:
            rect: 目标矩形区域
            grip_size: 手柄大小（像素）
            color: 手柄颜色
        """

        # 绘制斜线
        paint = skia.Paint(
            Color=skcolor_to_color(style_to_color(color, self.theme)),
            Style=skia.Paint.kStroke_Style,
            StrokeWidth=1.0,
            AntiAlias=self.anti_alias,
        )

        path = skia.Path()
        spacing = 4  # 线间距

        # 从右下角向左上方绘制平行斜线
        for i in range(0, grip_size, spacing):
            path.moveTo(rect.right(), rect.bottom() - i)
            path.lineTo(rect.right() - i, rect.bottom())

        canvas.drawPath(path, paint)

    def _draw_dotted_size_grip(
        self,
        canvas: skia.Canvas,
        rect: skia.Rect,
        grip_size=16,
        dot_size=2,
        spacing: int = 5,
        color=skia.ColorBLACK,
    ):
        """
        点阵风格的 SizeGrip
        """

        paint = skia.Paint(
            Color=skcolor_to_color(style_to_color(color, self.theme)),
            Style=skia.Paint.kFill_Style,
            AntiAlias=self.anti_alias,
        )

        rows = grip_size // spacing

        # 从右下角向左上方绘制点阵
        for i in range(rows):
            for j in range(rows - i):  # 每行减少一个点
                x = rect.right() - (j * spacing) - dot_size
                y = rect.bottom() - (i * spacing) - dot_size
                canvas.drawCircle(x, y, dot_size, paint)
