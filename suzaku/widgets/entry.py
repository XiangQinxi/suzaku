from .lineinput import SkLineInput


class SkEntry(SkLineInput):
    """A single-line input box with a border 【带边框的单行输入框】"""

    # region Init 初始化
    # endregion

    # region Draw 绘制

    def _draw(self, canvas, rect) -> None:
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

        # Draw the border
        self._draw_frame(
            canvas,
            rect,
            radius=self.theme.get_style_attr("SkEntry", "radius"),
            bg=style["bg"],
            bd=style["bd"],
            width=style["width"],
        )

        # Draw the text input
        self._draw_text_input(
            canvas, rect, fg=style["fg"], placeholder=style["placeholder"]
        )

    # endregion
