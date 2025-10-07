import suzaku

root = suzaku.Sk()

default_theme = suzaku.SkTheme.DEFAULT_THEME
special_theme = default_theme.special("SkButton:rest", bg="red")
print(special_theme.styles)

button = suzaku.SkTextButton(root, text="Test button").box(padx=20, pady=50)
button.apply_theme(special_theme)

root.mainloop()