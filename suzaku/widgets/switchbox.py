import skia

from ..event import SkEvent
from ..var import SkBooleanVar
from .checkbox import SkCheckBox
from .container import SkContainer
from .widget import SkWidget


class SkSwitchBox(SkCheckBox):
    def __init__(
        self,
        parent: SkContainer,
        *,
        style: str = "SkSwitchBox",
        **kwargs,
    ):
        super().__init__(parent, style=style, **kwargs)

        def record_mouse_pos(event: SkEvent):
            if self._pressing:
                self._x1 = event["x"]
                self.update(redraw=True)

        def record_mouse_pressing(event: SkEvent):
            self._pressing = True
            self._x1 = event["x"]

        def record_mouse_released(event: SkEvent):
            if self._pressing:
                self._pressing = False
                self._on_click(event)

        self._x1 = None
        self._pressing = False
        self.bind("mouse_press", record_mouse_pressing)
        self.window.bind("mouse_move", record_mouse_pos)
        self.window.bind("mouse_release", record_mouse_released)

    def _on_click(self, event: SkEvent):
        center_x = self.canvas_x + self.width / 2
        if self.checked:
            if self._x1 > center_x:
                return
        else:
            if self._x1 < center_x:
                return
        self.invoke()

    def draw_widget(self, canvas: skia.Canvas, rect: skia.Rect, style_selector=None) -> None:
        if style_selector is None:
            style_selector = self.get_style_selector()

            if self.is_mouse_floating:
                if self.is_mouse_press:
                    style_selector = style_selector + "-press"
                else:
                    style_selector = style_selector + "-hover"
            else:
                style_selector = style_selector + "-rest"

        bd_shadow = self._style2(self.theme, style_selector, "bd_shadow")
        width = self._style2(self.theme, style_selector, "width", 0)
        bd = self._style2(self.theme, style_selector, "bd")
        bg = self._style2(self.theme, style_selector, "bg")
        radius = self._style2(self.theme, style_selector, "radius", 0)

        self._draw_rect(
            canvas,
            rect,
            radius=radius,
            bd_shadow=bd_shadow,
            width=width,
            bd=bd,
            bg=bg,
        )

        x = 0
        left = rect.x() + rect.height() / 2
        right = rect.x() + rect.width() - rect.height() / 2

        if self.checked:
            if self._pressing:
                x = max(min(self._x1, right), left)
            else:
                x = right
        else:
            if self._pressing:
                x = min(max(self._x1, left), right)
            else:
                x = left

        button = self._style2(self.theme, style_selector, "button")
        padding = self._style2(self.theme, style_selector, "button-padding", 0)
        shape = self._style2(self.theme, style_selector, "shape", "circle")
        radius2 = self._style2(self.theme, style_selector, "radius2", radius / 2)

        match shape:
            case "circle":
                self._draw_circle(
                    canvas,
                    x,
                    rect.centerY(),
                    radius=rect.height() / 2 - padding / 2,
                    bg=button,
                )
            case "rect":
                button_rect = skia.Rect.MakeLTRB(
                    x - rect.height() / 2 + padding / 2,
                    rect.top() + padding / 2,
                    x + rect.height() / 2 - padding / 2,
                    rect.bottom() - padding / 2,
                )
                self._draw_rect(
                    canvas,
                    button_rect,
                    radius=radius2,
                    bg=button,
                )
