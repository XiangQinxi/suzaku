def color(color):
    c = Color()
    return c.get(color)


class Color:
    def get(self, color):
        typec = type(color)
        if typec is str:
            if color.startswith("#"):
                return self.get_color_hex(color)
            return self.get_color_name(color)
        elif typec is tuple or typec is list:
            if len(color) == 3:
                return self.get_color_rgb(color[0], color[1], color[2])
            elif len(color) == 4:
                return self.get_color_rgb(color[0], color[1], color[2], color[3])
            else:
                raise ValueError("Color tuple/list must have 3 (RGB) or 4 (RGBA) elements")

    def get_color_name(self, name: str):
        import skia
        try:
            color = getattr(skia, f"Color{name.upper()}")
        except:
            raise ValueError(f"Unknown color name: {name}")
        else:
            return color

    def get_color_rgb(self, r, g, b, a=255):
        import skia
        return skia.Color(r, g, b, a)

    def get_color_hex(self, hex: str):
        import skia
        hex_color = hex.lstrip('#')
        if len(hex_color) == 6:  # RRGGBB 格式，默认不透明(Alpha=255)
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            return skia.ColorSetRGB(r, g, b)  # 返回不透明颜色
        elif len(hex_color) == 8:  # AARRGGBB 格式(含 Alpha 通道)
            a = int(hex_color[0:2], 16)
            r = int(hex_color[2:4], 16)
            g = int(hex_color[4:6], 16)
            b = int(hex_color[6:8], 16)
            return skia.ColorSetARGB(a, r, g, b)  # 返回含透明度的颜色
        else:
            raise ValueError("HEX 颜色格式应为 #RRGGBB 或 #AARRGGBB")