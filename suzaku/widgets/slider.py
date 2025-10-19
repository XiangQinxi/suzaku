import skia

from .widget import SkWidget


class SkSlider(SkWidget):
    def __init__(
        self,
        parent,
        *,
        value: int | float = 50,
        minvalue: int | float = 0,
        maxvalue: int | float = 100,
        style: str = "SkSlider",
        **kwargs,
    ):
        super().__init__(parent, style_name=style, **kwargs)
        self.attributes["value"] = value
        self.attributes["minvalue"] = minvalue
        self.attributes["maxvalue"] = maxvalue

    def draw_widget(self, canvas: skia.Canvas, rect: skia.Rect) -> None:
        if not self.cget("disabled"):
            if self.is_mouse_floating:
                if self.is_mouse_press:
                    state = "pressed"
                else:
                    state = "hover"
            else:
                if "focus" in self.styles[self.style_name]:
                    if self.is_focus:
                        state = "focus"
                    else:
                        state = ""
                else:
                    state = ""
        else:
            state = "disabled"

        if state:
            selector = f"{self.style_name}:{state}"
        else:
            selector = self.style_name

        style = self.theme.select(selector)
        progress_style = self.theme.select(self.style_name + ".Progress")

        progress_rect = skia.Rect.MakeLTRB(
            rect.left(),
            rect.top() + self._style("pady", 0, progress_style),
            rect.width()
            * (self.cget("value") / (self.cget("maxvalue") - self.cget("minvalue"))),
            rect.bottom() - self._style("pady", 0, progress_style),
        )
        if self.cget("value") > self.cget("minvalue"):
            self._draw_rect(
                canvas,
                progress_rect,
                self._style("radius", 0, progress_style),
                bg=self._style("bg", skia.ColorBLACK, progress_style),
                bd=self._style("bd", 0, progress_style),
                width=self._style("width", 0, progress_style),
            )
