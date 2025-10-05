import skia


def draw_restore_button_clipped(
    canvas: skia.Canvas,
    rect: skia.Rect,
    color: int = skia.ColorBLACK,
    stroke_width: float = 1.5,
) -> None:
    """
    使用Clip裁剪隐藏重叠部分的恢复按钮（修正参数错误版）
    """
    # 计算内部矩形大小（保留边距）
    margin = rect.width() * 0.2
    inner_size = rect.width() - margin * 2

    # 右上角矩形（较小）
    right_rect = skia.Rect.MakeXYWH(
        rect.left() + margin * 1.5,
        rect.top() + margin,
        inner_size,
        inner_size,
    )

    # 左下角矩形（较大，覆盖右上）
    left_rect = skia.Rect.MakeXYWH(
        rect.left() + margin * 0.5,
        rect.top() + margin * 1.5,
        inner_size,
        inner_size,
    )

    # 绘制设置
    paint = skia.Paint(
        Color=color,
        Style=skia.Paint.kStroke_Style,
        StrokeWidth=stroke_width,
        AntiAlias=True,
    )

    # 1. 先绘制左下矩形（完整）
    canvas.drawRect(left_rect, paint)

    # 2. 设置裁剪区域（关键修正点）
    clip_path = skia.Path()
    clip_path.addRect(left_rect, skia.PathDirection.kCCW)

    canvas.save()
    # 正确调用方式（注意参数顺序）：
    canvas.clipPath(clip_path, skia.ClipOp.kDifference, True)  # 第三个参数是doAntiAlias
    canvas.drawRect(right_rect, paint)
    canvas.restore()


# 创建透明画布
surface = skia.Surface(100, 100, skia.ColorType.kRGBA_8888_ColorType)
canvas = surface.getCanvas()
canvas.clear(skia.ColorTRANSPARENT)

# 绘制按钮（自动处理重叠）
draw_restore_button_clipped(
    canvas, skia.Rect.MakeXYWH(20, 20, 60, 60), color=skia.ColorBLUE, stroke_width=2.0
)

# 保存结果（PNG保留透明度）
surface.makeImageSnapshot().save("restore_button_clipped.png")
