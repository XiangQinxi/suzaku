import suzaku as sk

root = sk.Sk()

sk.SkText(root, text="Loaded default font: " +
          sk.default_font.getTypeface().getFamilyName()).box("top", 0, 0)

root.run()
