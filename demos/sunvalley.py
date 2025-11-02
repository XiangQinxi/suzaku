from suzaku import *


sunvalley = SkTheme().load_from_file("./sunvalley.json")

root = Sk(theme=sunvalley)
# headerbar = titlebar(root)

for i in range(5):
    SkTextButton(root, text="Click me").box()

root.mainloop()
