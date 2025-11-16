import skia

from .container import SkContainer
from .textbutton import SkTextButton


class SkTabButton(SkTextButton):
    """A tab button"""

    def __init__(
        self,
        parent: SkContainer,
        text: str = None,
        style: str = "SkTabBar.Button",
        align: str = "center",
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
        self.focusable = False

    @property
    def selected(self):
        """Check if the tab button is selected"""
        if self.parent.selected_item is None:
            return False
        return self.parent.selected_item == self

    def _on_click(self):
        """Handle click event"""
        self.parent.select(self.parent.items.index(self))

    def draw_widget(
        self, canvas: skia.Canvas, rect: skia.Rect, style_selector: str | None = None
    ) -> None:
        """Draw the tab button

        :param canvas: The canvas to draw on
        :param rect: The rectangle to draw in
        :param style_selector: The style name
        :return: None
        """
        if self.selected:
            style_selector = f"{self.style_name}:selected"
        else:
            if self.is_mouse_floating:
                if self.is_mouse_press:
                    style_selector = f"{self.style_name}:press"
                else:
                    style_selector = f"{self.style_name}:hover"

        super().draw_widget(canvas, rect, style_selector)

        style = self.theme.select(style_selector)
        underline = self._style("underline", "transparent", style)
        underline_width = self._style("underline_width", 0, style)
        underline_shadow = self._style("underline_shadow", 0, style)
        underline_shader = self._style("underline_shader", None, style)
        underline_ipadx = self.unpack_padx(self._style("underline_ipadx", (5, 5), style))

        if self.selected:
            self._draw_line(
                canvas,
                self.canvas_x + underline_ipadx[0],
                self.canvas_y + self.height,
                self.canvas_x + self.width - underline_ipadx[1],
                self.canvas_y + self.height,
                width=underline_width,
                fg=underline,
                shader=underline_shader,
                shadow=underline_shadow,
            )
