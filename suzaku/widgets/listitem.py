import skia

from ..event import SkEvent
from ..var import SkBooleanVar
from .container import SkContainer
from .textbutton import SkTextButton


class SkListItem(SkTextButton):
    def __init__(
        self,
        parent: SkContainer,
        text: str = None,
        style: str = "SkListBox.Item",
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
        self.parent.select(self)

    def draw_widget(
        self, canvas: skia.Canvas, rect: skia.Rect, style_selector: str | None = None
    ) -> None:
        if self.selected:
            style_selector = f"{self.style_name}:selected"
        else:
            if self.is_mouse_floating:
                if self.is_mouse_press:
                    style_selector = f"{self.style_name}:press"
                else:
                    style_selector = f"{self.style_name}:hover"
        style = self.theme.select(style_selector)
        super().draw_widget(canvas, rect, style_selector)

        if self.selected:
            if "leftline" in style and "leftline_width" in style:
                leftline = self._style("leftline", None, style)
                leftline_width = self._style("leftline_width", 0, style)
                leftline_ipadx = self._style("leftline_ipadx", 2, style)
                leftline_ipady = self.unpack_pady(self._style("leftline_ipady", (5, 5), style))
                self._draw_line(
                    canvas,
                    rect.left() + leftline_ipadx,
                    rect.top() + leftline_ipady[0],
                    rect.left() + leftline_ipadx,
                    rect.bottom() - leftline_ipady[1],
                    width=leftline_width,
                    fg=leftline,
                )
