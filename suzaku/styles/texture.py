import skia


class SkAcrylic:
    def acrylic(self, canvas: skia.Canvas):
        canvas.drawImage()

    @staticmethod
    def _blur(style: skia.BlurStyle | None = None, sigma: float = 5.0):
        if not style:
            style = skia.kNormal_BlurStyle
        return skia.MaskFilter.MakeBlur(style, sigma)

    def _draw_blur(self, paint: skia.Paint, style=None, sigma=None):
        paint.setMaskFilter(self._blur(style, sigma))

