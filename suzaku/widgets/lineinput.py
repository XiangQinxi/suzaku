"""
text为总文本
cursor_index为在text中的光标索引
visible_start_index为可显文本向左移动的长度

如何计算呢显示光标的位置呢？
！！！计算text[:cursor_index]长度，减去text[visible_start_index:]

xxxxxx|xxxxxxx|xxxx

"""

from typing import Self

import glfw
import skia

from ..event import SkEvent
from ..styles.color import make_color, style_to_color
from ..var import SkStringVar
from .widget import SkWidget


class SkLineInput(SkWidget):
    """A single-line input box without border 【不带边框的单行输入框】"""

    # region Init 初始化

    def __init__(
        self,
        *args,
        size: tuple[int, int] = (105, 35),
        text: str = "",
        textvariable: SkStringVar | None = None,
        placeholder: str | None = None,
        cursor="ibeam",
        **kwargs,
    ) -> None:
        """Text input widget

        :param text: 初始文本
        :param textvariable: 绑定的字符串变量
        :param placeholder: 占位符
        :param cursor: 光标样式
        """
        super().__init__(*args, size=size, cursor=cursor, **kwargs)
        self.attributes["text"] = text
        self.attributes["textvariable"]: SkStringVar = textvariable
        self.attributes["placeholder"] = placeholder  # 占位文本
        self._cursor_index = 0  # 光标索引
        self.visible_start_index = 0  # 文本可显的初始索引（文本向左移的索引）
        self._left = 0  # 文本左边离画布的距离
        self._right = 0  # 文本右边离画布的距离

        self.cursor_visible = True  # 文本光标是否可显
        self.attributes["blink_interval"] = 0.5  # 闪烁间隔 (毫秒)

        def blink(_=None):
            self.cursor_visible = not self.cursor_visible
            self.after(self.cget("blink_interval"), blink)

        blink()

        self.textvariable = textvariable

        self.focusable = True

        self.bind("char", self._char)
        self.bind("key_pressed", self._key)
        self.bind("key_repeated", self._key)
        self.bind("mouse_pressed", self._pressed)

    # endregion

    # region Text&Cursor 文本、光标操作

    def _pressed(self, event: SkEvent):
        canvas_mouse_x = event.x
        canvas_left = self._left + self.canvas_x
        canvas_right = self._right + self.canvas_x
        if canvas_mouse_x >= canvas_right:
            self.cursor_end()
        elif canvas_mouse_x <= canvas_left:
            self.cursor_home()
        else:
            # for item in self.get():
            pass

    def _char(self, event: SkEvent):
        """Triggered when input text is entered."""
        cursor_index = self._cursor_index
        text = self.get()

        self.set(text[:cursor_index] + event.char + text[cursor_index:])
        self.cursor_right()

    def _key(self, event: SkEvent):
        """Key event 按键事件触发

        :param event:
        :return:
        """

        text = self.get()
        key = event.key

        match key:
            case glfw.KEY_BACKSPACE:
                """Delete the text before the cursor"""
                self.cursor_backspace()
            case glfw.KEY_LEFT:
                """Move the cursor to the left"""
                self.cursor_left()
            case glfw.KEY_RIGHT:
                """Move the cursor to the right"""
                self.cursor_right()
            case glfw.KEY_V:
                """Paste Text"""
                if event.mods == "control":
                    if isinstance(self.clipboard(), str):
                        self.set(
                            text[: self._cursor_index]
                            + self.clipboard()
                            + text[self._cursor_index :]
                        )
                        self.cursor_right(len(self.clipboard()))
            case glfw.KEY_HOME:
                """Move the cursor to the start"""
                self.cursor_home()
            case glfw.KEY_END:
                """Move the cursor to the end"""
                self.cursor_end()
        self._update()

    def _update(self):
        text = self.get()

    def get(self) -> str:
        """Get the input text"""
        if self.attributes["textvariable"]:
            return self.attributes["textvariable"].get()
        else:
            return self.attributes["text"]

    def set(self, text) -> Self:
        """Set the input text"""
        if self.attributes["textvariable"]:
            self.attributes["textvariable"].set(text)
        else:
            self.attributes["text"] = text
        return self

    def cursor_index(self, index: int | None = None) -> Self | int:
        """Set cursor index"""
        if index:
            self._cursor_index = index
        else:
            return self._cursor_index
        return self

    def cursor_left(self, move: int = 1) -> Self:
        """Move the cursor to the left"""
        if self.cursor_index() > 0:
            self._cursor_index -= move
            # 光标向左移动时，若文本可显的初始索引大于等于光标索引，且文本可显的初始索引不为0
            if (
                self.visible_start_index >= self.cursor_index()
                and self.visible_start_index != 0
            ):
                self.visible_start_index -= move

        return self

    def cursor_right(self, move: int = 1) -> Self:
        """Move the cursor to the right"""
        if self.cursor_index() < len(self.get()):
            self._cursor_index += move
            if (
                self.measure_text(
                    self.get()[
                        self.visible_start_index : self.cursor_index()
                    ]  # 光标左边的可显文本
                )
                + self.padding
                >= self.width - self.padding
            ):
                self.visible_start_index += move
        return self

    def cursor_backspace(self) -> Self:
        """Delete the text before the cursor"""
        if self.cursor_index() > 0:
            self.set(
                self.get()[: self.cursor_index() - 1]
                + self.get()[self.cursor_index() :]
            )
            self.cursor_left()
        return self

    def cursor_home(self) -> Self:
        """Move the cursor to the start"""
        self._cursor_index = 0
        return self

    def cursor_end(self) -> Self:
        """Move the cursor to the end"""
        self._cursor_index = len(self.get())
        return self

    # endregion

    def _draw_text_input(
        self, canvas: skia.Canvas, rect: skia.Rect, fg, placeholder
    ) -> None:
        """Draw the text input"""

        # Draw text
        font: skia.Font = self.attributes["font"]

        # Define the display area for text to prevent overflow
        # 【划定文本可以显示的区域，防止文本超出显示】

        self.padding = 10

        canvas.save()
        canvas.clipRect(
            skia.Rect.MakeLTRB(
                rect.left() + self.padding - 2,
                rect.top(),
                rect.right() - self.padding + 2,
                rect.bottom(),
            )
        )

        text = self.get()

        if text:
            # Draw the text
            self._draw_text(
                canvas=canvas,
                text=text[self.visible_start_index :],
                font=font,
                fg=fg,
                align="left",
                padding=self.padding,
                canvas_x=self.canvas_x,
                canvas_y=self.canvas_y,
                width=self.width,
                height=self.height,
            )
            self._left = round(rect.left() + self.padding)
            # 如何计算右边的呢！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
            # 左边缘加上可显文本索引后面文字的长度
            self._right = round(
                self._left + self.measure_text(text[self.visible_start_index :])
            )
        metrics = self.metrics

        if self.is_focus:
            if self.cursor_visible:
                # 计算text[:cursor_index]长度，减去text[visible_start_index:]
                # Draw the cursor
                cursor_x = (
                    rect.left()
                    + self.padding
                    + self.measure_text(
                        text[
                            self.visible_start_index : self.cursor_index()
                        ]  # 光标左边的可显文本
                    )
                )
                draw_y = (
                    rect.top()
                    + rect.height() / 2
                    - (metrics.fAscent + metrics.fDescent) / 2
                )
                canvas.drawLine(
                    x0=cursor_x,
                    y0=draw_y + metrics.fAscent,
                    x1=cursor_x,
                    y1=draw_y + metrics.fDescent,
                    paint=skia.Paint(
                        AntiAlias=False,
                        Color=style_to_color(fg, self.theme).color,
                        StrokeWidth=1.5,
                    ),
                )
        else:
            # Draw the placeholder
            if self.attributes["placeholder"] and not text:
                self._draw_text(
                    canvas=canvas,
                    text=self.attributes["placeholder"],
                    fg=placeholder,
                    font=font,
                    align="left",
                    padding=self.padding,
                    canvas_x=self.canvas_x,
                    canvas_y=self.canvas_y,
                    width=self.width,
                    height=self.height,
                )

        canvas.restore()
