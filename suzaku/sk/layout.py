class Boxes:

    from .window import SkWindow

    def __init__(self, parent: SkWindow, direction="h"):

        self.parent = parent
        self.children = []
        self.direction = direction

    def add_child(self, child, padx=5, pady=5, expand=False):
        self.children.append(
            {
                "child": child,
                "padx": padx,
                "pady": pady,
                "expand": expand,
            }
        )

        self.parent.bind("resize", self.update)

    def change_direction(self, direction):
        self.direction = direction
        self.update(self.parent.winfo_width(), self.parent.winfo_height())

    def update(self, width, height):
        if self.direction == "h":
            # 水平布局

            width -= self.children[-1]["padx"]

            fixed_width = 0
            expand_count = 0
            total_padx = 0

            # 计算固定宽度元素总宽度和可扩展元素数量
            for child in self.children:
                total_padx += child["padx"]
                if child["expand"]:
                    expand_count += 1
                else:
                    fixed_width += child["child"].visual_attr["width"]

            # 计算剩余可分配宽度(减去所有padx)
            remaining_width = max(0, width - fixed_width - total_padx)
            expand_width = remaining_width // expand_count if expand_count > 0 else 0

            current_x = 0
            for child in self.children:
                c = child["child"]
                current_x += child["padx"]  # 添加当前元素的padx

                if child["expand"]:
                    c.visual_attr["x"] = current_x
                    c.visual_attr["y"] = child["pady"]
                    c.visual_attr["width"] = expand_width
                    c.visual_attr["height"] = height - child["pady"] * 2
                else:
                    c.visual_attr["x"] = current_x
                    c.visual_attr["y"] = child["pady"]
                    c.visual_attr["height"] = height - child["pady"] * 2

                current_x += c.visual_attr["width"]  # 移动到下一个元素的位置
        else:
            # 垂直布局

            height -= self.children[-1]["pady"]

            fixed_height = 0
            expand_count = 0
            total_pady = 0

            for child in self.children:
                total_pady += child["pady"]
                if child["expand"]:
                    expand_count += 1
                else:
                    fixed_height += child["child"].visual_attr["height"]

            remaining_height = max(0, height - fixed_height - total_pady)
            expand_height = remaining_height // expand_count if expand_count > 0 else 0

            current_y = 0
            for child in self.children:
                c = child["child"]
                current_y += child["pady"]

                if child["expand"]:
                    c.visual_attr["x"] = child["padx"]
                    c.visual_attr["y"] = current_y
                    c.visual_attr["width"] = width - child["padx"] * 2
                    c.visual_attr["height"] = expand_height
                else:
                    c.visual_attr["x"] = child["padx"]
                    c.visual_attr["y"] = current_y
                    c.visual_attr["width"] = width - child["padx"] * 2

                current_y += c.visual_attr["height"]

class Box:
    def box_configure(self, padx=5, pady=5, expand=False, direction=None):
        parent = self.winfo_parent()
        layout = parent.winfo_layout()
        if not layout:
            if direction is None:
                direction = "h"
            l = Boxes(parent, direction)
            parent.set_layout(l)
        else:
            l = layout
        if not self in l.children:
            l.add_child(self, padx=padx, pady=pady, expand=expand)
            l.update(parent.winfo_width(), parent.winfo_height())

    box = box_configure

    def hbox_configure(self, *args, **kwargs):
        self.box_configure(*args, **kwargs, direction="h")

    hbox = hbox_configure

    def vbox_configure(self, *args, **kwargs):
        self.box_configure(*args, **kwargs, direction="v")

    vbox = vbox_configure



class Place:
    def place_configure(self, x: int, y: int, width: int = None, height: int = None):
        self.winfo_parent().set_layout("place")

        self.visual_attr["x"] = x
        self.visual_attr["y"] = y
        if width is not None:
            self.visual_attr["width"] = width
        if height is not None:
            self.visual_attr["height"] = height

    place = place_configure


class Puts:

    from .window import SkWindow

    def __init__(self, parent: SkWindow):

        self.parent = parent
        self.children = []

    def add_child(self, child, margin: tuple[int, int, int, int] = (5, 5, 5, 5)):
        self.children.append(
            {
                "child": child,
                "margin": margin,
            }
        )

        self.parent.bind("resize", self.update)

    def update(self, width, height):
        for child in self.children:
            c = child["child"]
            c.visual_attr["x"] = child["margin"][0]
            c.visual_attr["y"] = child["margin"][1]
            c.visual_attr["width"] = width - child["margin"][2] - child["margin"][3]
            c.visual_attr["height"] = height - child["margin"][1] - child["margin"][3]


class Put:

    """
    相对位置布局
    """

    def put_configure(self, margin: tuple[int, int, int, int] = (0, 0, 0, 0)):
        parent = self.winfo_parent()
        layout = parent.winfo_layout()
        if not layout:
            l = Puts(parent)
            parent.set_layout(l)
        else:
            l = layout
        if not self in l.children:
            l.add_child(self, margin=margin)
            l.update(parent.winfo_width(), parent.winfo_height())

    put = put_configure


class Layout(Box, Place, Put):
    pass
