import suzaku

root = suzaku.Sk()

default_theme = suzaku.SkTheme.INTERNAL_THEMES["default.light"]

button = suzaku.SkTextButton(root, text="Test button").box(padx=20, pady=50)
button.apply_theme(default_theme.special("SkButton:rest", background="red"))

root.mainloop()