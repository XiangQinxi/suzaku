# Suzaku 朱雀

Advanced UI module based on `skia-python`, `pyopengl` and `glfw`.

基于`skia-python`、`pyopengl`与`glfw`高级界面库。

> Still under developing... / 正在抓紧制作中...
> 
> Evaluate out current achievements by downloading this project while it is still under development.
> 
> 您可以下载正在开发的版本来进行评估。
> 

---

## Basic Example / 简单示例

```bash
python3 -m suzaku
```

### 0.0.4
![0.0.4.png](https://youke1.picui.cn/s1/2025/08/17/68a1c75ec1ac1.png)

### 0.0.2a1
> This is an old version of the design, and it will be re-enabled in the future.
>
> 这个是老版本的设计，未来将会将它重新启用

![0.0.2a1.png](https://youke1.picui.cn/s1/2025/08/02/688dd38fc1d9a.png)
)

## How it Works / 原理
### Basic Pricinples / 基础原理
`SkApp` manages all `SkWindow` objects. We may consider each of the visible elements and ocmponents as a `SkWidget` in `SkWindow`.

`SkApp`管理着所有的`SkWindow`。我们将每一个可视化的元素&组件视为一个个的`SkWidget`，居于`SkWindow`中。

A number of properties are owned by `SkWidget`, telling `SkWindow` how it should be drawn. `SkWidget` components are added to the window via`SkWindow.add_draw()`, then be drawn by `SkWindow.draw()`.

`SkWidget`具有一个个属性，告诉`SkWindow`自己该如何被绘制，用`SkWindow.add_draw()`将自己的绘制方式加入进去，然后在`SkWindow.draw()`中被一个个的绘制在画布上。

## Layout / 布局
**Under construction / 正在开发**

## Naming / 取名
Suzaku is one of the four mythical beasts in ancient China. ~~Sounds cool isn't it?~~

`suzaku`是朱雀的意思，朱雀是中国古代的四大神兽之一。~~取这名呢感觉很霸气，先占个名先。~~

## Plans / 计划
It may be compatible with multiple frameworks in the future, such as `SDL2`.
可能后续会兼容多个框架，如`SDL2`。
