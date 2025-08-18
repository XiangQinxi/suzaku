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
    paint.setColor(skia.Color(0, 0, 0, 255))  # 黑色
    paint.setShader(
        skia.GradientShader.MakeLinear(
            points=[(50, 50), (250, 250)],
            colors=[skia.Color(0, 0, 255, 255), skia.Color(255, 0, 0, 255)],
        )
    )

    rect = skia.Rect.MakeXYWH(x=50, y=50, w=200, h=200)
    canvas.drawRect(rect, paint)

    paint.setShader(
        skia.GradientShader.MakeLinear(
            points=[(50, 300), (250, 500)],
            colors=[skia.Color(0, 0, 255, 255), skia.Color(255, 0, 0, 255)],
        )
    )

    rect = skia.Rect.MakeXYWH(x=50, y=300, w=200, h=200)
    canvas.drawRect(rect, paint)


image = surface.makeImageSnapshot()
image.save("gradient.png", skia.kPNG)
