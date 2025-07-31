# Suzuka 朱雀

基于`skia-python`、`pyopengl`与`glfw`高级界面库

正在抓紧制作中...

正处于开发中可以自行下载，来预览我暂时的成果

---

## 简单示例

![v0.0.1a1.png](https://youke1.picui.cn/s1/2025/07/29/68888666134bf.png)

```python
from suzaku import *

app = SkApp()
window = SkWindow()
btn = SkButton(window, text="Hello World")
btn.place(10, 10)
app.run()
```

## 原理
### 基础原理
`SkApp`管理着所有的`SkWindow`。我们将每一个可视化的元素&组件视为一个个的`SkVisual`，居于`SkWindow`中。
`SkVisual`具有一个个属性，告诉`SkWindow`自己该如何被绘制，用`SkWindow.add_draw()`将自己的绘制方式加入进去，然后在`SkWindow.draw()`中被一个个的绘制在画布上。

## 布局
###

## 取名原因
`suzuka`是朱雀的意思，朱雀是中国古代的四大神兽之一。取这名呢感觉很霸气，先占个名先。

## 计划
我将会使用跨平台的`Canvas`库，用`svg`来绘制图形。