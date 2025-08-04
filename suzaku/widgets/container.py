class SkContainer():

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
        self.children = []
        self.draw_list = [[], []]

    def bind_layout(self):
        """
        Bind layout event to container.

        :return: None
        """
        self.bind("resize", self._handle_layout)

    def add_child_with_layout(self, child_config):
        """

        :param child_config:
        :return: None
        """
        self.children_with_layout.append(child_config)
        self._handle_layout()

    def set_layout_name(self, name: str):
        """
        Set the container layout name

        :param name:
        """
        self.layout_name = name

    def _handle_layout(self):
        self._handle_flow()

    def _handle_pack(self):
        pass

    def _handle_place(self):
        pass

    def _handle_grid(self):
        pass



