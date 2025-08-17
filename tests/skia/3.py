import skia


class AdvancedTextLayout:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.surface = skia.Surface(width, height)
        self.canvas = self.surface.getCanvas()
        self.canvas.clear(skia.Color(255, 255, 255, 255))

    def create_text_block(self, text, x, y, width, height, **kwargs):
        """创建文本块（支持滚动和裁剪）"""
        # 创建裁剪区域
        clip_rect = skia.Rect.MakeXYWH(x, y, width, height)
        self.canvas.save()
        self.canvas.clipRect(clip_rect, skia.ClipOp.kIntersect)

        # 绘制文本
        lines = self.wrap_text_to_height(text, width, height, **kwargs)
        line_height = kwargs.get('line_height', kwargs.get('font_size', 24) * 1.2)

        for i, line in enumerate(lines):
            current_y = y + i * line_height
            if current_y < y + height:  # 确保不超出边界
                self.draw_styled_text(line, x, current_y, **kwargs)

        self.canvas.restore()

    def wrap_text_to_height(self, text, max_width, max_height, **kwargs):
        """将文本包装到指定高度"""
        font_size = kwargs.get('font_size', 24)
        line_height = kwargs.get('line_height', font_size * 1.2)
        max_lines = int(max_height / line_height)

        lines = self.auto_wrap_text(text, max_width, font_size,
                                    kwargs.get('font_family', 'Microsoft Yahei'))

        return lines[:max_lines]  # 限制行数

    def auto_wrap_text(self, text, max_width, font_size=24, font_family='Microsoft Yahei'):
        """自动换行文本（优化版本）"""
        typeface = skia.Typeface(font_family)
        font = skia.Font(typeface, font_size)

        # 处理换行符
        paragraphs = text.split('\n')
        all_lines = []

        for paragraph in paragraphs:
            if not paragraph.strip():
                all_lines.append("")
                continue

            words = paragraph.split()
            if not words:
                continue

            lines = []
            current_line = ""

            for word in words:
                test_line = current_line + (" " if current_line else "") + word
                text_width = font.measureText(test_line)

                if text_width <= max_width:
                    current_line = test_line
                else:
                    if current_line:
                        lines.append(current_line)
                        current_line = word
                    else:
                        # 单词太长，需要字符级换行
                        lines.extend(self.wrap_long_word(word, max_width, font))
                        current_line = ""

            if current_line:
                lines.append(current_line)

            all_lines.extend(lines)

        return all_lines

    def wrap_long_word(self, word, max_width, font):
        """处理超长单词的字符级换行"""
        chars = list(word)
        lines = []
        current_line = ""

        for char in chars:
            test_line = current_line + char
            if font.measureText(test_line) <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = char

        if current_line:
            lines.append(current_line)

        return lines if lines else [word]

    def draw_styled_text(self, text, x, y, font_size=24, color=(0, 0, 0, 255),
                         font_family='Microsoft Yahei', bold=False, italic=False):
        """绘制样式化文本"""
        typeface = skia.Typeface(font_family,
                                 skia.FontStyle.Bold() if bold else skia.FontStyle.Normal())
        font = skia.Font(typeface, font_size)

        paint = skia.Paint()
        paint.setColor(skia.Color(*color))

        self.canvas.drawString(text, x, y, font, paint)

    def draw_rich_text(self, text_elements, x, y):
        """绘制富文本（不同样式）"""
        current_x = x
        current_y = y

        for element in text_elements:
            text = element['text']
            font_size = element.get('font_size', 24)
            color = element.get('color', (0, 0, 0, 255))
            font_family = element.get('font_family', 'Microsoft Yahei')
            bold = element.get('bold', False)

            typeface = skia.Typeface(font_family,
                                     skia.FontStyle.Bold() if bold else skia.FontStyle.Normal())
            font = skia.Font(typeface, font_size)

            paint = skia.Paint()
            paint.setColor(skia.Color(*color))

            self.canvas.drawString(text, current_x, current_y, font, paint)

            # 更新下一个文本的位置
            text_width = font.measureText(text)
            current_x += text_width

    def save(self, filename):
        """保存图片"""
        image = self.surface.makeImageSnapshot()
        image.save(filename, skia.kPNG)


# 富文本示例
def rich_text_example():
    layout = AdvancedTextLayout(1000, 600)

    # 创建富文本元素
    rich_text = [
        {'text': '这是', 'font_size': 24, 'color': (0, 0, 0, 255)},
        {'text': '红色', 'font_size': 24, 'color': (255, 0, 0, 255), 'bold': True},
        {'text': '的文本，', 'font_size': 24, 'color': (0, 0, 0, 255)},
        {'text': '这是', 'font_size': 24, 'color': (0, 0, 0, 255)},
        {'text': '蓝色', 'font_size': 24, 'color': (0, 0, 255, 255), 'bold': True},
        {'text': '的文本。', 'font_size': 24, 'color': (0, 0, 0, 255)},
    ]

    layout.draw_rich_text(rich_text, 50, 50)

    # 文本块示例
    long_text = """这是一个文本块示例。它会自动换行并限制在指定区域内。
    这个功能非常适合用来显示长篇文章或者用户输入的内容。
    Skia-Python 提供了强大的文本处理能力，可以轻松实现复杂的文本布局。"""

    layout.create_text_block(long_text, 50, 100, 400, 200, font_size=16)

    layout.save('rich_text.png')


rich_text_example()
