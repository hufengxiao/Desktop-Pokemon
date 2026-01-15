"""
生成占位符图像资源
用于开发阶段测试，真实资源准备好后可替换
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_placeholder_image(size, text, filename, bg_color=(100, 149, 237, 200)):
    """
    创建带文字的占位符图像

    Args:
        size: 图像尺寸 (width, height)
        text: 显示的文字
        filename: 保存的文件名
        bg_color: 背景颜色 RGBA
    """
    # 创建带透明通道的图像
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 绘制圆形背景
    circle_margin = 10
    draw.ellipse(
        [circle_margin, circle_margin, size[0]-circle_margin, size[1]-circle_margin],
        fill=bg_color,
        outline=(255, 255, 255, 255),
        width=3
    )

    # 绘制简单的"脸"
    eye_y = size[1] // 3
    eye_size = size[0] // 10

    # 左眼
    draw.ellipse(
        [size[0]//3 - eye_size, eye_y - eye_size,
         size[0]//3 + eye_size, eye_y + eye_size],
        fill=(0, 0, 0, 255)
    )

    # 右眼
    draw.ellipse(
        [2*size[0]//3 - eye_size, eye_y - eye_size,
         2*size[0]//3 + eye_size, eye_y + eye_size],
        fill=(0, 0, 0, 255)
    )

    # 嘴巴（微笑）
    mouth_y = 2*size[1]//3
    draw.arc(
        [size[0]//4, mouth_y - size[0]//6,
         3*size[0]//4, mouth_y + size[0]//8],
        start=0, end=180,
        fill=(0, 0, 0, 255),
        width=3
    )

    # 添加文字标签
    try:
        # 尝试使用默认字体
        font = ImageFont.truetype("arial.ttf", size[0]//12)
    except:
        font = ImageFont.load_default()

    # 计算文字位置（底部居中）
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = (size[0] - text_width) // 2
    text_y = size[1] - text_height - 15

    # 绘制文字
    draw.text((text_x, text_y), text, fill=(255, 255, 255, 255), font=font)

    # 保存图像
    img.save(filename, 'PNG')
    print(f"[OK] 已创建: {filename}")


def create_animated_placeholder():
    """
    创建简单的 GIF 动画占位符
    """
    frames = []
    size = (128, 128)

    # 创建多帧，模拟"呼吸"效果
    for i in range(8):
        img = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # 计算缩放比例（呼吸效果）
        scale = 1.0 + 0.1 * (i / 8.0)
        margin = int(10 * scale)

        # 绘制圆形
        color_intensity = int(200 + 30 * (i / 8.0))
        bg_color = (100, 149, 237, min(255, color_intensity))

        draw.ellipse(
            [margin, margin, size[0]-margin, size[1]-margin],
            fill=bg_color,
            outline=(255, 255, 255, 255),
            width=3
        )

        # 眼睛
        eye_y = size[1] // 3
        eye_size = size[0] // 10

        # 根据帧数改变眼睛（模拟眨眼）
        if i == 4:  # 第5帧闭眼
            # 闭眼用线条表示
            draw.line([size[0]//3 - eye_size, eye_y, size[0]//3 + eye_size, eye_y],
                     fill=(0, 0, 0, 255), width=2)
            draw.line([2*size[0]//3 - eye_size, eye_y, 2*size[0]//3 + eye_size, eye_y],
                     fill=(0, 0, 0, 255), width=2)
        else:
            # 睁眼
            draw.ellipse([size[0]//3 - eye_size, eye_y - eye_size,
                         size[0]//3 + eye_size, eye_y + eye_size], fill=(0, 0, 0, 255))
            draw.ellipse([2*size[0]//3 - eye_size, eye_y - eye_size,
                         2*size[0]//3 + eye_size, eye_y + eye_size], fill=(0, 0, 0, 255))

        # 嘴巴
        mouth_y = 2*size[1]//3
        draw.arc([size[0]//4, mouth_y - size[0]//6,
                 3*size[0]//4, mouth_y + size[0]//8],
                start=0, end=180, fill=(0, 0, 0, 255), width=3)

        frames.append(img)

    # 保存为 GIF
    filename = 'assets/sprites/pikachu/idle.gif'
    frames[0].save(
        filename,
        save_all=True,
        append_images=frames[1:],
        duration=150,  # 每帧150毫秒
        loop=0,  # 无限循环
        transparency=0,
        disposal=2
    )
    print(f"[OK] 已创建动画: {filename}")


def create_click_reaction():
    """
    创建点击反应动画（跳跃效果）
    """
    frames = []
    size = (128, 128)

    # 创建跳跃动画帧
    jump_sequence = [0, -10, -20, -25, -20, -10, 0]

    for offset_y in jump_sequence:
        img = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # 绘制圆形（带Y轴偏移）
        margin = 10
        bg_color = (255, 193, 37, 220)  # 金黄色（更像皮卡丘）

        adjusted_y_start = margin + offset_y
        adjusted_y_end = size[1] - margin + offset_y

        draw.ellipse(
            [margin, adjusted_y_start, size[0]-margin, adjusted_y_end],
            fill=bg_color,
            outline=(255, 255, 255, 255),
            width=3
        )

        # 眼睛（开心的样子，变成 ^ ^）
        eye_y = size[1] // 3 + offset_y
        eye_size = size[0] // 10

        # 左眼 ^
        draw.arc([size[0]//3 - eye_size, eye_y - eye_size//2,
                 size[0]//3 + eye_size, eye_y + eye_size//2],
                start=180, end=360, fill=(0, 0, 0, 255), width=3)

        # 右眼 ^
        draw.arc([2*size[0]//3 - eye_size, eye_y - eye_size//2,
                 2*size[0]//3 + eye_size, eye_y + eye_size//2],
                start=180, end=360, fill=(0, 0, 0, 255), width=3)

        # 嘴巴（大笑）
        mouth_y = 2*size[1]//3 + offset_y
        draw.arc([size[0]//4, mouth_y - size[0]//8,
                 3*size[0]//4, mouth_y + size[0]//6],
                start=0, end=180, fill=(0, 0, 0, 255), width=4)

        frames.append(img)

    # 保存为 GIF
    filename = 'assets/sprites/pikachu/click.gif'
    frames[0].save(
        filename,
        save_all=True,
        append_images=frames[1:],
        duration=80,  # 每帧80毫秒，更快
        loop=0,
        transparency=0,
        disposal=2
    )
    print(f"[OK] 已创建点击动画: {filename}")


if __name__ == '__main__':
    print("正在生成占位符图像...")
    print()

    # 确保目录存在
    os.makedirs('assets/sprites/pikachu', exist_ok=True)

    # 创建待机动画
    create_animated_placeholder()

    # 创建点击反应动画
    create_click_reaction()

    # 创建应用图标
    create_placeholder_image(
        (256, 256),
        "Desktop-Pokemon",
        "assets/icons/app_icon.png",
        bg_color=(255, 193, 37, 255)
    )

    print()
    print("=" * 50)
    print("占位符图像生成完成！")
    print("真实资源准备好后，请替换 assets/sprites/pikachu/ 下的文件")
    print("=" * 50)
