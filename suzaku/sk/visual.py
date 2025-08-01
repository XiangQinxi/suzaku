from .layout import Layout
from ..base.event import EventHanding


class SkVisual(Layout, EventHanding):
    """
    基础可视化组件，告诉SkWindow如何绘制
    """

    _instance_count = 0

    from .window import SkWindow

    from ..themes import theme

    theme = theme

    def __init__(self, parent: SkWindow, size=(100, 30), id: str = None) -> None:

        """
        初始化

        :param parent: 父组件，一般为"Window"
        :param size: 默认大小(而非布局后的实际大小)
        :param id: 标识码
        """

        super().__init__()

        SkVisual._instance_count += 1

        self.visual_attr = {
            "parent": parent,
            "name": "sk_visual",
            "cursor": "arrow",
            "x": -999,
            "y": -999,
            "d_width": size[0],  # 默认宽度
            "d_height": size[1],  # 默认高度
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

        self.draw_func = lambda canvas: self._draw(canvas)

        self.bind("mouse_enter", mouse_enter)
        self.bind("mouse_leave", mouse_leave)
        self.bind("mouse_pressed", mouse_pressed)
        self.bind("mouse_released", mouse_released)

    def __str__(self) -> str:
        return self.winfo_id()

    def _show(self) -> None:
        """
        显示组件
        :return: None
        """
        self.winfo_parent().add_draw(self.draw_func)

    def _hide(self) -> None:
        """
        隐藏组件
        :return: None
        """
        self.winfo_parent().remove_draw(self.draw_func)

    def configure(self, **kwargs) -> None:
        """
        配置组件属性

        :param kwargs: 属性名和属性值
        :return: None
        """
        self.visual_attr.update(kwargs)

    config = configure  # 别名

    def cget(self, name) -> any:
        """
        通过值获取对应的属性值

        :param name: 属性名
        :return: 属性值
        """
        return self.visual_attr[name]

    def draw(self, canvas, rect) -> None:
        """
        负责绘制组件

        :param canvas: 画布
        :param rect: 绘制区域
        :return: None
        """
        pass

    def _draw(self, canvas) -> None:
        """
        负责传给draw函数画布和绘制时组件的位置

        :param canvas: 画布
        :return:
        """
        import skia
        rect = skia.Rect(self.visual_attr["x"], self.visual_attr["y"], self.visual_attr["x"] + self.visual_attr["width"], self.visual_attr["y"] + self.visual_attr["height"])
        #print(self.winfo_id(), self.visual_attr["x"], self.visual_attr["y"], self.visual_attr["x"] + self.visual_attr["width"], self.visual_attr["y"] + self.visual_attr["height"])
        self.draw(canvas, rect)

    @classmethod
    def get_instance_count(cls) -> int:
        """
        获取当前实例数量

        :return: 实例数量
        """
        return cls._instance_count  # 返回当前计数

    def winfo(self) -> dict:
        """
        获取组件属性

        :return: 属性字典
        """
        return self.visual_attr

    def winfo_parent(self) -> SkWindow:
        """
        获取组件父组件

        :return: 父组件
        """
        return self.visual_attr["parent"]

    def winfo_id(self) -> str:
        """
        获取组件ID

        :return: ID值
        """
        return self.visual_attr["id"]

    def winfo_width(self) -> int | float:
        """
        获取组件当前宽度

        :return: 宽度值
        """
        return self.visual_attr["width"]

    def winfo_height(self) -> int | float:
        """
        获取组件当前高度

        :return: 高度值
        """
        return self.visual_attr["height"]

    def winfo_dwidth(self) -> int | float:
        """
        获取组件默认宽度

        :return: 默认宽度值
        """
        return self.visual_attr["d_width"]

    def winfo_dheight(self) -> int | float:
        """
        获取组件默认高度

        :return: 默认高度值
        """
        return self.visual_attr["d_height"]

    def winfo_x(self) -> int | float:
        """
        获取组件相对窗口的X坐标

        :return: X坐标值
        """
        return self.visual_attr["x"]

    def winfo_y(self) -> int | float:
        """
        获取组件相对窗口的Y坐标

        :return: Y坐标值
        """
        return self.visual_attr["y"]

    def winfo_name(self) -> str:
        """
        获取组件名称

        :return:
        """
        return self.visual_attr["name"]
