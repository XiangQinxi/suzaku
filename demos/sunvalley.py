from suzaku import *


sunvalley = SkTheme().load_from_file("./sunvalley.json")

root = Sk(theme=sunvalley)
headerbar = titlebar(root)

button = SkTextButton(root, text="Click me")
button.box()

root.mainloop()
