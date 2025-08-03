from typing import Union, Any

import warnings
import os
import json
import re

class SkTheme():
    def __init__(self, style: dict={}):
        """Theme for SkWindow and SkWidgets.

        :param style: Style of the theme
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
    
    def select(self, selector: str) -> list:
        """Parse style selector.

        ## Selector

        `<Widget>` indicates the style of Widget, e.g. `SkButton`.

        `<Widget>:<state>` indicates the style of the state of Widget, e.g. `SkButton:hover`.

        :param selector: The selector string
        """
        # Validation
        if not re.match("[a-zA-Z0-9-_.:]", selector):
            raise ValueError(f"Invalid style selector [{selector}].")
        # Handling
        if ":" in selector:
            result = selector.split(":")
            # Validation
            if len(result) >= 2:
                raise ValueError(f"Invalid style selector [{selector}].")
        else:
            result = [selector]
        # Validation
        level_dict = self.styles
        for selector_level in result:
            if selector_level not in level_dict.keys():
                raise ValueError(f"Cannot find style with selector [{selector}]")
        return result
    
    def get_style(self, selector: str, copy: bool=True) -> dict:
        """Get style config using a selector.

        :param selector: The selector string, indicating which style to get
        :param copy: Whether to copy a new style json, otherwise returns the style itself
        """
        result = self.styles
        for selector_level in self.select(selector):
            result = result[selector_level]
        if copy:
            return result.copy()
        else:
            return result
    
    def mixin(self, selector: str, new_style: dict, copy: bool=False):
        """Mix a custom style into the theme.
        
        :param selector: The selector string, indicates where to mix in
        :param new_style: A style json, to be mixed in
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

        e.g. `SkButton(window, style=style.special(background=(255, 0, 0, 0)))`
        
        :param selector: The selector string, indicates where to mix in
        :param **kwargs: Styles to change
        """
        new_theme = SkTheme(self.styles)
        style_operate = new_theme.get_style(selector, copy=False)
        style_operate.update(kwargs)
        return new_theme
    NotImplemented

default_theme = SkTheme({}).load_from_file(os.path.join(os.path.split(__file__)[0], 
                                                        "../styles/light.json"))