class Element:
    def __init__(self, parent: "SkWidget"):
        self.parent = parent
        self.layout = None

    def draw(self, canvas, rect, theme):
        pass

    def fill(self, padx=0, pady=0):
        self.layout = {
            "name": "fill",
            "padx": padx,
            "pady": pady,
        }

    def update_layout(self):
        if self.layout == "fill":
            self.x = self.parent.x
            self.y = self.parent.y
            self.width = self.parent.width
            self.height = self.parent.height
