import os
import warnings
from pathlib import Path
from typing import Any, Union

import skia


class SkFontDefaultFontCannotGet(Exception): ...


class SkFont:
    """SkFont object. For customizing fonts in your UI"""

    default_font_retrieval_method = "tkinter"

    @property
    def default_font(self) -> skia.Font | None:
        """Get default font via different system

        Example
        -------
        .. code-block:: python
            # get the system default font
            default_font = SkFont().default_font
        """

        # _ = skia.FontMgr.RefDefault().legacyMakeTypeface("", skia.FontStyle()) # seems right, but won't return font that support Chinese, shit

        match self.default_font_retrieval_method:
            case "tkinter":
                import platform
                import tkinter as tk
                import tkinter.font as tkfont

                root = tk.Tk()
                f = tkfont.nametofont("TkDefaultFont").actual().get("family")
                root.destroy()

                if f == ".AppleSystemUIFont":
                    if int(platform.mac_ver()[0].split(".")[0]) >= 11:
                        f = "SF Pro"
                    elif platform.mac_ver()[0] == "10.15":
                        f = "Helvetica Neue"
                    else:
                        f = "Lucida Grande"

                del root, tk, tkfont, platform

                return self.font(name=f)
            case "skia":
                return self.font(name=None)
        raise SkFontDefaultFontCannotGet

    @staticmethod
    def font(
        name: str = None,
        font_path: Path | str = None,
        size: int | float = 14,
        anti_alias: bool = False,
    ) -> skia.Font:
        """
        Get font from path

        >>> font = SkFont.font(font_path="Sans.ttf")
        >>> font2 = SkFont.font(name="Microsoft YaHei", size=16)

        :param font_path: Path to a font file.
        :param str name: Name of the local font.
        :param int | float size: SkFont size.
        :param anti_alias: Whether to enable anti-alias.

        :return: skia.Font object
        """

        if name:
            _font = skia.Font(skia.Typeface(name), size)
        elif font_path:
            if not os.path.exists(font_path):
                raise FileNotFoundError
            _font = skia.Font(skia.Typeface.MakeFromFile(path=font_path), size)
        else:
            _font = skia.Font(skia.Typeface(None), size)
        if anti_alias:
            _font.setEdging(skia.Font.Edging.kSubpixelAntiAlias)
            _font.setSubpixel(True)
        return _font


default_font = SkFont().default_font
