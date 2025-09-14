import skia

from ..event import SkEvent
from .container import SkContainer
from .widget import SkWidget


class SkSwitchBox(SkWidget):
    def __init__(
        self,
        parent: SkContainer,
        *,
        style: str = "SkSwitchBox",
        cursor="hand",
        command=None,
        **kwargs,
    ):
        super().__init__(parent, style=style, cursor=cursor, **kwargs)
        self.checked = False
        self.attributes["command"] = command
        self.bind("click", self._on_click)

    def _on_click(self, event: SkEvent):
        self.invoke()
        if self.cget("command"):
            self.cget("command")(self.checked)

    def invoke(self):
        self.checked = not self.checked

    def draw_widget(
        self, canvas: skia.Canvas, rect: skia.Rect, style_name=None
    ) -> None:
        if style_name is None:
            if self.checked:
                style_name = f"{self.style}:checked"
            else:
                style_name = f"{self.style}:unchecked"

            if self.is_mouse_floating:
                if self.is_mouse_pressed:
                    style_name = style_name + "-pressed"
                else:
                    style_name = style_name + "-hover"
            else:
                style_name = style_name + "-rest"

        style = self.theme.get_style(style_name)

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
            radius=self.theme.get_style(self.style)["radius"],
            bg_shader=bg_shader,
            bd_shadow=bd_shadow,
            bd_shader=bd_shader,
            width=width,
            bd=bd,
            bg=bg,
        )

        pressed = self.is_mouse_floating and self.is_mouse_pressed

        x = 0
        left = rect.x() + rect.height() / 2
        right = rect.x() + rect.width() - rect.height() / 2
        if self.checked:
            if pressed:
                x = max(min(self.mouse_x, right), left)
            else:
                x = right
        else:
            if pressed:
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
        self._draw_circle(
            canvas,
            x,
            rect.centerY(),
            radius=rect.height() / 2 - padding / 2,
            bg=button,
        )
