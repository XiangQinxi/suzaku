import skia


def draw_custom_rounded_rect(canvas, rect, radii, paint):
    """
    绘制自定义圆角的矩形

    参数:
        canvas: skia.Canvas
        rect: [left, top, right, bottom] 矩形坐标
        radii: {
            'top_left': (x_radius, y_radius),
            'top_right': (x_radius, y_radius),
            'bottom_right': (x_radius, y_radius),
            'bottom_left': (x_radius, y_radius)
        }
        paint: skia.Paint 绘制样式
    """
    # 创建 RRect
    rrect = skia.RRect.MakeRect(skia.Rect.MakeLTRB(*rect))

    # 设置每个角的半径（支持X/Y不对称）
    rrect.setRectRadii(
        skia.Rect.MakeLTRB(*rect),
        [
            skia.Point(*radii["top_left"]),  # 左上
            skia.Point(*radii["top_right"]),  # 右上
            skia.Point(*radii["bottom_right"]),  # 右下
            skia.Point(*radii["bottom_left"]),  # 左下
        ],
    )

    path = skia.Path()
    path.addRRect(rrect)
    canvas.drawPath(path, paint)


# 示例用法
width, height = 400, 300
surface = skia.Surface(width, height)
canvas = surface.getCanvas()
canvas.clear(skia.ColorWHITE)

rect = [50, 50, 350, 250]  # left, top, right, bottom
radii = {
    "top_left": (20, 20),  # 左上圆角
    "top_right": (30, 10),  # 右上椭圆角（宽30px，高10px）
    "bottom_right": (0, 0),  # 右下直角
    "bottom_left": (15, 15),  # 左下圆角
}

paint = skia.Paint(Color=skia.ColorBLUE, Style=skia.Paint.kFill_Style, AntiAlias=True)

draw_custom_rounded_rect(canvas, rect, radii, paint)
surface.makeImageSnapshot().save("custom_rounded_rect.png", skia.kPNG)
