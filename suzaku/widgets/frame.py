import skia

from .container import SkContainer
from .widget import SkWidget


class SkFrame(SkWidget, SkContainer):
    """Used for layout components or decoration 【用于布局组件、或装饰】

    >>> frame = SkFrame(parent)
    >>> button = SkTextButton(frame, text="I`m a Button")
    >>> button.fixed(x=10, y=10, width=100, height=100)
    >>> frame.box(expand=True)

    :param args:
    :param size: Default size
    :param border: Whether to draw a border
    :param kwargs:
    """

    def __init__(
        self, parent: SkContainer, *, style: str = "SkFrame", **kwargs
    ) -> None:
        SkWidget.__init__(self, parent, style=style, **kwargs)
        SkContainer.__init__(self)

    # region Draw

    def draw_widget(self, canvas: skia.Canvas, rect: skia.Rect) -> None:
        """Draw the Frame border（If self.attributes["border"] is True）

        :param canvas: skia.Canvas
        :param rect: skia.Rect
        :return: None
        """
        style = self.theme.get_style(self.style)
        if "bd_shadow" in style:
            bd_shadow = style["bd_shadow"]
        else:
            bd_shadow = False
        if "bd_shader" in style:
            bd_shader = style["bd_shader"]
        else:
            bd_shader = None
        self._draw_frame(
            canvas,
            rect,
            radius=style["radius"],
            bg=style["bg"],
            width=style["width"],
            bd=style["bd"],
            bd_shadow=bd_shadow,
            bd_shader=bd_shader,
        )
        return None

    # endregion
