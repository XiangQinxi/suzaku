import skia

from .container import SkContainer
from .textbutton import SkTextButton
from ..event import SkEvent


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
        self.has_focus_style = False
        self.parent.bind("change", self._on_change)

    def _on_change(self, event: SkEvent):
        if event["item"] is self:
            self.style_state("selected")
        else:
            self.style_state("rest")

    @property
    def selected(self):
        """Check if the tab button is selected"""
        if self.parent.selected_item is None:
            return False
        return self.parent.selected_item == self

    def _on_mouse_enter(self, event: SkEvent):
        if not self.selected:
            super()._on_mouse_enter(event)

    def _on_mouse_leave(self, event: SkEvent):
        if not self.selected:
            super()._on_mouse_leave(event)

    def _on_mouse_press(self, event: SkEvent):
        if not self.selected:
            super()._on_mouse_press(event)

    def _on_focus_loss(self, event: SkEvent):
        pass

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
        if style_selector is None:
            style_selector = self.style_selector()

        super().draw_widget(canvas, rect, style_selector)

        if self.selected:
            underline_ipadx = self.unpack_padx(
                self._style2(self.theme, style_selector, "underline_ipadx", (5, 5))
            )
            self._draw_line(
                canvas,
                self.canvas_x + underline_ipadx[0],
                self.canvas_y + self.height,
                self.canvas_x + self.width - underline_ipadx[1],
                self.canvas_y + self.height,
                width=self._style2(self.theme, style_selector, "underline_width", 0),
                fg=self._style2(self.theme, style_selector, "underline", "transparent"),
                shader=self._style2(self.theme, style_selector, "underline_shader", None),
                shadow=self._style2(self.theme, style_selector, "underline_shadow", None),
            )
