import ctypes
import collections

import glfw

import skia
import numpy as np


class _GLFWimage(ctypes.Structure):
    """
    GLFW图像包装器（纯Skia实现，无PIL依赖）
    """

    _fields_ = [
        ("width", ctypes.c_int),
        ("height", ctypes.c_int),
        ("pixels", ctypes.POINTER(ctypes.c_ubyte)),
    ]

    GLFWimage = collections.namedtuple("GLFWimage", ["width", "height", "pixels"])

    def __init__(self):
        ctypes.Structure.__init__(self)
        self.width = 0
        self.height = 0
        self.pixels = None
        self.pixels_array = None

    def wrap(self, image: skia.Image):
        """
        包装skia.Image为GLFW可用的格式
        Args:
            image: skia.Image对象（必须为RGBA格式）
        """
        # 确保图像是RGBA格式
        if not isinstance(image, skia.Image):
            raise TypeError("只支持skia.Image类型")

        # 获取像素数据
        self.width, self.height = image.width(), image.height()
        pixmap = skia.Pixmap()
        if not image.peekPixels(pixmap):
            # 如果无法直接访问像素，转为光栅图像
            image = image.makeRasterImage()
            if not image.peekPixels(pixmap):
                raise RuntimeError("无法获取图像像素数据")

        # 转换为连续的numpy数组（形状为[height, width, 4]）
        pixels_np = np.array(pixmap, copy=False).reshape(self.height, self.width, 4)

        # 创建ctypes数组并设置指针
        array_type = ctypes.c_ubyte * (4 * self.width * self.height)
        self.pixels_array = array_type()
        ctypes.memmove(
            self.pixels_array,
            pixels_np.ctypes.data_as(ctypes.POINTER(ctypes.c_ubyte)),
            len(self.pixels_array),
        )
        self.pixels = ctypes.cast(self.pixels_array, ctypes.POINTER(ctypes.c_ubyte))

    def unwrap(self):
        """
        返回解包后的数据（兼容原接口）
        """
        if not self.pixels_array:
            return self.GLFWimage(self.width, self.height, None)

        # 将一维数组转为三维结构[height][width][4]
        pixels_3d = [
            [
                [self.pixels_array[(i * self.width + j) * 4 + k] for k in range(4)]
                for j in range(self.width)
            ]
            for i in range(self.height)
        ]
        return self.GLFWimage(self.width, self.height, pixels_3d)


from glfw.library import glfw as _glfw


def set_window_icon(window, count, images):
    """
    Sets the icon for the specified window.

    Wrapper for:
        void glfwSetWindowIcon(GLFWwindow* window, int count, const GLFWimage* images);
    """
    if count == 1 and (not hasattr(images, "__len__") or len(images) == 3):
        # Stay compatible to calls passing a single icon
        images = [images]
    array_type = _GLFWimage * count
    _images = array_type()
    for i, image in enumerate(images):
        _images[i].wrap(image)
    _glfw.glfwSetWindowIcon(window, count, _images)


# 创建skia图像
import os.path

icon1_path = os.path.abspath(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..",
        "suzaku",
        "resources",
        "imgs",
        "icon.ico",
    )
)
image = skia.Image.open(icon1_path)

# 包装为GLFW格式
glfw_image = _GLFWimage()
glfw_image.wrap(image)  # 自动处理RGBA转换

# 现在可以传递给GLFW函数
# 例如设置窗口图标：

glfw.init()
window = glfw.create_window(640, 480, "GLFW Icon Test", None, None)
glfw.set_window_icon(window, 1, ctypes.byref(glfw_image))
