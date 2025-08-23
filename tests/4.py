import skia


def draw_wrapped_text(
    canvas: skia.Canvas, text: str, rect: skia.Rect, font: skia.Font, paint: skia.Paint
):
    """
    在指定 rect 内绘制自动换行文本（支持中英文混排）
    rect: skia.Rect 指定绘制区域
    """
    # 拿到字体度量
    metrics = font.getMetrics()
    ascent, descent = -metrics.fAscent, metrics.fDescent
    line_height = (descent + ascent) * 1.2  # 行高
    y = rect.top() + ascent  # 首行 baseline

    # 文本分割（中文按字，英文按词）
    tokens = []
    for word in text.split(" "):
        if any("\u4e00" <= ch <= "\u9fff" for ch in word):  # 包含中文
            tokens.extend(list(word))  # 按字切
        else:
            tokens.append(word)
        tokens.append(" ")  # 保留空格
    if tokens:
        tokens.pop()  # 去掉最后多余的空格

    current_line = ""
    for token in tokens:
        test_line = current_line + token
        width = font.measureText(test_line, paint=paint)

        if rect.left() + width > rect.right():  # 换行
            blob = skia.TextBlob(current_line.rstrip(), font)
            canvas.drawTextBlob(blob, rect.left(), y, paint)
            y += line_height
            current_line = token.lstrip()

            if y + descent > rect.bottom():  # 超出底部
                break
        else:
            current_line = test_line

    # 绘制最后一行
    if current_line and y + descent <= rect.bottom():
        blob = skia.TextBlob(current_line.rstrip(), font)
        canvas.drawTextBlob(blob, rect.left(), y, paint)


# ========== 测试 ==========
if __name__ == "__main__":
    surface = skia.Surface(400, 300)
    canvas = surface.getCanvas()
    canvas.clear(skia.ColorWHITE)

    font = skia.Font(skia.Typeface("Microsoft Yahei"), 20)
    paint = skia.Paint(AntiAlias=True, Color=skia.ColorBLACK)

    rect = skia.Rect(20, 20, 380, 280)
    canvas.drawRect(
        rect, skia.Paint(Color=skia.ColorGRAY, Style=skia.Paint.kStroke_Style)
    )

    text = "This is a long text string 自动换行测试 with 中文 characters inside to check 自动 line wrapping."
    draw_wrapped_text(canvas, text, rect, font, paint)

    image = surface.makeImageSnapshot()
    image.save("wrapped_text_full.png", skia.kPNG)
