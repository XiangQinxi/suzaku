from typing import Union

import skia

from .widget import SkWidget


class SkCheckBox(SkWidget):
    def __init__(
        self,
        *args,
        size=(32, 32),
        cursor: Union[str, None] = "hand",
        command: Union[callable, None] = None,
        selected: bool = False,
        **kwargs,
    ):
        super().__init__(*args, size=size, cursor=cursor, **kwargs)
        self.attributes["selected"] = selected
        self.focusable = True

        if command:
            self.bind("click", lambda _: command())

    def _draw(self, canvas: skia.Canvas, rect: skia.Rect):
        pass
import typing

import skia

from .widget import SkWidget


class SkCheckBox(SkWidget):
    def __init__(
        self,
        *args,
        size=(32, 32),
        cursor: typing.Union[str, None] = "hand",
        command: typing.Union[typing.Callable, None] = None,
        selected: bool = False,
        **kwargs,
    ):
        super().__init__(*args, size=size, cursor=cursor, **kwargs)
        self.attributes["selected"] = selected
        self.focusable = True

        if command:
            self.bind("click", lambda _: command())

    def _draw(self, canvas: skia.Canvas, rect: skia.Rect):
        pass
