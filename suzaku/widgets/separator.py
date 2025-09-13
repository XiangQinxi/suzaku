import typing

import skia

from ..constants import Orient
from .widget import SkWidget


class SkSeparator(SkWidget):
    def __init__(
        self,
        master=None,
        *,
        style: str = "SkSeparator",
        orient: Orient | None = Orient.H,
        **kwargs,
    ):
        super().__init__(master, style=style, **kwargs)

        if orient is None:
            orient = Orient.H

        width = self.theme.get_style_attr(self.style, "width")
        if orient == Orient.H:
            self.configure(dheight=width)
        else:
            self.configure(dwidth=width)

        self.attributes["orient"] = orient

        self.help_parent_scroll = True

    def draw_widget(self, canvas: skia.Canvas, rect: skia.Rect) -> None:
        style = self.theme.get_style(self.style)
        orient = self.cget("orient")
        width = self.theme.get_style_attr(self.style, "width")
        # print(self.id, orient)

        if orient == Orient.H:
            self.configure(dheight=width)
        else:
            self.configure(dwidth=width)

        if orient == Orient.H:
            self._draw_line(
                canvas,
                x0=rect.left(),
                y0=rect.centerY(),
                x1=rect.right(),
                y1=rect.centerY(),
                fg=style["fg"],
                width=style["width"],
            )
        else:
            self._draw_line(
                canvas,
                x0=rect.centerX(),
                y0=rect.top(),
                x1=rect.centerX(),
                y1=rect.bottom(),
                fg=style["fg"],
                width=style["width"],
            )
