from .visual import SkVisual


class SkEmpty(SkVisual):
    """
    空元素
    仅作布局中占位使用
    """

    def __init__(self, *args, size=(0, 0), **kwargs):
        super().__init__(*args, size=size, **kwargs)
        self.visual_attr["name"] = "sk_empty"

    def draw(self, canvas, rect):
        pass
