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

from .. import SkColor
from ..event import SkEvent
from ..styles.color import skcolor2color, style_to_color
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
        self.start_index = 0
        self.end_index = 0
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
        self.window.bind("mouse_motion", self._motion)
        self.bind("mouse_motion", self._motion)

    # endregion

    # region Text&Cursor 文本、光标操作

    def is_selected(self) -> bool:
        return self.start_index != self.end_index

    def _motion(self, event: SkEvent) -> None:
        if self.is_mouse_pressed:
            self.end_index = self.index(event.x)

    def _pressed(self, event: SkEvent) -> None:
        self.start_index = self.end_index = self.index(event.x)

    def _char(self, event: SkEvent):
        """Triggered when input text is entered."""
        cursor_index = self._cursor_index
        text = self.get()

        if not self.is_selected():
            self.set(text[:cursor_index] + event.char + text[cursor_index:])
            self.cursor_right()
        else:
            start, end = sorted([self.start_index, self.end_index])
            self.set(text[:start] + event.char + text[end:])
            self.start_index = self.end_index = self._cursor_index = len(
                text[:start] + event.char
            )

    def _key(self, event: SkEvent):
        """Key event 按键事件触发

        :param event:
        :return:
        """

        match event.key:
            case glfw.KEY_BACKSPACE | glfw.KEY_DELETE:
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
                    self.cursor_paste()
            case glfw.KEY_C:
                if event.mods == "control":
                    self.cursor_copy()
            case glfw.KEY_A:
                """Select All"""
                if event.mods == "control":
                    self.cursor_select_all()
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

    def index(self, mouse_x: int) -> int:
        # 如果鼠标超出可见文本的范围
        if mouse_x >= self._left + self.width - self.padding * 2:
            self.cursor_right(cancel_selected=False)
        # 如果鼠标超出画出的文本范围
        if mouse_x >= self._right:
            self.cursor_end()
            return len(self.get())
        # 如果鼠标超出文本左边的范围
        elif mouse_x <= self._left:
            if self.visible_start_index == 0:
                self.cursor_home()
                return 0
            else:
                # 如果文本向左滚动了
                self.cursor_left(cancel_selected=False)
                return self.visible_start_index
        # 遍历可见文本，找到鼠标所在的位置
        visible_text = self.get()[self.visible_start_index :]
        for index, _ in enumerate(visible_text):
            _text = visible_text[:index]
            if self.measure_text(_text) + self._left >= mouse_x:
                _text2 = len(_text) + self.visible_start_index
                self.cursor_index(_text2)
                return _text2
                break
        return self.cursor_index()

    def cursor_index(self, index: int | None = None) -> Self | int:
        """Set cursor index"""
        if index and isinstance(index, int):
            self._cursor_index = index
        else:
            return self._cursor_index
        return self

    def cursor_left(self, move: int = 1, cancel_selected: bool = True) -> Self:
        """Move the cursor to the left"""
        if self.cursor_index() > 0:
            # 如果文本被选中，则光标向左移动时，光标索引为选中文本的起始索引
            if cancel_selected:
                if self.is_selected():
                    start, end = self.start_index, self.end_index
                    if end > start:
                        move = end - start
                    else:
                        move = 0
            self._cursor_index -= move
            if cancel_selected:
                self.start_index = self.end_index = self._cursor_index
            else:
                self.end_index = self._cursor_index
            # 光标向左移动时，若文本可显的初始索引大于等于光标索引，且文本可显的初始索引不为0
            if (
                self.visible_start_index
                >= self.cursor_index()
                - 1  # 当光标向左移动时，如果光标在可显文本的第二位
                and self.visible_start_index != 0
            ):
                self.visible_start_index -= move

        return self

    def cursor_right(self, move: int = 1, cancel_selected: bool = True) -> Self:
        """Move the cursor to the right"""
        if self.cursor_index() < len(self.get()):
            if cancel_selected:
                if self.is_selected():
                    start, end = self.start_index, self.end_index
                    if start > end:
                        move = start - end
                    else:
                        move = 0
            self._cursor_index += move
            if cancel_selected:
                self.start_index = self.end_index = self._cursor_index
            else:
                self.end_index = self._cursor_index
            if self._cursor_index >= len(self.get()):
                self.cursor_index(len(self.get()))
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
        if not self.is_selected():
            if self.cursor_index() > 0:
                self.set(
                    self.get()[: self.cursor_index() - 1]
                    + self.get()[self.cursor_index() :]
                )
                self.cursor_left()
        else:
            start, end = sorted([self.start_index, self.end_index])
            self.start_index = self.end_index = self._cursor_index = len(
                self.get()[:start]
            )
            self.set(self.get()[:start] + self.get()[end:])
        return self

    def cursor_home(self) -> Self:
        """Move the cursor to the start"""
        self._cursor_index = 0
        return self

    def cursor_end(self) -> Self:
        """Move the cursor to the end"""
        self._cursor_index = len(self.get())
        return self

    def cursor_paste(self):
        text = self.get()
        if isinstance(self.clipboard(), str):
            if not self.is_selected():
                self.set(
                    text[: self._cursor_index]
                    + self.clipboard()
                    + text[self._cursor_index :]
                )
                self.cursor_right(len(self.clipboard()))
            else:
                clipboard = self.clipboard()
                if isinstance(clipboard, str):
                    start, end = sorted([self.start_index, self.end_index])
                    _text = text[:start] + clipboard + text[end:]
                    self.set(_text)
                    self.cursor_index(len(_text))
                    self.start_index = len(_text)
                    self.end_index = len(_text)

    def cursor_copy(self):
        text = self.get()
        if self.is_selected():
            start, end = sorted([self.start_index, self.end_index])
            self.clipboard(text[start:end])

    def cursor_select_all(self):
        """Select all text"""
        self.start_index = 0
        self._cursor_index = self.end_index = len(self.get())

    # endregion

    def _draw_text_input(
        self,
        canvas: skia.Canvas,
        rect: skia.Rect,
        fg: int | SkColor,
        bg: int | SkColor = None,
        placeholder: int | SkColor = None,
        font: skia.Font = None,
        cursor: int | SkColor = None,
        selected_bg=skia.ColorBLUE,
        selected_fg=skia.ColorWHITE,
    ) -> None:
        """Draw the text input"""

        fg = skcolor2color(style_to_color(fg, self.theme))  # 设置文本颜色
        if bg:
            bg = skcolor2color(style_to_color(bg, self.theme))  # 设置背景颜色
        else:
            bg = skia.ColorTRANSPARENT
        if placeholder:
            placeholder = skcolor2color(
                style_to_color(placeholder, self.theme)
            )  # 设置占位符颜色
        else:
            placeholder = fg
        if cursor:
            cursor = skcolor2color(style_to_color(cursor, self.theme))  # 设置光标颜色
        else:
            cursor = fg
        # 设置文本字体
        if font is None:
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

        # 排序选择文本的起始、终点，使start<=end，不出错
        start, end = sorted([self.start_index, self.end_index])

        def draw_with_seletect_text():
            _text = (
                text[self.visible_start_index :],
                {
                    "start": start - self.visible_start_index,
                    "end": end - self.visible_start_index,
                    "fg": selected_fg,
                    "bg": selected_bg,
                },
            )
            self._draw_styled_text(
                canvas=canvas,
                text=_text,
                font=font,
                fg=fg,
                bg=bg,
                padding=self.padding,
                canvas_x=self.canvas_x,
                canvas_y=self.canvas_y,
                width=self.width,
                height=self.height,
            )

        def draw_text():
            _text = text[self.visible_start_index :]
            self._draw_text(
                canvas=canvas,
                text=_text,
                font=font,
                fg=fg,
                bg=bg,
                align="left",
                padding=self.padding,
                canvas_x=self.canvas_x,
                canvas_y=self.canvas_y,
                width=self.width,
                height=self.height,
            )

        if text:
            # Draw the text
            # 如果有选择文本，则使用特殊样式
            if self.is_selected():
                if self.is_focus:
                    draw_with_seletect_text()
                else:
                    draw_text()
            else:
                draw_text()

            self._left = round(rect.left() + self.padding)  # 文本左边缘
            self._right = round(
                self._left + self.measure_text(text[self.visible_start_index :])
            )  # 文本右边缘

        metrics = self.metrics

        if self.is_focus:
            if self.is_selected():
                pass
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
                    y0=draw_y + metrics.fAscent - self.padding / 4,
                    x1=cursor_x,
                    y1=draw_y + metrics.fDescent + self.padding / 4,
                    paint=skia.Paint(
                        AntiAlias=False,
                        Color=cursor,
                        StrokeWidth=2,
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
