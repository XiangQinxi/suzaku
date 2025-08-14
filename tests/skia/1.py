import skia

surface = skia.Surface(256, 256)
print(type(surface))
with surface as canvas:
    print(type(canvas))
    canvas.save()
    canvas.translate(128., 128.)
    canvas.rotate(45.)
    rect = skia.Rect(-90.5, -90.5, 90.5, 90.5)
    paint = skia.Paint(Color=skia.Color(0, 0, 255))
    canvas.drawRect(rect, paint)
    canvas.restore()

image = surface.makeImageSnapshot()
image.save('output.png', skia.kPNG)