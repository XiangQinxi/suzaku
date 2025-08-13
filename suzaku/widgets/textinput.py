from .textinputbase import SkTextInputBase


class SkTextInput(SkTextInputBase):
    """A single-line input box with a border 【带边框的单行输入框】"""

    # region Init 初始化

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # endregion

    # region Draw 绘制

    def _draw(self, canvas, rect) -> None:
        if self.is_mouse_floating:
            if self.is_focus:
                sheets = self.styles["SkTextInput"]["focus"]
            else:
                sheets = self.styles["SkTextInput"]["hover"]
        elif self.is_focus:
            sheets = self.styles["SkTextInput"]["focus"]
        else:
            sheets = self.styles["SkTextInput"]["rest"]

        # Draw the border
        self._draw_frame(
            canvas,
            rect,
            radius=self.theme.get_style("SkTextInput")["radius"],
            bg=sheets["bg"],
            bd=sheets["bd"],
            width=sheets["width"],
        )

        # Draw the text input
        self._draw_text_input(
            canvas, rect, fg=sheets["fg"], placeholder=sheets["placeholder"]
        )

    # endregion
