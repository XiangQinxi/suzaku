class SkTheme():

    """
    主题配置类
    用于配置和管理应用程序的主题，包括颜色、字体等。
    """

    themes = {}  # 记录所有已经加载过的主题
    theme_name = ""  # 当前使用的主题的名称

    def __init__(self, name: str = "light"):
        """
        加载'light'与'dark'主题，并启用默认主题

        :param name: 默认主题名称
        """
        import os.path
        self.load_theme(os.path.join(os.path.dirname(__file__), 'light.json'))
        self.load_theme(os.path.join(os.path.dirname(__file__), 'dark.json'))
        self.use_theme(name)

    def load_theme(self, path: str) -> "SkTheme":
        """
        加载主题

        :param path: 主题文件 (.json)
        :return: cls
        """
        from os.path import exists
        if not exists(path):
            raise FileNotFoundError(f"主题文件 {path} 不存在")
        import json
        with open(path, "r") as f:
            data = json.load(f)
            self.themes[data["name"]] = data
        return self

    def use_theme(self, name) -> "SkTheme":
        """
        启用主题

        :param name: 主题名称
        :return: cls
        """
        if not name in self.themes:
            raise ValueError(f"主题 {name} 不存在！请使用 {self.themes.keys()} 中的主题，或者使用load_theme导入主题")
        self.theme_name = name
        return self

    def get_theme(self):
        """

        :return:
        """
        return self.themes[self.theme_name]

    def get_theme_sheets(self, name):
        """
        获取当前主题的所有样式表

        :return:
        """
        return self.themes[self.theme_name]["sheets"]

    def get_theme_with_name(self, name: str):
        return self.themes[name]


theme = SkTheme(name="light")
