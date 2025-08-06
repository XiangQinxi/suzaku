import os
import warnings
from pathlib import Path
from typing import Any, Union

import skia


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

    def default_font(self):
        from sys import platform

        if platform == "win32":
            f = "Microsoft YaHei"

        return self.font(name=f, size=14.5)

    def font(
        self,
        name: str = None,
        font_path: Union[Path, str] = None,
        size: int | float = 14,
    ):
        size = size

        if name:
            name = name
            font = skia.Font(skia.Typeface(name), size)
        elif font_path:
            if not os.path.exists(font_path):
                raise FileNotFoundError
            font = skia.Font(skia.Typeface.MakeFromFile(path=font_path), size)
        else:
            font = self.default_font()
        return font


default_font = SkFont().default_font()
