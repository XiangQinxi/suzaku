import suzaku as sk

root = sk.Sk(size=(512, 512))
sk.SkImage(
    root,
    "C:\\Users\\Xiang\\PycharmProjects\\suzaku\\suzaku\\resources\\imgs\\logo.png",
    0,
    0,
    256,
    256,
).fixed(x=10, y=10, width=256, height=256)
root.mainloop()
