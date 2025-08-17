import skia
import numpy as np

width, height = 800, 600
surface = skia.Surface(width, height)

with surface as canvas:

    # 清空画布
    canvas.clear(skia.Color(255, 255, 255, 255))  # 白色背景

    # 创建画笔
    paint = skia.Paint()
    paint.setColor(skia.Color(0, 0, 0, 255))  # 黑色

    # 创建字体
    font = skia.Font(skia.Typeface('Arial'), 24)

    # 绘制简单文本
    canvas.drawString("Hello, Skia!", 50, 50, font, paint)


image = surface.makeImageSnapshot()
image.save('basic_text.png', skia.kPNG)
