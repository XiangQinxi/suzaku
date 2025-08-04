from typing import Union, Any

import warnings
import os
import json
import re

class SkStyleNotFoundError(NameError):
    pass

class SkTheme:
    def __init__(self, style: dict={}, parent: Union["SkTheme", None] = None):
        """Theme for SkWindow and SkWidgets.

        :param styles: Styles of the theme
        :param parent: Parent theme
        """
        self.styles = style
    
    def load_from_file(self, file_path: str) -> "SkTheme":
        """Load styles to theme from a file.
        
        :param file_path: Path to the theme file.
        """
        f = open(file_path, mode="r", encoding="utf-8")
        style_raw = f.read()
        style = json.loads(style_raw)
        self.styles = style
        return self

    def load_from_json(self, style_json: dict) -> "SkTheme":
        """Load styles to theme from a file.
        
        :param file_path: Path to the theme file.
        """
        self.styles = style_json
        return self
    
    def select(self, selector: str, create_if_not_existed: bool=False) -> list:
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
            if len(result) >= 2: # Validation
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
            if selector_level not in level_dict.keys():
                if create_if_not_existed:
                    checking[selector_level] = {}
                raise SkStyleNotFoundError(f"Cannot find styles with selector [{selector}]")
            if create_if_not_existed:
                checking = checking[selector_level]
        return result
    
    def get_style(self, selector: str, copy: bool=True) -> dict:
        """Get styles config using a selector.

        :param selector: The selector string, indicating which styles to get
        :param copy: Whether to copy a new styles json, otherwise returns the styles itself
        """
        result = self.styles
        try:
            selector_parsed = self.select(selector)
        except SkStyleNotFoundError:
            return default_theme.get_style(selector, copy=True)
        for selector_level in selector_parsed:
            result = result[selector_level]
        if copy:
            return result.copy()
        else:
            return result
    
    def mixin(self, selector: str, new_style: dict, copy: bool=False):
        """Mix a custom styles into the theme.
        
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
            warnings.warn("<SkWidget.ITSELF> is not supported by SkTheme.special()! "+\
                          "It will be regarded as <SkWidget.rest>")
            selector = selector.replace("ITSELF", "rest")
        new_theme = SkTheme(self.styles)
        style_operate = new_theme.get_style(selector, copy=False)
        style_operate.update(kwargs)
        return new_theme
    
    def apply_on(self, widget: "SkWidget"):
        """Apply theme on a widget.
        
        :param widget: The widget to apply theme to.
        """
        widget.apply_theme(self)


light_path = os.path.normpath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "resources",
        "themes",
        "light.json"
    )
)

dark_path = os.path.normpath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "resources",
        "themes",
        "dark.json"
    )
)

default_theme = light_theme =  SkTheme({}).load_from_file(light_path)
dark_theme = SkTheme({}).load_from_file(dark_path)
