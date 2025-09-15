import skia


def draw_inset_rounded_rect(
    canvas, rect: skia.Rect, radius: float, shadow_params: dict
):
    """
    绘制带内阴影的圆角矩形

    参数:
        canvas: skia.Canvas
        rect: skia.Rect 目标矩形
        radius: 圆角半径
        shadow_params: {
            'color': skia.Color,  # 阴影颜色
            'blur_sigma': float,  # 模糊强度
            'offset': (dx, dy),   # 阴影偏移
            'inset': float        # 内缩距离
        }
    """
    # 1. 创建圆角矩形路径（外框）
    outer_path = skia.Path()
    outer_path.addRoundRect(rect, radius, radius)

    # 2. 创建内缩路径（用于裁剪）
    inset_rect = rect.makeInset(shadow_params["inset"], shadow_params["inset"])
    inner_path = skia.Path()
    inner_path.addRoundRect(
        inset_rect,
        max(0, radius - shadow_params["inset"]),
        max(0, radius - shadow_params["inset"]),
    )

    # 3. 设置阴影效果
    paint = skia.Paint(
        Color=shadow_params["color"],
        MaskFilter=skia.MaskFilter.MakeBlur(
            skia.kNormal_BlurStyle, shadow_params["blur_sigma"], respectCTM=True
        ),
        AntiAlias=True,
    )

    # 4. 使用差值路径绘制内阴影
    canvas.save()
    canvas.clipPath(outer_path, skia.ClipOp.kIntersect, True)
    canvas.clipPath(inner_path, skia.ClipOp.kDifference, True)
    canvas.translate(shadow_params["offset"][0], shadow_params["offset"][1])
    canvas.drawPath(outer_path, paint)
    canvas.restore()

    # 5. 可选：绘制边框
    border_paint = skia.Paint(
        Color=skia.ColorBLACK,
        StrokeWidth=1,
        Style=skia.Paint.kStroke_Style,
        AntiAlias=True,
    )
    canvas.drawRoundRect(rect, radius, radius, border_paint)


# 示例用法
width, height = 400, 300
surface = skia.Surface(width, height)
canvas = surface.getCanvas()
canvas.clear(skia.ColorWHITE)

# 定义圆角矩形
rect = skia.Rect.MakeLTRB(50, 50, 350, 250)
radius = 20

# 绘制内阴影
draw_inset_rounded_rect(
    canvas,
    rect,
    radius,
    shadow_params={
        "color": skia.Color(0, 0, 0, 200),  # 半透明黑色
        "blur_sigma": 4.0,
        "offset": (2, 2),  # 右下偏移
        "inset": 8.0,  # 内缩8像素
    },
)

# 保存结果
surface.makeImageSnapshot().save("inset_shadow_rect.png", skia.kPNG)
