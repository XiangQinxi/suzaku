from .textinputbase import SkTextInputBase


class SkTextInput(SkTextInputBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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

        self._draw_frame(
            canvas,
            rect,
            radius=self.styles["SkTextInput"]["radius"],
            bg=sheets["bg"],
            bd=sheets["bd"],
            width=sheets["width"],
        )
        self._draw_text_input(
            canvas, rect, fg=sheets["fg"], placeholder=sheets["placeholder"]
        )
