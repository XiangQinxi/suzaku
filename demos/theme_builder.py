import json

from suzaku import *
from crossfiledialog import open_file


DEFAULT_WINDOW_SIZE = (640, 480)
DEFAULT_THEME = sv_light_theme


class MainWindow(SkWindow):
    def __init__(self, *args, **kwargs):
        SkWindow.__init__(self, *args, title="Suzaku Theme Builder", **kwargs)

        self.loaded = False

        self.setup()

    def setup(self):
        self.setup_titlebar()
        self.setup_menubar()
        self.setup_tabs()

    def setup_titlebar(self):
        self.titlebar = titlebar(self)

    def setup_menubar(self):
        self.menubar = SkMenuBar(self)
        self.menubar.box(side="top", padx=0, pady=0)

        def import_theme():
            file = open_file(filter={"JSON File": "*.json"})
            if file:
                self.configs = json.load(open(file, "r", encoding="utf-8"))
                self.apply_theme(SkTheme().load_from_file(file))
                self.config(title=f"Theme Builder - {self.configs['friendly_name']}")
                self.setup_tabs_pages()
                self.loaded = True

        def save_theme():
            if self.loaded:
                self.theme.save_to_file(f"{self.theme.friendly_name}.json")

        themes = {}
        for theme in SkTheme.loaded_themes:
            themes[theme.friendly_name] = theme

        menu_file = SkPopupMenu(self)
        menu_file.add_command(text="Import a theme (*.json)", command=import_theme)
        menu_file.add_command(text="Save current theme (*.json)", disabled=True, command=save_theme)
        menu_file.add_command(text="Close")
        menu_file.add_separator()
        menu_file.add_command(
            text="New window",
            command=lambda: self.__class__(app, size=DEFAULT_WINDOW_SIZE, theme=DEFAULT_THEME),
        )
        menu_file.add_command(text="Exit", command=self.destroy)
        self.menubar.add_cascade("File", menu=menu_file)

    def setup_tabs(self):
        self.tabs = SkTabs(self, expand=False)
        self.tabs.box(side="top", expand=True, padx=10, pady=10)

        text = SkText(self.tabs, "Please import a theme first.")
        self.tabs.add(text)
        self.tabs.select(0)

    def setup_tabs_pages(self):
        self.tabs.delete_all()

        #####################
        self.tab_config = SkFrame(self.tabs)
        SkText(self.tab_config, "Theme name:", align="left").grid(row=0, column=0, padx=(10, 0))
        SkEntry(self.tab_config, text=self.theme.name).grid(row=1, column=0)
        SkText(self.tab_config, "Theme friendly name:", align="left").grid(
            row=0, column=1, padx=(10, 0)
        )
        SkEntry(self.tab_config, text=self.theme.friendly_name).grid(row=1, column=1)
        SkText(self.tab_config, "Theme base:", align="left").grid(row=0, column=2, padx=(10, 0))
        if self.theme.parent:
            base = self.theme.parent.name
        else:
            base = "ROOT"
        SkCombobox(self.tab_config, text=base, readonly=True).grid(row=1, column=2)

        #####################
        self.tab_styles = SkFrame(self.tabs)
        self.tab_styles.bind_scroll_event()
        SkLabel(self.tab_styles, "Color palette").grid(row=0, column=0, padx=(10, 0), pady=(10, 0))

        for index, color_name in enumerate(self.configs["color_palette"]):
            SkText(self.tab_styles, color_name, align="left").grid(
                row=0,
                column=index + 1,
                padx=(10, 0),
            )
            SkEntry(self.tab_styles, text=str(self.configs["color_palette"][color_name])).grid(
                row=1,
                column=index + 1,
                padx=(10, 0),
                ipadx=(0, 60),
            )

        self.tabs.add(self.tab_config, "Config")
        self.tabs.add(self.tab_styles, "Styles")
        self.tabs.select(0)


if __name__ == "__main__":
    app = SkApp()

    mainwindow = MainWindow(app, size=DEFAULT_WINDOW_SIZE, theme=DEFAULT_THEME)

    app.mainloop()
