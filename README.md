# Suzaku 朱雀

Advanced UI module based on `skia-python`, `pyopengl` and `glfw`.

> Still under developing...
> 
> versions under dev are provided for evaluation purposes.


---

## Basic Example

```bash
python3 -m suzaku
```

### The Latest Snapshot
![0.2.1.png](./snapshot.png)

### 0.1.9
![0.1.9.png](https://i.postimg.cc/HxvvFF3B/0-1-9.png)
![0.1.9-Dark.png](https://i.postimg.cc/2yBGMyVJ/0-1-9-Dark.png)
![0.1.9-SV.png](https://i.postimg.cc/1z5LT0s5/0-1-9-SV.png)

### 0.1.1
![0.1.1.png](https://i.postimg.cc/nLQnc4Kx/18c79b883afd9b6d1b44139b6fa2f1ec.png)
![0.1.1-Dark.png](https://i.postimg.cc/gjc9R8hn/d3b64d01e06c87b8abc26efb99aa0663.png)

## Installation

### Using pip
```bash
pip install suzaku
```

### From source
```bash
git clone https://github.com/yourusername/suzaku.git
cd suzaku
pip install -e .
```

## Features

- **Modern UI**: Beautiful, modern UI components with customizable themes
- **Easy Layout**: Simple box-based layout system, similar to tkinter
- **Cross-platform**: Works on Windows, macOS, and Linux
- **Hardware Accelerated**: Uses OpenGL for rendering via skia-python
- **Event-driven**: Comprehensive event handling system
- **Themable**: Supports custom themes and built-in light/dark themes
- **Rich Component Set**: Wide range of UI components available

## Components

| Component | Description | Status |
|-----------|-------------|--------|
| SkApp | Application base | ✅ |
| SkWindow | Main window | ✅ |
| SkButton | Clickable button | ✅ |
| SkCard | Card container | ✅ |
| SkCheckBox | Checkbox | ✅ |
| SkCheckItem | Checkable menu item | ✅ |
| SkComboBox | Dropdown menu | ✅ |
| SkContainer | Base container | ✅ |
| SkEmpty | Empty placeholder | ✅ |
| SkEntry | Single-line input | ✅ |
| SkFrame | Frame container | ✅ |
| SkImage | Image display with color processing | ✅ |
| SkLabel | Text label | ✅ |
| SkLineInput | Line input | ✅ |
| SkListBox | List container | ✅ |
| SkListItem | List item | ✅ |
| SkMenu | Menu | ✅ |
| SkMenuBar | Menu bar | ✅ |
| SkMenuItem | Menu item | ✅ |
| SkMessageBox | Message box | ✅ |
| SkMultiLineInput | Multi-line input | ⛔ |
| SkPopup | Popup window | ✅ |
| SkPopupMenu | Popup menu | ✅ |
| SkRadioBox | Radio button group | ✅ |
| SkRadioItem | Radio button | ✅ |
| SkSeparator | Separator line | ✅ |
| SkSizeGrip | Window resize grip | ✅ |
| SkSlider | Slider control | ✅ |
| SkStack | Stack container | ✅ |
| SkSwitch | Toggle switch | ✅ |
| SkSwitchBox | Switch group | ✅ |
| SkTabBar | Tab bar | ✅ |
| SkTabButton | Tab button | ✅ |
| SkTabs | Tab container | ✅ |
| SkText | Text display | ✅ |
| SkTextButton | Text button | ✅ |
| SkTitleBar | Window title bar | ✅ |
| SkTreeView | Tree view | ⛔ |
| SkWidget | Base widget | ✅ |

## Layout

Each component can use layout methods to arrange itself using, for instance, `widget.box()`, which is similar to how things work in `tkinter`. Comparing to other solutions used in Qt or other UI frameworks, we believe this approach is more simple and user-friendly.

每个组件都可以使用布局方法来布局自己，例如`widget.box()`，类似于`tkinter`，我觉得这样更简洁易用点。

### Box Layout

It can be considered a simplified version of `tkinter.pack`—with `side`, `expand`, `padx`, `pady`, `ipadx`, and `ipady` attributes.
Each container can only choose one layout direction. For example, 
you cannot use both `widget.box(side="left")` and `widget.box(side="right")` simultaneously.

可以被称为`tkinter.pack`的简易版，包含`side`、`expand`、`padx`、`pady`、`ipadx`和`ipady`属性。
每个容器只能选择一种布局方向，例如，不能同时使用`widget.box(side="left")`和`widget.box(side="right")`。

#### Vertical layout / 垂直布局
The default layout is vertical.

默认为垂直方向布局。
```python
widget.box()
```

#### Horizontal layout / 水平布局
```python
widget.box(side="left")
widget2.box(side="right")
```

#### Layout with padding
```python
widget.box(padx=10, pady=5, ipadx=2, ipady=2)
```

#### Expanding widgets
```python
widget.box(expand=True)
```

### Grid Layout

Grid layout allows you to arrange widgets in a grid pattern.

```python
widget.grid(row=0, column=0)
widget2.grid(row=0, column=1)
widget3.grid(row=1, column=0, columnspan=2)
```

### Fixed Layout

Fixed layout allows you to position widgets at specific coordinates.

```python
widget.fixed(x=10, y=10, width=100, height=30)
```

## How it Works / 原理

### Basic Principles / 基础原理

- Uses `glfw` as window management library
- Uses `pyopengl` as rendering backend
- Uses `skia-python` for 2D graphics rendering
- Event-driven architecture for handling user interactions

使用`glfw`作为窗口管理库，使用`pyopengl`作为渲染后端，使用`skia-python`作为2D图形渲染库，采用事件驱动架构处理用户交互。

## Themes

Suzaku supports multiple themes, including:

- Light theme
- Dark theme
- Special themes (SV Light, SV Dark)

### Applying Themes

```python
from suzaku.styles.theme import SkTheme

# Load a theme
theme = SkTheme.load("path/to/theme.json")

# Apply theme to window
window.apply_theme(theme)
```

## Events

### Basic Event Handling

```python
# Bind a function to a widget event
widget.bind("click", lambda evt: print("Clicked!"))

# Bind to keyboard events
window.bind("key_press", lambda evt: print(f"Key pressed: {evt['key']}"))

# Bind to mouse events
widget.bind("mouse_enter", lambda evt: print("Mouse entered!"))
widget.bind("mouse_leave", lambda evt: print("Mouse left!"))
```

### Available Events

- `click`: Mouse click
- `double_click`: Double click
- `mouse_enter`: Mouse enters widget
- `mouse_leave`: Mouse leaves widget
- `mouse_press`: Mouse button pressed
- `mouse_release`: Mouse button released
- `key_press`: Key pressed
- `key_release`: Key released
- `focus_gain`: Widget gains focus
- `focus_loss`: Widget loses focus
- `resize`: Widget resized
- `configure`: Widget configured
- `update`: Widget updated
- `scroll`: Mouse wheel scrolled

## Examples

### Basic Application

```python
from suzaku import *

app = SkApp()

window = SkWindow(title="My App", size=(400, 300))

# Create a button
button = SkButton(window, text="Click Me")
button.box(padx=10, pady=10)
button.bind("click", lambda evt: print("Button clicked!"))

# Create a label
label = SkLabel(window, text="Hello, Suzaku!")
label.box(padx=10, pady=5)

window.update_layout()
app.run()
```

## Naming / 取名

Suzaku is one of the four mythical beasts in ancient China, representing the south and the element of fire. It symbolizes vitality, growth, and transformation.  

`suzaku`是中国古代的四大神兽之一，代表南方和火元素，象征着生命力、成长和变革。

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

## Plans / 计划

- Support for more frameworks (SDL2)
- Additional UI components
- Improved layout system
- Enhanced theme support
- Documentation improvements
- More examples and tutorials

## Credits

- [skia-python](https://github.com/kyamagu/skia-python) - Skia Python bindings
- [glfw](https://www.glfw.org/) - Window management
- [pyopengl](https://pypi.org/project/PyOpenGL/) - OpenGL bindings for Python

## Support

If you encounter any issues or have questions, please open an issue on the GitHub repository.

---

Enjoy using Suzaku!
