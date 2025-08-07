from typing import Any, Literal, Union

import skia

from ..event import SkEvent, SkEventHanding
from ..styles.color_old import color
from ..styles.font import default_font
from ..styles.theme import SkTheme, default_theme
from ..widgets.appwindow import SkAppWindow
from .window import SkWindow


class SkWidget(SkEventHanding):

    _instance_count = 0

    theme = default_theme

    # region __init__ 初始化

    def __init__(
        self,
        parent,
        size: tuple[int, int] = (100, 30),
        cursor: str = "arrow",
        widget_id: Union[str, None] = None,
        name="SkWidget",
    ) -> None:
        """Basic visual component, telling SkWindow how to draw.

        :param parent: Parent component (Usually a SkWindow)
        :param size: Default size (not the final drawn size)
        :param cursor: Cursor style
        :param name: Name of the widget
        :param widget_id: Identification code
        """

        super().__init__()

        self.__class__._instance_count += 1

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

        self.attributes: dict[str, Any] = {
            "name": name,
            "cursor": cursor,
            "id": widget_id,
            "theme": None,
            "dwidth": size[0],  # default width
            "dheight": size[1],  # default height
        }

        self.theme: SkTheme = self.parent.theme
        self.styles = self.theme.styles

        self.x: int | float = 0
        self.y: int | float = 0

        self.width: int | float = size[0]
        self.height: int | float = size[1]

        self.focusable: bool = False
        self.visible: bool = False

        if not widget_id:
            self.attributes["id"] = name + "." + str(self.__class__._instance_count)

        self.events = {
            "mouse_motion": [],
            "mouse_enter": [],
            "mouse_leave": [],
            "mouse_pressed": [],
            "mouse_released": [],
            "focus_gain": [],
            "focus_loss": [],
            "key_pressed": [],
            "key_released": [],
            "key_repeated": [],
            "char": [],
        }

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

    # endregion

    # region Draw the widget 绘制组件

    def draw(self, canvas: skia.Surfaces) -> None:
        """Execute the widget rendering and subwidget rendering

        :param canvas:
        :return: None
        """
        if self.width <= 0 or self.height <= 0:
            return
        rect = skia.Rect(self.x, self.y, self.x + self.width, self.y + self.height)
        self._draw(canvas, rect)
        if hasattr(self, "draw_children"):
            self.draw_children(canvas)

    def _draw(self, canvas: skia.Surface, rect: skia.Rect) -> None:
        """Execute the widget rendering

        :param canvas: skia.Surface
        :param rect: skia.Rect
        :return:
        """
        ...

    @staticmethod
    def _drop_shadow(dx=3, dy=3, sigmaX=2, sigmaY=2, colr: skia.Color = None):
        """Draw drop shadow of the rect

        :param dx: The x offset of the drop shadow
        :param dy: The y offset of the drop shadow
        :param sigmaX: The standard deviation of the drop shadow in the x direction
        :param sigmaY: The standard deviation of the drop shadow in the y direction
        :param colr: The color of the drop shadow
        :return: skia.ImageFilters.DropShadow
        """
        return skia.ImageFilters.DropShadow(
            dx=dx, dy=dy, sigmaX=sigmaX, sigmaY=sigmaY, color=color(colr)
        )

    @staticmethod
    def _rainbow_shader(rect, colors: list | tuple[skia.Color] | None):
        """Draw the raindow shader of the rect
        
        :param color: The color of the raindow shader
        """
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
                colors2.append(color(_color))
            colors = tuple(colors2)
        return skia.GradientShader.MakeSweep(
            cx=rect.centerX(),  # Center x position of the sweep
            cy=rect.centerY(),  # Center y position of the sweep
            startAngle=0,  # Start angle of the sweep in degrees
            endAngle=360,  # End angle of the sweep in degrees
            colors=colors,
            localMatrix=None,  # Local matrix for the gradient
        )

    def _draw_drop_shadow(self, rect_paint, dx=3, dy=3, sigmaX=2, sigmaY=2, colr=None):
        """Draw drop shadow of the rect

        :param rect_paint: The paint of the rect
        :param dx: The x offset of the drop shadow
        :param dy: The y offset of the drop shadow
        :param sigmaX: The standard deviation of the drop shadow in the x direction
        :param sigmaY: The standard deviation of the drop shadow in the y direction
        :param colr: The color of the drop shadow
        :return: None
        """

        rect_paint.setImageFilter(self._drop_shadow(dx, dy, sigmaX, sigmaY, colr))

    def _draw_rainbow_shader(
        self, rect_paint, rect, colors: list | tuple[skia.Color] | None = None
    ):
        """Set rainbow shader of the rect

        :param rect_paint: The paint of the rect
        :param rect: The rect
        :return: None
        """
        rect_paint.setShader(self._rainbow_shader(rect, colors))

    @staticmethod
    def _draw_central_text(
        canvas, text, fg, x, y, width, height, font: skia.Font = None
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
            font: skia.Font = default_font

        # 绘制字体
        text_paint = skia.Paint(AntiAlias=True, Color=color(fg))

        text_width = font.measureText(text)
        metrics = font.getMetrics()

        draw_x = x + width / 2 - text_width / 2
        draw_y = y + height / 2 - (metrics.fAscent + metrics.fDescent) / 2

        canvas.drawSimpleText(text, draw_x, draw_y, font, text_paint)

    def _draw_frame(
        self,
        canvas: any,
        rect: any,
        radius: int,
        bg: str,
        width: int,
        bd: str,
        bd_shadow: bool = True,
        bd_shader: None | Literal["rainbow"] = "rainbow",
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
        # Draw background
        rect_paint = skia.Paint(
            AntiAlias=True,
            Style=skia.Paint.kStrokeAndFill_Style,
        )

        rect_paint.setColor(color(bg))
        rect_paint.setStrokeWidth(width)

        canvas.drawRoundRect(rect, radius, radius, rect_paint)

        # Draw border
        # Draw shadow
        if bd_shadow:
            self._draw_drop_shadow(
                rect_paint, dx=3, dy=3, sigmaX=10, sigmaY=10, colr=bd
            )

        # Draw border
        if bd_shader:
            if bd_shader.lower() == "rainbow":
                self._draw_rainbow_shader(rect_paint, rect)

        rect_paint.setColor(color(bd))
        rect_paint.setStyle(skia.Paint.kStroke_Style)

        canvas.drawRoundRect(rect, radius, radius, rect_paint)

    # endregion

    # region Widget attribute configs 组件属性配置

    def get_attribute(self, attribute_name: str) -> Any:
        """Get attribute of a widget by name.

        :param attribute_name: attribute name
        """
        return self.attributes[attribute_name]

    cget = get_attribute

    def set_attribute(self, **kwargs):
        """Set attribute of a widget by name.

        :param kwargs: attribute name and value
        :return: self
        """
        self.attributes.update(**kwargs)
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

        :param anchor:
        :param
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
        padx: int | float | tuple[int | float, int | float] = 10,
        pady: int | float | tuple[int | float, int | float] = 10,
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
            self.window.focus_get().event_generate(
                "focus_loss", SkEvent(event_type="focus_loss")
            )
            self.window.focus_get().is_focus = False
            self.window.focus_widget = self
            self.is_focus = True
            self.event_generate("focus_gain", SkEvent(event_type="focus_gain"))

    def focus_get(self) -> None:
        """
        Get focus
        """
        return self.window.focus_get()

    # endregion
