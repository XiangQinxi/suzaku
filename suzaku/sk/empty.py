from .visual import SkVisual


class SkEmpty(SkVisual):
    """
    空元素
    仅作布局中占位使用
    """

    def __init__(self, *args, size=(0, 0), **kwargs) -> None:
        """
        初始化

        :param args: SkVisual参数
        :param size: 默认大小
        :param kwargs: SkVisual参数
        """
        super().__init__(*args, size=size, **kwargs)
        self.visual_attr["name"] = "sk_empty"

    def draw(self, canvas, rect) -> None:
        """
        绘制方法，不执行任何绘制操作

        :param canvas: 传入的skia.Surface
        :param rect: 给出的矩形
        :return: None
        """
        pass
