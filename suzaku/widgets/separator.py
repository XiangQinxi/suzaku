import typing

import skia

from .widget import SkWidget

H = HORIZONTAL = "horizontal"
V = VERTICAL = "vertical"


class SkSeparator(SkWidget):
    def __init__(
        self,
        master=None,
        *,
        style: str = "SkSeparator",
        orient: typing.Literal["horizontal", "vertical"] = "horizontal",
        **kwargs,
    ):
        super().__init__(master, style=style, **kwargs)

        self.attributes["orient"] = orient

        if orient == HORIZONTAL:
            self.configure(dheight=self.theme.get_style_attr(self.style, "width"))
        else:
            self.configure(dwidth=self.theme.get_style_attr(self.style, "height"))
        self.help_parent_scroll = True

    def draw_widget(self, canvas: skia.Canvas, rect: skia.Rect) -> None:
        style = self.theme.get_style(self.style)
        if self.attributes["orient"] == HORIZONTAL:
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
