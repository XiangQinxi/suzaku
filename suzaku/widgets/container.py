from __future__ import annotations as _

import array
import typing

import skia

from ..const import Orient
from ..event import SkEvent
from ..misc import SkMisc

if typing.TYPE_CHECKING:
    from .. import SkEventHandling
    from . import SkWidget


class SkLayoutError(TypeError):
    pass


def get_padding_value(padding):
    """Helper to handle tuple or single padding values"""
    if isinstance(padding, tuple):
        return padding[0], padding[1]
    return padding, padding


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
        if isinstance(self, SkEventHandling):
            self.trigger("update", SkEvent(widget=self, event_type="update"))
            self.update()

    def __init__(self, allowed_out_of_bounds: bool = False, is_combo_widget: bool = False):

        # self.parent = None
        self.is_combo_widget: bool = (
            is_combo_widget  # if True, then this container is a combo widget and help parent scroll
        )
        self.need_redraw: bool
        self.is_mouse_floating: bool
        self.children: list[SkWidget] = []  # Children

        self.draw_list: list[list[SkWidget]] = [
            [],  # Layout layer [SkWidget1, SkWidget2, ...]
            [],  # Floating layer [SkWidget1, SkWidget2, ...]
            [],  # Fixed layer [SkWidget1, SkWidget2, ...]
        ]
        self.layout_names = [None, None, None]

        # 【内部组件统计总占大小】
        self.content_width: int | float = 0
        self.content_height: int | float = 0

        # 【内部组件偏移，用于实现容器内部的滚动】
        self._x_offset: int | float = 0
        self._y_offset: int | float = 0
        self.allowed_scrolled: bool = False
        self.scroll_speed: float | int = 18  # 滚动距离：滚动量x滚动速度

        self._grid_lists = []  # [ [row1, ], [] ]
        self._box_direction: Orient | None = None  # h(horizontal) or v(vertical)
        self._flow_row = 0
        self.allowed_out_of_bounds = allowed_out_of_bounds  # 【是否允许组件超出容器范围】

        # Events
        self.bind("resize", lambda _: self.update_layout())

    # endregion

    # region Scroll
    def bind_scroll_event(self):
        # 【容器绑定滚动事件，鼠标滚轮滚动可以滚动容器】
        self.allowed_scrolled = True
        self.window.bind("scroll", self.scroll_event)

    def scroll_event(self, event: SkEvent) -> None:
        """【处理滚动事件】"""
        if self.allowed_scrolled:
            # typing.cast("SkWidget", self)
            if self.is_mouse_floating:
                self.scroll(event["x_offset"] * 18, event["y_offset"] * 18)
                return

            for child in self.children:
                if child.is_mouse_floating and child.help_parent_scroll and child.parent == self:
                    if isinstance(child, SkContainer):
                        if not child.is_combo_widget:
                            break
                    self.scroll(event["x_offset"] * 18, event["y_offset"] * 18)
                    return

    def update_scroll(self) -> None:
        """【检查并更新滚动偏移量】"""
        if self.content_width < self.width:
            self._x_offset = 0
        else:
            self._x_offset = max(self.x_offset, -(self.content_width - self.width))
        # 【防止容器超出下边界】
        if self.content_height < self.height:
            self._y_offset = 0
        else:
            self._y_offset = max(self.y_offset, -(self.content_height - self.height))

    def scroll(
        self,
        x_offset: int | float,
        y_offset: int | float,
    ) -> None:
        """【滚动容器】

        :param x_offset: 【水平滚动量】
        :param y_offset: 【垂直滚动量】
        """
        """if self._check_scroll(x_offset, y_offset):
        self.y_offset = min(y_offset + self.y_offset, self.content_height)
        """
        self.x_offset = min(self.x_offset + x_offset, 0)
        # 防止容器超出上边界
        self.y_offset = min(self.y_offset + y_offset, 0)
        self.update(redraw=True)
        self.trigger("scrolled", SkEvent(self, "scrolled"))

    # endregion

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

    def remove_child(self, child):
        """Remove child widget from window.
        :param child: The child to remove"""
        pass

    def remove_all(self):
        for child in self.children:
            child.layout_forget()

    def grid_map(self):
        # Grid Map
        # [ [widget1, widget2, ...], [widget3, widget4, ...], ... ]
        # 【根据网格布局配置，将子元素组织成网格地图】

        grid_map: list[list[SkWidget | None]] = []
        children: list[SkWidget] = self.draw_list[0]

        for child in children:
            if child is None:
                continue
            child_config = child.layout_config["grid"]
            row, col = child_config["row"], child_config["column"]

            if row < 0 or col < 0:
                continue

            # 确保有足够的行
            while len(grid_map) <= row:
                grid_map.append([])

            # 确保当前行有足够的列
            current_row = grid_map[row]
            while len(current_row) <= col:
                current_row.append(None)

            # 放置组件
            grid_map[row][col] = child

        return grid_map

    def add_layer_child(self, layer, child):
        self.draw_list[layer].append(child)

        self.update_layout()

    def add_layer1_child(self, child):
        """Add layout child widget to window.

        :arg child: SkWidget
        :return: None
        """
        layout_config = child.layout_config

        if "box" in layout_config:
            side = layout_config["box"]["side"]
            if side == "left" or side == "right":
                direction = Orient.H
            elif side == "top" or side == "bottom":
                direction = Orient.V
            else:
                raise ValueError("Box layout side must be left, right, top or bottom.")

            if self._box_direction == Orient.V:
                if direction == Orient.H:
                    raise ValueError("Box layout can only be used with vertical direction.")
            elif self._box_direction == Orient.H:
                if direction == Orient.V:
                    raise ValueError("Box layout can only be used with horizontal direction.")
            else:
                self._box_direction = direction

        self.add_layer_child(0, child)

    def add_layer2_child(self, child):
        """Add floating child widget to window.

        :arg child: SkWidget
        :return: None
        """

        self.add_layer_child(1, child)

    def add_layer3_child(self, child):
        """Add fixed child widget to window.

        Example:
            .. code-block:: python

                widget.fixed(x=10, y=10, width=100, height=100)

        :arg child: SkWidget
        :return: None
        """
        self.add_layer_child(2, child)

    # endregion

    # region draw 绘制

    def draw_children(self, canvas: skia.Canvas):
        """Draw children widgets.

        :param canvas: The canvas to draw on
        :return: None
        """

        if "SkWindow" not in SkMisc.sk_get_type(self):
            if "SkWidget" in SkMisc.sk_get_type(self):
                typing.cast("SkWidget", self)
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
        """if self.allowed_scrolled and self.y_offset < 0:
        if not self._check_scroll(0, -5):
            self._y_offset = self.height - self.content_height
            if self._y_offset > 0:
                self._y_offset = 0"""
        self.update_scroll()
        self._handle_layout()
        for widget in self.children:
            widget.trigger("resize", SkEvent(widget=self, event_type="resize"))

    def reset_content_size(self):
        self.content_width, self.content_height = 0, 0

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
                        case {"grid": _}:
                            self.layout_names[0] = "grid"
                            self._handle_grid()
                            break
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
        self.reset_content_size()

        # Grid
        row_heights: list[int | float] = []
        col_widths: list[int | float] = []
        grid_map = self.grid_map()

        # 第一步：计算行列尺寸（包含ipadx/ipady）
        for row, rows in enumerate(grid_map):
            for col, widget in enumerate(rows):
                if widget is None:
                    continue
                child_config = widget.layout_config["grid"]

                # 解包外部padding
                pad_left, pad_top, pad_right, pad_bottom = self.unpack_padding(
                    child_config["padx"],
                    child_config["pady"],
                )

                # 解包内部padding（形式相同）
                ipad_left, ipad_top, ipad_right, ipad_bottom = self.unpack_padding(
                    child_config["ipadx"],
                    child_config["ipady"],
                )

                if len(col_widths) <= col:
                    col_widths.append(0)
                # 总宽度 = 内容宽度 + 内部padding
                total_width = widget.dwidth + ipad_left + ipad_right + pad_left + pad_right
                col_widths[col] = max(col_widths[col], total_width)

                if len(row_heights) <= row:
                    row_heights.append(0)
                # 总高度 = 内容高度 + 内部padding
                total_height = widget.dheight + ipad_top + ipad_bottom + pad_top + pad_bottom
                row_heights[row] = max(row_heights[row], total_height)

        self.content_height = total_row_height = sum(row_heights)
        self.content_width = total_col_width = sum(col_widths)

        # 第二步：定位widgets（包含ipadx/ipady）
        for row, rows in enumerate(grid_map):
            row_top = sum(row_heights[:row])
            col_left = 0

            for col, widget in enumerate(rows):
                if widget is None:
                    continue
                child_config = widget.layout_config["grid"]

                # 解包外部padding
                pad_left, pad_top, pad_right, pad_bottom = self.unpack_padding(
                    child_config["padx"],
                    child_config["pady"],
                )

                # 解包内部padding
                ipad_left, ipad_top, ipad_right, ipad_bottom = self.unpack_padding(
                    child_config["ipadx"],
                    child_config["ipady"],
                )

                col_width = sum(col_widths[col : col + child_config["columnspan"]])
                row_height = sum(row_heights[row : row + child_config["rowspan"]])

                # widget实际尺寸 = 单元格尺寸 - 外部padding - 内部padding
                widget.width, widget.height = (
                    col_width - pad_left - pad_right,
                    row_height - pad_top - pad_bottom,
                )

                # widget位置 = 单元格位置 + 外部padding + 内部padding
                widget.x, widget.y = (
                    col_left + pad_left,
                    row_top + pad_top,
                )
                widget.x += self.x_offset
                widget.y += self.y_offset

                col_left = widget.x + widget.width + ipad_right

    def _handle_box(self) -> None:
        """Process box layout.

        :return: None
        """

        # TODO 做好ipadx、ipady的处理
        self.reset_content_size()

        width = self.width  # container width
        height = self.height  # container height
        children: list[SkWidget] = self.draw_list[0]  # Components using the Box layout

        # Categorize children by side and expand
        start_children: list[SkWidget] = []  # side="top" or "left" children
        end_children: list[SkWidget] = []  # side="bottom" or "right" children
        expanded_children: list[SkWidget] = []  # expand=True children
        fixed_children: list[SkWidget] = []  # expand=False children

        for child in children:
            if not child.visible:
                continue
            layout_config = child.layout_config["box"]
            side = layout_config["side"].lower()

            if side in ("top", "left"):
                start_children.append(child)
            elif side in ("bottom", "right"):
                end_children.append(child)

            if layout_config["expand"]:
                expanded_children.append(child)
            else:
                fixed_children.append(child)

        if self._box_direction == Orient.H:
            # Horizontal Layout
            # Calculate total fixed width
            fixed_width = 0
            for fixed_child in fixed_children:
                padx_left, padx_right = get_padding_value(fixed_child.layout_config["box"]["padx"])
                fixed_width += padx_left + fixed_child.width + padx_right

            expanded_width = (
                (width - fixed_width) / len(expanded_children) if expanded_children else 0
            )

            # Process start children (left side)
            last_x = 0
            for child in start_children:
                self._process_child_layout(
                    child, width, height, expanded_width, last_x, is_start=True, is_horizontal=True
                )
                last_x = child.x + child.width + self._get_padding_right(child)
                child.x += self.x_offset

            # Process end children (right side)
            last_x = width
            for child in end_children:
                self._process_child_layout(
                    child, width, height, expanded_width, last_x, is_start=False, is_horizontal=True
                )
                last_x = last_x - child.width - self._get_padding_left(child) * 2
                child.x += self.x_offset

        else:
            # Vertical Layout
            # Calculate total fixed height
            fixed_height = 0
            for fixed_child in fixed_children:
                pady_top, pady_bottom = get_padding_value(fixed_child.layout_config["box"]["pady"])
                fixed_height += pady_top + fixed_child.height + pady_bottom

            expanded_height = (
                (height - fixed_height) / len(expanded_children) if expanded_children else 0
            )

            # Process start children (top side)
            last_y = 0
            for child in start_children:
                self._process_child_layout(
                    child,
                    width,
                    height,
                    expanded_height,
                    last_y,
                    is_start=True,
                    is_horizontal=False,
                )
                last_y = child.y + child.height + self._get_padding_bottom(child)
                child.y += self.y_offset

            # Process end children (bottom side)
            last_y = height
            for child in end_children:
                self._process_child_layout(
                    child,
                    width,
                    height,
                    expanded_height,
                    last_y,
                    is_start=False,
                    is_horizontal=False,
                )
                last_y = last_y - child.height - self._get_padding_top(child) * 2
                child.y += self.y_offset

    def _process_child_layout(
        self,
        child,
        container_size1,
        container_size2,
        expanded_size,
        last_position,
        is_start,
        is_horizontal,
    ):
        """Process individual child layout positioning"""
        layout_config = child.layout_config["box"]
        padx_left, padx_right = get_padding_value(layout_config["padx"])
        pady_top, pady_bottom = get_padding_value(layout_config["pady"])

        if is_horizontal:
            # Horizontal layout
            child.width = container_size1 - padx_left - padx_right
            if not layout_config["expand"]:
                child.width = child.dwidth
            else:
                child.width = expanded_size - padx_left - padx_right
            child.height = container_size2 - pady_top - pady_bottom

            if is_start:
                child.x = last_position + padx_left
                child.y = pady_top + self.y_offset
            else:
                child.x = last_position - child.width - padx_right + self.x_offset
                child.y = pady_top + self.y_offset
        else:
            # Vertical layout
            child.width = container_size1 - padx_left - padx_right
            if not layout_config["expand"]:
                child.height = child.dheight
            else:
                child.height = expanded_size - pady_top - pady_bottom
            child.x = padx_left + self.x_offset

            if is_start:
                child.y = last_position + pady_top
            else:
                child.y = last_position - child.height - pady_bottom + self.x_offset

        self.record_content_size(child, padx_right, pady_bottom)

    def _get_padding_left(self, child):
        padx = child.layout_config["box"]["padx"]
        return padx[0] if isinstance(padx, tuple) else padx

    def _get_padding_right(self, child):
        padx = child.layout_config["box"]["padx"]
        return padx[1] if isinstance(padx, tuple) else padx

    def _get_padding_top(self, child):
        pady = child.layout_config["box"]["pady"]
        return pady[0] if isinstance(pady, tuple) else pady

    def _get_padding_bottom(self, child):
        pady = child.layout_config["box"]["pady"]
        return pady[1] if isinstance(pady, tuple) else pady

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

    def update(self):
        self.update_layout()
        for child in self.children:
            child.update()

    # endregion
