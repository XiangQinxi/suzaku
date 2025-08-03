class SkContainer:

    def __init__(self):
        self.children = []
        self.children_with_layout = []

        self.layout_name = "None"

    def bind_layout(self):
        self.bind("resize", self._handle_layout)

    def add_child_with_layout(self, child_config):
        self.children_with_layout.append(child_config)
        self._handle_layout()

    def set_layout_name(self, name: str):
        self.layout_name = name

    def _handle_layout(self):
        self._handle_flow()

    def _handle_pack(self):
        pass

    def _handle_place(self):
        pass

    def _handle_grid(self):
        pass



