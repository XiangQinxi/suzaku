import skia

from .card import SkCard
from .sizegrip import SkSizeGrip
from .text import SkText


class SkTipBar(SkCard):
    def __init__(self, parent, *, style="SkTipBar", prefix: str | None = "Tip: ", **kwargs):
        super().__init__(parent, style=style, **kwargs)

        self.attributes["prefix"] = prefix

        self.text = SkText(self)
        self.text.box(side="left", padx=2, pady=2)

        self.sizegrip = SkSizeGrip(self)
        self.sizegrip.box(side="right", padx=2, pady=2)

    def draw_widget(self, canvas: skia.Canvas, rect: skia.Rect) -> None:
        super().draw_widget(canvas, rect)
        if self.window.last_entered_widget:
            self.text.set(
                f'{self.cget("prefix")}{self.window.last_entered_widget.cget("status_tip")}'
            )
