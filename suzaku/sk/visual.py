from .layout import Layout
from ..base.event import EventHanding

from typing import Union, Any


class SkVisual(Layout, EventHanding):

    _instance_count = 0

    from .window import SkWindow

    from skia import Canvas, Rect

    from suzaku.style.themes import theme

    theme = theme

    def __init__(self, parent: Union[SkWindow, "SkVisual"], size: tuple[int, int]=(100, 30), style="", id: str = None, name="sk_visual") -> None:

        """
        Basic visual component, telling SkWindow how to draw.

        基础可视化组件，告诉SkWindow如何绘制。

        Args:
            parent (SkWindow):
                Parent component (Usually a SkWindow).

                父级控件（一般为SkWindow）。

            size (tuple[int, int]):
                Default size (not the final drawn size).

                默认尺寸（不是最终渲染尺寸）。

            id (str):
                Identification code.

                控件识别码，用于区分并找到控件。

        Returns:
            None
        """

        super().__init__()

        SkVisual._instance_count += 1

        self.visual_attr = {
            "parent": parent,
            "name": name,
            "cursor": "arrow",
            "x": -999,
            "y": -999,
            "d_width": size[0],  # Default width
            "d_height": size[1],  # Default height
            "width": size[0],
            "height": size[1],
            "style": style,
            "visible": False,
        }

        if not id:
            self.visual_attr["id"] = name + "." + str(self.get_instance_count())

        self.evts = {
            "mouse_motion": [],
            "mouse_enter": [],
            "mouse_leave": [],
            "mouse_pressed": [],
            "mouse_released": [],
            "focus_in": [],
            "focus_out": [],
            "key_press": [],
            "key_release": [],
            "key_repeat": [],
            "char": [],
        }

        try:
            self.winfo_parent().add(self)
        except AttributeError:
            raise AttributeError("Parent component is not SkWindow or SkVisual.")

        self.is_mouse_enter = False
        self.is_mouse_pressed = False
        self.is_focus = False

        self.draw_func = lambda canvas: self._draw(canvas)
        self.winfo_master_window().add_draw(self.draw_func)

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

        def focus_in(evt):
            self.is_focus = True

        def focus_out(evt):
            self.is_focus = False

        self.bind("focus_in", focus_in)
        self.bind("focus_out", focus_out)

    def __str__(self) -> str:
        return self.winfo_id()

    def _show(self) -> None:
        """
        Show the component.

        显示组件。

        Returns:
            None
        """
        # self.winfo_parent().add_draw(self.draw_func)
        self.visual_attr["visible"] = True

    def _hide(self) -> None:
        """
        Hide the component.

        隐藏组件。

        Returns:
            None
        """
        # self.winfo_parent().remove_draw(self.draw_func)
        self.visual_attr["visible"] = False

    def configure(self, **kwargs) -> None:
        """
        Configure component properties.

        配置组件属性。

        Args:
            **kwargs: 
                Names and values of attributes.

                属性名和属性值。

        Returns:
            None
        """
        self.visual_attr.update(kwargs)

    config = configure  # Alias

    def cget(self, name: str) -> Any:
        """
        Get value of the property with the given name.

        通过值获取对应的属性值。

        Args:
            name (str): 
                Property name. 
                
                属性名。

        Returns: 
            self.visual_attr[name] (Any): Property value. 属性值。
        """
        return self.visual_attr[name]

    def draw(self, canvas: Canvas, rect: Rect) -> None:
        """
        Draws the component.

        负责绘制组件。

        Args:
            canvas (Canvas): 
                Which canvas to draw.

                画布。

            rect (Rect): 
                Region to draw.

                绘制区域。

        Returns:
            None
        """
        pass

    def _draw(self, canvas) -> None:
        """
        Passes the canvas to the draw function and the position of the component when drawing.

        负责传给draw函数画布和绘制时组件的位置。

        Args:
            canvas: 
                Which canvas to draw.

                画布。

        Returns:
            None
        """
        import skia
        rect = skia.Rect(self.visual_attr["x"], self.visual_attr["y"], self.visual_attr["x"] + self.visual_attr["width"], 
                         self.visual_attr["y"] + self.visual_attr["height"])
        self.draw(canvas, rect)

    @classmethod
    def get_instance_count(cls) -> int:
        """
        Get current instance count.

        获取当前实例数量。

        Returns:
            cls._instance_count (int): Instance count. 示例数量。
        """
        return cls._instance_count  # 返回当前计数

    def winfo(self) -> dict:
        """
        Get component properties.

        获取组件属性。

        Returns:
            self.visual_attr (dict): Properties of the component. 控件属性字典。
        """
        return self.visual_attr

    def winfo_parent(self) -> Union[SkWindow, "SkVisual"]:
        """
        Get parent component.

        获取组件父组件。

        Returns:
            self.visual_attr["parent"] (SkWindow | SkVisual): Parent component. 父级控件。
        """
        return self.visual_attr["parent"]

    def winfo_master_window(self) -> SkWindow:
        """
        获取组件主窗口

        :return: 主窗口
        """
        return self.winfo_parent().winfo_master_window()


    def winfo_id(self) -> str:
        """
        Get component ID.

        获取组件ID。

        Returns:
            self.visual_attr["id"] (str): ID value. ID值。
        """
        return self.visual_attr["id"]

    def winfo_width(self) -> Union[int, float]:
        """
        Get current width of the component.

        获取组件当前宽度。

        Returns:
            self.visual_attr["width"] (int | float): Width value. 宽度值。
        """
        return self.visual_attr["width"]

    def winfo_height(self) -> Union[int, float]:
        """
        Get current height of the component.

        获取组件当前高度。

        Returns:
            self.visual_attr["height"] (int | float): Height value. 高度值。
        """
        return self.visual_attr["height"]

    def winfo_dwidth(self) -> Union[int, float]:
        """
        Get default width of the component.

        获取组件默认宽度。

        Returns:
            self.visual_attr["d_width"] (int | float): Default width value. 默认宽度值。
        """
        return self.visual_attr["d_width"]

    def winfo_dheight(self) -> Union[int, float]:
        """
        Get default height of the component.

        获取组件默认高度。

        Returns:
            self.visual_attr["d_height"] (int | float): Default height value. 默认高度值。
        """
        return self.visual_attr["d_height"]

    def winfo_x(self) -> Union[int, float]:
        """
        Get X coordinate of the component relative to the window.

        获取组件相对窗口的X坐标。

        Returns:
            self.visual_attr["x"] (int | float): X coordinate value. X坐标值。
        """
        return self.visual_attr["x"]

    def winfo_y(self) -> Union[int, float]:
        """
        Get Y coordinate of the component relative to the window.

        获取组件相对窗口的Y坐标。

        Returns:
            self.visual_attr["y"] (int | float): Y coordinate value. Y坐标值。
        """
        return self.visual_attr["y"]

    def winfo_name(self) -> str:
        """
        Get component name.

        获取组件名称。

        Returns:
            self.visual_attr["name"] (str): Name value. 名称值。
        """
        return self.visual_attr["name"]

    def winfo_style(self) -> dict:
        """
        获取组件样式

        Returns:
            self.visual_attr["style"] (dict): Style value. 样式值。
        """
        return self.visual_attr["style"]


    def winfo_visible(self) -> bool:
        """
        Get whether the component is visible.

        获取组件是否可见。

        Returns:
            self.visual_attr["visible"] (bool): Visible state. 可见状态。
        """
        return self.visual_attr["visible"]

    def focus_set(self):
        """
        使当前组件获得焦点

        :return: None
        """
        self.is_focus = True
        if isinstance(self.winfo_master_window().window_attr["focus_visual"], SkVisual):
            self.winfo_master_window().window_attr["focus_visual"].focus_forget()
        self.winfo_master_window().window_attr["focus_visual"] = self
        from ..base.event import Event
        self.event_generate("focus_in", Event())


    def focus_get(self):
        """
        获取窗口当前获得焦点的组件

        :return: 组件对象
        """
        return self.winfo_master_window().window_attr["focus_visual"]

    def focus_forget(self):
        """
        使当前组件失去焦点

        :return: None
        """
        self.is_focus = False
        from ..base.event import Event
        self.event_generate("focus_out", Event())

