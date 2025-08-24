import typing
from functools import cache
from typing import Any, Literal

import glfw
import skia

from ..event import SkEvent, SkEventHanding
from ..misc import SkMisc
from ..styles.color import SkColor, SkGradient, skcolor2color, style_to_color
from ..styles.drop_shadow import SkDropShadow
from ..styles.font import default_font
from ..styles.theme import SkStyleNotFoundError, SkTheme, default_theme
from .appwindow import SkAppWindow
from .window import SkWindow


class SkWidget(SkEventHanding, SkMisc):

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
        style: str = "SkWidget",
        font: skia.Font | None = default_font,
    ) -> None:
        """Basic visual component, telling SkWindow how to draw.

        :param parent: Parent component (Usually a SkWindow)
        :param size: Default size (not the final drawn size)
        :param cursor: Cursor style
        """

        SkEventHanding.__init__(self)

        self.parent = parent
        self.style = style

        try:
            self.window: SkWindow | SkAppWindow = (
                self.parent
                if isinstance(self.parent, SkWindow | SkAppWindow)
                else self.parent.window
            )
            self.application = self.window.application
        except AttributeError:
            raise AttributeError(
                f"Parent component is not a SkWindow-based object. {self.parent}"
            )
        self.anti_alias = self.window.anti_alias
        self.id = (
            self.window.id
            + "."
            + self.__class__.__name__
            + str(self._instance_count + 1)
        )
        SkWidget._instance_count += 1

        self.events = {
            "resize": dict(),
            "move": dict(),
            "mouse_motion": dict(),
            "mouse_enter": dict(),
            "mouse_leave": dict(),
            "mouse_pressed": dict(),
            "mouse_released": dict(),
            "focus_gain": dict(),
            "focus_loss": dict(),
            "key_pressed": dict(),
            "key_released": dict(),
            "key_repeated": dict(),
            "char": dict(),
            "click": dict(),
            "configure": dict(),
            "update": dict(),
            "scroll": dict(),
        }

        # TODO 制作个双击&三击事件

        # Mouse events
        buttons = [
            "button1",
            "button2",
            "button3",
            "b1",
            "b2",
            "b3",
        ]  # Left Right Middle
        button_states = ["pressed", "released", "motion"]

        for button in buttons:
            for state in button_states:
                self.event_generate(f"{button}_{state}")

        self.attributes: dict[str, Any] = {
            "cursor": cursor,
            "theme": None,
            "dwidth": 100,  # default width
            "dheight": 30,  # default height
            "font": font,
        }

        self.apply_theme(self.parent.theme)
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

        self.width: int | float = 0
        self.height: int | float = 0

        self.ipadx: int | float = 3
        self.ipady: int | float = 3

        self.focusable: bool = False
        self.visible: bool = False

        self.layout_config: dict[str, dict] = {"none": {}}

        try:
            self.parent.add_child(self)
        except TypeError:
            raise TypeError("Parent component is not a SkContainer-based object.")

        # Events-related
        self.is_mouse_floating: bool = False
        self.is_mouse_pressed: bool = False
        self.is_focus: bool = False
        self.gradient = SkGradient()
        self.button: typing.Literal[0, 1, 2] = 0

        def _on_mouse(event: SkEvent):
            self.mouse_x = event.x
            self.mouse_y = event.y

        self.bind("mouse_enter", _on_mouse)
        self.bind("mouse_motion", _on_mouse)

        self.bind("b1_released", self._click)

    # endregion

    # region Event

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
        if self.button != 1:
            if self.is_mouse_floating:
                self.event_trigger("click", event)

    # endregion

    # region Draw the widget 绘制组件

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

        _rect = rect(self.canvas_x, self.canvas_y, self.width, self.height)

        self.draw_widget(canvas, _rect)

        if self.debug:
            canvas.drawRoundRect(
                _rect,
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

    def draw_widget(self, canvas: skia.Canvas, rect: skia.Rect) -> None:
        """Execute the widget rendering

        :param canvas: skia.Surface
        :param rect: skia.Rect
        :return:
        """
        ...

    @staticmethod
    def _radial_shader(
        center: tuple[float | int, float | int],
        radius: float | int,
        colors: list | tuple[skia.Color] | set,
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

    def _draw_text(
        self,
        canvas: skia.Canvas,
        rect: skia.Rect,
        text: str | None = "",
        bg: None | str | int | SkColor = None,
        fg: None | str | int | SkColor = None,
        radius: float | int = 3,
        align: typing.Literal["center", "right", "left"] = "center",
        font: skia.Font = None,
    ) -> None:
        """Draw central text

        .. note::
            >>> self._draw_text(canvas, "Hello", skia.ColorBLACK, 0, 0, 100, 100)

        :param canvas: The canvas
        :param rect: The skia Rect
        :param text: The text
        :param fg: The color of the text
        :return: None
        """
        if not font:
            font = self.attributes["font"]

        # bg = skia.ColorBLACK

        text = str(text)

        # 绘制字体
        @cache
        def cache_paint(anti_alias, fg_):
            return skia.Paint(AntiAlias=anti_alias, Color=fg_)

        text_paint = cache_paint(
            self.anti_alias, skcolor2color(style_to_color(fg, self.theme))
        )

        text_width = self.measure_text(text)

        if align == "center":
            draw_x = rect.left() + (rect.width() - text_width) / 2
        elif align == "right":
            draw_x = rect.left() + rect.width() - text_width
        else:  # left
            draw_x = rect.left()

        metrics = self.metrics
        draw_y = (
            rect.top() + rect.height() / 2 - (metrics.fAscent + metrics.fDescent) / 2
        )

        if bg:
            bg = skcolor2color(style_to_color(bg, self.theme))
            bg_paint = skia.Paint(AntiAlias=self.anti_alias, Color=bg)
            canvas.drawRoundRect(
                rect=skia.Rect.MakeLTRB(
                    draw_x,
                    rect.top(),
                    draw_x + text_width,
                    rect.bottom(),
                ),
                rx=radius,
                ry=radius,
                paint=bg_paint,
            )

        canvas.drawSimpleText(text, draw_x, draw_y, font, text_paint)

        return draw_x, draw_y

    def _draw_styled_text(
        self,
        canvas: skia.Canvas,
        rect: skia.Rect,
        bg: None | str | int | SkColor = None,
        fg: None | str | int | SkColor = None,
        radius: float | int = 3,
        # [ "Content", {"start": 5, "end": 10, "fg": skia.ColorRED, "bg": skia.ColorBLACK, "font": skia.Font} ]
        text: tuple[str, dict[str, str | int | SkColor | skia.Font]] = ("",),
        font: skia.Font = None,
    ):
        if isinstance(text, str):
            _text = text
            return None
        else:
            _text = text[0]
        self._draw_text(
            canvas=canvas,
            text=_text,
            rect=rect,
            bg=bg,
            fg=fg,
            align="left",
            font=font,
        )
        if isinstance(text, str):
            return None

        for item in text:
            if "font" in item:
                font = item["font"]
            if "fg" in item:
                fg = item["fg"]
            if "bg" in item:
                bg = item["bg"]
            if isinstance(item, dict):

                _rect = skia.Rect.MakeLTRB(
                    rect.left() + self.measure_text(_text[: item["start"]]),
                    rect.top(),
                    rect.right(),
                    rect.bottom(),
                )
                self._draw_text(
                    canvas=canvas,
                    rect=_rect,
                    text=_text[item["start"] : item["end"]],
                    bg=bg,
                    fg=fg,
                    radius=radius,
                    align="left",
                    font=font,
                )
        return None

    def _draw_rect(
        self,
        canvas: skia.Canvas,
        rect: typing.Any,
        radius: int = 0,
        bg: str | SkColor | int | None | tuple[int, int, int, int] = None,
        bd: str | SkColor | int | None | tuple[int, int, int, int] = None,
        width: int | float = 0,
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

        if bg:
            bg_paint = skia.Paint(
                AntiAlias=self.anti_alias,
                Style=skia.Paint.kStrokeAndFill_Style,
            )
            bg = skcolor2color(style_to_color(bg, self.theme))

            # Background
            bg_paint.setStrokeWidth(width)
            bg_paint.setColor(bg)
            shadow = SkDropShadow(config_list=bd_shadow)
            shadow.draw(bg_paint)
            if bg_shader:
                if isinstance(bg_shader, dict):
                    if "linear_gradient" in bg_shader:
                        self.gradient.linear(
                            widget=self,
                            config=bg_shader["linear_gradient"],
                            paint=bg_paint,
                        )
                else:
                    if bg_shader.lower() == "rainbow":
                        self._draw_rainbow_shader(bg_paint, rect)

            canvas.drawRoundRect(rect, radius, radius, bg_paint)
        if bd and width > 0:
            bd_paint = skia.Paint(
                AntiAlias=self.anti_alias,
                Style=skia.Paint.kStroke_Style,
            )
            bd = skcolor2color(style_to_color(bd, self.theme))

            # Border
            bd_paint.setStrokeWidth(width)
            bd_paint.setColor(bd)
            if bd_shader:
                if isinstance(bd_shader, dict):
                    if "linear_gradient" in bd_shader:
                        self.gradient.linear(
                            widget=self,
                            config=bd_shader["linear_gradient"],
                            paint=bd_paint,
                        )
                else:
                    if bd_shader.lower() == "rainbow":
                        self._draw_rainbow_shader(bd_paint, rect)

            canvas.drawRoundRect(rect, radius, radius, bd_paint)

    def _draw_line(
        self, canvas: skia.Canvas, x0, y0, x1, y1, fg=skia.ColorGRAY, width: int = 1
    ):
        fg = skcolor2color(style_to_color(fg, self.theme))
        paint = skia.Paint(Color=fg, StrokeWidth=width)

        canvas.drawLine(x0, y0, x1, y1, paint)

    @staticmethod
    def _draw_image(
        canvas: skia.Canvas, rect: Any, uri: str | None = None, path: str | None = None
    ) -> None:
        if path:
            image = skia.Image.open(path)
        elif uri:
            image = skia.Image()
        else:
            image = None
        if image:
            canvas.drawImageRect(image, rect, skia.SamplingOptions(), skia.Paint())
        del image

    # endregion

    # region Widget attribute configs 组件属性配置

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

    def measure_text(self, text: str, *args) -> float | int:
        font: skia.Font = self.cget("font")
        return font.measureText(text, *args)

    def update(self):
        self._pos_update()
        self.post()

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

    def clipboard(self, value: str | None = None) -> str | typing.Self:
        """Get string from clipboard

        anti images
        """
        if value is not None:
            glfw.set_clipboard_string(self.window.the_window, value)
            return self
        else:
            try:
                return glfw.get_clipboard_string(self.window.the_window).decode("utf-8")
            except AttributeError:
                return ""

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

    def mouse_pos(self) -> tuple[int | float, int | float]:
        """Get the mouse pos

        :return:
        """
        return self.window.mouse_pos()

    # endregion

    # region Theme related 主题相关

    def read_size(self, selector: str):
        try:
            size = self.theme.get_style_attr(selector, "size")
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
        self.read_size(self.style)
        if hasattr(self, "children"):
            for child in self.children:
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
                    child.visible = True

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
            self.parent.add_fixed_child(self)

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
        self.parent.add_floating_child(self)

        return self

    def grid(
        self,
        row: int,  # 行 横
        column: int,  # 列 竖
        rowspan: int = 1,
        columnspan: int = 1,
    ):

        self.show()
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

        self.show()
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
        padx: int | float | tuple[int | float, int | float] = 10,
        pady: int | float | tuple[int | float, int | float] = 10,
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
                    "expand": expand,
                }
            )
        else:
            self.layout_config = {
                "box": {
                    "side": side,
                    "padx": padx,
                    "pady": pady,
                    "expand": expand,
                }
            }
            self.parent.add_layout_child(self)
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
        if self.focusable:
            if not self.is_focus:
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
