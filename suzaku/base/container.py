import warnings

from ..event import SkEvent


class SkLayoutError(TypeError):
    pass

class SkContainer:

    def __init__(self, pos: tuple[int, int]=(0, 0), size: tuple[int, int]=(0, 0)):
        """A SkContainer represents a widget that has the ability to contain other widgets inside.

        SkContainer is only for internal use. If any user would like to create a widget from 
        several of existed ones, they should use SkComboWidget instead. The authors will not 
        guarantee the stability of inheriting SkContainer for third-party widgets.
        
        SkContainer class contains code for widget embedding, and layout handling, providing the 
        ability of containing `children` to widgets inerit from it. All other classes with such 
        abilities should be inherited from SkContainer.

        SkContainer has a `children` list, each item is a `SkWidget`, called `child`. This helps 
        the SkContainer knows which `SkWidget`s it should handle.
        
        SkContainer has a `draw_list` that stores all widgets contained in it that should be drawn. 
        They are separated into a few layers which are listed below, in the order of from behind to 
        the top: 

        1. `Layout layer`: The layer for widgets using pack or grid layout.
        2. `Floating layer`: The layer for widgets using place layout.
        3. `Fixed layer`: The layer for widgets using fixed layout.

        In each layer, items will be drawn in the order of index. Meaning that those with lower 
        index will be drawn first, and may get covered by those with higher index. Same for layers, 
        layers with higher index cover those with lower index.

        :param pos: The coordinates of the container in tuple (x, y), default is (0, 0)
        :param size: Size of the container, in tuple (width, height), default is (0, 0)
        """
        self.children = []  # Children
        self.draw_list: list[list[dict]] = [
            [],  # Layout layer [SkWidget1, SkWidegt2, ...]
            [],  # Floating layer [SkWidget1, SkWidget2, ...]
            [],  # Fixed layer [SkWidget1, SkWidget2, ...]
        ]
        self.layers_layout_type = ["none" for i in range(len(self.draw_list))]

        self._box_direction = None  # h(horizontal) or v(vertical)

        self.bind("resize", self._handle_layout)

        self.x = pos[0]
        self.y = pos[1]
        self.width = size[0]
        self.height = size[1]
    
    def bind(self, *args, **kwargs):
        raise RuntimeError("Anything inherited from SkContainer should support binding events!" + \
                           "This error should be overrode by the actual bind function of " + \
                           "SkWindow or SkWidget in normal cases.")

    def draw_children(self, canvas):
        for item in self.draw_list:
            for child in item:
                if child.visible:
                    child.draw(canvas)

    def add_child(self, child):
        """Add child widget to window.

        :param child: The child to add
        """
        self.children.append(child)

    def add_layout_child(self, child):
        """Add layout child widget to window.

        :arg draw_dict: dict
        :return: None
        """
        layout_config = child.layout_config

        if layout_config["layout"] == "box":
            side = layout_config["side"]
            if side == "left" or side == "right":
                direction = "h"
            elif side == "top" or side == "bottom":
                direction = "v"
            else:
                raise ValueError("Box layout side must be left, right, top or bottom.")

            if self._box_direction == "v":
                if direction == "h":
                    raise ValueError("Box layout can only be used with vertical direction.")
            elif self._box_direction == "h":
                if direction == "v":
                    raise ValueError("Box layout can only be used with horizontal direction.")
            else:
                self._box_direction = direction

        self.draw_list[0].append(child)
        event = SkEvent(event_type="resize", width=self.width, height=self.height)
        self._handle_layout(event)

    def add_floating_child(self, child):
        """
        Add floating child widget to window.

        :arg draw_dict: dict
        :return: None
        """
        self.draw_list[1].append(child)
        event = SkEvent(event_type="resize", width=self.width, height=self.height)
        self._handle_layout(event)

    # Processing Layouts

    def _handle_layout(self, event):
        for child in self.children:
            if child.visible:
                layout_type = list(child.layout_config.keys())[0]
                # Build draw_item dict
                draw_item = {
                    "widget": child,
                    "x": 0,
                    "y": 0,
                    "width": 0,
                    "height": 0,
                }
                # Sort children
                match layout_type:
                    case "none":
                        continue
                    case "pack" | "box" | "grid": # -> Layout layer
                        if self.layers_layout_type[0] == "none":
                            self.layers_layout_type[0] = layout_type
                        elif self.layers_layout_type[0] != layout_type:
                            raise SkLayoutError("Layout layer can only contain no more than " + \
                                                f"one layout type. Not {layout_type} with " + \
                                                f"{self.layers_layout_type[0]} which is existed.")
                        self.draw_list[0].append(draw_item)
                    case "place": # -> Floating layer
                        if self.layers_layout_type[1] != "place":
                            self.layers_layout_type[1] = layout_type
                        self.draw_list[1].append(draw_item)
                    case "fixed": # -> Fixed layer
                        if self.layers_layout_type[2] != "fixed":
                            self.layers_layout_type[2] = layout_type
                        self.draw_list[2].append(draw_item)
        # Process layouts
        for layout_type in self.layers_layout_type:
            vars(self)[f"_handle_{layout_type}"]()
        # self._handle_fixed()

    def _handle_pack(self, event: SkEvent):
        pass

    def _handle_place(self, event: SkEvent):
        pass

    def _handle_grid(self, event: SkEvent):
        pass

    def _handle_box(self, event: SkEvent):
        """Process box layout.
        
        :param event: The resize event
        """
        width = self.width
        height = self.height
        start_children = []
        end_children = []
        expanded_children = []
        fixed_children = []
        boxes_children = self.draw_list[0]

        for child in boxes_children:
            layout_config = child["widget"].layout_config
            match layout_config["direction"].lower():
                case "n" | "w":
                    start_children.append(child["widget"])
                case "s" | "e":
                    end_children.append(child["widget"])
            if layout_config["expand"]:
                expanded_children.append(child["widget"])
            else:
                fixed_children.append(child["widget"])

        if self._box_direction == "h":
            # Horizontal Layout

            fixed_width = 0
            for fixed_child in fixed_children:
                if fixed_child["padx"] is tuple:
                    fixed_width += fixed_child["padx"][0]
                else:
                    fixed_width += fixed_child["padx"]
                fixed_width += fixed_child["child"].width
                if fixed_child["padx"] is tuple:
                    fixed_width += fixed_child["padx"][1]
                else:
                    fixed_width += fixed_child["padx"]

            if len(expanded_children):
                expanded_width = (self.width - fixed_width) / len(expanded_children)
            else:
                expanded_width = 0

            # Left side
            last_child_left_x = 0
            for child in start_children:
                if child["padx"] is tuple:
                    left = child["padx"][0]
                    right = child["padx"][1]
                else:
                    left = right = child["padx"]
                if child["pady"] is tuple:
                    top = child["pady"][0]
                    bottom = child["pady"][1]
                else:
                    top = bottom = child["pady"]
                if not child["expand"]:
                    child["child"].width = child["child"].cget("dheight")
                else:
                    child["child"].width = expanded_width - left - right
                child["child"].height = self.height - top - bottom
                child["child"].x = last_child_left_x + left
                child["child"].y = top
                last_child_left_x = child["child"].x + child["child"].width + right

            # Right side
            last_child_right_x = self.width
            for child in end_children:
                if child["padx"] is tuple:
                    left = child["padx"][0]
                    right = child["padx"][1]
                else:
                    left = right = child["padx"]
                if child["pady"] is tuple:
                    top = child["pady"][0]
                    bottom = child["pady"][1]
                else:
                    top = bottom = child["pady"]
                if not child["expand"]:
                    child["child"].width = child["child"].cget("dheight")
                else:
                    child["child"].width = expanded_width - left - right
                child["child"].height = self.height - top - bottom
                child["child"].x = last_child_right_x - child["child"].width - right
                child["child"].y = top
                last_child_right_x = last_child_right_x - child["child"].width - left * 2
        else:
            # Vertical Layout

            fixed_height = 0
            for fixed_child in fixed_children:
                if fixed_child["pady"] is tuple:
                    fixed_height += fixed_child["pady"][0]
                else:
                    fixed_height += fixed_child["pady"]
                fixed_height += fixed_child["child"].height
                if fixed_child["pady"] is tuple:
                    fixed_height += fixed_child["pady"][1]
                else:
                    fixed_height += fixed_child["pady"]

            if len(expanded_children):
                expanded_height = (self.height - fixed_height) / len(expanded_children)

            last_child_bottom_y = 0
            for child in start_children:
                if child["padx"] is tuple:
                    left = child["padx"][0]
                    right = child["padx"][1]
                else:
                    left = right = child["padx"]
                if child["pady"] is tuple:
                    top = child["pady"][0]
                    bottom = child["pady"][1]
                else:
                    top = bottom = child["pady"]
                child["child"].width = self.width - left - right
                if not child["expand"]:
                    child["child"].height = child["child"].cget("dheight")
                else:
                    child["child"].height = expanded_height - top - bottom
                child["child"].x = left
                child["child"].y = last_child_bottom_y + top
                last_child_bottom_y = child["child"].y + child["child"].height + bottom

            last_child_top_y = self.height
            for child in end_children:
                if child["padx"] is tuple:
                    left = child["padx"][0]
                    right = child["padx"][1]
                else:
                    left = right = child["padx"]
                if child["pady"] is tuple:
                    top = child["pady"][0]
                    bottom = child["pady"][1]
                else:
                    top = bottom = child["pady"]
                child["child"].width = self.width - left - right
                if not child["expand"]:
                    child["child"].height = child["child"].cget("dheight")
                else:
                    child["child"].height = expanded_height - top - bottom
                child["child"].x = left
                child["child"].y = last_child_top_y - child["child"].height - bottom
                last_child_top_y = last_child_top_y - child["child"].height - top * 2

    def _handle_fixed(self, event: SkEvent):
        """Process fixed layout.
        
        :param event: The resize event
        """
        for item in self.draw_list[1]:
            if item["layout"] == "fixed":
                from ..widgets.window import SkWindow
                if not isinstance(self, SkWindow):
                    item["child"].x = item["x"] + self.x
                    item["child"].y = item["y"] + self.y
                else:
                    item["child"].x = item["x"]
                    item["child"].y = item["y"]
                item["child"].width = item["width"]
                item["child"].height = item["height"]

