from .layout import Layout
from ..base.event import EventHanding

from typing import Union


class SkVisual(Layout, EventHanding):

    _instance_count = 0

    from .window import SkWindow

    from ..themes import theme

    theme = theme

    def __init__(self, parent: Union[SkWindow], size: tuple[int, int]=(100, 30), id: str = None) -> None:

        """
        Basic visual component, telling SkWindow how to draw.

        基础可视化组件，告诉SkWindow如何绘制。

        :param parent: 
        Parent component (Usually a SkWindow).
        :param size: 
        Default size (not the final drawn size).
        :param id: 
        Identification code.
        """

        super().__init__()

        SkVisual._instance_count += 1

        self.visual_attr = {
            "parent": parent,
            "name": "sk_visual",
            "cursor": "arrow",
            "x": 0,
            "y": 0,
            "d_width": size[0],  # Default width
            "d_height": size[1],  # Default height
            "width": size[0],
            "height": size[1],
            "id": id or ("sk_visual." + str(self.get_instance_count())),
            "visible": True,
        }

        self.evts = {
            "mouse_motion": [],
            "mouse_enter": [],
            "mouse_leave": [],
            "mouse_pressed": [],
            "mouse_released": [],
        }

        self.winfo_parent().add_draw(lambda canvas: self._draw(canvas))
        self.winfo_parent().add(self)

        self.is_mouse_enter = False
        self.is_mouse_pressed = False

        def mouse_enter(evt):
            self.is_mouse_enter = True

        def mouse_leave(evt):
            self.is_mouse_enter = False

        def mouse_pressed(evt):
            self.is_mouse_pressed = True

        def mouse_released(evt):
            self.is_mouse_pressed = False

        self.bind("mouse_enter", mouse_enter)
        self.bind("mouse_leave", mouse_leave)
        self.bind("mouse_pressed", mouse_pressed)
        self.bind("mouse_released", mouse_released)

    def __str__(self) -> str:
        return self.winfo_id()

    def configure(self, **kwargs):
        self.visual_attr.update(kwargs)

    config = configure

    def cget(self, name):
        return self.visual_attr[name]

    def draw(self, canvas, rect):
        pass

    def _draw(self, canvas):
        import skia
        rect = skia.Rect(self.visual_attr["x"], self.visual_attr["y"], self.visual_attr["x"] + self.visual_attr["width"], 
                         self.visual_attr["y"] + self.visual_attr["height"])
        self.draw(canvas, rect)

    @classmethod
    def get_instance_count(cls):
        return cls._instance_count  # Return current count

    def winfo(self):
        return self.visual_attr

    def winfo_parent(self):
        return self.visual_attr["parent"]

    def winfo_id(self):
        return self.visual_attr["id"]

    def winfo_width(self):
        return self.visual_attr["width"]

    def winfo_height(self):
        return self.visual_attr["height"]

    def winfo_dwidth(self):
        return self.visual_attr["d_width"]

    def winfo_dheight(self):
        return self.visual_attr["d_height"]

    def winfo_x(self):
        return self.visual_attr["x"]

    def winfo_y(self):
        return self.visual_attr["y"]

    def winfo_name(self):
        return self.visual_attr["name"]
