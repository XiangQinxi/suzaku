import skia

from .frame import SkFrame


class SkCanvas(SkFrame):
    def __init__(self, parent, *args, **kwargs):
        SkFrame.__init__(self, parent, *args, **kwargs)
        self.elements = {}
