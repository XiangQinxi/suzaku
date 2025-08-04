import os
import warnings
from pathlib import Path
from typing import Any, Union

import skia


def default_font() -> "SkFont":
    """
    Returns:
        font (SkFont): The default font.
    """
    from sys import platform
    if platform == "win32":
        f = "Microsoft YaHei"
    return font(name=f, size=14.5)


def font(*args, **kwargs):
    return SkFont(*args, **kwargs).font


class SkFont:

    """
    SkFont
    
    字体
    """

    def __init__(self, name: str = None, path: Union[Path, str] = None, size: int = 14):
        """
        SkFont object. For customizing fonts in your UI
    
        字体对象。用于自定义您界面上的字体

        Args:
            name (str): 
                Name of the local font.

                本地电脑存在的字体名称。

            path (Path | str):
                Path to a font file.
                
                字体文件路径。

            size (int): 
                SkFont size.

                字体大小。

        """


        self.size = size

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
            self.font = default_font()
