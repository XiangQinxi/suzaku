from suzaku import *


root = Sk()

tabs = SkTabs(root)

tab1 = SkFrame(tabs)
btn = SkTextButton(tab1, text="Test 1")
btn.box()

tabs.add(tab1, text="Tab 1")

tab2 = SkFrame(tabs)
btn = SkTextButton(tab2, text="Test 2")
btn.box()
tabs.add(tab2, text="Tab 2")

tabs.box(expand=True)

root.mainloop()
