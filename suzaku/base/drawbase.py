import skia

from suzaku.styles.font import default_font


def set_rainbow_shader(rect_paint, rect):
    """Set rainbow shader of the rect

    :param rect_paint: The paint of the rect
    :param rect: The rect
    :return: None
    """
    rect_paint.setShader(
        skia.GradientShader.MakeSweep(
            cx=rect.centerX(),  # Center x position of the sweep
            cy=rect.centerY(),  # Center y position of the sweep
            startAngle=0,  # Start angle of the sweep in degrees
            endAngle=360,  # End angle of the sweep in degrees
            colors=[
                skia.ColorCYAN,  # Cyan
                skia.ColorMAGENTA,  # Magenta
                skia.ColorYELLOW,  # Yellow
                skia.ColorCYAN,  # Cyan
            ],
            localMatrix=None,  # Local matrix for the gradient
        )
    )


def set_drop_shadow(
    rect_paint, dx=5, dy=5, sigmaX=10, sigmaY=10, color=skia.ColorBLACK
):
    """Draw drop shadow of the rect

    :param rect_paint: The paint of the rect
    :param dx: The x offset of the drop shadow
    :param dy: The y offset of the drop shadow
    :param sigmaX: The standard deviation of the drop shadow in the x direction
    :param sigmaY: The standard deviation of the drop shadow in the y direction
    :param color: The color of the drop shadow
    :return: None
    """

    rect_paint.setImageFilter(
        skia.ImageFilters.DropShadow(dx, dy, sigmaX, sigmaY, color)
    )


def central_text(canvas, text, fg, x, y, width, height):
    """Draw central text

    .. note::
        >>> central_text(canvas, "Hello", skia.ColorBLACK, 0, 0, 100, 100)

    :param canvas: The canvas
    :param text: The text
    :param fg: The color of the text
    :param x: The x of the text
    :param y: The y of the text
    :param width: The width of the text
    :param height: The height of the text
    :return: None
    :raises: None
    """

    # 绘制字体
    text_paint = skia.Paint(AntiAlias=True, Color=fg)

    font = default_font()

    text_width = font.measureText(text)
    metrics = font.getMetrics()

    draw_x = x + width / 2 - text_width / 2
    draw_y = y + height / 2 - (metrics.fAscent + metrics.fDescent) / 2

    canvas.drawSimpleText(text, draw_x, draw_y, font, text_paint)
