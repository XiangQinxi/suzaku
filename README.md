# Suzaku 朱雀

Advanced UI module based on `skia-python`, `pyopengl` and `glfw`.

基于`skia-python`、`pyopengl`与`glfw`高级界面库。

> Still under developing... / 正在抓紧制作中...
> 
> Evaluate out current achievements by downloading this project whilt it is still under development.
> 
> 您可以下载正在开发的版本来进行评估。

---

## Basic Example / 简单示例

![v0.0.1a1.png (This image is stored on external site. If failed to load then check the URL.)](https://youke1.picui.cn/s1/2025/07/29/68888666134bf.png)

```python
from suzaku import *

app = SkApp()
window = SkWindow()
btn = SkButton(window, text="Hello World")
btn.place(10, 10)
app.run()
```

## How it Works / 原理
### Basic Pricinples / 基础原理
`SkApp` manages all `SkWindow` objects. We may consider each of the visible elements and ocmponents as a `SkVisual` in `SkWindow`.

`SkApp`管理着所有的`SkWindow`。我们将每一个可视化的元素&组件视为一个个的`SkVisual`，居于`SkWindow`中。

A number of properties are owned by `SkVisual`, telling `SkWindow` how it should be drawn. `SkVisual` components are added to the window via`SkWindow.add_draw()`, then be drawn by `SkWindow.draw()`.

`SkVisual`具有一个个属性，告诉`SkWindow`自己该如何被绘制，用`SkWindow.add_draw()`将自己的绘制方式加入进去，然后在`SkWindow.draw()`中被一个个的绘制在画布上。

## Layout / 布局
**Under construction / 正在开发**

## Naming / 取名
Suzaku is one of the four mythical beasts in ancient China. ~~Sounds cool isn't it?~~

`suzaku`是朱雀的意思，朱雀是中国古代的四大神兽之一。~~取这名呢感觉很霸气，先占个名先。~~

## Plans / 计划
`svg` in `Canvas` module will be used to draw shapes.

我将会使用跨平台的`Canvas`库，用`svg`来绘制图形。