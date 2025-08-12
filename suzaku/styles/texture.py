import os
import os.path

import skia


class SkAcrylic:
    def acrylic(self, canvas: skia.Canvas):
        path = current_dir = os.path.dirname(os.path.abspath(__file__))
        image = skia.Image.open(os.path.join(path, "acrylic.jpg"))
        blur_filter = skia.ImageFilters.Blur(
            sigmaX=5.0,  # 水平模糊强度
            sigmaY=5.0,  # 垂直模糊强度
            input=None,  # 直接作用于图像
            cropRect=None,  # 可选：限制模糊范围
        )
        paint = skia.Paint(ImageFilter=blur_filter)
        canvas.drawImage(image=image, top=-self.root_x, left=-self.root_y, paint=paint)
