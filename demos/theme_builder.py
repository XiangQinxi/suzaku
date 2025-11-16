from suzaku import *
from crossfiledialog import open_file


root = Sk(size=(500, 300))

stack = SkStack(root)

page1 = SkFrame(stack)


def import_theme():
    file = open_file()
    if file:
        print(f"Opened file: {file}")


button1 = SkTextButton(page1, text="Import a theme (*.json)", command=import_theme).box(
    side="top", padx=20, pady=(20, 5)
)
themes = {}
for theme in SkTheme.loaded_themes:
    themes[theme.friendly_name] = theme
button2 = SkCombobox(
    page1, values=themes.keys(), placeholder="Select a loaded theme", readonly=True
).box(side="top", padx=20, pady=(5, 20))

stack.add(page1)
stack.select(0)

stack.box(expand=True)

root.mainloop()
