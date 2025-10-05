from suzaku import *


root = Sk()

statusbar = SkFrame(root)
sizegrip = SkSizegrip(statusbar)
sizegrip.box(side="right", padx=0, pady=0)
statusbar.box(side="bottom", padx=0, pady=0)

root.mainloop()
