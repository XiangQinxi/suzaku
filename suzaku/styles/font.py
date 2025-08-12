import os
import warnings
from pathlib import Path
from typing import Any, Union

import skia


class SkFont:
    """
    SkFont
    """

    def __init__(
        self,
        name: str | None = None,
        path: Union[Path, str] | None = None,
        size: int = 14,
    ):
        """
        SkFont object. For customizing fonts in your UI
        """
        ...

    def default_font(self):
        """Get default font via different system

        Example
        -------
        .. code-block:: python
            # get the system default font
            default_font = SkFont.default_font()
        """
        # _ = skia.FontMgr.RefDefault().legacyMakeTypeface("", skia.FontStyle()) # seems right, but won't return font that support Chinese, shit
        import platform
        import tkinter as tk
        import tkinter.font as tkfont

        f = None

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


default_font = SkFont().default_font()
