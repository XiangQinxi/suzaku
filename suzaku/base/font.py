def default_font() -> "Font":
    """
    默认字体 (鸿蒙SC字体)

    :return: Font
    """
    import os
    font_path = os.path.join(os.path.dirname(__file__), 'fonts', 'HarmonyOS_Sans_SC_Regular.ttf')
    return font(path=font_path, size=14)


def font(*args, **kwargs):
    return Font(*args, **kwargs).get_font()


class Font:

    """
    字体
    """

    from pathlib import Path

    def __init__(self, name: str = None, path: Path = None, size: int = 14):
        """
        初始化

        :param name: 本地电脑存在的字体名称
        :param size: 字体大小
        """
        import skia

        self.size = size

        if name:
            self.name = name
            self.font = skia.Font(skia.Typeface(name), size)
        elif path:
            self.path = path
            self.font = skia.Font(skia.Typeface.MakeFromFile(self.path), size)

    def get_font(self):
        return self.font