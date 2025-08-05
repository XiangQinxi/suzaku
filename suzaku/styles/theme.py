import json
import os
import pathlib
import re
import warnings
from typing import Any, Union


class SkStyleNotFoundError(NameError):
    pass


class SkTheme():
    loaded_themes: list["SkTheme"] = []
    INTERNAL_THEME_DIR = pathlib.Path(__file__).parent.parent / "resources" / "themes"
    INTERNAL_THEMES: dict[str, "SkTheme"] = {}
    DEFAULT_THEME: Union["SkTheme", None] = None
    DEFAULT_THEME_NAME: str = "light"

    @classmethod
    def find_loaded_theme(cls, theme_name: str) -> Union["SkTheme", bool]:
        """
        Search for a loaded theme by name, returns the SkTheme object if found, or False is not.
        :param theme_name: Name of the theme to load
        """
        for theme in cls.loaded_themes:
            if theme.name == theme_name:
                return theme
        return False

    @classmethod
    def validate_theme_existed(cls, theme_name: str) -> bool:
        """
        Validate if the theme with given name existed and loaded.

        :param theme_name: Name of the theme to validate
        """
        return SkTheme.find_loaded_theme(theme_name) != False  # ☝🤓

    def __init__(self, style: dict = {}, parent: Union["SkTheme", None] = None) -> None:
        """Theme for SkWindow and SkWidgets.

        :param styles: Styles of the theme
        :param parent: Parent theme
        """
        self.styles: dict = style

        self.name: str = f"untitled.{len(SkTheme.loaded_themes) + 1}"
        self.friendly_name = f"Untitled theme {len(SkTheme.loaded_themes) + 1}"  # friendly_name感觉有点多余?
        self.parent: Union["SkTheme", None] = parent

        SkTheme.loaded_themes.append(self)  # TODO: figure out.
        return

    def load_from_file(self, file_path: Union[str, pathlib.Path]) -> "SkTheme":
        """
        Load styles to theme from a file.

        :param file_path: Path to the theme file
        """

        f = open(file_path, mode="r", encoding="utf-8")

        style_raw = f.read()
        theme_data = json.loads(style_raw)
        if search_result := SkTheme.find_loaded_theme(theme_data["name"]) != False:
            warnings.warn(f"Theme <{theme_data["name"]}> already loaded or existed.")
            return search_result

        return self.load_from_json(theme_data)

    def load_from_json(self, theme_data: dict) -> "SkTheme":
        """Load all data (including matadata) to the theme.

        :param theme_data: dict that contains the theme data
        """
        self.styles = theme_data["styles"]

        self.rename(theme_data["name"], theme_data["friendly_name"])
        self.set_parent(theme_data["base"])

        return self

    def load_styles_from_json(self, style_json: dict) -> "SkTheme":
        """Load styles to theme from a given dict.

        :param style_json: dict that contains the styles
        """
        self.styles = style_json
        return self

    def set_parent(self, parent_name: str) -> Union["SkTheme", None]:
        """
        Set the parent for the theme via string stored in theme json.
        Returns the SkTheme object of the parent theme.

        ## Parent Name

        - `ROOT` means the theme does not have a parent. This is not recommended for third-party
          themes, use `DEFAULT` instead.
        - `DEFAULT` means the parent of the theme is the default internal theme.

        If the parent name is none of above, it should be the theme of the name and will be set as
        parent directly. However, if the theme specified is not yet loaded, parent will fall back
        to `DEFAULT`.

        :param parent_name: Name of the parent
        """
        match parent_name:
            case "ROOT":
                self.parent = None
            case "DEFAULT":
                self.parent = self.DEFAULT_THEME
            case _:
                search_result = SkTheme.find_loaded_theme(parent_name)
                if search_result != False:
                    self.parent = search_result
                else:
                    warnings.warn(f"Parent theme specified with name <{parent_name}> is not yet " + \
                                  "loaded. Will fall back to <DEFAULT> for parent instead.")
                    self.set_parent("DEFAULT")
        return self.parent

    def rename(self, new_name: str, friendly_name: str) -> "SkTheme":
        """Rename the theme.

        :param new_name: The new name for the theme
        """
        if not SkTheme.validate_theme_existed(new_name):
            self.name = new_name
            self.friendly_name = friendly_name  # 🤔
        else:
            warnings.warn(f"Theme name <{new_name}> occupied. Rename for <{self.name}> is canceled")
        return self

    def select(self, selector: str, create_if_not_existed: bool = False) -> list:
        """Parse styles selector.

        ## Selector

        `<Widget>` indicates the styles of Widget at rest state, e.g. `SkButton`.

        `<Widget>:<state>` indicates the styles of the state of Widget, e.g. `SkButton:hover`.

        `<Widget>:ITSELF` indecates the styles of the widget, e.g. `SkButton.ITSELF`.
        Note that this is not available everywhere.

        :param selector: The selector string
        :param create_if_not_existed: Create the styles if not existed.
        """
        # Validation
        if not re.match("[a-zA-Z0-9-_.:]", selector):
            raise ValueError(f"Invalid styles selector [{selector}].")
        # Handling
        if ":" in selector:
            result = selector.split(":")
            if len(result) > 2:  # Validation
                raise ValueError(f"Invalid styles selector [{selector}].")
            if result[1] == "ITSELF":
                result = [result[0]]
        else:
            result = [selector, "rest"]
        # Validation / Create if not existed
        level_dict = self.styles
        if create_if_not_existed:
            checking = self.styles
        for selector_level in result:
            # dict_keys(['SkWindow', 'SkFrame', 'SkBadge', 'SkButton', 'Close.SkButton', 'SkEntry', 'SkText'])
            if selector_level not in level_dict.keys():
                if create_if_not_existed:
                    checking[selector_level] = {}
                raise SkStyleNotFoundError(f"Cannot find styles with selector [{selector}]")
            if create_if_not_existed:
                checking = checking[selector_level]
        return result

    def get_style(self, selector: str, copy: bool = True) -> dict:
        """Get styles config using a selector.

        :param selector: The selector string, indicating which styles to get
        :param copy: Whether to copy a new styles json, otherwise returns the styles itself
        """
        result = self.styles
        if not selector: return

        try:
            selector_parsed = self.select(selector)
        except SkStyleNotFoundError:
            if self.name == f"default.{SkTheme.DEFAULT_THEME_NAME}":
                return
            return default_theme.get_style(selector, copy=True)
        for selector_level in selector_parsed:
            result = result[selector_level]
        if copy:
            return result.copy()
        else:
            return result

    def get_style_attr(self, selector: str, attr_name: str):
        """Get style attribute value.

        :param selector: The selector to the style
        :attr_name: The attribute
        """
        NotImplemented

    def mixin(self, selector: str, new_style: dict, copy: bool = False):
        """Mix custom styles into the theme.

        :param selector: The selector string, indicates where to mix in
        :param new_style: A styles json, to be mixed in
        :param copy: Whether to copy a new theme, otherwise modify the current object
        """
        if copy:
            theme_operate = SkTheme(self.styles)
        else:
            theme_operate = self
        style_operate = theme_operate.get_style(selector, copy=False)
        style_operate.update(new_style)
        return theme_operate

    def special(self, selector: str, **kwargs):
        """Create a sub-theme with few modifications on the theme.

        Can be used when applying custom styles on a specific widget.

        e.g. `SkButton(window, styles=styles.special(background=(255, 0, 0, 0)))`

        :param selector: The selector string, indicates where to mix in
        :param **kwargs: Styles to change
        """
        if "ITSELF" in selector:
            warnings.warn("<SkWidget.ITSELF> is not supported by SkTheme.special()! " + \
                          "It will be regarded as <SkWidget.rest>")
            selector = selector.replace("ITSELF", "rest")
        new_theme = SkTheme(self.styles, parent=self)
        style_operate = new_theme.get_style(selector, copy=False)
        style_operate.update(kwargs)
        return new_theme

    def apply_on(self, widget: "SkWidget"):
        """Apply theme on a widget.

        :param widget: The widget to apply theme to.
        """
        widget.apply_theme(self)


SkTheme.DEFAULT_THEME = default_theme = SkTheme({}).load_from_file( \
    SkTheme.INTERNAL_THEME_DIR / f"{SkTheme.DEFAULT_THEME_NAME}.json")

for file in os.listdir(SkTheme.INTERNAL_THEME_DIR):
    if file == f"{SkTheme.DEFAULT_THEME_NAME}.json":  # For default theme, no need to reload it
        SkTheme.INTERNAL_THEMES[SkTheme.DEFAULT_THEME_NAME] = SkTheme.DEFAULT_THEME
        continue
    SkTheme.INTERNAL_THEMES[file.split(".")[0]] = (SkTheme({}).load_from_file( \
        SkTheme.INTERNAL_THEME_DIR / file))

#print(SkTheme.INTERNAL_THEMES["light"].get_style("SkButton:hover"))