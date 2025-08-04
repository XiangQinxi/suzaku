def central_text(canvas, text, fg, x, y, width, height):
    """
    绘制居中文本

    Args:
        canvas: skia.Canvas
        text: 文本内容
        fg: 字体颜色
        x: 文本框左边界
        y: 文本框上边界
        width: 文本框宽度
        height: 文本框高度
    Returns：
        None
    Examples:
        >>> central_text(canvas, "Hello", skia.ColorBLACK, 0, 0, 100, 100)
    """
    import skia
    # 绘制字体
    text_paint = skia.Paint(
        AntiAlias=True,
        Color=fg
    )

    from suzaku.styles.font import default_font
    font = default_font()

    text_width = font.measureText(text)
    metrics = font.getMetrics()

    draw_x = x + width / 2 - text_width / 2
    draw_y = y + height / 2 - (metrics.fAscent + metrics.fDescent) / 2

    canvas.drawSimpleText(text, draw_x, draw_y, font, text_paint)


def set_rainbow_shader(rect_paint, rect):
    import skia
    rect_paint.setShader(
        skia.GradientShader.MakeSweep(
            cx=rect.centerX(),
            cy=rect.centerY(),
            colors=[
                skia.ColorCYAN,
                skia.ColorMAGENTA,
                skia.ColorYELLOW,
                skia.ColorCYAN,
            ]
        )
    )

def set_drop_shadow(rect_paint, color):
    import skia
    rect_paint.setImageFilter(
        skia.ImageFilters.DropShadow(dx=2, dy=2, sigmaX=4, sigmaY=4, color=color)
    )