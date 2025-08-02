from typing import Union, Any

import os


class SkTheme:
    def __init__(self, styles: dict = {}):
        """
        Theme for SkWindow and SkWidgets

        :param style: Style of the theme
        """
        self.styles = styles
    
    def load_from_file(self, file_path):
        with open(file_path, "r") as f:
            return self.load_fromm_json(f.read())

    def load_fromm_json(self, json):
        from json import loads
        self.styles = loads(json)
        return self


default_theme = SkTheme().load_from_file(os.path.join(os.path.split(__file__)[0],
                                                        "../styles/light.json"))
