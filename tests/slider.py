from suzaku import *

root = Sk(size=(400, 300), title="Minimal", minsize=(360, 80), theme=light_theme)
titlebar = titlebar(root)


def switch():
    if switch_theme.checked:
        root.apply_theme(dark_theme)
    else:
        root.apply_theme(light_theme)


switch_theme = SkSwitch(titlebar, text="Dark mode", command=switch).box(
    side="right",
    padx=0,
)

slider = SkSlider(root).box(side="top")

root.mainloop()
