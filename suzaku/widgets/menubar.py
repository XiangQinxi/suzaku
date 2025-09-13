from typing import Callable

import skia

from ..styles.color import skcolor_to_color
from .card import SkCard
from .checkitem import SkCheckItem
from .menu import SkMenu
from .menuitem import SkMenuItem
from .radioitem import SkRadioItem
from .separator import SkSeparator
from .window import SkWindow


class SkMenuBar(SkCard):
    def __init__(self, parent: SkWindow, *, style: str = "SkMenuBar", **kwargs):
        super().__init__(parent, style=style, **kwargs)

        self.items: list[
            SkMenuItem | SkSeparator | SkCheckItem | SkRadioItem | SkMenu
        ] = []

    def draw_widget(self, canvas: skia.Canvas, rect: skia.Rect) -> None:
        super().draw_widget(canvas, rect)
        style = self.theme.get_style(self.style)
        self._draw_line(
            canvas,
            self.canvas_x,
            self.canvas_y + self.height,
            self.canvas_x + self.width,
            self.canvas_y + self.height,
            fg=style["fg"],
            width=style["width"],
        )

    def add(self, item: SkMenuItem | SkCheckItem | SkSeparator | SkRadioItem | SkMenu):
        self.items.append(item)

    def add_command(self, text: str | None = None, **kwargs):
        button = SkMenuItem(self, text=text, **kwargs)
        button.box(side="left", padx=(2, 4), pady=3)
        self.add(button)
        return button.id

    def add_cascade(self, text: str | None = None, **kwargs):
        button = SkMenu(self, text=text, **kwargs)
        button.box(side="left", padx=(2, 4), pady=3)
        self.add(button)
        return button.id

    def add_separator(self, orient: str = "vertical", **kwargs):
        separator = SkSeparator(self, orient=orient, **kwargs)
        separator.box(side="left", padx=0, pady=3)
        self.add(separator)
        return separator.id
