import skia

from .container import SkContainer
from .textbutton import SkTextButton


class SkTabButton(SkTextButton):
    def __init__(
        self,
        parent: SkContainer,
        text: str = None,
        style: str = "SkTabBar.Button",
        align: str = "left",
        **kwargs,
    ):
        super().__init__(
            parent,
            style=style,
            text=text,
            align=align,
            command=lambda: self._on_click(),
            **kwargs,
        )

    @property
    def selected(self):
        if self.parent.selected_item is None:
            return False
        return self.parent.selected_item == self

    def _on_click(self):
        self.parent.select(self.parent.items.index(self))

    def draw_widget(
        self, canvas: skia.Canvas, rect: skia.Rect, style_name: str | None = None
    ) -> None:
        if self.selected:
            style_name = f"{self.style}:selected"
        else:
            if self.is_mouse_floating:
                if self.is_mouse_pressed:
                    style_name = f"{self.style}:pressed"
                else:
                    style_name = f"{self.style}:hover"

        super().draw_widget(canvas, rect, style_name)

        style = self.theme.get_style(style_name)

        if self.selected:
            self._draw_line(
                canvas,
                self.canvas_x,
                self.canvas_y + self.height,
                self.canvas_x + self.width,
                self.canvas_y + self.height,
                width=style["underline_width"],
                fg=style["underline"],
            )
