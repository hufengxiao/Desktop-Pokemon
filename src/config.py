"""
配置管理模块
管理应用的各种配置参数
"""

import os
import json
from pathlib import Path


class Config:
    """应用配置类"""

    def __init__(self):
        # 项目根目录
        self.BASE_DIR = Path(__file__).resolve().parent.parent

        # 资源路径
        self.ASSETS_DIR = self.BASE_DIR / 'assets'
        self.SPRITES_DIR = self.ASSETS_DIR / 'sprites'
        self.SOUNDS_DIR = self.ASSETS_DIR / 'sounds'
        self.ICONS_DIR = self.ASSETS_DIR / 'icons'

        # 窗口配置
        self.WINDOW_SIZE = (128, 128)  # 窗口尺寸
        self.WINDOW_OPACITY = 1.0  # 窗口不透明度（1.0 = 完全不透明）

        # 默认宠物类型
        self.DEFAULT_PET = 'pikachu'

        # 动画配置
        self.ANIMATION_SPEED = 1.0  # 动画速度倍率

        # 配置文件路径
        self.CONFIG_FILE = self.BASE_DIR / 'config.json'

        # 加载用户配置
        self.load_config()

    def load_config(self):
        """从配置文件加载用户设置"""
        if self.CONFIG_FILE.exists():
            try:
                with open(self.CONFIG_FILE, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)

                # 更新配置
                self.window_x = user_config.get('window_x', None)
                self.window_y = user_config.get('window_y', None)
                self.WINDOW_OPACITY = user_config.get('opacity', 1.0)
                self.DEFAULT_PET = user_config.get('pet_type', 'pikachu')

                print(f"[Config] Loaded config file")
            except Exception as e:
                print(f"[Config] Failed to load config: {e}")
                self.window_x = None
                self.window_y = None
        else:
            self.window_x = None
            self.window_y = None

    def save_config(self, window_x=None, window_y=None):
        """保存配置到文件"""
        config_data = {
            'window_x': window_x if window_x is not None else self.window_x,
            'window_y': window_y if window_y is not None else self.window_y,
            'opacity': self.WINDOW_OPACITY,
            'pet_type': self.DEFAULT_PET
        }

        try:
            with open(self.CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=4, ensure_ascii=False)
            print(f"[Config] Config saved")
        except Exception as e:
            print(f"[Config] Failed to save config: {e}")

    def get_pet_sprite_dir(self, pet_name=None):
        """获取宠物精灵图目录"""
        if pet_name is None:
            pet_name = self.DEFAULT_PET
        return self.SPRITES_DIR / pet_name


# 全局配置实例
config = Config()
