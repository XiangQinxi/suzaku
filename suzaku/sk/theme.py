from typing import Union, Any

import warnings
import os
import json

class SkTheme():
    def __init__(self, styles: dict={}):
        """
        Theme for SkWindow and SkWidgets.

        :param styles: styles of the theme
        """
        self.styles = styles
    
    def load_from_file(self, file_path: str) -> "SkTheme":
        """
        Load styles to theme from a file.
        
        :param file_path: Path to the theme file.
        """
        with open(file_path, mode="r", encoding="utf-8") as f:
            self.styles = json.loads(f.read())
            return self

    def load_fromm_json(self, json_stings: dict) -> "SkTheme":
        """
        Load styles to theme from a file.
        
        :param file_path: Path to the theme file.
        """
        self.styles = json.loads(json_stings)
        return self

default_theme = light_theme =  SkTheme({}).load_from_file(os.path.join(os.path.split(__file__)[0], "themes", "light.json"))