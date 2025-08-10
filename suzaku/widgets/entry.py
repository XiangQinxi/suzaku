from time import time

import skia
from glfw import KEY_BACKSPACE, KEY_DELETE, KEY_LEFT, KEY_RIGHT

from ..event import SkEvent
from ..styles.color_old import color
from ..styles.font import default_font
from ..var import SkVar
from .widget import SkWidget


class SkEntry(SkWidget):
    """
    输入框组件
    """

    def __init__(
        self,
        *args,
        placeholder: str = "",
        size=(105, 35),
        cursor="ibeam",
        textvariable: SkVar = None,
        **kwargs,
    ) -> None:
        """Entry box component.

        :param args: SkVisual arguments
        :param placeholder: Placeholder text
        :param size: Default size
        :param cursor: Cursor styles when hovering
        :param style: Style name
        :param id: Optional ID code
        :param textvariable: Optional variable for binding text content
        :param kwargs: SkVisual arguments
        """

        super().__init__(*args, size=size, cursor=cursor, **kwargs)

        self.attributes["right_margin"] = 20

        self.bind("click", self._on_click)
        self.attributes["placeholder"] = placeholder
        self.attributes["cursor_pos"] = 0
        self.attributes["scroll_offset"] = 0
        self.attributes["textvariable"] = textvariable
        if textvariable is not None:
            self.attributes["text"] = textvariable.get()
            textvariable.bind("change", self._textvariable)
        else:
            self.attributes["text"] = ""

        # 光标闪烁相关属性
        self.attributes["cursor_visible"] = True  # 光标是否可见
        self.attributes["blink_interval"] = 500  # 闪烁间隔 (毫秒)
        self.attributes["last_blink_time"] = 0  # 上次闪烁时间戳
        self.focusable = True

        self.bind("key_pressed", self._key)
        self.bind("key_repeated", self._key)
        self.bind("char", self._char)
        self.bind("focus_gain", self._on_focus)

    def _textvariable(self, evt):
        self.attributes["text"] = self.attributes["textvariable"].get()

    def _key(self, evt: SkEvent):
        if self.attributes["textvariable"] is not None:
            text = self.attributes["textvariable"].get()
        else:
            text = self.attributes["text"]
        cursor_pos = self.attributes["cursor_pos"]

        if evt.key == KEY_BACKSPACE:
            if cursor_pos > 0:
                # 在光标位置删除字符

                if self.attributes["textvariable"] is not None:
                    self.attributes["textvariable"].set(
                        text[: cursor_pos - 1] + text[cursor_pos:]
                    )
                else:
                    self.attributes["text"] = text[: cursor_pos - 1] + text[cursor_pos:]

                self.attributes["cursor_pos"] = max(0, cursor_pos - 1)
                self._update_scroll_offset()
        elif evt.key == KEY_DELETE:
            if cursor_pos < len(text):
                # 删除光标后的字符
                if self.attributes["textvariable"] is not None:
                    self.attributes["textvariable"].set(
                        text[:cursor_pos] + text[cursor_pos + 1 :]
                    )
                else:
                    self.attributes["text"] = text[:cursor_pos] + text[cursor_pos + 1 :]
                self._update_scroll_offset()
        elif evt.key == KEY_LEFT:
            # 左箭头移动光标
            self.attributes["cursor_pos"] = max(0, cursor_pos - 1)
            self._update_scroll_offset()
        elif evt.key == KEY_RIGHT:
            # 右箭头移动光标
            self.attributes["cursor_pos"] = min(len(text), cursor_pos + 1)
            self._update_scroll_offset()

    def _char(self, evt):
        if self.attributes["textvariable"] is not None:
            text = self.attributes["textvariable"].get()
        else:
            text = self.attributes["text"]
        cursor_pos = self.attributes["cursor_pos"]
        # 在光标位置插入字符
        if self.attributes["textvariable"] is not None:
            self.attributes["textvariable"].set(
                text[:cursor_pos] + evt.char + text[cursor_pos:]
            )
        else:
            self.attributes["text"] = text[:cursor_pos] + evt.char + text[cursor_pos:]
        self.attributes["cursor_pos"] = cursor_pos + 1
        self._update_scroll_offset()

    def _on_click(self, evt):
        """Handle mouse click event to set cursor position."""
        if not self.is_focus:
            # 如果当前没有焦点，先获取焦点
            self._on_focus()
            return

        # 获取当前状态的样式
        if self.is_focus:
            sheets = self.styles["SkEntry"]["focus"]
        elif self.is_mouse_floating:
            sheets = self.styles["SkEntry"]["hover"]
        else:
            sheets = self.styles["SkEntry"]["rest"]

        # 获取点击位置相对于输入框的坐标
        x = evt.x - self.x - sheets["width"] * 2
        y = evt.y - self.y

        # 考虑滚动偏移
        x += self.attributes["scroll_offset"]

        # 获取文本内容
        if self.attributes["textvariable"] is not None:
            text = self.attributes["textvariable"].get()
        else:
            text = self.attributes["text"]

        font = default_font
        cursor_pos = 0

        # 计算点击位置对应的字符索引
        if text:
            # 使用二进制搜索找到最接近点击位置的字符
            left, right = 0, len(text)
            while left < right:
                mid = (left + right) // 2
                width = font.measureText(text[:mid])
                if width < x:
                    left = mid + 1
                else:
                    right = mid
            cursor_pos = left
        else:
            cursor_pos = 0

        # 设置光标位置
        self.attributes["cursor_pos"] = cursor_pos
        self._update_scroll_offset()

    def _on_focus(self, evt=None):
        """Handle focus in event and reset display state."""
        # 重置滚动偏移
        self.attributes["scroll_offset"] = 0
        # 重置光标位置到文本开头
        if evt is None or not hasattr(evt, "x"):
            self.attributes["cursor_pos"] = 0
        # 重置光标闪烁状态
        self.attributes["cursor_visible"] = True
        self.attributes["last_blink_time"] = time() * 1000

    def _update_scroll_offset(self):
        """更新滚动偏移量，确保光标可见"""
        font = default_font
        if self.attributes["textvariable"] is not None:
            text = self.attributes["textvariable"].get()
        else:
            text = self.attributes["text"]
        cursor_pos = self.attributes["cursor_pos"]

        # 计算光标位置的x坐标
        cursor_x = font.measureText(text[:cursor_pos])

        # 获取输入框的可用宽度
        sheets = self.theme.styles["SkEntry"]["rest"]
        available_width = self.width - 2 * sheets["width"]

        # 调整滚动偏移
        if cursor_x - self.attributes["scroll_offset"] > available_width:
            self.attributes["scroll_offset"] = cursor_x - available_width
        elif cursor_x < self.attributes["scroll_offset"]:
            self.attributes["scroll_offset"] = cursor_x

        # 确保光标可见
        self.attributes["cursor_visible"] = True
        # 重置闪烁时间
        self.attributes["last_blink_time"] = time() * 1000

    def _draw(self, canvas, rect) -> None:
        """
        Draw the entry widget.

        :param canvas: skia.Surface
        :param rect: skia.Rect
        :return:
        """

        if self.is_mouse_floating:
            if self.is_focus:
                sheets = self.styles["SkEntry"]["focus"]
            else:
                sheets = self.styles["SkEntry"]["hover"]
        elif self.is_focus:
            sheets = self.styles["SkEntry"]["focus"]
        else:
            sheets = self.styles["SkEntry"]["rest"]

        if "bd_shadow" in sheets:
            bd_shadow = sheets["bd_shadow"]
        else:
            bd_shadow = False

        if "bd_shader" in sheets:
            bd_shader = sheets["bd_shader"]
        else:
            bd_shader = None

        self._draw_frame(
            canvas,
            rect,
            radius=self.styles["SkEntry"]["radius"],
            bg=sheets["bg"],
            width=sheets["width"],
            bd=sheets["bd"],
            bd_shadow=bd_shadow,
            bd_shader=bd_shader,
        )

        # Draw text.
        # 绘制文本。
        text_paint = skia.Paint(AntiAlias=True, Color=color(sheets["fg"]))

        font = default_font

        metrics = font.getMetrics()

        # Calculate text drawing position (relative to rect)
        # 计算文本绘制位置（相对于rect）
        padding = sheets["width"] * 2
        draw_x = rect.left() + padding
        draw_y = (
            rect.top() + rect.height() / 2 - (metrics.fAscent + metrics.fDescent) / 2
        )

        # Text visible area width
        # 文本可见区域宽度
        visible_width = rect.width() - 2 * padding

        if self.attributes["textvariable"] is not None:
            text = self.attributes["textvariable"].get()
        else:
            text = self.attributes["text"]
        cursor_pos = self.attributes["cursor_pos"]
        scroll_offset = self.attributes["scroll_offset"]

        # Save canvas state and set crop area
        # 保存画布状态并设置裁剪区域
        canvas.save()
        canvas.clipRect(
            skia.Rect.MakeLTRB(
                rect.left() + padding, rect.top(), rect.right() - padding, rect.bottom()
            )
        )

        if not self.is_focus:
            if self.attributes["placeholder"] and not text:
                if "placeholder" in sheets:
                    text_paint.setColor(color(sheets["placeholder"]))
                canvas.drawSimpleText(
                    self.attributes["placeholder"], draw_x, draw_y, font, text_paint
                )
            else:
                # Drawing text (considering scrolling and cropping)
                # 绘制文本（考虑滚动和裁剪）
                canvas.drawSimpleText(
                    text, draw_x - scroll_offset, draw_y, font, text_paint
                )
        else:
            # Drawing text (considering scrolling and cropping)
            # 绘制文本（考虑滚动和裁剪）
            canvas.drawSimpleText(
                text, draw_x - scroll_offset, draw_y, font, text_paint
            )

            # Calculate cursor position
            # 计算光标位置
            cursor_x = font.measureText(text[:cursor_pos])
            # 确保光标在可见区域内
            if cursor_x - scroll_offset > visible_width:
                # 如果光标超出可见区域右侧，调整滚动偏移
                self.attributes["scroll_offset"] = (
                    cursor_x - visible_width + 5
                )  # 加5像素的边距
                scroll_offset = self.attributes["scroll_offset"]
            elif cursor_x - scroll_offset < 0:
                # 如果光标超出可见区域左侧，调整滚动偏移
                self.attributes["scroll_offset"] = max(0, cursor_x - 5)  # 加5像素的边距
                scroll_offset = self.attributes["scroll_offset"]

            # Draw the cursor.
            # 更新光标闪烁状态
            current_time = time() * 1000
            if (
                current_time - self.attributes["last_blink_time"]
                >= self.attributes["blink_interval"]
            ):
                # Switch the cursor visibility.
                # 切换光标可见性
                self.attributes["cursor_visible"] = not self.attributes[
                    "cursor_visible"
                ]
                self.attributes["last_blink_time"] = current_time

            # Draw the cursor only when it is visible.
            # 只在光标可见时绘制光标
            if self.attributes["cursor_visible"]:
                canvas.drawSimpleText(
                    "|", draw_x + cursor_x - scroll_offset, draw_y, font, text_paint
                )

        # Restore canvas state
        canvas.restore()

    def get(self):
        if self.attributes["textvariable"] is not None:
            return self.attributes["textvariable"].get()
        else:
            return self.attributes["text"]
