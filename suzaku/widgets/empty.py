from .widget import SkWidget


class SkEmpty(SkWidget):
    """
    Empty element, used only as a placeholder in layouts.
    """

    def __init__(self, *args, size=(0, 0), **kwargs) -> None:
        """Initialize empty element.

        * *args: SkVisual arguments
        * size: Default size
        * **kwargs: SkVisual arguments
        """
        super().__init__(*args, size=size, **kwargs)
        self.visual_attr["name"] = "sk_empty"

    def draw(self, canvas, rect) -> None:
        """Draw method, does nothing.

        * canvas: skia.Surface to draw on
        * rect: Rectangle to draw in
        """
        pass
