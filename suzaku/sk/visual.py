from .layout import Layout
from ..base.event import EventHanding


class SkVisual(Layout, EventHanding):
    "基础可视化组件，告诉SkWindow如何绘制"

    _instance_count = 0

    from .window import SkWindow

    from ..themes import theme

    theme = theme

    def __init__(self, parent: SkWindow, size=(100, 30), id=None):
        SkVisual._instance_count += 1

        self.visual_attr = {
            "parent": parent,
            "name": "sk_visual",
            "cursor": "arrow",
            "x": 0,
            "y": 0,
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

    def configure(self, **kwargs):
        self.visual_attr.update(kwargs)

    config = configure

    def cget(self, name):
        return self.visual_attr[name]

    def draw(self, canvas, rect):
        pass

    def _draw(self, canvas):
        import skia
        rect = skia.Rect(self.visual_attr["x"], self.visual_attr["y"], self.visual_attr["x"] + self.visual_attr["width"], self.visual_attr["y"] + self.visual_attr["height"])
        #print(self.winfo_id(), self.visual_attr["x"], self.visual_attr["y"], self.visual_attr["x"] + self.visual_attr["width"], self.visual_attr["y"] + self.visual_attr["height"])
        self.draw(canvas, rect)

    @classmethod
    def get_instance_count(cls):
        return cls._instance_count  # 返回当前计数

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

    def winfo_x(self):
        return self.visual_attr["x"]

    def winfo_y(self):
        return self.visual_attr["y"]

    def winfo_name(self):
        return self.visual_attr["name"]
