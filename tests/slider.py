from suzaku import *

root = Sk(size=(400, 300), title="Slider Test", minsize=(360, 80), theme=light_theme)

slider = SkSlider(root, tick=10).fixed(10, 10, 200, 20)

root.mainloop()
