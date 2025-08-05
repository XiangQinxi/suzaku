import skia
from ..event import SkEvent


class SkContainer:

    def __init__(self):
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

        In each layer, items will be drawn in the order of index. Meaning that those with lower 
        index will be drawn first, and may get covered by those with higher index. Same for layers, 
        layers with higher index cover those with lower index.
        """
        self.children = []  # Children
        self.draw_list = [
            [],  # Layout layer
            []  # Floating layer
        ]
        self._box_direction = None  # h(horizontal) or v(vertical)
        self.bind("resize", self._handle_layout)

    def draw_children(self, canvas):
        for item in self.draw_list:
            for child_dict in item:
                #print(i, f)
                if child_dict["child"].visible:
                    child_dict["child"].draw(canvas)

    def add_child(self, child):
        """
        Add child widget to window.

        Args:
            child: SkWidget

        Returns:
            None
        """
        self.children.append(child)

    def add_layout_child(self, draw_dict):
        """
        Add layout child widget to window.

        :arg child: SkWidget
        :arg draw_dict: dict
        :return: None
        """
        if draw_dict["layout"] == "box":
            side = draw_dict["side"]
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

        self.draw_list[0].append(draw_dict)
        event = SkEvent(event_type="resize", width=self.width, height=self.height)
        self._handle_layout(event)

    def add_floating_child(self, draw_dict):
        """
        Add floating child widget to window.

        :arg child: SkWidget
        :arg draw_dict: dict
        :return: None
        """
        self.draw_list[1].append(draw_dict)
        event = SkEvent(event_type="resize", width=self.width, height=self.height)
        self._handle_layout(event)

    def _handle_layout(self, evt):
        self._handle_box(evt)
        self._handle_fixed(evt)

    def _handle_pack(self, evt):
        pass

    def _handle_place(self, evt):
        pass

    def _handle_grid(self, evt):
        pass

    def _handle_box(self, evt):
        width = evt.width
        height = evt.height
        start_children = []
        end_children = []
        expanded_children = []
        fixed_children = []
        boxes_children = self.draw_list[0]

        for child in boxes_children:
            if child["side"] == "left":
                start_children.append(child)
            elif child["side"] == "right":
                end_children.append(child)
            if child["side"] == "top":
                start_children.append(child)
            elif child["side"] == "bottom":
                end_children.append(child)
            if child["expand"]:
                expanded_children.append(child)
            else:
                fixed_children.append(child)

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
                child["child"].x = last_child_left_x + child["child"].width - right
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

    def _handle_fixed(self, evt):
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

