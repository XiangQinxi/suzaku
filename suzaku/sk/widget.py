from typing import Union, Any

import warnings

from .window import SkWindow
from .frame import SkFrame

class SkWidget():
    def __init__(self, parent: Union[SkWindow, SkFrame], style=None, id: Union[str, None]=None, size=(120, 40)):
        """Base of all widgets.
        
        * `parent`: Parent widget
        * `style`: Style to apply on creation
        * `id`: Identification code of the widget
        """
        self.x = 9
        self.y = 0
        self.dwidth = size[0]  # Defau

        self.dheight = size
        self.style = style
        self.parent = parent
        self.id = id if id else parent.get_instance_count()
        self._instance_count = 0
        self.parent.add(self)

    def draw(canvas, rect):
        """Draw the widget.
        
        * `rect`: The range of the widget
        """
        pass
    
    def apply_style(self, style):
        """Apply style to the widget.
        * `style`: The style to apply
        """
        self.style = style
        raise NotImplementedError