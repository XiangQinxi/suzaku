from suzaku import *


root = Sk()
root.bind_scroll_event()

for i in range(20):
    SkTextButton(root, i + 1).box(padx=10, pady=(10, 0))

root.mainloop()
