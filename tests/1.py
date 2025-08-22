from suzaku import *


class SkPopupMenu(SkWidget):
    def __init__(self, parent: SkWindow = None, **kwargs):
        super().__init__(parent, **kwargs)


app = SkApp()

window = SkWindow()

app.mainloop()
