import array
import typing

import skia

from ..event import SkEvent


class SkLayoutError(TypeError):
    pass


class SkContainer:
    """A SkContainer represents a widget that has the ability to contain other widgets inside.

    SkContainer is only for internal use. If any user would like to create a widget from
    several of existed ones, they should use SkComboWidget instead. The authors will not
    guarantee the stability of inheriting SkContainer for third-party widgets.

    SkContainer class contains code for widget embedding, and layout handling, providing the
    ability of containing `children` to widgets inherit from it. All other classes with such
    abilities should be inherited from SkContainer.

    SkContainer has a `children` list, each item is a `SkWidget`, called `child`. This helps
    the SkContainer knows which `SkWidget`s it should handle.

    SkContainer has a `draw_list` that stores all widgets contained in it that should be drawn.
    They are separated into a few layers which are listed below, in the order of from behind to
    the top:

    1. `Layout layer`: The layer for widgets using pack or grid layout.
    2. `Floating layer`: The layer for widgets using place layout.
    3. `Fixed layer`: The layer for widgets using fixed layout.

    In each layer, items will be drawn in the order of index. Meaning that those with lower
    index will be drawn first, and may get covered by those with higher index. Same for layers,
    layers with higher index cover those with lower index.

    Example:

    .. code-block:: python

        container = SkContainer()
        widget = SkWidget(parent=container)
        widget.fixed(x=10, y=10, width=100, height=100)

    """

    # region __init__ 初始化

    parent: typing.Self
    width: int | float
    height: int | float

    def __enter__(self):
        self._handle_layout()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._handle_layout()
        # 触发更新事件
        self.event_trigger("update", SkEvent(event_type="update"))

    def __init__(self, allowed_out_of_bounds: bool = False):

        # self.parent = None
        self.children = []  # Children

        from ..widgets.widget import SkWidget

        self.draw_list: list[list[SkWidget]] = [
            [],  # Layout layer [SkWidget1, SkWidget2, ...]
            [],  # Floating layer [SkWidget1, SkWidget2, ...]
            [],  # Fixed layer [SkWidget1, SkWidget2, ...]
        ]
        self.layout_names = [None, None, None]

        # 【内部组件统计总占大小】
        self.content_width = 0
        self.content_height = 0

        # 【内部组件偏移，用于实现容器内部的滚动】
        self._x_offset = 0
        self._y_offset = 0
        self.allowed_scrolled: bool = False
        self.scroll_speed: float | int = 18  # 滚动距离：滚动量x滚动速度

        self._grid_lists = []  # [ [row1, ], [] ]
        self._box_direction = None  # h(horizontal) or v(vertical)
        self._flow_row = 0
        self.allowed_out_of_bounds = (
            allowed_out_of_bounds  # 【是否允许组件超出容器范围】
        )

        # Events
        self.bind("resize", lambda _: self.update_layout())

    # endregion

    def bind_scroll_event(self):
        # 容器绑定滚动事件，鼠标滚轮滚动可以滚动容器
        self.allowed_scrolled = True
        self.window.bind("scroll", self.scroll_event)

    def scroll_event(self, event: SkEvent):
        if self.allowed_scrolled:
            if self.is_mouse_floating:
                self.scroll(event.x_offset * 18, event.y_offset * 18)
                return

            for child in self.children:
                if child.is_mouse_floating and child.help_parent_scroll:
                    if hasattr(child, "allowed_scrolled"):
                        if not child.allowed_scrolled:
                            return
                    self.scroll(event.x_offset * 18, event.y_offset * 18)
                    return

    def _check_scroll(self, x_offset: int, y_offset: int):
        if y_offset < 0:
            # 总体向上
            if self.content_height + self.y_offset >= self.height:
                return True
        else:
            # 总体向下
            if self.y_offset <= -y_offset:
                return True
        return False

    def scroll(
        self,
        x_offset: int | float,
        y_offset: int | float,
    ):
        if self._check_scroll(x_offset, y_offset):
            self.y_offset = min(y_offset + self.y_offset, self.content_height)

    # region add_child 添加子元素
    def add_child(self, child):
        """Add child widget to window.

        :param child: The child to add
        """
        from .app import SkApp

        if not child in self.children:
            if not isinstance(self.parent, SkApp):
                self.parent.add_child(child)
            self.children.append(child)

    def add_layout_child(self, child):
        """Add layout child widget to window.

        :arg child: SkWidget
        :return: None
        """
        layout_config = child.layout_config

        if "box" in layout_config:
            side = layout_config["box"]["side"]
            if side == "left" or side == "right":
                direction = "h"
            elif side == "top" or side == "bottom":
                direction = "v"
            else:
                raise ValueError("Box layout side must be left, right, top or bottom.")

            if self._box_direction == "v":
                if direction == "h":
                    raise ValueError(
                        "Box layout can only be used with vertical direction."
                    )
            elif self._box_direction == "h":
                if direction == "v":
                    raise ValueError(
                        "Box layout can only be used with horizontal direction."
                    )
            else:
                self._box_direction = direction

        self.draw_list[0].append(child)
        self.update_layout()

    def add_floating_child(self, child):
        """Add floating child widget to window.

        :arg child: SkWidget
        :return: None
        """

        self.draw_list[1].append(child)
        self.update_layout()

    def add_fixed_child(self, child):
        """Add fixed child widget to window.

        Example:
            .. code-block:: python

                widget.fixed(x=10, y=10, width=100, height=100)

        :arg child: SkWidget
        :return: None
        """
        self.draw_list[2].append(child)
        self.update_layout()

    # endregion

    # region draw 绘制

    def draw_children(self, canvas: skia.Canvas):
        """Draw children widgets.

        :param canvas: The canvas to draw on
        :return: None
        """
        from ..widgets.widget import SkWidget
        from .window import SkWindow

        if not isinstance(self, SkWindow):
            if isinstance(self, SkWidget):
                x = self.canvas_x
                y = self.canvas_y
            else:
                x = 0
                y = 0

            if not self.allowed_out_of_bounds:
                canvas.save()
                canvas.clipRect(
                    skia.Rect.MakeXYWH(
                        x=x,
                        y=y,
                        w=self.width,
                        h=self.height,
                    )
                )
        for layer in self.draw_list:
            for child in layer:
                if child.visible:
                    child.draw(canvas)
        canvas.restore()

    # endregion

    # region layout 布局

    def update_layout(self, event: SkEvent | None = None):
        if self.allowed_scrolled and self.y_offset < 0:
            if not self._check_scroll(0, -5):
                self._y_offset = self.height - self.content_height
                if self._y_offset > 0:
                    self._y_offset = 0
        self._handle_layout()
        for widget in self.children:
            widget.event_trigger("resize", SkEvent(event_type="resize"))

    def record_content_size(self, child, padx=0, pady=0):
        self.content_width = max(child.x + child.dwidth + padx, self.content_width)
        self.content_height = max(child.y + child.dheight + pady, self.content_height)

    def _handle_layout(self, event=None):
        """Handle layout of the container.

        :return: None
        """
        for layer in self.draw_list:
            for child in layer:
                if child.visible:
                    match child.layout_config:
                        case {"place": _}:
                            pass
                        case {"box": _}:
                            self.layout_names[0] = "box"
                            self._handle_box()
                            break
                        case {"fixed": _}:
                            self.layout_names[2] = "fixed"
                            self._handle_fixed(child)
                        case {"flow": _}:
                            self.layout_names[0] = "flow"
                            self._handle_flow(child)

    def _handle_flow(self, child):
        pass

    def _handle_pack(self):
        pass

    def _handle_place(self):
        pass

    def _handle_grid(self):
        pass

    @staticmethod
    def unpack_padding(padx, pady):
        """Unpack padding.
        【左上右下】
        :param padx:
        :param pady:
        :return:
        """
        if type(padx) is tuple:
            left = padx[0]
            right = padx[1]
        else:
            left = right = padx

        if type(pady) is tuple:
            top = pady[0]
            bottom = pady[1]
        else:
            top = bottom = pady
        return left, top, right, bottom

    def _handle_box(self) -> None:
        """Process box layout.

        :return: None
        """

        from ..widgets.widget import SkWidget

        width = self.width  # container width
        height = self.height  # container height
        start_children: list[SkWidget] = []  # side="top" or "left" children
        end_children: list[SkWidget] = []  # side="bottom" or "right" children
        expanded_children: list[SkWidget] = []  # expand=True children
        fixed_children: list[SkWidget] = []  # expand=False children
        children: list[SkWidget] = self.draw_list[0]  # Components using the Box layout

        # Iterate through all the subcomponents first, categorize them, and separate components with different values for expand, side.
        # 先遍历一遍所有子组件，将它们分类，将expand、side值不同的组件分开
        for child in children:
            layout_config = child.layout_config
            match layout_config["box"]["side"].lower():
                case "top" | "left":
                    start_children.append(child)
                case "bottom" | "right":
                    end_children.append(child)
            if layout_config["box"]["expand"]:
                expanded_children.append(child)
            else:
                fixed_children.append(child)

        # Horizontal Layout
        if self._box_direction == "h":
            # Calculate the width of the fixed children
            fixed_width: int | float = 0  # Occupied width of all fixed widgets enabled
            for fixed_child in fixed_children:
                fixed_child_layout_config = fixed_child.layout_config["box"]

                if type(fixed_child_layout_config["padx"]) is tuple:
                    fixed_width += fixed_child_layout_config["padx"][0]
                else:
                    fixed_width += fixed_child_layout_config["padx"]
                fixed_width += fixed_child.width

                if type(fixed_child_layout_config["padx"]) is tuple:
                    fixed_width += fixed_child_layout_config["padx"][1]
                else:
                    fixed_width += fixed_child_layout_config["padx"]

            if len(expanded_children):
                expanded_width = (width - fixed_width) / len(expanded_children)
            else:
                expanded_width = 0

            # Left side
            last_child_left_x = 0
            for child in start_children:
                child_layout_config = child.layout_config["box"]
                left, top, right, bottom = self.unpack_padding(
                    child_layout_config["padx"],
                    child_layout_config["pady"],
                )

                if not child_layout_config["expand"]:
                    child.width = child.dheight
                else:
                    child.width = expanded_width - left - right
                child.height = height - top - bottom
                child.x = last_child_left_x + left
                child.y = top + self.y_offset
                self.record_content_size(child, right, bottom)
                last_child_left_x = child.x + child.width + right
                child.x += self.x_offset

            # Right side
            last_child_right_x = width
            for child in end_children:
                child_layout_config = child.layout_config["box"]
                left, top, right, bottom = self.unpack_padding(
                    child_layout_config["padx"],
                    child_layout_config["pady"],
                )

                if not child_layout_config["expand"]:
                    child.width = child.dheight
                else:
                    child.width = expanded_width - left - right
                child.height = height - top - bottom
                child.x = last_child_right_x - child.width - right + self.x_offset
                child.y = top + self.y_offset
                self.record_content_size(child, right, bottom)
                last_child_right_x = last_child_right_x - child.width - left * 2
        else:  # Vertical Layout
            # Calculate the height of the fixed children
            fixed_height = 0  # Occupied height of all fixed widgets enabled
            for fixed_child in fixed_children:
                fixed_child_layout_config = fixed_child.layout_config["box"]

                if type(fixed_child_layout_config["pady"]) is tuple:
                    fixed_height += fixed_child_layout_config["pady"][0]
                else:
                    fixed_height += fixed_child_layout_config["pady"]
                fixed_height += fixed_child.height

                if type(fixed_child_layout_config["pady"]) is tuple:
                    fixed_height += fixed_child_layout_config["pady"][1]
                else:
                    fixed_height += fixed_child_layout_config["pady"]

            if len(expanded_children):
                expanded_height = (height - fixed_height) / len(
                    expanded_children
                )  # Height of expanded children
            else:
                expanded_height = 0

            last_child_bottom_y = 0  # Last bottom y position of the child component
            for child in start_children:  # Top side
                child_layout_config = child.layout_config["box"]
                left, top, right, bottom = self.unpack_padding(
                    child.layout_config["box"]["padx"],
                    child.layout_config["box"]["pady"],
                )

                child.width = width - left - right
                if not child_layout_config["expand"]:
                    child.height = child.dheight
                else:
                    child.height = expanded_height - top - bottom
                child.x = left + self.x_offset
                child.y = last_child_bottom_y + top
                self.record_content_size(child, right, bottom)
                last_child_bottom_y = child.y + child.height + bottom
                child.y += self.y_offset

            last_child_top_y = height  # Last top y position of the child component
            for child in end_children:  # Bottom side
                child_layout_config = child.layout_config["box"]
                left, top, right, bottom = self.unpack_padding(
                    child.layout_config["box"]["padx"],
                    child.layout_config["box"]["pady"],
                )

                child.width = width - left - right
                if not child_layout_config["expand"]:
                    child.height = child.dheight
                else:
                    child.height = expanded_height - top - bottom
                child.x = left + self.x_offset
                child.y = last_child_top_y - child.height - bottom + self.x_offset
                self.record_content_size(child, right, bottom)
                last_child_top_y = last_child_top_y - child.height - top * 2

    def _handle_fixed(self, child):
        """Process fixed layout.

        :param child: The child widget
        """
        config = child.layout_config["fixed"]
        child.x = config["x"] + self.x_offset
        child.y = config["y"] + self.y_offset

        width = config["width"]
        if not width:
            width = child.dwidth

        height = config["height"]
        if not height:
            height = child.dheight

        child.width = width
        child.height = height

    # endregion

    # region other 其他
    def bind(self, *args, **kwargs):
        raise RuntimeError(
            "Anything inherited from SkContainer should support binding events!"
            + "This error should be overrode by the actual bind function of "
            + "SkWindow or SkWidget in normal cases."
        )

    @property
    def visible_children(self):
        children = []
        for layer in self.draw_list:
            for child in layer:
                children.append(child)
                if hasattr(child, "visible_children"):
                    children.extend(child.visible_children)
        return children

    # endregion

    # region Configure 属性配置
    @property
    def x_offset(self) -> int | float:
        """
        【x方向内部偏移，用于实现容器内部的滚动】
        """
        return self._x_offset

    @x_offset.setter
    def x_offset(self, value: int | float):
        self._x_offset = value
        self.update_layout(None)

    @property
    def y_offset(self) -> int | float:
        """
        【y方向内部偏移，用于实现容器内部的滚动】
        """
        return self._y_offset

    @y_offset.setter
    def y_offset(self, value: int | float):
        self._y_offset = value
        self.update_layout(None)

    # endregion
