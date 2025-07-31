def default_font():
    import skia
    import os
    font_path = os.path.join(os.path.dirname(__file__), 'fonts', 'HarmonyOS_Sans_SC_Regular.ttf')
    return skia.Font(skia.Typeface.MakeFromFile(font_path), 14)


class Font:
    def __init__(self, name: str = None, size: int = 14):
        import skia
        self.name = name
        self.size = size
        self.font = skia.Font(skia.Typeface(name), size)
