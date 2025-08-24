import skia

from .container import SkContainer
from .lineinput import SkLineInput


class SkEntry(SkLineInput):
    """A single-line input box with a border 【带边框的单行输入框】"""

    # region Init 初始化
    def __init__(self, parent: SkContainer, *, style: str = "SkEntry", **kwargs):
        super().__init__(parent=parent, style=style, **kwargs)

        self.padding = 5

    # endregion

    # region Draw 绘制

    def draw_widget(self, canvas, rect) -> None:
        if self.is_mouse_floating:
            if self.is_focus:
                style_name = self.style + ":focus"
            else:
                style_name = self.style + ":hover"
        elif self.is_focus:
            style_name = self.style + ":focus"
        else:
            style_name = self.style

        style = self.theme.get_style(style_name)
        radius = self.theme.get_style_attr(self.style, "radius")

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

        if "selected_bg" in style:
            selected_bg = style["selected_bg"]
        else:
            selected_bg = skia.ColorBLUE
        if "selected_fg" in style:
            selected_fg = style["selected_fg"]
        else:
            selected_fg = skia.ColorWHITE
        if "cursor" in style:
            cursor = style["cursor"]
        else:
            cursor = None
        if "placeholder" in style:
            placeholder = style["placeholder"]
        else:
            placeholder = None
        if "selected_radius" in style:
            selected_radius = style["selected_radius"]
        else:
            selected_radius = True
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
            bg=style["bg"],
            bd=style["bd"],
            width=style["width"],
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
            fg=style["fg"],
            placeholder=placeholder,
            selected_bg=selected_bg,
            selected_fg=selected_fg,
            cursor=cursor,
            radius=selected_radius,
        )

    # endregion
