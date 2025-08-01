from .window import SkWindow


class SkAppWindow(SkWindow):

    """
    将SkApp与SkWindow组合起来的主窗口
    """

    def __init__(self, *args, **kwargs) -> None:
        """
        初始化
        """
        from .app import SkApp
        self.app = SkApp()
        super().__init__(parent=self.app, *args, **kwargs)
        self.window_attr["name"] = "sk_appwindow"

    def run(self, *args, **kwargs) -> None:
        """运行应用程序"""
        self.app.run(*args, **kwargs)

    def quit(self, *args, **kwargs) -> None:
        """退出应用程序"""
        self.app.quit(*args, **kwargs)

    from .app import SkApp

    def winfo_app(self) -> SkApp:
        """获取SkApp类"""
        return self.app