import sys
import os

sys.path.append(os.path.abspath('.'))

from suzaku.widgets.app import SkApp
from suzaku.widgets.entry import SkEntry
from suzaku.widgets.window import SkWindow

class TestApp(SkApp):
    def __init__(self):
        super().__init__(title="输入框点击测试")
        self.window = SkWindow(size=(400, 200))
        self.entry = SkEntry(placeholder="点击输入框测试光标定位", size=(200, 35))
        self.window.add_child(self.entry)
        self.set_main_window(self.window)

if __name__ == "__main__":
    app = TestApp()
    app.run()