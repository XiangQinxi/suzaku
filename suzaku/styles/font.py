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
        """
        ...

    @staticmethod
    def font(
        name: str = None,
        font_path: Union[Path, str] = None,
        size: int | float = 14,
    ) -> skia.Font:
        """
        Get font from path

        :param font_path: Path to a font file.
        :param name: Name of the local font.

        :param path: Path to a font file.

        :param size: SkFont size.
        :return: skia.Font object
        """
        size = size

        if name:
            _font = skia.Font(skia.Typeface(name), size)
        elif font_path:
            if not os.path.exists(font_path):
                raise FileNotFoundError
            _font = skia.Font(skia.Typeface.MakeFromFile(path=font_path), size)
        else:
            _font = skia.Font(skia.Typeface(), size=14.5)
        return _font


default_font = SkFont.font(None)
