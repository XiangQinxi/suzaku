import glfw
import skia

from ..event import SkEvent
from ..styles.color import color
from ..var import SkStringVar
from .widget import SkWidget


class SkTextInput(SkWidget):

    # region Init 初始化

    def __init__(
        self,
        parent: SkWidget,
        *args,
        text: str = "",
        textvariable: SkStringVar | None = None,
        placeholder: str | None = None,
        cursor="ibeam",
        **kwargs,
    ) -> None:
        """
        初始化文本输入框

        :param parent: 父控件
        :param text: 初始文本
        :param textvariable: 绑定的字符串变量
        :param placeholder: 占位符
        :param cursor: 光标样式
        """
        super().__init__(parent, *args, cursor=cursor, **kwargs)
        self.attributes["text"] = text
        self.attributes["textvariable"]: SkStringVar = textvariable
        self.attributes["placeholder"] = placeholder
        self.attributes["cursor_index"] = 0
        self.attributes["visible_start_index"] = 0

        self.textvariable = textvariable

        self.focusable = True

        self.bind("char", self._char)
        self.bind("key", self._key)

    # endregion

    # region Text&Cursor 文本、光标操作

    def _char(self, event: SkEvent):
        cursor_index = self.attributes["cursor_index"]
        text = self.get()

        self.set(text[:cursor_index] + event.char + text[cursor_index:])
        self.attributes["cursor_index"] += 1

    def _key(self, event: SkEvent):
        """Key event 按键事件触发

        :param event:
        :return:
        """

        cursor_index = self.attributes["cursor_index"]
        text = self.get()
        key = event.key

        match key:
            case glfw.KEY_BACKSPACE:
                if cursor_index > 0:
                    self.set(text[: cursor_index - 1] + text[cursor_index:])
            case glfw.KEY_DELETE:
                print(cursor_index, text)
                if cursor_index < len(text):
                    self.set(text[:cursor_index] + text[cursor_index + 1 :])
            case glfw.KEY_LEFT:
                if cursor_index > 0:
                    cursor_index -= 1
            case glfw.KEY_RIGHT:
                if cursor_index < len(text):
                    cursor_index += 1
        self._update()

    def _update(self): ...

    def get(self) -> str:
        if self.attributes["textvariable"]:
            return self.attributes["textvariable"].get()
        else:
            return self.attributes["text"]

    def set(self, text) -> "SkTextInput":
        if self.attributes["textvariable"]:
            self.attributes["textvariable"].set(text)
        else:
            self.attributes["text"] = text
        return self

    def cursor_index(self, index: int) -> "SkTextInput":
        self.attributes["cursor_index"] = index
        return self

    def cursor_left(self) -> "SkTextInput":
        self.attributes["cursor_index"] -= 1
        return self

    def cursor_right(self) -> "SkTextInput":
        self.attributes["cursor_index"] += 1
        return self

    def cursor_home(self) -> "SkTextInput":
        self.attributes["cursor_index"] = 0
        return self

    def cursor_end(self) -> "SkTextInput":
        self.attributes["cursor_index"] = len(self.get())
        return self

    # endregion

    def _draw(self, canvas, rect) -> None:
        sheets = self.styles["SkTextInput"]

        text_paint = skia.Paint(
            AntiAlias=True,
        )
        text_paint.setColor(color(sheets["fg"]))
        # Draw text
        font = self.attributes["font"]
        padding = 2  # sheets["width"] * 2
        metrics = font.getMetrics()
        draw_x = rect.left() + padding
        draw_y = (
            rect.top() + rect.height() / 2 - (metrics.fAscent + metrics.fDescent) / 2
        )

        canvas.save()
        canvas.clipRect(
            skia.Rect.MakeLTRB(
                rect.left() + padding, rect.top(), rect.right() - padding, rect.bottom()
            )
        )

        if self.get():
            canvas.drawSimpleText(self.get(), draw_x, draw_y, font, text_paint)

        if self.is_focus:
            ...
        else:
            if self.attributes["placeholder"] and not self.get():
                text_paint.setColor(color(sheets["placeholder"]))
                canvas.drawSimpleText(
                    self.attributes["placeholder"], draw_x, draw_y, font, text_paint
                )
