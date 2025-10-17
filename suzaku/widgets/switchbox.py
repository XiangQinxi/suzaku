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

    def _on_click(self, event: SkEvent):
        center_x = self.canvas_x + self.width / 2
        if self.checked:
            if self.mouse_x > center_x:
                return
        else:
            if self.mouse_x < center_x:
                return
        self.invoke()

    def draw_widget(
        self, canvas: skia.Canvas, rect: skia.Rect, style_name=None
    ) -> None:
        rest_style = self.theme.select(self.style_name)

        if style_name is None:
            if self.checked:
                style_name = f"{self.style_name}:checked"
            else:
                style_name = f"{self.style_name}:unchecked"

            if self.is_mouse_floating:
                if self.is_mouse_press:
                    style_name = style_name + "-press"
                else:
                    style_name = style_name + "-hover"
            else:
                style_name = style_name + "-rest"

        style = self.theme.select(style_name)

        if "bg_shader" in style:
            bg_shader = style["bg_shader"]
        else:
            bg_shader = None

        if "bd_shadow" in style:
            bd_shadow = style["bd_shadow"]
        else:
            bd_shadow = None
        if "bd_shader" in style:
            bd_shader = style["bd_shader"]
        else:
            bd_shader = None

        if "width" in style:
            width = style["width"]
        else:
            width = 0
        if "bd" in style:
            bd = style["bd"]
        else:
            bd = None
        if "bg" in style:
            bg = style["bg"]
        else:
            bg = None

        self._draw_rect(
            canvas,
            rect,
            radius=rest_style["radius"],
            bg_shader=bg_shader,
            bd_shadow=bd_shadow,
            bd_shader=bd_shader,
            width=width,
            bd=bd,
            bg=bg,
        )

        press = self.is_mouse_floating and self.is_mouse_press

        x = 0
        left = rect.x() + rect.height() / 2
        right = rect.x() + rect.width() - rect.height() / 2
        if self.checked:
            if press:
                x = max(min(self.mouse_x, right), left)
            else:
                x = right
        else:
            if press:
                x = min(max(self.mouse_x, left), right)
            else:
                x = left

        if "button" in style:
            button = style["button"]
        else:
            button = None
        if "button-padding" in style:
            padding = style["button-padding"]
        else:
            padding = 0
        if "shape" in rest_style:
            shape = rest_style["shape"]
        else:
            shape = "circle"
        if "radius2" in rest_style:
            radius2 = rest_style["radius2"]
        else:
            radius2 = rest_style["radius"] / 2

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
