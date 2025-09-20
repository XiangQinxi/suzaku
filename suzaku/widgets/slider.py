from .widget import SkWidget


class SkSlider(SkWidget):
    def __init__(
        self,
        parent,
        *,
        value: int | float = 0,
        minvalue: int | float = 0,
        maxvalue: int | float = 100,
        style: str = "SkSlider",
        **kwargs,
    ):
        super().__init__(parent, style=style, **kwargs)
        self.attributes["value"] = value
        self.attributes["minvalue"] = minvalue
        self.attributes["maxvalue"] = maxvalue
