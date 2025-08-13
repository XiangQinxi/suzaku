import skia
import numpy as np
import matplotlib.pyplot as plt

width, height = 200, 200
array = np.zeros((height, width, 4), dtype=np.uint8)

with skia.Surface(array) as canvas:
    canvas.drawCircle(100, 100, 40, skia.Paint(Color=skia.ColorGREEN))

plt.imshow(array)
plt.show()