from suzaku import *


cosmic = SkTheme().load_from_file("./cosmic.json")

root = Sk(theme=cosmic)
headerbar = titlebar(root)
headerbar.command.box(side="right", padx=5, pady=5)

button = SkTextButton(root, text="Click me")
button.box()

root.mainloop()
