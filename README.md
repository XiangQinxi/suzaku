# Suzaku 朱雀

Advanced UI module based on `skia-python`, `pyopengl` and `glfw`.

基于`skia-python`、`pyopengl`与`glfw`高级界面库。

> Still under developing... / 正在抓紧制作中...
> 
> versions under dev are provided for evulation purposes.
> 
> 您可以下载正在开发的版本来进行评估。
> 

---

## Basic Example / 简单示例

```bash
python3 -m suzaku
```

### 0.1.1
![0.1.1.png](https://i.postimg.cc/nLQnc4Kx/18c79b883afd9b6d1b44139b6fa2f1ec.png)
![0.1.1-Dark.png](https://i.postimg.cc/gjc9R8hn/d3b64d01e06c87b8abc26efb99aa0663.png)

## Layout / 布局
Each component can use layout methods to arrange itself using, for instance, `widget.box()`, which is similar to how things work in `tkinter`. Comparing to other solutions used in Qt or other UI frameworks, we believe this approach is more simple and user-friendly.

每个组件都可以使用布局方法来布局自己，例如`widget.box()`，类似于`tkinter`，我觉得这样更简洁易用点。

### Box
It can be considered a simplified version of `tkinter.pack`—without `anchor`, `expand`, or `fill` attributes, only `side`, `expand`, `padx`, and `pady` attributes.  
(In the future, `ipadx` and `ipady` attributes will be added.)
Each container can only choose one layout direction. For example, 
you cannot use both `widget.box(side="left")` and `widget.box(side="right")` simultaneously.

可以被称为`tkinter.pack`的简易版，就是没有`anchor`、`expand`、`fill`属性，只有`side`、`expand`、`padx`、`pady`属性。
（未来会做`ipadx`、`ipady`属性）
每个容器只能选择一种布局方向，例如，不能同时使用`widget.box(side="left")`和`widget.box(side="right")`。

### Vertical layout / 垂直布局
The default layout is vertical.

默认为垂直方向布局。
```python
widget.box()
```
### Horizontal layout / 水平布局
```python
widget.box(side="left")
widget2.box(side="right")
```

## How it Works / 原理
### Basic Pricinples / 基础原理
Several (only 2 now actually) modules are used to provide several (same, only 2 now) window base, to enable us showing and modifying the window. After that, `skia-python` is used as a drawing backend.

使用`glfw`作为窗口管理库，使用`pyopengl`作为后端，使用`skia-python`作为绘画后端。

## Naming / 取名
Suzaku is one of the four mythical beasts in ancient China. ~~Sounds cool isn't it?~~

`suzaku`是朱雀的意思，朱雀是中国古代的四大神兽之一。~~取这名呢感觉很霸气，先占个名先。~~

## Plans / 计划
It may be compatible with multiple frameworks in the future, such as `SDL2`.

可能后续会兼容多个框架，如`SDL2`。
