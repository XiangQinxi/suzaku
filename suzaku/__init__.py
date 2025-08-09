__version__ = "0.0.1alpha"

import OpenGL

OpenGL.ERROR_CHECKING = False

from .event import SkEvent
from .styles import *  # 基础样式，包括颜色等
from .var import (SkBooleanVar, SkEventHanding, SkFloatVar, SkIntVar,
                  SkStringVar, SkVar)
from .widgets import *
