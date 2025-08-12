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

    def __init__(self, name: str | None = None, path: Union[Path, str] | None = None, size: int = 14):
        """
        SkFont object. For customizing fonts in your UI

        字体对象。用于自定义您界面上的字体
        """
        ...

    def default_font(self):
        """Get default font via different system"""
        import platform

        _font = skia.FontMgr.RefDefault().legacyMakeTypeface("", skia.FontStyle())

        if _font == ".AppleSystemUIFont":
            if int(platform.mac_ver()[0].split(".")[0]) >= 11:
                _font = "SF Pro"
            elif platform.mac_ver()[0] == "10.15":
                _font = "Helvetica Neue"
            else:
                _font = "Lucida Grande"

        return self.font(name=_font, size=14.5)

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

        if name:
            _font = skia.Font(skia.Typeface(name), size)
        elif font_path:
            if not os.path.exists(font_path):
                raise FileNotFoundError
            _font = skia.Font(skia.Typeface.MakeFromFile(path=font_path), size)
        else:
            raise ValueError("Unexcepted name or font_path in default_font()")
      
        return _font


default_font = SkFont.font(None)
