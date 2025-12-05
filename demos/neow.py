from suzaku import *


neow_theme = SkTheme().load_from_file("./neow.json")


root = Sk(theme=neow_theme)
# root.window_attr("border", False)

card = SkCard(root)
card.bind_scroll_event()

button = SkTextButton(card, text="Click me")
button.grid(row=0, column=0)
button2 = SkTextButton(card, text="Click me", disabled=True)
button2.grid(row=0, column=1)

entry = SkEntry(card, placeholder="Enter something")
entry.grid(row=1, column=0)
entry2 = SkEntry(card, placeholder="Entry something", disabled=True)
entry2.grid(row=1, column=1)

card.box(expand=True, padx=10, pady=10)

root.mainloop()
