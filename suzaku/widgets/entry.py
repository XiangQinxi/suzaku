from time import time

import skia
from glfw import KEY_BACKSPACE, KEY_DELETE, KEY_LEFT, KEY_RIGHT

from suzaku.base import Event, Var
from suzaku.styles.font import default_font

from ..styles.color import color
from .visual import SkVisual


class SkEntry(SkVisual):

    """
    输入框组件
    """

    def __init__(self, *args, placeholder: str = "", size=(105, 35), cursor="ibeam", style="SkEntry", id=None, textvariable: Var = None, **kwargs) -> None:
        """Entry box component.

        * *args: SkVisual arguments
        * placeholder: Placeholder text
        * size: Default size
        * cursor: Cursor styles when hovering
        * styles: Style name
        * id: Optional ID code
        * textvariable: Optional variable for binding text content
        * **kwargs: SkVisual arguments
        """

        super().__init__(*args, size=size, style=style, name="sk_entry", id=id, **kwargs)

        self.visual_attr["right_margin"] = 20

        self.evts["click"] = []
        self.visual_attr["placeholder"] = placeholder
        self.visual_attr["cursor_pos"] = 0
        self.visual_attr["scroll_offset"] = 0
        self.visual_attr["cursor"] = cursor
        self.visual_attr["textvariable"] = textvariable
        if textvariable is not None:
            self.visual_attr["text"] = textvariable.get()
            textvariable.bind("change", self._textvariable)
        else:
            self.visual_attr["text"] = ""

        # 光标闪烁相关属性
        self.visual_attr["cursor_visible"] = True  # 光标是否可见
        self.visual_attr["blink_interval"] = 500  # 闪烁间隔 (毫秒)
        self.visual_attr["last_blink_time"] = 0  # 上次闪烁时间戳

        self.bind("key_press", self._key)
        self.bind("key_repeat", self._key)
        self.bind("char", self._char)
        self.bind("focus_in", self._on_focus)

    def _textvariable(self, evt):
        self.visual_attr["text"] = self.visual_attr["textvariable"].get()

    def _key(self, evt: Event):
        if self.visual_attr["textvariable"] is not None:
            text = self.visual_attr["textvariable"].get()
        else:
            text = self.visual_attr["text"]
        cursor_pos = self.visual_attr["cursor_pos"]

        if evt.key == KEY_BACKSPACE:
            if cursor_pos > 0:
                # 在光标位置删除字符

                if self.visual_attr["textvariable"] is not None:
                    self.visual_attr["textvariable"].set(text[:cursor_pos-1] + text[cursor_pos:])
                else:
                    self.visual_attr["text"] = text[:cursor_pos - 1] + text[cursor_pos:]

                self.visual_attr["cursor_pos"] = max(0, cursor_pos - 1)
                self._update_scroll_offset()
        elif evt.key == KEY_DELETE:
            if cursor_pos < len(text):
                # 删除光标后的字符
                if self.visual_attr["textvariable"] is not None:
                    self.visual_attr["textvariable"].set(text[:cursor_pos] + text[cursor_pos+1:])
                else:
                    self.visual_attr["text"] = text[:cursor_pos] + text[cursor_pos+1:]
                self._update_scroll_offset()
        elif evt.key == KEY_LEFT:
            # 左箭头移动光标
            self.visual_attr["cursor_pos"] = max(0, cursor_pos - 1)
            self._update_scroll_offset()
        elif evt.key == KEY_RIGHT:
            # 右箭头移动光标
            self.visual_attr["cursor_pos"] = min(len(text), cursor_pos + 1)
            self._update_scroll_offset()

    def _char(self, evt):
        if self.visual_attr["textvariable"] is not None:
            text = self.visual_attr["textvariable"].get()
        else:
            text = self.visual_attr["text"]
        cursor_pos = self.visual_attr["cursor_pos"]
        # 在光标位置插入字符
        if self.visual_attr["textvariable"] is not None:
            self.visual_attr["textvariable"].set(text[:cursor_pos] + evt.char + text[cursor_pos:])
        else:
            self.visual_attr["text"] = text[:cursor_pos] + evt.char + text[cursor_pos:]
        self.visual_attr["cursor_pos"] = cursor_pos + 1
        self._update_scroll_offset()

    def _on_focus(self, evt=None):
        """Handle focus in event and reset display state."""
        # 重置滚动偏移
        self.visual_attr["scroll_offset"] = 0
        # 重置光标位置到文本开头
        self.visual_attr["cursor_pos"] = 0
        # 重置光标闪烁状态
        self.visual_attr["cursor_visible"] = True
        self.visual_attr["last_blink_time"] = time() * 1000

    def _update_scroll_offset(self):
        """更新滚动偏移量，确保光标可见"""
        font = default_font()
        if self.visual_attr["textvariable"] is not None:
            text = self.visual_attr["textvariable"].get()
        else:
            text = self.visual_attr["text"]
        cursor_pos = self.visual_attr["cursor_pos"]

        # 计算光标位置的x坐标
        cursor_x = font.measureText(text[:cursor_pos])

        # 获取输入框的可用宽度
        sheets = self.theme.get_theme()[self.winfo_style()]["rest"]
        available_width = self.winfo_width() - 2 * sheets["width"]

        # 调整滚动偏移
        if cursor_x - self.visual_attr["scroll_offset"] > available_width:
            self.visual_attr["scroll_offset"] = cursor_x - available_width
        elif cursor_x < self.visual_attr["scroll_offset"]:
            self.visual_attr["scroll_offset"] = cursor_x

        # 确保光标可见
        self.visual_attr["cursor_visible"] = True
        # 重置闪烁时间
        self.visual_attr["last_blink_time"] = time() * 1000

    def draw(self, canvas, rect) -> None:
        """
        绘制输入框方法。

        :param canvas: 传入的skia.Surface
        :param rect: 给出的矩形
        :return:
        """
        rect_paint = skia.Paint(
            AntiAlias=True,
            Style=skia.Paint.kStrokeAndFill_Style,
        )


        if self.is_mouse_enter:
            if self.is_focus:
                sheets = self.theme.get_theme()[self.winfo_style()]["focus"]
            else:
                sheets = self.theme.get_theme()[self.winfo_style()]["hover"]
        elif self.is_focus:
            sheets = self.theme.get_theme()[self.winfo_style()]["focus"]
        else:
            sheets = self.theme.get_theme()[self.winfo_style()]["rest"]

        # 绘制背景
        radius = self.theme.get_theme()[self.winfo_style()]["radius"]
        rect_paint.setColor(color(sheets["bg"]))
        rect_paint.setStrokeWidth(sheets["width"])

        canvas.drawRoundRect(rect, radius, radius, rect_paint)

        # 绘制边框
        rect_paint.setStyle(skia.Paint.kStroke_Style)

        # 绘制阴影
        if "bd_shadow" in sheets:
            if "bd_shadw":
                from suzaku.base.drawbase import set_drop_shadow
                set_drop_shadow(rect_paint, color(sheets["bd"]))

        # Rainbow Border Effect
        if "bd_shader" in sheets:
            if sheets["bd_shader"] == "rainbow":
                from suzaku.base.drawbase import set_rainbow_shader
                set_rainbow_shader(rect_paint, rect)

        rect_paint.setColor(color(sheets["bd"]))

        canvas.drawRoundRect(rect, radius, radius, rect_paint)

        # 绘制文本
        text_paint = skia.Paint(
            AntiAlias=True,
            Color=color(sheets["fg"])
        )

        font = default_font()

        metrics = font.getMetrics()

        # 计算文本绘制位置（相对于rect）
        padding = sheets["width"] * 2
        draw_x = rect.left() + padding
        draw_y = rect.top() + rect.height() / 2 - (metrics.fAscent + metrics.fDescent) / 2

        # 文本可见区域宽度
        visible_width = rect.width() - 2 * padding

        if self.visual_attr["textvariable"] is not None:
            text = self.visual_attr["textvariable"].get()
        else:
            text = self.visual_attr["text"]
        cursor_pos = self.visual_attr["cursor_pos"]
        scroll_offset = self.visual_attr["scroll_offset"]

        # 保存画布状态并设置裁剪区域
        canvas.save()
        canvas.clipRect(skia.Rect.MakeLTRB(
            rect.left() + padding,
            rect.top(),
            rect.right() - padding,
            rect.bottom()
        ))

        if not self.is_focus:
            if self.visual_attr["placeholder"] and not text:
                if "placeholder" in sheets:
                    text_paint.setColor(color(sheets["placeholder"]))
                canvas.drawSimpleText(self.visual_attr["placeholder"], draw_x, draw_y, font, text_paint)
            else:
                # 绘制文本（考虑滚动和裁剪）
                canvas.drawSimpleText(text, draw_x - scroll_offset, draw_y, font, text_paint)
        else:
            # 绘制文本（考虑滚动和裁剪）
            canvas.drawSimpleText(text, draw_x - scroll_offset, draw_y, font, text_paint)

            # 计算光标位置
            cursor_x = font.measureText(text[:cursor_pos])
            # 确保光标在可见区域内
            if cursor_x - scroll_offset > visible_width:
                # 如果光标超出可见区域右侧，调整滚动偏移
                self.visual_attr["scroll_offset"] = cursor_x - visible_width + 5  # 加5像素的边距
                scroll_offset = self.visual_attr["scroll_offset"]
            elif cursor_x - scroll_offset < 0:
                # 如果光标超出可见区域左侧，调整滚动偏移
                self.visual_attr["scroll_offset"] = max(0, cursor_x - 5)  # 加5像素的边距
                scroll_offset = self.visual_attr["scroll_offset"]

            # 更新光标闪烁状态
            current_time = time() * 1000
            if current_time - self.visual_attr["last_blink_time"] >= self.visual_attr["blink_interval"]:
                # 切换光标可见性
                self.visual_attr["cursor_visible"] = not self.visual_attr["cursor_visible"]
                self.visual_attr["last_blink_time"] = current_time

            # 只在光标可见时绘制
            if self.visual_attr["cursor_visible"]:
                canvas.drawSimpleText("|", draw_x + cursor_x - scroll_offset, draw_y, font, text_paint)

        # 恢复画布状态
        canvas.restore()

    def get(self):
        if self.visual_attr["textvariable"] is not None:
            return self.visual_attr["textvariable"].get()
        else:
            return self.visual_attr["text"]
