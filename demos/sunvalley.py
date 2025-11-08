from suzaku import *


root = Sk(theme=SkTheme.find_loaded_theme("sun_valley.light"))
# headerbar = titlebar(root)

for i in range(5):
    SkTextButton(root, text="Click me").box()

root.mainloop()
