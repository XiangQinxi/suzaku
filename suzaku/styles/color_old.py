def color(_):
    """

    颜色对象工厂函数

    根据输入参数类型自动转换颜色格式，支持以下格式：
    - 颜色名称字符串(如 'RED')
    - 十六进制字符串(如 '#RRGGBB' 或 '#AARRGGBB')
    - RGB/RGBA 元组或列表(3或4个元素)

    :param _ 颜色参数，支持多种格式的输入
    :return

    .. note::
        >>> color('red')
        >>> color('#ff0000')
        >>> color((255, 0, 0))

    """
    typec = type(_)
    if typec is str:
        if _.startswith("#"):
            return get_color_hex(_)
        return get_color_name(_)
    elif typec is tuple or typec is list:
        if len(_) == 3:
            return get_color_rgba(_[0], _[1], _[2])
        elif len(_) == 4:
            return get_color_rgba(_[0], _[1], _[2], _[3])
        else:
            raise ValueError("Color tuple/list must have 3 (RGB) or 4 (RGBA) elements")
    return None


def get_color_name(name: str):
    """转换颜色名称字符串为Skia颜色

    Args:
        name: 颜色名称(如 'RED')

    Returns:
        skia.Color: 对应的预定义颜色对象

    Raises:
        ValueError: 颜色名称不存在时抛出
    """
    import skia

    try:
        _ = getattr(skia, f"Color{name.upper()}")
    except:
        raise ValueError(f"Unknown color name: {name}")
    else:
        return _


def get_color_rgba(r, g, b, a=255):
    """
    转换RGB/RGBA值为Skia颜色

    Args:
        r: 红色通道 (0-255)
        g: 绿色通道 (0-255)
        b: 蓝色通道 (0-255)
        a: 透明度通道 (0-255, 默认255)

    Returns:
        skia.Color: 对应的RGBA颜色对象
    """
    import skia

    return skia.Color(r, g, b, a)


def get_color_hex(_: str):
    """
    转换十六进制颜色字符串为Skia颜色

    Args:
        _: 十六进制颜色字符串(支持 #RRGGBB 和 #AARRGGBB 格式)

    Returns:
        skia.Color: 对应的RGBA颜色对象

    Raises:
        ValueError: 当十六进制格式无效时抛出
    """
    import skia

    hex_color = _.lstrip("#")
    if len(hex_color) == 6:  # RGB 格式，默认不透明(Alpha=255)
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return skia.ColorSetRGB(r, g, b)  # 返回不透明颜色
    elif len(hex_color) == 8:  # ARGB 格式(含 Alpha 通道)
        a = int(hex_color[0:2], 16)
        r = int(hex_color[2:4], 16)
        g = int(hex_color[4:6], 16)
        b = int(hex_color[6:8], 16)
        return skia.ColorSetARGB(a, r, g, b)  # 返回含透明度的颜色
    else:
        raise ValueError("HEX 颜色格式应为 #RRGGBB 或 #AARRGGBB")
