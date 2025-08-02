from .visual import SkVisual

from typing import Union

class SkButton(SkVisual):

    def __init__(self, *args, text: str = "SkButton", size: tuple[int, int] = (105, 35),
                 cursor: Union[str, None] = "hand", style="SkButton",
                 command: Union[callable, None] = None, id: Union[str, None] = None, **kwargs) -> None:
        """Button Component.

        **Will be re-written in future.**

        * *args: Passed to SkVisual
        * text: Button text
        * size: Default size
        * cursor: Cursor style when hovering
        * style: Style name
        * command: Function to run when clicked
        * id: Identification code (optional)
        * **kwargs: Passed to SkVisual
        """

        super().__init__(*args, size=size, style=style, name="sk_button", **kwargs)

        self.evts["click"] = []
        self.visual_attr["text"] = text

        self.visual_attr["cursor"] = cursor

        self.command = command

        if command:
            self.bind("click", lambda evt: command())

        """self.bind("mouse_enter", lambda evt: print("enter"))
        self.bind("mouse_leave", lambda evt: print("leave"))
        self.bind("mouse_motion", lambda evt: print("motion"))"""

        #self.bind("mouse_pressed", lambda evt: print("pressed"))
        self.bind("mouse_released", self._click)

    def _click(self, evt) -> None:
        """Check click event (not pressed).

        判断点击事件，而非按下事件。

        :return: None
        """
        if self.is_mouse_enter:
            self.event_generate("click", evt)

    def draw(self, canvas, rect) -> None:
        """Draw button.

        * canvas: skia.Surface to draw on
        * rect: Rectangle to draw in
        """

        from ..style.color import color

        if self.is_mouse_enter:
            if self.is_mouse_pressed:
                sheets = self.theme.get_theme()[self.winfo_style()]["pressed"]
            else:
                sheets = self.theme.get_theme()[self.winfo_style()]["hover"]
        else:
            if self.focus_get() is self and "focus" in self.theme.get_theme()[self.winfo_style()]:
                sheets = self.theme.get_theme()[self.winfo_style()]["focus"]
            else:
                sheets = self.theme.get_theme()[self.winfo_style()]["rest"]

        radius = self.theme.get_theme()[self.winfo_style()]["radius"]

        # 绘制背景
        import skia
        rect_paint = skia.Paint(
            AntiAlias=True,
            Style=skia.Paint.kStrokeAndFill_Style,
        )

        rect_paint.setColor(color(sheets["bg"]))
        rect_paint.setStrokeWidth(sheets["width"])

        canvas.drawRoundRect(rect, radius, radius, rect_paint)

        # 绘制边框
        rect_paint.setStyle(skia.Paint.kStroke_Style)

        # 绘制阴影
        if "bd_shadow" in sheets:
            if "bd_shadw":
                from .packs import set_drop_shadow
                set_drop_shadow(rect_paint, color(sheets["bd"]))

        # Rainbow Border Effect
        if "bd_shader" in sheets:
            if sheets["bd_shader"] == "rainbow":
                from .packs import set_rainbow_shader
                set_rainbow_shader(rect_paint, rect)

        rect_paint.setColor(color(sheets["bd"]))

        canvas.drawRoundRect(rect, radius, radius, rect_paint)

        # 绘制文本
        from .packs import central_text

        central_text(canvas, self.cget("text"), color(sheets["fg"]), self.winfo_x(), self.winfo_y(), self.winfo_width(), self.winfo_height())

