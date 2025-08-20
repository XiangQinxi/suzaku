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
        """Text input widget (no border)

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
        """Determine whether the text is selected.
        【判断文本是否被选中】
        :return: bool
        """
        return self.start_index != self.end_index

    def _motion(self, event: SkEvent) -> None:
        """Record the `end_index` when the text is pressed and moved.
        【当文本被按住并移动时，记录end_index】
        :param event: SkEvent
        """
        if self.is_mouse_pressed:
            self.end_index = self.index(event.x)

    def _pressed(self, event: SkEvent) -> None:
        """Record the `start_index` and `end_index` when the text is pressed.
        【当文本被按住时，记录`start_index`与`end_index`。】
        """
        self.start_index = self.end_index = self.index(event.x)

    def _char(self, event: SkEvent):
        """Triggered when input text is entered.
        【当输入框文本输入时触发】
        """
        cursor_index = self._cursor_index
        text = self.get()
        self.cursor_visible = True

        # 当文本未被选中时，正常在文本后添加文本，并更新光标索引
        if not self.is_selected():
            self.set(text[:cursor_index] + event.char + text[cursor_index:])
            self.cursor_right()
        # 当文本被选中时，将选中文本替代为输入的文本
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

        # 快捷键
        match event.key:
            # Backspace 删除光标前面文本
            case glfw.KEY_BACKSPACE:
                """Delete the text before the cursor"""
                self.cursor_backspace()
            # Delete 删除光标后面文本
            case glfw.KEY_DELETE:
                """Delete the text after the cursor"""
                self.cursor_delete()
            # Ctrl + V 粘贴
            case glfw.KEY_V:
                """Paste Text"""
                if event.mods == "control":
                    self.cursor_paste()
            # Ctrl + C 复制
            case glfw.KEY_C:
                if event.mods == "control":
                    self.cursor_copy()
            # Ctrl + A 全选
            case glfw.KEY_A:
                """Select All"""
                if event.mods == "control":
                    self.cursor_select_all()
            # Ctrl + X 剪切
            case glfw.KEY_X:
                """Cut Text"""
                if event.mods == "control":
                    self.cursor_cut()
            # Home ↑ 光标移至最左
            case glfw.KEY_HOME | glfw.KEY_UP:
                """Move the cursor to the start"""
                self.cursor_home()
            # End ↓ 光标移至最有
            case glfw.KEY_END | glfw.KEY_DOWN:
                """Move the cursor to the end"""
                self.cursor_end()
            # Left ← 光标左移
            case glfw.KEY_LEFT:
                """Move the cursor to the left"""
                self.cursor_left()
            # Right → 光标右移
            case glfw.KEY_RIGHT:
                """Move the cursor to the right"""
                self.cursor_right()

    def get(self) -> str:
        """Get the input text
        【获取输入框中文本】
        """
        if self.attributes["textvariable"]:
            return self.attributes["textvariable"].get()
        else:
            return self.attributes["text"]

    def set(self, text) -> Self:
        """Set the input text
        【设置输入框文本】
        """
        if self.attributes["textvariable"]:
            self.attributes["textvariable"].set(text)
        else:
            self.attributes["text"] = text
        return self

    def index(self, mouse_x: int) -> int:
        # 【如果鼠标超出可见文本的范围】
        left = self._rect.left()
        if mouse_x >= left + self._rect.width():
            self.cursor_right(cancel_selected=False)
        # 【如果鼠标超出画出的文本范围】
        if mouse_x >= self._right:
            self.cursor_end()
            return len(self.get())
        # 【如果鼠标超出文本左边的范围】
        if mouse_x <= left:
            if self.visible_start_index == 0:
                self.cursor_home()
                return 0
            # 【如果文本向左滚动了】
            else:
                self.cursor_left(cancel_selected=False)
                return self.visible_start_index
        # 【遍历可见文本，找到鼠标所在的位置】
        visible_text = self.get()[self.visible_start_index :]
        for index, _ in enumerate(visible_text):
            _text = visible_text[:index]
            if self.measure_text(_text) + left >= mouse_x:
                _text2 = len(_text) + self.visible_start_index
                self.cursor_index(_text2)
                return _text2
        return self.cursor_index()

    def check(self):
        if self.visible_start_index >= self.cursor_index() > 0:
            self.visible_start_index = self.cursor_index() - 2
            if self.visible_start_index < 0:
                self.visible_start_index = 0

    def cursor_index(self, index: int | None = None) -> Self | int:
        """Set cursor index
        【设置光标索引】
        """
        if index and isinstance(index, int):
            self._cursor_index = index
        else:
            return self._cursor_index
        return self

    def cursor_left(self, move: int = 1, cancel_selected: bool = True) -> Self:
        """Move the cursor to the left
        【光标左移】

        :param int move: 【光标左移的距离】
        :param bool cancel_selected: 【是否取消光标的选择状态（点击左按键时建议启用）】
        """
        # 【光标在最左的时候不执行接下判断】
        if self.cursor_index() > 0:
            # 【如果文本被选中，则光标向左移动时，光标索引为选中文本的起始索引】
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
            # 【光标向左移动时，若文本可显的初始索引大于等于光标索引，且文本可显的初始索引不为0】
            while (
                self.visible_start_index
                >= self._cursor_index
                - 1  # 【当光标向左移动时，如果光标在可显文本的第二位】
                and self.visible_start_index != 0
            ):
                self.visible_start_index -= move

        return self

    def cursor_right(self, move: int = 1, cancel_selected: bool = True) -> Self:
        """Move the cursor to the right
        【光标右移】

        :param int move: 【光标右移的距离】
        :param bool cancel_selected: 【是否取消光标的选择状态（点击右按键时建议启用）】
        """
        # 【光标在最右的时候不执行接下判断】
        if self.cursor_index() < len(self.get()):
            # 【如果文本被选中，则光标向左移动时，光标索引为选中文本的起始索引】
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
            # 【光标向右移动时，若可显文本到光标大于等于可见文本范围】
            while (
                self.measure_text(
                    self.get()[
                        self.visible_start_index : self.cursor_index()
                    ]  # 【光标左边的可显文本】
                )
                >= self._rect.width()
            ):
                self.visible_start_index += move
        return self

    def delete_selected(self):
        """Delete the selected text
        【删除选择文本】
        """
        if self.is_selected():
            start, end = sorted([self.start_index, self.end_index])
            self.start_index = self.end_index = self._cursor_index = len(
                self.get()[:start]
            )
            self.set(self.get()[:start] + self.get()[end:])
            self.check()

    def cursor_backspace(self) -> Self:
        """Delete the text before the cursor
        【删除光标前的文本】
        """
        if not self.is_selected():
            if self.cursor_index() > 0:
                self.set(
                    self.get()[: self.cursor_index() - 1]
                    + self.get()[self.cursor_index() :]
                )
                self.cursor_left()
        else:
            self.delete_selected()
        return self

    def cursor_delete(self) -> Self:
        """Delete the text after the cursor
        【删除光标后的文本】
        """
        _index = self.cursor_index()
        _text = self.get()
        if not self.is_selected():
            if +1 < len(_text):
                self.set(_text[: _index + 1] + _text[_index + 2 :])
            elif _index == len(_text) - 1:
                self.set(_text[_index + 1 :])
        else:
            self.delete_selected()
        return self

    def cursor_home(self) -> Self:
        """Move the cursor to the start
        【将光标移至最前（左）】
        """
        self._cursor_index = 0
        self.visible_start_index = 0

        return self

    def cursor_end(self) -> Self:
        """Move the cursor to the end
        【将光标移至最后（右）】
        """
        self._cursor_index = len(self.get())
        while (
            self.measure_text(
                self.get()[
                    self.visible_start_index : self.cursor_index()
                ]  # 光标左边的可显文本
            )
            >= self._rect.width()
        ):
            self.visible_start_index += 1
        return self

    def cursor_paste(self):
        """Paste the selected text
        【粘贴文本（如选中文本则覆盖）】
        """
        text = self.get()
        clipboard = self.clipboard()
        # 【检查剪切板是否保存的是文本（而非图片等）】
        if isinstance(clipboard, str):
            # 【如没有选中文本，则在光标后粘贴文本】
            if not self.is_selected():
                self.set(
                    text[: self._cursor_index] + clipboard + text[self._cursor_index :]
                )
                self.cursor_right(len(clipboard))
            # 【如选中文本，则粘贴并覆盖选中文本】
            else:
                start, end = sorted([self.start_index, self.end_index])
                _text = text[:start] + clipboard + text[end:]
                self.set(_text)
                index = start + len(clipboard)
                self.cursor_index(index)
                self.start_index = self.end_index = index

    def cursor_copy(self):
        """Copy the selected text
        【复制选中的文本】
        """
        text = self.get()
        if self.is_selected():
            start, end = sorted([self.start_index, self.end_index])
            self.clipboard(text[start:end])

    def cursor_cut(self):
        """Cut the selected text
        【剪切选择文本】
        """
        if self.is_selected():
            self.cursor_copy()
            self.cursor_backspace()

    def cursor_select_all(self):
        """Select all text
        【全选文本】
        """
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
        radius: int | float = None,
    ) -> None:
        """Draw the text input
        【绘制输入框（不含边框）】
        """

        self._rect = rect

        # 【各可选属性设置】
        fg = skcolor2color(style_to_color(fg, self.theme))  # 【设置文本颜色】
        if bg:
            bg = skcolor2color(style_to_color(bg, self.theme))  # 【设置背景颜色】
        else:
            bg = skia.ColorTRANSPARENT

        if placeholder:
            placeholder = skcolor2color(
                style_to_color(placeholder, self.theme)
            )  # 【设置占位符颜色】
        else:
            placeholder = fg

        if cursor:
            cursor = skcolor2color(style_to_color(cursor, self.theme))  # 设置光标颜色
        else:
            cursor = fg

        if font is None:
            font: skia.Font = self.attributes["font"]

        # Define the display area for text to prevent overflow
        # 【划定文本可以显示的区域，防止文本超出显示】

        canvas.save()
        canvas.clipRect(
            skia.Rect.MakeLTRB(
                rect.left(),
                rect.top(),
                rect.right(),
                rect.bottom(),
            )
        )

        text = self.get()

        # 排序选择文本的起始、终点，使start<=end，不出错
        start, end = sorted([self.start_index, self.end_index])
        _start = start - self.visible_start_index
        # 防止为负数时，输入框消失
        if _start < 0:
            _start = 0
        _end = end - self.visible_start_index

        def draw_with_selected_text():
            # 【绘制文本（带文本选中框）】
            _text = (
                text[self.visible_start_index :],
                {
                    "start": _start,
                    "end": _end,
                    "fg": selected_fg,
                    "bg": selected_bg,
                },
            )
            self._draw_styled_text(
                canvas=canvas,
                rect=self._rect,
                text=_text,
                font=font,
                fg=fg,
                bg=bg,
                radius=radius,
            )

        def draw_text():
            # 【绘制文本（不带文本选中框）】
            _text = text[self.visible_start_index :]
            self._draw_text(
                canvas=canvas,
                rect=self._rect,
                text=_text,
                font=font,
                fg=fg,
                bg=bg,
                align="left",
                radius=radius,
            )

        # Draw the text 【绘制文本呢】
        if text:
            # 【如果选中文本，则使用draw_with_selected_text】
            if self.is_selected():
                if self.is_focus:
                    draw_with_selected_text()
                else:
                    draw_text()
            else:
                draw_text()

            self._right = round(
                self._rect.left() + self.measure_text(text[self.visible_start_index :])
            )  # 文本右边缘

        if self.is_focus:
            # Draw the cursor 【绘制光标】
            if self.cursor_visible:
                # 【计算出的光标位置】
                cursor_x = self._rect.left() + self.measure_text(
                    text[
                        self.visible_start_index : self.cursor_index()
                    ]  # 光标左边的可显文本
                )
                canvas.drawLine(
                    x0=cursor_x,
                    y0=self._rect.top() + 2,
                    x1=cursor_x,
                    y1=self._rect.bottom() - 2,
                    paint=skia.Paint(
                        AntiAlias=False,
                        Color=cursor,
                        StrokeWidth=2,
                    ),
                )
        else:
            # Draw the placeholder 【绘制占位文本】
            if self.attributes["placeholder"] and not text:
                self._draw_text(
                    canvas=canvas,
                    rect=self._rect,
                    text=self.attributes["placeholder"],
                    fg=placeholder,
                    font=font,
                    align="left",
                )

        # 【关闭文本裁剪】
        canvas.restore()
