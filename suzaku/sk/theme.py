from typing import Union, Any

import warnings
import os
import json

class SkTheme():
    def __init__(self, style: dict={}):
        """
        Theme for SkWindow and SkWidgets.

        :param style: Style of the theme
        """
        self.style = style
    
    def load_from_file(self, file_path: str) -> "SkTheme":
        """
        Load styles to theme from a file.
        
        :param file_path: Path to the theme file.
        """
        f = open(file_path, mode="r", encoding="utf-8")
        style_raw = f.read()
        style = json.loads(style_raw)
        self.style = style
        return self

    def load_fromm_json(self, style_json: dict) -> "SkTheme":
        """
        Load styles to theme from a file.
        
        :param file_path: Path to the theme file.
        """
        self.style = style_json
        return self
    
    NotImplemented

default_theme = SkTheme({}).load_from_file(os.path.join(os.path.split(__file__)[0], 
                                                        "../styles/light.json"))