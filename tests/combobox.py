from suzaku import *


root = Sk(theme=sv_light_theme)

combobox = SkCombobox(
    root, default="Item 1", values=[f"Item {i}" for i in range(10)], readonly=True
)
combobox.box()

root.mainloop()
