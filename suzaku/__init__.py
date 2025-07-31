__version__ = '0.0.1alpha'

import OpenGL
OpenGL.ERROR_CHECKING = False

from .base import *  # 基础界面库
from .sk import *  # 高级界面库
from .style import *  # 基础样式，包括颜色等