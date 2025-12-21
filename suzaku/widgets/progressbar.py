import typing

import skia

from .container import SkContainer
from .widget import SkWidget
from ..const import Orient
from ..var import SkIntVar, SkFloatVar


class SkProgressBar(SkWidget):

    def __init__(
        self,
        parent: SkContainer,
        *,
        style: str = "SkProgressBar",
        value: int | float = 50,
        minvalue: int | float = 0,
        maxvalue: int | float = 100,
        state: typing.Literal["normal", "indeterminate"] = "normal",
        variable: SkFloatVar | SkIntVar = None,
        orient: Orient = Orient.HORIZONTAL,
        **kwargs,
    ) -> None:
        super().__init__(parent, style_name=style, **kwargs)

        self.attributes["orient"]: Orient = orient
        self.attributes["minvalue"]: int | float = minvalue
        self.attributes["maxvalue"]: int | float = maxvalue
        self.attributes["state"]: typing.Literal["normal", "indeterminate"] = state
        self.attributes["variable"]: SkFloatVar | SkIntVar = variable
        if variable:
            self.attributes["value"] = variable.get()
            variable.bind("change", lambda _: self.configure(value=variable.get()))
        else:
            self.attributes["value"]: int | float = value

    def set_attribute(self, **kwargs):
        if "value" in kwargs:
            raw_value = kwargs.pop("value")
            min_value = self.attributes.get("minvalue", 0)
            max_value = self.attributes.get("maxvalue", 100)
            aligned_value = max(min_value, min(max_value, raw_value))
            self.attributes["value"] = aligned_value
            if self.attributes["variable"] is not None:
                self.attributes["variable"].set(aligned_value)
        return super().set_attribute(**kwargs)

    config = configure = set_attribute

    @property
    def percent(self):
        return self.cget("value") / (self.cget("maxvalue") - self.cget("minvalue"))

    @percent.setter
    def percent(self, value: float):
        self.configure(
            value=self.cget("minvalue") + (self.cget("maxvalue") - self.cget("minvalue")) * value
        )

    def draw_widget(self, canvas: skia.Canvas, rect: skia.Rect) -> None:
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
                    bd_shadow=self._style2(self.theme, rail_selector, "bd_shadow"),
                )

        # Progress进度条
        if self.cget("value") > self.cget("minvalue"):
            progress_selector = self.style_name + ".Progress"
            progress_half_size = self._style2(self.theme, progress_selector, "size", 0) / 2
            if progress_half_size > 0:
                progress_rect = skia.Rect.MakeXYWH(
                    rect.x(),
                    rect.centerY() - progress_half_size,
                    rect.width() * self.percent,
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
                        bd_shadow=self._style2(self.theme, progress_selector, "bd_shadow"),
                    )
