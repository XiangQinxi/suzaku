import skia

from ..styles.color_old import color
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

        self.textvariable = textvariable

        self.focusable = True

    # endregion

    # region Text&Cursor 文本、光标操作

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
            if self.is_focus:
                ...
        else:
            if self.attributes["placeholder"]:
                text_paint.setColor(color(sheets["placeholder"]))
                canvas.drawSimpleText(
                    self.attributes["placeholder"], draw_x, draw_y, font, text_paint
                )
