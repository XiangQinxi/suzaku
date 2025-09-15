import skia


def draw_checkmark_with_lines(canvas, rect: skia.Rect, paint: skia.Paint):
    """使用 drawLine 在矩形内绘制自适应对勾"""
    # 获取矩形边界和尺寸
    left, top = rect.left(), rect.top()
    width, height = rect.width(), rect.height()

    # 定义对勾的 3 个关键点（比例坐标 0~1）
    points = [
        (0.2, 0.6),  # 起点（左下）
        (0.4, 0.8),  # 中间拐点
        (0.8, 0.2),  # 终点（右上）
    ]

    # 转换为实际坐标
    real_points = [(left + p[0] * width, top + p[1] * height) for p in points]

    # 分段绘制线条
    canvas.drawLine(*real_points[0], *real_points[1], paint)  # 左下到中间
    canvas.drawLine(*real_points[1], *real_points[2], paint)  # 中间到右上


# 示例用法
width, height = 400, 300
surface = skia.Surface(width, height)
canvas = surface.getCanvas()
canvas.clear(skia.ColorWHITE)

# 定义目标矩形（任意大小和位置）
target_rect = skia.Rect.MakeLTRB(50, 50, 350, 250)  # left, top, right, bottom

# 可选：绘制矩形边界（可视化范围）
canvas.drawRect(
    target_rect,
    skia.Paint(Color=skia.ColorBLUE, StrokeWidth=1, Style=skia.Paint.kStroke_Style),
)

# 绘制对勾（使用纯线条）
draw_checkmark_with_lines(
    canvas,
    target_rect,
    skia.Paint(
        Color=skia.ColorGREEN,  # 绿色
        StrokeWidth=max(4, int(0.02 * target_rect.height())),  # 动态线条粗细
        Style=skia.Paint.kStroke_Style,
        AntiAlias=True,
        StrokeCap=skia.Paint.kRound_Cap,  # 圆角线头
    ),
)

# 保存结果
surface.makeImageSnapshot().save("checkmark_lines_scaled.png", skia.kPNG)
