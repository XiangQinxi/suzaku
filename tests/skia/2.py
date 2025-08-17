import skia


class TextRenderer:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.surface = skia.Surface(width, height)
        self.canvas = self.surface.getCanvas()
        self.canvas.clear(skia.Color(255, 255, 255, 255))

    def draw_styled_text(self, text, x, y, font_size=24, color=(0, 0, 0, 255),
                         font_family='Microsoft Yahei', bold=False, italic=False):
        """绘制样式化文本"""
        # 创建字体
        typeface = skia.Typeface(font_family,
                                 skia.FontStyle.Bold() if bold else skia.FontStyle.Normal())
        font = skia.Font(typeface, font_size)

        # 创建画笔
        paint = skia.Paint()
        paint.setColor(skia.Color(*color))

        # 绘制文本
        self.canvas.drawString(text, x, y, font, paint)

    def draw_multiline_text(self, lines, x, y, line_height=None, **kwargs):
        """绘制多行文本"""
        font_size = kwargs.get('font_size', 24)
        line_height = line_height or font_size * 1.2

        for i, line in enumerate(lines):
            current_y = y + i * line_height
            self.draw_styled_text(line, x, current_y, **kwargs)

    def measure_text(self, text, font_size=24, font_family='Microsoft Yahei'):
        """测量文本尺寸"""
        typeface = skia.Typeface(font_family)
        font = skia.Font(typeface, font_size)
        return font.measureText(text)

    def auto_wrap_text(self, text, max_width, font_size=24, font_family='Microsoft Yahei'):
        """自动换行文本"""
        typeface = skia.Typeface(font_family)
        font = skia.Font(typeface, font_size)

        words = text.split()
        lines = []
        current_line = ""

        for word in words:
            # 测试添加当前单词后的行宽
            test_line = current_line + (" " if current_line else "") + word
            text_width = font.measureText(test_line)

            if text_width <= max_width:
                current_line = test_line
            else:
                # 如果当前行不为空，保存当前行并开始新行
                if current_line:
                    lines.append(current_line)
                    current_line = word
                else:
                    # 单个单词就超出宽度，强制换行
                    lines.append(word)
                    current_line = ""

        # 添加最后一行
        if current_line:
            lines.append(current_line)

        return lines

    def draw_wrapped_text(self, text, x, y, max_width, font_size=24,
                          line_height=None, **kwargs):
        """绘制自动换行文本"""
        lines = self.auto_wrap_text(text, max_width, font_size,
                                    kwargs.get('font_family', 'Microsoft Yahei'))
        self.draw_multiline_text(lines, x, y, line_height, font_size=font_size, **kwargs)
        return len(lines)  # 返回行数

    def draw_text_with_background(self, text, x, y, padding=10,
                                  bg_color=(200, 200, 200, 255), **kwargs):
        """绘制带背景的文本"""
        font_size = kwargs.get('font_size', 24)
        typeface = skia.Typeface(kwargs.get('font_family', 'Microsoft Yahei'))
        font = skia.Font(typeface, font_size)

        # 测量文本尺寸
        text_width = font.measureText(text)
        text_height = font_size

        # 绘制背景矩形
        bg_paint = skia.Paint()
        bg_paint.setColor(skia.Color(*bg_color))
        bg_rect = skia.Rect.MakeXYWH(x - padding, y - text_height - padding,
                                     text_width + 2 * padding,
                                     text_height + 2 * padding)
        self.canvas.drawRect(bg_rect, bg_paint)

        # 绘制文本
        self.draw_styled_text(text, x, y, **kwargs)

    def draw_aligned_text(self, text, x, y, width, alignment='left', **kwargs):
        """绘制对齐文本"""
        font_size = kwargs.get('font_size', 24)
        typeface = skia.Typeface(kwargs.get('font_family', 'Microsoft Yahei'))
        font = skia.Font(typeface, font_size)

        text_width = font.measureText(text)

        if alignment == 'center':
            draw_x = x + (width - text_width) / 2
        elif alignment == 'right':
            draw_x = x + width - text_width
        else:  # left
            draw_x = x

        self.draw_styled_text(text, draw_x, y, **kwargs)

    def draw_text_with_shadow(self, text, x, y, shadow_offset=(2, 2),
                              shadow_color=(0, 0, 0, 128), **kwargs):
        """绘制带阴影的文本"""
        # 绘制阴影
        shadow_paint = skia.Paint()
        shadow_paint.setColor(skia.Color(*shadow_color))
        shadow_font = skia.Font(
            skia.Typeface(kwargs.get('font_family', 'Microsoft Yahei')),
            kwargs.get('font_size', 24)
        )
        self.canvas.drawString(text, x + shadow_offset[0], y + shadow_offset[1],
                               shadow_font, shadow_paint)

        # 绘制主文本
        self.draw_styled_text(text, x, y, **kwargs)

    def save(self, filename):
        """保存图片"""
        image = self.surface.makeImageSnapshot()
        image.save(filename, skia.kPNG)


# 使用示例
def advanced_text_examples():
    renderer = TextRenderer(1000, 800)

    # 1. 样式化文本
    renderer.draw_styled_text("Bold Text", 50, 50, font_size=30,
                              color=(255, 0, 0, 255), bold=True)
    renderer.draw_styled_text("Italic Text", 50, 100, font_size=24,
                              color=(0, 0, 255, 255), italic=True)

    # 2. 多行文本
    lines = ["Line 1", "Line 2", "Line 3"]
    renderer.draw_multiline_text(lines, 50, 150, font_size=20,
                                 color=(0, 128, 0, 255))

    # 3. 自动换行文本
    long_text = "这是一个很长的文本，需要自动换行显示。Skia-Python提供了强大的文本渲染功能，可以轻松实现各种复杂的文本布局。"
    renderer.draw_wrapped_text(long_text, 50, 250, max_width=400,
                               font_size=18, color=(128, 0, 128, 255))

    # 4. 带背景的文本
    renderer.draw_text_with_background("带背景的文本", 50, 400,
                                       bg_color=(255, 255, 0, 255),
                                       font_size=24, color=(0, 0, 0, 255))

    # 5. 对齐文本
    renderer.draw_aligned_text("左对齐", 500, 50, 300, 'left', font_size=20)
    renderer.draw_aligned_text("居中对齐", 500, 100, 300, 'center', font_size=20)
    renderer.draw_aligned_text("右对齐", 500, 150, 300, 'right', font_size=20)

    # 6. 带阴影的文本
    renderer.draw_text_with_shadow("带阴影的文本", 500, 200,
                                   shadow_offset=(3, 3),
                                   shadow_color=(0, 0, 0, 100),
                                   font_size=24, color=(255, 0, 0, 255))

    renderer.save('advanced_text.png')


advanced_text_examples()
