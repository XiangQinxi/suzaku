
# Suzuka

Based on `skia-python`, `pyopengl` and `glfw` advanced interface libraries

Under development...

You can download it yourself to preview my current progress

> [查阅中文文档？](https://github.com/XiangQinxi/suzaku/blob/master/README-zh_hans.md)

---

## Simple Example

![v0.0.1a1.png](https://youke1.picui.cn/s1/2025/07/29/68888666134bf.png)

```python
from suzaku import *

app = SkApp()
window = SkWindow()
btn = SkButton(window, text="Hello World")
btn.place(10, 10)
app.run()
```

With Layout

![VBox.png](https://youke1.picui.cn/s1/2025/08/01/688c4cbfe26ec.png)

```python
from suzaku import *

app = SkApp()
window = SkWindow()

for i in range(2):
    SkButton(window, text=f"Button {i+1}").vbox(padx=10, pady=10)

app.run()
```

## Principle
### Basic Principle
`SkApp` manages all `SkWindow`s. We regard each visual element & component as individual `SkVisual`s, residing within `SkWindow`s.
`SkVisual`s have various properties that tell `SkWindow` how they should be drawn. They add their drawing methods using `SkWindow.add_draw()`, and then get drawn one by one on the canvas in `SkWindow.draw()`.

## Layout
###

## Naming Reason
`suzuka` means "Vermilion Bird", which is one of the four legendary神兽 in ancient Chinese mythology. I chose this name because it sounds powerful and霸气, so I'm claiming it first.