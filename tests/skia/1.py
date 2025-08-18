import skia
import numpy as np

width, height = 800, 600
surface = skia.Surface(width, height)

with surface as canvas:

    # 清空画布
    canvas.clear(skia.Color(255, 255, 255, 255))  # 白色背景

    # 创建画笔
    paint = skia.Paint(
        AntiAlias=True,
    )
    # paint.setBlendMode(skia.BlendMode.kPlus)
    paint.setColor(skia.ColorBLUE)  # 黑色
    paint.setStyle(skia.Paint.kFill_Style)
    paint.setStrokeWidth(10)

    rect: skia.Rect = skia.Rect.MakeXYWH(x=50, y=50, w=200, h=200)
    rect.makeOutset(10, 10)

    paint.setImageFilter(skia.ImageFilters.DropShadow(5, 5, 15, 15, skia.ColorBLACK))

    canvas.drawRect(rect, paint)

    paint.reset()
    paint.setAntiAlias(True)

    paint.setColor(skia.ColorRED)  # 黑色
    paint.setStyle(skia.Paint.kStroke_Style)
    paint.setStrokeWidth(10)

    canvas.drawRect(rect, paint)

    """rect = skia.Rect.MakeXYWH(x=50, y=300, w=200, h=200)
    canvas.drawRect(rect, paint)
    """

image = surface.makeImageSnapshot()
image.save("rect.png", skia.kPNG)
