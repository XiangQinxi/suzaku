import skia

from .lineinput import SkLineInput


class SkEntry(SkLineInput):
    """A single-line input box with a border 【带边框的单行输入框】"""

    # region Init 初始化
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.padding = 5

    # endregion

    # region Draw 绘制

    def draw_widget(self, canvas, rect) -> None:
        if self.is_mouse_floating:
            if self.is_focus:
                style_name = "SkEntry:focus"
            else:
                style_name = "SkEntry:hover"
        elif self.is_focus:
            style_name = "SkEntry:focus"
        else:
            style_name = "SkEntry"

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

        # Draw the border
        self._draw_frame(
            canvas,
            rect,
            radius=self.theme.get_style_attr("SkEntry", "radius"),
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
            rect.top() + self.padding,
            rect.right() - self.padding,
            rect.bottom() - self.padding,
        )

        self._draw_text_input(
            canvas,
            input_rect,
            fg=style["fg"],
            placeholder=placeholder,
            selected_bg=selected_bg,
            selected_fg=selected_fg,
            cursor=cursor,
        )

    # endregion
