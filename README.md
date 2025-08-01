
# Suzuka

Based on `skia-python`, `pyopengl` and `glfw` advanced interface libraries

Under development...

You can download it yourself to preview my current progress

> [是否要查阅中文文档？](README-zh_hans.md)

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

## Principle
### Basic Principle
`SkApp` manages all `SkWindow`s. We regard each visual element & component as individual `SkVisual`s, residing within `SkWindow`s.
`SkVisual`s have various properties that tell `SkWindow` how they should be drawn. They add their drawing methods using `SkWindow.add_draw()`, and then get drawn one by one on the canvas in `SkWindow.draw()`.

## Layout
###

## Naming Reason
`suzuka` means "Vermilion Bird", which is one of the four legendary神兽 in ancient Chinese mythology. I chose this name because it sounds powerful and霸气, so I'm claiming it first.