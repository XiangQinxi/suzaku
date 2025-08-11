import skia

# 获取系统默认字体（通常是无衬线字体，如 Arial 或 Helvetica）
default_typeface = skia.Typeface()  # 无参数时返回系统默认字体
default_family = default_typeface.getFamilyName()

print("System Default Font Family:", default_family)