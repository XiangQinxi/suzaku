import typing
from functools import cache

import skia

from ..event import SkEvent, SkEventHandling
from ..misc import SkMisc
from ..styles.color import SkGradient
from ..styles.drop_shadow import SkDropShadow
from ..styles.font import default_font
from ..styles.theme import SkStyleNotFoundError, SkTheme, default_theme
from .appwindow import SkAppWindow
from .draw import SkDraw
from .window import SkWindow


class SkWidget(SkEventHandling, SkMisc, SkDraw):

    _instance_count = 0

    theme = default_theme
    debug = False
    debug_border = skia.ColorBLUE

    # region __init__ 初始化

    def __init__(
        self,
        parent,
        *,
        cursor: str = "arrow",
        style_name: str = "SkWidget",
        font: skia.Font | None = default_font,
        disabled: bool = False,
        status_tip: str | None = None,
    ) -> None:
        """Basic visual component, telling SkWindow how to draw.

        :param parent: Parent component (Usually a SkWindow)
        :param size: Default size (not the final drawn size)
        :param cursor: Cursor style
        """

        SkEventHandling.__init__(self)

        self.focused_redraw: bool = False
        self.parent: SkWidget = parent
        self.style_name: str = style_name

        try:
            self.window: SkWindow | SkAppWindow = (
                self.parent
                if isinstance(self.parent, SkWindow | SkAppWindow)
                else self.parent.window
            )
            self.application = self.window.application
        except AttributeError:
            raise AttributeError(f"Parent component is not a SkWindow-based object. {self.parent}")
        self.anti_alias = self.window.anti_alias
        self.id = self.window.id + "." + self.__class__.__name__ + str(self._instance_count + 1)
        SkWidget._instance_count += 1

        # self.task = {
        #     "resize": dict(),
        #     "move": dict(),
        #     "mouse_move": dict(),
        #     "mouse_motion": dict(),
        #     "mouse_enter": dict(),
        #     "mouse_leave": dict(),
        #     "mouse_press": dict(),
        #     "mouse_release": dict(),
        #     "focus_gain": dict(),
        #     "focus_loss": dict(),
        #     "key_press": dict(),
        #     "key_release": dict(),
        #     "key_repeated": dict(),
        #     "double_click": dict(),
        #     "char": dict(),
        #     "click": dict(),
        #     "configure": dict(),
        #     "update": dict(),
        #     "scroll": dict(),
        # }

        # Mouse events
        buttons = [
            "button1",
            "button2",
            "button3",
            "b1",
            "b2",
            "b3",
        ]  # Left Right Middle
        button_states = ["press", "release", "motion", "move"]

        # for button in buttons:
        #     for state in button_states:
        #         self.trigger(f"mouse_{state}[{button}]")

        self.attributes: dict[str, typing.Any] = {
            "cursor": cursor,
            "theme": None,
            "dwidth": 100,  # default width
            "dheight": 30,  # default height
            "font": font,
            "double_click_interval": 0.24,
            "disabled": disabled,
        }

        self.apply_theme(self.parent.theme)
        self.styles = self.theme.styles

        self._state = "rest"
        self._preview_state = self._state
        # 相对于父组件的坐标
        self._x: int | float = 0
        self._y: int | float = 0
        # 相对于整个画布、整个窗口（除了标题栏）的坐标
        self._canvas_x: int | float = self.parent.x + self._x
        self._canvas_y: int | float = self.parent.y + self._y
        # 相对于整个屏幕的坐标
        self._root_x: int | float = self.window.root_x
        self._root_y: int | float = self.window.root_y
        # 鼠标坐标
        self.mouse_x = 0
        self.mouse_y = 0
        self.mouse_root_x = 0
        self.mouse_root_y = 0

        self.width: int | float = 0
        self.height: int | float = 0

        self.ipadx: int | float = 3
        self.ipady: int | float = 3

        self.focusable: bool = False
        self.visible: bool = False
        self.help_parent_scroll: bool = (
            False  # 当鼠标放在该组件上，并且鼠标滚轮滚动、父组件支持滚动，也会滚动父组件
        )

        self.layout_config: dict[str, dict] = {"none": {}}

        if "SkContainer" in SkMisc.sk_get_type(self.parent):
            self.parent.add_child(self)
        else:
            raise TypeError("Parent component is not a SkContainer-based object.")

        # Events-related
        self.is_mouse_floating: bool = False
        self.is_focus: bool = False
        self.gradient = SkGradient()
        self.drop_shadow = SkDropShadow()
        self.button: typing.Literal[0, 1, 2] = 0
        self.click_time: float | int = 0
        self.need_redraw: bool = False

        def _on_motion(event: SkEvent):
            self.mouse_x = event["x"]
            self.mouse_y = event["y"]

        def _draw(event: SkEvent):
            self.update(redraw=True)

        self.bind("mouse_enter", _draw)
        self.bind("mouse_leave", _draw)
        self.bind("mouse_press", _draw)
        self.bind("mouse_motion", _on_motion)

        self.bind("mouse_release", self._on_mouse_release)

        self.bind("mouse_enter", self._on_mouse_enter)
        self.bind("mouse_leave", self._on_mouse_leave)
        self.bind("mouse_press", self._on_mouse_press)
        self.bind("mouse_release", self._on_mouse_release2)
        self.bind("focus_loss", self._on_focus_loss)

        if status_tip is None:
            status_tip = self.__class__.__name__
        self.attributes["status_tip"] = status_tip

    def __str__(self):
        return self.id

    # endregion

    # region Event

    def _on_focus_loss(self, event: SkEvent):
        """【失去焦点时，组件样式设为rest】"""
        if self.cget("disabled"):
            self.style_state("disabled")
        else:
            self.style_state("rest")

    def _on_mouse_enter(self, event: SkEvent):
        """【鼠标悬停在组件上时，组件样式设为hover】"""
        if self.cget("disabled"):
            self.style_state("disabled")
        else:
            self.style_state("hover")

    def _on_mouse_leave(self, event: SkEvent):
        """【鼠标离开组件时，组件样式设为rest或focus】"""
        if self.cget("disabled"):
            self.style_state("disabled")
        else:
            if self.focusable and self.is_focus:
                self.style_state("focus")
            else:
                self.style_state("rest")

    def _on_mouse_press(self, event: SkEvent):
        """【鼠标按下在组件上时，组件样式设为press】"""
        if self.cget("disabled"):
            self.style_state("disabled")
        else:
            self.style_state("press")

    def _on_mouse_release2(self, event: SkEvent):
        if self.is_mouse_floating:
            self._on_mouse_enter(event)
        else:
            self._on_mouse_leave(event)

    def _pos_update(self, event: SkEvent | None = None):
        # 更新组件的位置
        # 相对整个画布的坐标

        @cache
        def update_pos():
            self._canvas_x = self.parent.canvas_x + self._x
            self._canvas_y = self.parent.canvas_y + self._y
            # 相对整个窗口（除了标题栏）的坐标
            self._root_x = self.canvas_x + self.window.root_x
            self._root_y = self.canvas_y + self.window.root_y

        update_pos()

        self.trigger(
            "move",
            SkEvent(
                widget=self,
                event_type="move",
                x=self._x,
                y=self._y,
                rootx=self._root_x,
                rooty=self._root_y,
            ),
        )

    def _on_mouse_release(self, event) -> None:
        if self.is_mouse_floating:
            self.update(redraw=True)
            self.trigger("click", event)
            time = self.time()

            if self.click_time + self.cget("double_click_interval") > time:
                self.trigger("double_click", event)
                self.click_time = 0
            else:
                self.click_time = time

    # endregion

    # region Draw the widget 绘制组件

    def update(self, redraw: bool | None = None) -> None:
        if redraw is not None:
            self.need_redraw = redraw
            if redraw:
                self.trigger("update", SkEvent(widget=self, event_type="update"))

        if "SkContainer" in SkMisc.sk_get_type(self):
            from .container import SkContainer

            SkContainer.update(self)

        self._pos_update()

    def draw(self, canvas: skia.Canvas) -> None:
        """Execute the widget rendering and subwidget rendering

        :param canvas:
        :return: None
        """
        if self.width <= 0 or self.height <= 0:
            return

        @cache
        def rect(x, y, w, h):
            return skia.Rect.MakeXYWH(x, y, w, h)

        self.rect = rect(self.canvas_x, self.canvas_y, self.width, self.height)

        self.draw_widget(canvas, self.rect)

        if self.debug:
            canvas.drawRoundRect(
                self.rect,
                0,
                0,
                skia.Paint(
                    Style=skia.Paint.kStroke_Style,
                    Color=self.debug_border,
                    StrokeWidth=3,
                ),
            )

        if hasattr(self, "draw_children"):
            self.update_layout(None)
            self.draw_children(canvas)

        self.trigger("redraw", SkEvent(self, "redraw"))

    def draw_widget(self, canvas: skia.Canvas, rect: skia.Rect) -> None:
        """Execute the widget rendering

        :param canvas: skia.Surface
        :param rect: skia.Rect
        :return:
        """
        ...

    # endregion

    # region Widget attribute configs 组件属性配置

    def get_style_selector(self, style_name=None, state=None):
        if style_name is None:
            style_name = self.style_name
        if state is None:
            state = self.style_state()
        return f"{style_name}:{state}"

    @property
    def style_preview_state(self):
        return self._preview_state

    def style_state(self, state: str | None = None) -> typing.Self | str:
        """Style the widget according to the state.
        【根据状态为组件设置样式】
        :param state: str
        :return: None
        """
        if state:
            if state == self._state:
                return self
            self.trigger(
                "style_state_change",
                SkEvent(self, "style_state_change", preview_state=self._state, new_state=state),
            )
            self._preview_state = self._state
            self._state = state
            return self
        else:
            return self._state

    def is_entered(self, mouse_x, mouse_y) -> bool:
        """Check if within the widget's bounds.
        【检查是否进入组件范围（即使超出父组件，其超出部分进入仍判定为True）】
        :param widget: SkWidget
        :param event: SkEvent
        :return bool:
        """
        if self.visible:
            cx, cy = self.canvas_x, self.canvas_y
            x, y = mouse_x, mouse_y
            width, height = self.width, self.height
            return cx <= x <= cx + width and cy <= y <= cy + height
        return False

    @property
    def is_mouse_press(self):
        return (
            self.is_mouse_floating
            and self.window.is_mouse_press
            and self.window.pressing_widget is self
        )

    @property
    def dwidth(self):
        _width = self.cget("dwidth")
        return _width

    @property
    def dheight(self):
        _height = self.cget("dheight")
        return _height

    def destroy(self) -> None:
        self.gradient = None
        del self

    @property
    def text_height(self):
        return self.metrics.fDescent - self.metrics.fAscent

    @property
    def metrics(self):
        return self.cget("font").getMetrics()

    def measure_text(self, text, *args) -> float | int:
        font: skia.Font = self.cget("font")
        return font.measureText(str(text), *args)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self._pos_update()

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self._pos_update()

    @property
    def canvas_x(self):
        return self._canvas_x

    @canvas_x.setter
    def canvas_x(self, value):
        self._canvas_x = value
        self._pos_update()

    @property
    def canvas_y(self):
        return self._canvas_y

    @canvas_y.setter
    def canvas_y(self, value):
        self._canvas_y = value
        self._pos_update()

    @property
    def root_x(self):
        return self._root_x

    @root_x.setter
    def root_x(self, value):
        self._root_x = value
        self._pos_update()

    @property
    def root_y(self):
        return self._root_y

    @root_y.setter
    def root_y(self, value):
        self._root_y = value
        self._pos_update()

    def get_attribute(self, attribute_name: str) -> typing.Any:
        """Get attribute of a widget by name.

        :param attribute_name: attribute name
        """
        return self.attributes[attribute_name]

    cget = get_attribute

    def set_attribute(self, **kwargs):
        """Set attribute of a widget by name.

        :param kwargs: attribute name and _value
        :return: self
        """
        self.attributes.update(**kwargs)
        self.trigger("configure", SkEvent(event_type="configure", widget=self))
        return self

    configure = config = set_attribute

    def mouse_pos(self) -> tuple[int | float, int | float]:
        """Get the mouse pos

        :return:
        """
        return self.window.mouse_pos()

    # endregion

    # region Theme related 主题相关

    def read_size(self, selector: str):
        try:
            # print("Get style: ", selector, "size")
            size = self.theme.get_style_attr(selector, "size")
            # print(self.id, size)
            if size:
                self.config(dwidth=size[0], dheight=size[1])
        except SkStyleNotFoundError:
            pass

    def apply_theme(self, new_theme: SkTheme):
        """Apply theme to the widget and its children.`

        :param new_theme:
        :return:
        """
        self.theme = new_theme
        self.styles = self.theme.styles
        self.read_size(self.style_name)
        if hasattr(self, "children"):
            child: SkWidget
            self.children: list
            for child in self.children:
                if child.theme.is_special:
                    child.theme.set_parent(new_theme.name)
                else:
                    child.apply_theme(new_theme)

    # endregion

    # region Layout related 布局相关

    def show(self):
        """Make the component visible
        【将自己、有布局的子类的visible设为True】
        :return: self
        """
        self.visible = True

        if hasattr(self, "children"):
            for child in self.children:
                if not child.layout_config.get("none"):
                    child.show()

        return self

    def hide(self):
        """Make the component invisible

        :return: self
        """
        self.visible = False
        if hasattr(self, "children"):
            for child in self.children:
                child.visible = False
        return self

    def layout_forget(self):
        """Remove widget from parent layout.

        :return: self
        """
        self.hide()
        self.layout_config = {"none": None}
        for layer in self.parent.draw_list:
            if self in layer:
                layer.remove(self)
        return self

    def fixed(
        self,
        x: int | float,
        y: int | float,
        width: int | float | None = None,
        height: int | float | None = None,
    ) -> "SkWidget":
        """Fix the widget at a specific position.

        Example:
            .. code-block:: python

                widget.fixed(x=10, y=10, width=100, height=100)

        :param x:
        :param y:
        :param width:
        :param height:
        :return: self
        """

        self.show()

        if self.layout_config.get("fixed"):
            self.layout_config["fixed"].update(
                {
                    "x": x,
                    "y": y,
                    "width": width,
                    "height": height,
                }
            )
            self.parent.update_layout()
        else:
            self.layout_config = {
                "fixed": {
                    "layout": "fixed",
                    "x": x,
                    "y": y,
                    "width": width,
                    "height": height,
                }
            }
            self.parent.add_layer3_child(self)

        return self

    def place(self, anchor: str = "nw", x: int = 0, y: int = 0) -> "SkWidget":
        """Place widget at a specific position.

        :param x: X coordinate
        :param y: Y coordinate
        :param anchor:
        :return: self
        """

        self.show()

        self.layout_config = {
            "place": {
                "anchor": anchor,
                "x": x,
                "y": y,
            }
        }
        self.parent.add_layer2_child(self)

        return self

    floating = place

    def grid(
        self,
        row: int = 0,  # 行 横
        column: int = 1,  # 列 竖
        rowspan: int = 1,
        columnspan: int = 1,
        padx: int | float | tuple[int | float, int | float] | None = 5,
        pady: int | float | tuple[int | float, int | float] | None = 5,
        ipadx: int | float | tuple[int | float, int | float] | None = 0,
        ipady: int | float | tuple[int | float, int | float] | None = 0,
    ):

        self.show()
        self.layout_config = {
            "grid": {
                "row": row,
                "column": column,
                "rowspan": rowspan,
                "columnspan": columnspan,
                "padx": padx,
                "pady": pady,
                "ipadx": ipadx,
                "ipady": ipady,
            }
        }
        self.parent.add_layer1_child(self)

        return self

    def pack(
        self,
        direction: str = "n",
        padx: int | float | tuple[int | float, int | float] = 0,
        pady: int | float | tuple[int | float, int | float] = 0,
        expand: bool | tuple[bool, bool] = False,
    ):
        """Position the widget with box layout.

        :param direction: Direction of the layout
        :param padx: Paddings on x direction
        :param pady: Paddings on y direction
        :param expand: Whether to expand the widget
        :return: self
        """

        self.show()
        self.layout_config = {
            "pack": {
                "direction": direction,
                "padx": padx,
                "pady": pady,
                "expand": expand,
            }
        }
        self.parent.add_layer1_child(self)

        return self

    def box(
        self,
        side: typing.Literal["top", "bottom", "left", "right"] = "top",
        padx: int | float | tuple[int | float, int | float] = 5,
        pady: int | float | tuple[int | float, int | float] = 5,
        ipadx: int | float | tuple[int | float, int | float] | None = None,
        ipady: int | float | tuple[int | float, int | float] | None = None,
        expand: bool | tuple[bool, bool] = False,
    ):
        """Position the widget with box layout.

        :param side: Side of the widget layout
        :param padx: Paddings on x direction
        :param pady: Paddings on y direction
        :param ipadx: Internal paddings on x direction
        :param ipady: Internal paddings on y direction
        :param expand: Whether to expand the widget
        :return: self
        """

        self.show()
        if self.layout_config.get("box"):
            self.layout_config["box"].update(
                {
                    "side": side,
                    "padx": padx,
                    "pady": pady,
                    "ipadx": ipadx,
                    "ipady": ipady,
                    "expand": expand,
                }
            )
        else:
            self.layout_config = {
                "box": {
                    "side": side,
                    "padx": padx,
                    "pady": pady,
                    "ipadx": ipadx,
                    "ipady": ipady,
                    "expand": expand,
                }
            }
            self.parent.add_layer1_child(self)
        if ipadx:
            self.ipadx = ipadx
        if ipady:
            self.ipady = ipady
        return self

    # endregion

    # region Focus Related 焦点相关

    def focus_set(self) -> None:
        """
        Set focus
        """
        if self.focusable and not self.cget("disabled"):
            if not self.is_focus:
                self.window.focus_get().trigger("focus_loss", SkEvent(event_type="focus_loss"))
                self.window.focus_get().is_focus = False
                self.window.focus_widget = self
                self.is_focus = True

                self.trigger("focus_gain", SkEvent(event_type="focus_gain"))

    def focus_get(self) -> None:
        """
        Get focus
        """
        return self.window.focus_get()

    # endregion
