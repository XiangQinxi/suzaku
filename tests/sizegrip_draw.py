import skia


def draw_size_grip(
    canvas: skia.Canvas, rect: skia.Rect, grip_size=16, color=skia.ColorBLACK
):
    """
    在矩形右下角绘制斜线风格的 SizeGrip
    Args:
        rect: 目标矩形区域
        grip_size: 手柄大小（像素）
        color: 手柄颜色
    """
    # 确保矩形足够大
    if rect.width() < grip_size or rect.height() < grip_size:
        return

    # 计算右下角区域
    grip_rect = skia.Rect.MakeLTRB(
        rect.right() - grip_size, rect.bottom() - grip_size, rect.right(), rect.bottom()
    )

    # 绘制斜线
    paint = skia.Paint(
        Color=color, Style=skia.Paint.kStroke_Style, StrokeWidth=1.0, AntiAlias=True
    )

    path = skia.Path()
    spacing = 4  # 线间距

    # 从右下角向左上方绘制平行斜线
    for i in range(0, grip_size, spacing):
        path.moveTo(grip_rect.right(), grip_rect.bottom() - i)
        path.lineTo(grip_rect.right() - i, grip_rect.bottom())

    canvas.drawPath(path, paint)


def draw_dotted_size_grip(
    canvas: skia.Canvas,
    rect: skia.Rect,
    grip_size=16,
    dot_size=2,
    color=skia.ColorBLACK,
):
    """
    点阵风格的 SizeGrip
    """
    grip_rect = skia.Rect.MakeLTRB(
        rect.right() - grip_size, rect.bottom() - grip_size, rect.right(), rect.bottom()
    )

    paint = skia.Paint(Color=color, Style=skia.Paint.kFill_Style, AntiAlias=True)

    spacing: int = 4

    rows = min(grip_size // spacing, grip_size // dot_size)

    for row in range(rows):
        dots_in_row = row + 1
        # 在当前行从左到右绘制点
        for col in range(dots_in_row):
            x = grip_rect.right() - (row * spacing) - (col * spacing) - dot_size
            y = grip_rect.bottom() - (row * spacing) - dot_size
            canvas.drawCircle(x, y, dot_size, paint)


def draw_windows_style_grip(
    canvas: skia.Canvas, rect: skia.Rect, grip_size=16, color=skia.ColorBLACK
):
    """
    Windows 风格的三段斜线
    """
    grip_rect = skia.Rect.MakeLTRB(
        rect.right() - grip_size, rect.bottom() - grip_size, rect.right(), rect.bottom()
    )

    paint = skia.Paint(
        Color=color, Style=skia.Paint.kStroke_Style, StrokeWidth=1.5, AntiAlias=True
    )

    # 绘制三段斜线
    lines = [
        (
            grip_rect.right() - 8,
            grip_rect.bottom(),
            grip_rect.right(),
            grip_rect.bottom() - 8,
        ),
        (
            grip_rect.right() - 12,
            grip_rect.bottom(),
            grip_rect.right(),
            grip_rect.bottom() - 12,
        ),
        (
            grip_rect.right() - 16,
            grip_rect.bottom(),
            grip_rect.right(),
            grip_rect.bottom() - 16,
        ),
    ]

    path = skia.Path()
    for x1, y1, x2, y2 in lines:
        path.moveTo(x1, y1)
        path.lineTo(x2, y2)

    canvas.drawPath(path, paint)


# 使用示例
surface = skia.Surface(400, 300)
canvas = surface.getCanvas()
canvas.clear(skia.ColorWHITE)

rect = skia.Rect.MakeLTRB(50, 50, 350, 250)
draw_size_grip(canvas, rect, grip_size=50, color=skia.ColorBLUE)
surface.makeImageSnapshot().save("size_grip.png", skia.kPNG)
