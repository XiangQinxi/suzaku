import suzaku as sk

root = sk.Sk(size=(512, 512))
sk.SkImage(root, "./suzaku/resources/imgs/logo.png", 0, 0, 1024, 1024).box(padx=0, pady=0)
root.mainloop()