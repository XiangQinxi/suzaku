import typing

import skia

from ..const import Orient
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
        super().__init__(master, style_name=style, **kwargs)

        if orient is None:
            orient = Orient.H

        width = self.theme.get_style_attr(self.style_name, "width")
        if orient == Orient.H:
            self.configure(dheight=width)
        else:
            self.configure(dwidth=width)

        self.attributes["orient"] = orient

        self.help_parent_scroll = True

    def draw_widget(self, canvas: skia.Canvas, rect: skia.Rect) -> None:
        orient = self.cget("orient")
        width = self.theme.get_style_attr(self.style_name, "width")
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
                fg=self._style2(self.theme, self.style_name, "fg", "gray"),
                width=self._style2(self.theme, self.style_name, "width", 2),
            )
        else:
            self._draw_line(
                canvas,
                x0=rect.centerX(),
                y0=rect.top(),
                x1=rect.centerX(),
                y1=rect.bottom(),
                fg=self._style2(self.theme, self.style_name, "fg", "gray"),
                width=self._style2(self.theme, self.style_name, "width", 2),
            )
