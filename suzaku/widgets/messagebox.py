from .window import SkWindow
from .text import SkText


ACTION_OK = "ok"


class SkMessageBox(SkWindow):
    def __init__(  # 修正拼写错误：__int__ -> __init__
        self,
        parent=None,
        *,
        message: str = "",
        actions: tuple[str] = (),  # 修正：list -> None 并默认空列表
        **kwargs,
    ):
        super().__init__(parent, **kwargs)  # 使用 super() 更规范
        self.attributes["message"] = message

        self.message = SkText(self, self.cget("message"))
        self.message.box(side="top", expand=True)

        self.actions = actions

        for action in self.actions:
            pass


def show_message(
    parent=None, message: str = "message", title: str = "Message", **kwargs
):
    window = SkMessageBox(parent, message=message, title=title, **kwargs)
    return window
