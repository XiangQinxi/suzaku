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
        self,
        parent: SkContainer,
        *,
        style: str = "SkFrame",
        allowed_out_of_bounds: bool = False,
        is_combo_widget: bool = False,
        **kwargs,
    ) -> None:
        SkWidget.__init__(self, parent, style_name=style, **kwargs)
        SkContainer.__init__(
            self, allowed_out_of_bounds=allowed_out_of_bounds, is_combo_widget=is_combo_widget
        )

    @property
    def dwidth(self):
        _width = self.cget("dwidth")
        if _width <= 0:
            _width = self.content_width
        return _width

    @property
    def dheight(self):
        _height = self.cget("dheight")
        if _height <= 0:
            _height = self.content_height
        return _height

    # region Draw

    # endregion
