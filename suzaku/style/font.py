import warnings
from typing import Union, Any


def default_font() -> "Font":
    """
    Default font (Harmony Sans SC).

    默认字体 (鸿蒙SC字体)。

    Returns:
        font (Font): The default font.
    """
    import os
    font_path = os.path.join(os.path.dirname(__file__), 'fonts', 'HarmonyOS_Sans_SC_Regular.ttf')
    return font(path=font_path, size=14.5)


def font(*args, **kwargs):
    return Font(*args, **kwargs).get_font()


class Font:

    """
    Font
    
    字体
    """

    from pathlib import Path

    def __init__(self, name: str = None, path: Union[Path, str] = None, size: int = 14):
        """
        Font object. For customizing fonts in your UI
    
        字体对象。用于自定义您界面上的字体

        Args:
            name (str): 
                Name of the local font.

                本地电脑存在的字体名称。

            path (Path | str):
                Path to a font file.
                
                字体文件路径。

            size (int): 
                Font size.

                字体大小。

        """
        import skia
        import os

        self.size = size

        try:
            if name:
                self.name = name
                self.font = skia.Font(skia.Typeface(name), size)
            elif path:
                if not os.path.exists(path):
                    raise FileNotFoundError
                self.path = path
                self.font = skia.Font(skia.Typeface.MakeFromFile(self.path), size)
            else:
                raise ValueError
        except:
            warnings.warn("Invalid font arguments or font! Falling back to default")


    def get_font(self):
        """
        Get the skia font object.

        获取skia字体对象。

        Returns:
            self.font (Font): skia font object. skia字体对象。
        """
        return self.font