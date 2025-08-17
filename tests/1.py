import glfw
import ctypes
import skia


# 确保您的GLFW绑定中已有以下结构体定义
class _GLFWimage(ctypes.Structure):
    _fields_ = [
        ("width", ctypes.c_int),
        ("height", ctypes.c_int),
        ("pixels", ctypes.POINTER(ctypes.c_ubyte))
    ]


# 使用Skia加载图像并转换为GLFW需要的格式（修复版本）
def load_icon_with_skia(file_path):
    """
    使用Skia加载图像并转换为GLFW兼容格式
    :param file_path: 图像文件路径
    :return: 包含width, height, pixels的字典
    """
    # 使用Skia加载图像
    image = skia.Image.open(file_path)
    if not image:
        raise ValueError(f"无法加载图像: {file_path}")

    # 获取图像尺寸
    width = image.width()
    height = image.height()

    # 创建目标图像信息（RGBA格式）
    target_info = skia.ImageInfo.Make(
        width,
        height,
        skia.ColorType.kRGBA_8888_ColorType,
        skia.AlphaType.kPremul_AlphaType
    )

    # 创建目标像素映射
    target_pixmap = skia.Pixmap()

    # 分配足够的内存来存储RGBA像素数据
    buffer_size = width * height * 4
    pixel_buffer = bytearray(buffer_size)

    # 设置目标像素映射
    if not target_pixmap.reset(target_info, pixel_buffer, width * 4):
        raise RuntimeError("无法重置像素映射")

    # 将图像像素读取到目标像素映射
    if not image.readPixels(target_pixmap, 0, 0):
        # 如果直接读取失败，尝试通过Surface绘制
        surface = skia.Surface.MakeRasterDirect(target_pixmap)
        if surface:
            surface.getCanvas().drawImage(image, 0, 0)
        else:
            raise RuntimeError("无法读取图像像素")

    # 转换为ctypes数组
    buffer_type = ctypes.c_ubyte * len(pixel_buffer)
    ctypes_buffer = buffer_type.from_buffer_copy(pixel_buffer)

    return {
        "width": width,
        "height": height,
        "pixels": ctypes_buffer
    }


# 主程序
def main():
    # 初始化GLFW
    if not glfw.init():
        return

    # 创建窗口
    window = glfw.create_window(800, 600, "Skia + GLFW Demo", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    # 使用Skia加载并设置窗口图标
    try:
        # 加载图标（支持PNG、JPEG等格式）
        icon = load_icon_with_skia("C:\\suzaku\\suzaku\\resources\\icon.ico")

        # 调用您提供的set_window_icon函数
        glfw.set_window_icon(window, 1, [icon])
        print("窗口图标设置成功")
    except Exception as e:
        print(f"图标加载失败: {e}")

    # 主循环
    while not glfw.window_should_close(window):
        glfw.poll_events()
        glfw.swap_buffers(window)

    glfw.terminate()


if __name__ == "__main__":
    main()
