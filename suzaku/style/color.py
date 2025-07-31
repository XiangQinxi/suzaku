def color(color):
    c = Color()
    return c.get(color)


class Color:
    def get(self, color):
        typec = type(color)
        if typec is str:
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
