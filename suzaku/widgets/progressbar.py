from .container import SkContainer
from .widget import SkWidget


class SkProgressBar(SkWidget):
    def __init__(
        self,
        parent: SkContainer,
        *,
        style: str = "SkProgressBar",
        **kwargs,
    ) -> None:
        super().__init__(parent, style_name=style, **kwargs)
