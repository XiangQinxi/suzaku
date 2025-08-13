from typing import Any, Literal, Union

import clipman
import glfw
import skia

from ..after import SkAfter
from ..event import SkEvent, SkEventHanding
from ..styles.color import SkGradient, make_color
from ..styles.drop_shadow import SkDropShadow
from ..styles.font import default_font
from ..styles.theme import SkTheme, default_theme
from ..widgets.appwindow import SkAppWindow
from .window import SkWindow

clipman.init()


class SkWidget(SkEventHanding, SkAfter):

    _instance_count = 0

    theme = default_theme

    # region __init__ 初始化

    def __init__(
        self,
        parent,
        size: tuple[int, int] = (100, 30),
        cursor: str = "arrow",
        font: skia.Font | None = default_font,
    ) -> None:
        """Basic visual component, telling SkWindow how to draw.

        :param parent: Parent component (Usually a SkWindow)
        :param size: Default size (not the final drawn size)
        :param cursor: Cursor style
        """

        SkEventHanding.__init__(self)
        SkAfter.__init__(self)

        self.parent = parent

        try:
            self.window: SkWindow | SkAppWindow = (
                self.parent
                if isinstance(self.parent, SkWindow | SkAppWindow)
                else self.parent.window
            )
        except AttributeError:
            raise AttributeError(
                f"Parent component is not a SkWindow-based object. {self.parent}"
            )

        self.id = (
            self.window.id
            + "."
            + self.__class__.__name__
            + str(self._instance_count + 1)
        )
        SkWidget._instance_count += 1

        self.attributes: dict[str, Any] = {
            "cursor": cursor,
            "theme": None,
            "dwidth": size[0],  # default width
            "dheight": size[1],  # default height
            "font": font,
        }

        self.theme: SkTheme = self.parent.theme
        self.styles = self.theme.styles

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

        self.width: int | float = size[0]
        self.height: int | float = size[1]

        self.focusable: bool = False
        self.visible: bool = False

        self.init_events(
            {
                "resize": {},
                "move": {},
                "mouse_motion": {},
                "mouse_enter": {},
                "mouse_leave": {},
                "mouse_pressed": {},
                "mouse_released": {},
                "focus_gain": {},
                "focus_loss": {},
                "key_pressed": {},
                "key_released": {},
                "key_repeated": {},
                "char": {},
                "click": {},
                "configure": {},
                "update": {},
            }
        )
        self.layout_config: dict[str, dict] = {"none": {}}

        try:
            self.parent.add_child(self)
        except TypeError:
            raise TypeError("Parent component is not a SkContainer-based object.")

        # Events-related
        self.is_mouse_floating: bool = False
        self.is_mouse_pressed: bool = False
        self.is_focus: bool = False

        self.parent.add_child(self)

        def _on_event(event: SkEvent):
            self.mouse_x = event.x
            self.mouse_y = event.y

        self.bind("mouse_enter", _on_event)
        self.bind("mouse_motion", _on_event)

        self.bind("mouse_released", self._click)

    # endregion

    # region Event

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

    def _pos_update(self, event: SkEvent | None = None):
        # 更新组件的位置
        # 相对整个画布的坐标
        self._canvas_x = self.parent.canvas_x + self._x
        self._canvas_y = self.parent.canvas_y + self._y
        # 相对整个窗口（除了标题栏）的坐标
        self._root_x = self.canvas_x + self.window.root_x
        self._root_y = self.canvas_y + self.window.root_y

        self.event_trigger(
            "move",
            SkEvent(
                event_type="move",
                x=self._x,
                y=self._y,
                rootx=self._root_x,
                rooty=self._root_y,
            ),
        )

    def _click(self, event) -> None:
        """
        Check click event (not pressed)

        :return: None
        """
        if self.is_mouse_floating:
            self.event_trigger("click", event)

    # endregion

    # region Draw the widget 绘制组件

    def draw(self, canvas: skia.Surfaces) -> None:
        """Execute the widget rendering and subwidget rendering

        :param canvas:
        :return: None
        """
        if self.width <= 0 or self.height <= 0:
            return

        rect = skia.Rect.MakeXYWH(
            x=self.canvas_x, y=self.canvas_y, w=self.width, h=self.height
        )
        self._draw(canvas, rect)
        if hasattr(self, "draw_children"):
            self.draw_children(canvas)
            self._handle_layout(None)

    def _draw(self, canvas: skia.Surface, rect: skia.Rect) -> None:
        """Execute the widget rendering

        :param canvas: skia.Surface
        :param rect: skia.Rect
        :return:
        """
        ...

    @staticmethod
    def _rainbow_shader(
        rect, colors: list | tuple[skia.Color] | None, cx=None, cy=None
    ):
        """Draw the raindow shader of the rect

        :param color: The color of the raindow shader
        """
        if not cx:
            cx = rect.centerX()
        if not cy:
            cy = rect.centerY()
        if not colors:
            colors = (
                skia.ColorCYAN,  # Cyan
                skia.ColorMAGENTA,  # Magenta
                skia.ColorYELLOW,  # Yellow
                skia.ColorCYAN,  # Cyan
            )
        else:
            colors2 = list
            for _color in colors:
                colors2.append(make_color(_color))
            colors = tuple(colors2)
        return skia.GradientShader.MakeSweep(
            cx=cx,  # Center x position of the sweep
            cy=cy,  # Center y position of the sweep
            startAngle=0,  # Start angle of the sweep in degrees
            endAngle=360,  # End angle of the sweep in degrees
            colors=colors,
            localMatrix=None,  # Local matrix for the gradient
        )

    @staticmethod
    def _radial_shader(
        center: tuple[float | int, float | int],
        radius: float | int,
        colors: list | tuple[skia.Color],
    ):
        return skia.GradientShader.MakeRadial(
            center=center,
            radius=radius,
            colors=colors,
        )

    def _draw_radial_shader(self, paint, center, radius, colors):
        """Draw radial shader of the rect

        :param paint: The paint of the rect
        :param center: The center of the radial shader
        :param radius: The radius of the radial shader
        :param colors: The colors of the radial shader
        :return: None
        """
        paint.setShader(self._radial_shader(center, radius, colors))

    @staticmethod
    def _blur(style: skia.BlurStyle | None = None, sigma: float = 5.0):
        if not style:
            style = skia.kNormal_BlurStyle
        return skia.MaskFilter.MakeBlur(style, sigma)

    def _draw_blur(self, paint: skia.Paint, style=None, sigma=None):
        paint.setMaskFilter(self._blur(style, sigma))

    def _draw_rainbow_shader(
        self,
        paint,
        rect,
        colors: list | tuple[skia.Color] | None = None,
        cx: float | int | None = None,
        cy: float | int | None = None,
    ):
        """Set rainbow shader of the rect

        :param paint: The paint of the rect
        :param rect: The rect
        :return: None
        """
        paint.setShader(self._rainbow_shader(rect=rect, colors=colors, cx=cx, cy=cy))

    def _draw_central_text(
        self,
        canvas,
        text,
        fg,
        canvas_x,
        canvas_y,
        width,
        height,
        font: skia.Font = None,
    ):
        """Draw central text

        .. note::
            >>> self._draw_central_text(canvas, "Hello", skia.ColorBLACK, 0, 0, 100, 100)

        :param canvas: The canvas
        :param text: The text
        :param fg: The color of the text
        :param x: The x of the text
        :param y: The y of the text
        :param width: The width of the text
        :param height: The height of the text
        :return: None
        :raises: None
        """
        if not font:
            font = self.attributes["font"]

        # 绘制字体
        text_paint = skia.Paint(AntiAlias=True, Color=make_color(fg))

        text_width = font.measureText(text)
        metrics = font.getMetrics()

        draw_x = canvas_x + width / 2 - text_width / 2
        draw_y = canvas_y + height / 2 - (metrics.fAscent + metrics.fDescent) / 2

        canvas.drawSimpleText(text, draw_x, draw_y, font, text_paint)

    def _draw_frame(
        self,
        canvas: skia.Canvas,
        rect: any,
        radius: int,
        bg: str,
        width: int,
        bd: str,
        bd_shadow: (
            None | tuple[int | float, int | float, int | float, int | float, str]
        ) = None,
        bd_shader: None | Literal["rainbow"] = None,
        bg_shader: None | Literal["rainbow"] = None,
    ):
        """Draw the frame

        :param canvas: The skia canvas
        :param rect: The skia rect
        :param radius: The radius of the rect
        :param bg: The background
        :param width: The width
        :param bd: The color of the border
        :param bd_shadow: The border_shadow switcher
        :param bd_shader: The shader of the border

        """

        if bd_shadow:
            drop_shadow_rect = skia.Rect.MakeXYWH(
                self.canvas_x, self.canvas_y, self.width, self.height
            )
            drop_shadow_paint = skia.Paint(
                AntiAlias=True,
                Style=skia.Paint.kStrokeAndFill_Style,
                Color=make_color(bg),
            )
            shadow = SkDropShadow(config_list=bd_shadow)
            shadow.draw(drop_shadow_paint)

            canvas.drawRoundRect(drop_shadow_rect, radius, radius, drop_shadow_paint)

        bg_paint = skia.Paint(
            AntiAlias=True,
            Style=skia.Paint.kStrokeAndFill_Style,
        )

        bd_paint = skia.Paint(
            AntiAlias=True,
            Style=skia.Paint.kStroke_Style,
        )

        # Background
        bg_paint.setColor(make_color(bg))
        if bg_shader:
            if isinstance(bg_shader, dict):
                if "linear_gradient" in bg_shader:
                    gradient = SkGradient()
                    gradient.set_linear(
                        widget=self, config=bg_shader["linear_gradient"]
                    )
                    gradient.draw(
                        paint=bg_paint,
                    )
            else:
                if bg_shader.lower() == "rainbow":
                    self._draw_rainbow_shader(bg_paint, rect)

        # Border
        bd_paint.setStrokeWidth(width)
        bd_paint.setColor(make_color(bd))
        if bd_shader:
            if isinstance(bd_shader, dict):
                if "linear_gradient" in bd_shader:
                    gradient = SkGradient()
                    gradient.set_linear(
                        widget=self, config=bd_shader["linear_gradient"]
                    )
                    gradient.draw(
                        paint=bd_paint,
                    )
            else:
                if bd_shader.lower() == "rainbow":
                    self._draw_rainbow_shader(bd_paint, rect)

        # Draw background first
        canvas.drawRoundRect(rect, radius, radius, bg_paint)

        # canvas.save()

        # shadow = SkDropShadow(config_list=bd_shadow)
        # shadow.draw(bd_paint)

        canvas.drawRoundRect(rect, radius, radius, bd_paint)

    # endregion

    # region Widget attribute configs 组件属性配置
    @staticmethod
    def clipboard_get() -> str:
        return clipman.paste()

    @staticmethod
    def clipboard_set(value) -> None:
        clipman.copy(value)

    def get_attribute(self, attribute_name: str) -> Any:
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
        self.event_trigger("configure", SkEvent(event_type="configure", widget=self))
        return self

    configure = config = set_attribute

    def show(self):
        """Make the component visible

        :return: self
        """
        self.visible = True
        return self

    def hide(self):
        """Make the component invisible

        :return: self
        """
        self.visible = False
        return self

    def mouse_pos(self) -> tuple[int | float, int | float]:
        """Get the mouse pos

        :return:
        """
        return self.window.mouse_pos()

    # endregion

    # region Theme related 主题相关

    def apply_theme(self, new_theme: SkTheme):
        """Apply theme to the widget and its children.`

        :param new_theme:
        :return:
        """
        self.theme = new_theme
        self.styles = self.theme.styles
        if hasattr(self, "children"):
            for child in self.children:
                child.apply_theme(new_theme)

    # endregion

    # region Layout related 布局相关

    def layout_forget(self):
        """Remove widget from parent layout.

        :return: self
        """
        self.visible = False
        self.layout_config = {"none": None}
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
        self.x = x
        self.y = y
        if width:
            self.width = width
        if height:
            self.height = height
        self.visible = True
        self.layout_config = {
            "fixed": {
                "layout": "fixed",
                "x": self.x,
                "y": self.y,
                "width": self.width,
                "height": self.height,
            }
        }
        self.parent.add_fixed_child(self)
        return self

    def place(self, anchor: str = "nw", x: int = 0, y: int = 0) -> "SkWidget":
        """Place widget at a specific position.

        :param x: X coordinate
        :param y: Y coordinate
        :param anchor:
        :return: self
        """
        self.visible = True
        self.layout_config = {
            "place": {
                "anchor": anchor,
                "x": x,
                "y": y,
            }
        }
        self.parent.add_floating_child(self)
        return self

    def grid(
        self,
        row: int,
        column: int,
        rowspan: int = 1,
        columnspan: int = 1,
    ):
        self.visible = True
        self.layout_config = {
            "grid": {
                "row": row,
                "column": column,
                "rowspan": rowspan,
                "columnspan": columnspan,
            }
        }
        self.parent.add_layout_child(self)
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
        self.visible = True
        self.layout_config = {
            "pack": {
                "direction": direction,
                "padx": padx,
                "pady": pady,
                "expand": expand,
            }
        }
        self.parent.add_layout_child(self)
        return self

    def box(
        self,
        side: Literal["top", "bottom", "left", "right"] = "top",
        padx: int | float | tuple[int | float, int | float] = 5,
        pady: int | float | tuple[int | float, int | float] = 5,
        ipadx: int | float | tuple[int | float, int | float] = 0,
        ipady: int | float | tuple[int | float, int | float] = 0,
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
        self.visible = True
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
        self.parent.add_layout_child(self)
        return self

    # endregion

    # region Focus Related 焦点相关

    def focus_set(self) -> None:
        """
        Set focus
        """
        if self.focusable:
            self.window.focus_get().event_trigger(
                "focus_loss", SkEvent(event_type="focus_loss")
            )
            self.window.focus_get().is_focus = False
            self.window.focus_widget = self
            self.is_focus = True
            self.event_trigger("focus_gain", SkEvent(event_type="focus_gain"))

    def focus_get(self) -> None:
        """
        Get focus
        """
        return self.window.focus_get()

    # endregion
