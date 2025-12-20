import skia

from ..const import Orient
from ..event import SkEvent
from .widget import SkWidget


class SkSlider(SkWidget):

    def __init__(
        self,
        parent,
        *,
        orient: Orient = Orient.HORIZONTAL,
        tick: int | float | None = None,  # 自动吸附
        value: int | float = 50,
        minvalue: int | float = 0,
        maxvalue: int | float = 100,
        style: str = "SkSlider",
        **kwargs,
    ):
        super().__init__(parent, style_name=style, **kwargs)

        def record_mouse_pos(event: SkEvent):
            if self._pressing:
                self._x1 = event["x"]
                self.update(redraw=True)

        def record_mouse_pressing(event: SkEvent):
            self._pressing = True
            self._x1 = event["x"]

        def record_mouse_released(event: SkEvent):
            if self._pressing:
                self._pressing = False
                self.trigger("changed", SkEvent(self, event_type="changed"))
                self.update(True)

        self.help_parent_scroll = True
        self.focusable = True
        self._x1 = None
        self._pressing = False
        self.bind("mouse_motion", lambda event: self.update(True))
        self.bind("mouse_press", record_mouse_pressing)
        self.window.bind("mouse_move", record_mouse_pos)
        self.window.bind("mouse_release", record_mouse_released)

        self.attributes["orient"]: Orient = orient
        self.attributes["tick"]: int | float | None = tick
        self.attributes["value"]: int | float = value
        self.attributes["minvalue"]: int | float = minvalue
        self.attributes["maxvalue"]: int | float = maxvalue

    @property
    def percent(self):
        return self.cget("value") / (self.cget("maxvalue") - self.cget("minvalue"))

    @percent.setter
    def percent(self, value: float):
        self.configure(
            value=self.cget("minvalue") + (self.cget("maxvalue") - self.cget("minvalue")) * value
        )

    def set_attribute(self, **kwargs):
        if "value" in kwargs:
            raw_value = kwargs.pop("value")

            tick = self.attributes.get("tick")
            if tick and tick > 0:
                # 对齐到最近的tick倍数
                aligned_value = round(raw_value / tick) * tick
                # 确保不超出范围
                min_value = self.attributes.get("minvalue", 0)
                max_value = self.attributes.get("maxvalue", 100)
                aligned_value = max(min_value, min(max_value, aligned_value))
                self.attributes["value"] = aligned_value
            else:
                self.attributes["value"] = raw_value

        super().set_attribute(**kwargs)

    config = configure = set_attribute

    def draw_widget(self, canvas: skia.Canvas, rect: skia.Rect) -> None:
        state = self.style_state()

        thumb_selector = f"{self.style_name}.Thumb:{state}"

        size = self._style2(self.theme, thumb_selector, "size", (20, 20))
        thumb_width, thumb_height = size

        # 计算滑块的有效移动范围（考虑滑块宽度）
        thumb_half_width = thumb_width / 2
        min_x = rect.left() + thumb_half_width
        max_x = rect.right() - thumb_half_width

        # 确保滑块移动范围有效
        if min_x >= max_x:
            min_x = max_x = rect.centerX()

        # 处理滑块拖动逻辑
        if self._pressing:
            # 限制x坐标在有效范围内
            x = max(min(self._x1, max_x), min_x)

            # 计算百分比并限制在0-1范围内
            percent = max(0, min(1, (x - min_x) / (max_x - min_x)))

            self.percent = percent

            self.trigger("changing", SkEvent(self, event_type="changing"))

        # 计算滑块位置（基于当前百分比）
        current_percent = self.percent
        x = min_x + (max_x - min_x) * current_percent
        x = max(min(x, max_x), min_x)  # 双重确保不越界

        # Rail轨道
        rail_selector = self.style_name + ".Rail"
        rail_half_size = self._style2(self.theme, rail_selector, "size", 0) / 2
        if rail_half_size > 0:
            rail_rect = skia.Rect.MakeXYWH(
                rect.x(),
                rect.centerY() - rail_half_size,
                rect.width(),
                rail_half_size * 2,
            )

            if rail_rect.height() > 0 and rail_rect.width() > 0:
                self._draw_rect(
                    canvas,
                    rail_rect,
                    self._style2(self.theme, rail_selector, "radius", 0),
                    bg=self._style2(self.theme, rail_selector, "bg", skia.ColorBLACK),
                    bd=self._style2(self.theme, rail_selector, "bd", 0),
                    width=self._style2(self.theme, rail_selector, "width", 0),
                    bd_shader=self._style2(self.theme, rail_selector, "bd_shader"),
                    bd_shadow=self._style2(self.theme, rail_selector, "bd_shadow"),
                    bg_shader=self._style2(self.theme, rail_selector, "bg_shader"),
                )

        # Progress进度条
        if self.cget("value") > self.cget("minvalue"):
            progress_selector = self.style_name + ".Progress"
            progress_half_size = self._style2(self.theme, progress_selector, "size", 0) / 2
            if progress_half_size > 0:
                progress_rect = skia.Rect.MakeXYWH(
                    rect.x(),
                    rect.centerY() - progress_half_size,
                    min(rect.right(), x) - rect.left(),  # 关键：使用x而不是rect.left() + x
                    progress_half_size * 2,
                )

                # 确保进度条矩形有效且不为空
                if progress_rect.width() > 0 and progress_rect.height() > 0:
                    self._draw_rect(
                        canvas,
                        progress_rect,
                        radius=self._style2(self.theme, progress_selector, "radius", 0),
                        bg=self._style2(self.theme, progress_selector, "bg", skia.ColorBLACK),
                        bd=self._style2(self.theme, progress_selector, "bd", 0),
                        width=self._style2(self.theme, progress_selector, "width", 0),
                        bd_shader=self._style2(self.theme, progress_selector, "bd_shader"),
                        bd_shadow=self._style2(self.theme, progress_selector, "bd_shadow"),
                        bg_shader=self._style2(self.theme, progress_selector, "bg_shader"),
                    )

        # Thumb滑块
        thumb_half_height = thumb_height / 2

        thumb_rect = skia.Rect.MakeLTRB(
            max(rect.left(), x - thumb_half_width),
            rect.centerY() - thumb_half_height,
            min(rect.right(), x + thumb_half_width),
            rect.centerY() + thumb_half_height,
        )

        if not thumb_rect.contains(self.window.mouse_x, self.window.mouse_y):
            if state == "hover":
                thumb_selector = f"{self.style_name}.Thumb"
        else:
            if state != "press":
                thumb_selector = f"{self.style_name}.Thumb:hover"

        if thumb_rect.width() > 0 and thumb_rect.height() > 0:
            self._draw_rect(
                canvas,
                thumb_rect,
                self._style2(self.theme, thumb_selector, "radius", 0),
                bg=self._style2(self.theme, thumb_selector, "bg", skia.ColorBLACK),
                bd=self._style2(self.theme, thumb_selector, "bd", 0),
                width=self._style2(self.theme, thumb_selector, "width", 0),
                bd_shader=self._style2(self.theme, thumb_selector, "bd_shader"),
                bd_shadow=self._style2(self.theme, thumb_selector, "bd_shadow"),
                bg_shader=self._style2(self.theme, thumb_selector, "bg_shader"),
            )

        if self._style2(self.theme, thumb_selector, "inner", False):
            size = self._style2(self.theme, thumb_selector, "inner_size", (10, 10))
            inner_thumb_width, inner_thumb_height = size
            inner_thumb_half_width = inner_thumb_width / 2
            inner_thumb_half_height = inner_thumb_height / 2

            inner_thumb_rect = skia.Rect.MakeLTRB(
                max(rect.left(), x - inner_thumb_half_width),
                rect.centerY() - inner_thumb_half_height,
                min(rect.right(), x + inner_thumb_half_width),
                rect.centerY() + inner_thumb_half_height,
            )

            if inner_thumb_rect.width() > 0 and inner_thumb_rect.height() > 0:
                self._draw_rect(
                    canvas,
                    inner_thumb_rect,
                    self._style2(self.theme, thumb_selector, "inner_radius", 0),
                    bg=self._style2(self.theme, thumb_selector, "inner_bg", skia.ColorBLACK),
                    bd=self._style2(self.theme, thumb_selector, "inner_bd", 0),
                    width=self._style2(self.theme, thumb_selector, "inner_width", 0),
                    bd_shader=self._style2(self.theme, thumb_selector, "inner_bd_shader"),
                    bd_shadow=self._style2(self.theme, thumb_selector, "inner_bd_shadow"),
                    bg_shader=self._style2(self.theme, thumb_selector, "inner_bg_shader"),
                )
