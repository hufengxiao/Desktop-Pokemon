"""
资源加载模块
负责加载和管理图像、动画等资源
"""

from pathlib import Path
from PySide6.QtGui import QPixmap, QMovie
from PySide6.QtCore import QSize


class ResourceLoader:
    """资源加载器"""

    def __init__(self, sprite_dir):
        """
        初始化资源加载器

        Args:
            sprite_dir: 精灵图资源目录路径
        """
        self.sprite_dir = Path(sprite_dir)
        self.cached_pixmaps = {}  # Cache static images
        self.cached_movies = {}  # Cache animations

        print(f"[Resource] Resource directory: {self.sprite_dir}")

    def load_pixmap(self, filename, size=None):
        """
        加载静态图像

        Args:
            filename: 文件名（相对于 sprite_dir）
            size: 可选的缩放尺寸 (width, height)

        Returns:
            QPixmap 对象
        """
        cache_key = f"{filename}_{size}"

        if cache_key in self.cached_pixmaps:
            return self.cached_pixmaps[cache_key]

        file_path = self.sprite_dir / filename

        if not file_path.exists():
            print(f"[Resource] Warning: Image file not found: {file_path}")
            return None

        pixmap = QPixmap(str(file_path))

        if pixmap.isNull():
            print(f"[Resource] Warning: Failed to load image: {file_path}")
            return None

        # 如果指定了尺寸，则缩放
        if size:
            pixmap = pixmap.scaled(
                QSize(*size),
                aspectRatioMode=1,  # KeepAspectRatio
                transformMode=1  # SmoothTransformation
            )

        self.cached_pixmaps[cache_key] = pixmap
        print(f"[Resource] Loaded image: {filename}")
        return pixmap

    def load_movie(self, filename, size=None):
        """
        加载动画（GIF）

        Args:
            filename: 文件名（相对于 sprite_dir）
            size: 可选的缩放尺寸 (width, height)

        Returns:
            QMovie 对象
        """
        file_path = self.sprite_dir / filename

        if not file_path.exists():
            print(f"[Resource] Warning: Animation file not found: {file_path}")
            return None

        movie = QMovie(str(file_path))

        if not movie.isValid():
            print(f"[Resource] Warning: Failed to load animation: {file_path}")
            return None

        # 如果指定了尺寸，则缩放
        if size:
            movie.setScaledSize(QSize(*size))

        print(f"[Resource] Loaded animation: {filename}")
        return movie

    def get_animation_path(self, animation_name):
        """
        获取动画文件路径

        Args:
            animation_name: 动画名称（如 'idle', 'click'）

        Returns:
            文件路径字符串，如果文件不存在则返回 None
        """
        # 尝试 GIF 格式
        gif_path = self.sprite_dir / f"{animation_name}.gif"
        if gif_path.exists():
            return str(gif_path)

        # 尝试 PNG 格式
        png_path = self.sprite_dir / f"{animation_name}.png"
        if png_path.exists():
            return str(png_path)

        print(f"[Resource] Warning: Animation not found: '{animation_name}'")
        return None

    def list_available_animations(self):
        """
        列出可用的动画文件

        Returns:
            动画名称列表
        """
        animations = []

        if not self.sprite_dir.exists():
            print(f"[Resource] Warning: Resource directory not found: {self.sprite_dir}")
            return animations

        # 扫描 GIF 和 PNG 文件
        for ext in ['*.gif', '*.png']:
            for file in self.sprite_dir.glob(ext):
                animation_name = file.stem  # 不带扩展名的文件名
                if animation_name not in animations:
                    animations.append(animation_name)

        print(f"[Resource] Available animations: {animations}")
        return animations

    def clear_cache(self):
        """清空缓存"""
        self.cached_pixmaps.clear()
        self.cached_movies.clear()
        print("[Resource] Cache cleared")
