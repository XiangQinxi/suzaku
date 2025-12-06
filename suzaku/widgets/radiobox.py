import typing

import skia

from ..event import SkEvent
from ..styles.color import skcolor_to_color, style_to_color
from ..var import SkVar
from .widget import SkWidget


class SkRadioBox(SkWidget):
    def __init__(
        self,
        *args,
        cursor: str | None = "arrow",
        command: typing.Callable | None = None,
        selected: bool = False,
        style: str = "SkRadioBox",
        value: bool | int | float | str | None = None,
        variable: SkVar | None = None,
        **kwargs,
    ):
        super().__init__(*args, cursor=cursor, style_name=style, **kwargs)
        self.attributes["selected"] = selected
        self.attributes["value"] = value
        self.attributes["variable"]: SkVar = variable

        self.focusable = True
        self.help_parent_scroll = True
        self.command = command
        self.bind("click", lambda _: self.invoke())

        self._state = "checked" if self.checked else "unchecked"

        if variable:
            variable.bind("change", self._on_variable_change)

    def _on_variable_change(self, event: SkEvent):
        """【处理变量变化事件，更新复选框的选中状态】"""
        self._checked = self.cget("variable").get()
        self.style_state("checked" if self.checked else "unchecked")
        self.update(True)

    def _on_mouse_leave(self, event: SkEvent):
        pass

    def _on_mouse_press(self, event: SkEvent):
        pass

    def _on_mouse_enter(self, event: SkEvent):
        pass

    def _on_focus_loss(self, event: SkEvent):
        pass

    @property
    def checked(self) -> bool:
        if self.cget("variable"):
            return self.cget("variable").get() == self.cget("value")
        else:
            return False

    def invoke(self):
        if self.attributes["variable"] is not None:
            self.attributes["variable"].set(self.cget("value"))
        if self.command:
            self.command()
        if self.checked:
            self.style_state("checked")
        else:
            self.style_state("unchecked")
        self.update(True)

    def _on_click(self, event: SkEvent):
        self.invoke()

    def draw_widget(self, canvas: skia.Canvas, rect: skia.Rect):
        """if self.is_mouse_floating:
            if self.is_mouse_press:
                style_selector = "SkCheckBox:press"
            else:
                style_selector = "SkCheckBox:hover"
        else:
            if self.is_focus:
                style_selector = "SkCheckBox:focus"
            else:"""
        style_selector = self.get_style_selector()
        if self.is_mouse_floating:
            style_selector = style_selector + "-hover"
        else:
            """if self.is_focus:
                style_selector = style_selector + "-focus"
            else:
                style_selector = style_selector + "-rest"""
            style_selector = style_selector + "-rest"

        bg_shader = self._style2(self.theme, style_selector, "bg_shader")
        bd_shadow = self._style2(self.theme, style_selector, "bd_shadow")
        bd_shader = self._style2(self.theme, style_selector, "bd_shader")
        width = self._style2(self.theme, style_selector, "width", 0)
        inner_width = self._style2(self.theme, style_selector, "inner_width", 3)
        bd = self._style2(self.theme, style_selector, "bd")
        bg = self._style2(self.theme, style_selector, "bg")
        fg = self._style2(self.theme, style_selector, "fg")

        _ = min(rect.width(), rect.height())
        self._draw_circle(
            canvas,
            rect.centerX(),
            rect.centerY(),
            radius=_ / 2,
            bg=bg,
            width=width,
            bd=bd,
            bd_shadow=bd_shadow,
            bd_shader=bd_shader,
            bg_shader=bg_shader,
        )

        if self.checked:
            self._draw_circle(
                canvas,
                rect.centerX(),
                rect.centerY(),
                radius=_ / 2 - inner_width,
                bg=fg,
                width=0,
                bg_shader=bg_shader,
            )
