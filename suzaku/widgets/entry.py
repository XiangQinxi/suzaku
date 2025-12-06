import skia

from .container import SkContainer
from .lineinput import SkLineInput
from .. import SkEvent


class SkEntry(SkLineInput):
    """A single-line input box with a border 【带边框的单行输入框】"""

    # region Init 初始化
    def __init__(self, parent: SkContainer, *, style_name: str = "SkEntry", **kwargs):
        super().__init__(parent=parent, style_name=style_name, **kwargs)

        self.padding = 5

    def _on_mouse_press(self, event: SkEvent):
        if self.cget("disabled"):
            self.style_state("disabled")
        else:
            self.style_state("focus")

    def _on_mouse_enter(self, event: SkEvent):
        if self.cget("disabled"):
            self.style_state("disabled")
        else:
            if self.is_focus:
                self.style_state("focus")
            else:
                self.style_state("hover")

    # endregion

    # region Draw 绘制

    def draw_widget(self, canvas, rect, style_selector: str | None = None) -> str:
        if style_selector is None:
            style_selector = self.style_selector()

        radius = self._style2(self.theme, style_selector, "radius", 0)
        bg_shader = self._style2(self.theme, style_selector, "bg_shader")
        bd_shader = self._style2(self.theme, style_selector, "bd_shader")
        bd_shadow = self._style2(self.theme, style_selector, "bd_shadow")
        width = self._style2(self.theme, style_selector, "width", 2)
        fg = self._style2(self.theme, style_selector, "fg", "black")
        bg = self._style2(self.theme, style_selector, "bg", "black")
        bd = self._style2(self.theme, style_selector, "bd", "black")
        selected_bg = self._style2(self.theme, style_selector, "selected_bg", "blue")
        selected_fg = self._style2(self.theme, style_selector, "selected_fg", "white")
        cursor = self._style2(self.theme, style_selector, "cursor")
        placeholder = self._style2(self.theme, style_selector, "placeholder")
        selected_radius = self._style2(self.theme, style_selector, "selected_radius", True)
        if isinstance(selected_radius, bool):
            if selected_radius:
                selected_radius = radius / 2
            else:
                selected_radius = 0

        # Draw the border
        self._draw_rect(
            canvas,
            rect,
            radius=radius,
            bg=bg,
            bd=bd,
            width=width,
            bd_shader=bd_shader,
            bg_shader=bg_shader,
            bd_shadow=bd_shadow,
        )

        # Draw the text input

        input_rect = skia.Rect.MakeLTRB(
            rect.left() + self.padding,
            rect.top() + self.padding - 2,
            rect.right() - self.padding,
            rect.bottom() - self.padding + 2,
        )

        self._draw_text_input(
            canvas,
            input_rect,
            fg=fg,
            placeholder=placeholder,
            selected_bg=selected_bg,
            selected_fg=selected_fg,
            cursor=cursor,
            radius=selected_radius,
        )

    # endregion
