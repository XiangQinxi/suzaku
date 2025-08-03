class SkStyle():
    def __init__(self):
        from suzaku.sk.themes import theme
        self.theme = theme

    def configure(self, style_name, *args, **kwargs):
        self.theme.themes[self.theme.theme_name][style_name].update(*args, **kwargs)

    def create(self, basestyle, name, *args, **kwargs):
        self.theme.themes[self.theme.theme_name][name] = self.theme.themes[self.theme.theme_name][basestyle].copy()
        self.configure(name, *args, **kwargs)

    def get_style(self, style_name):
        return self.theme.themes[self.theme.theme_name][style_name]
