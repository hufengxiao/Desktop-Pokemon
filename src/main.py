"""
Desktop-Pokemon 主入口
赛博桌宠应用
"""

import sys
import os

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from PySide6.QtWidgets import QApplication
from src.ui.pet_window import PetWindow


def main():
    """主函数"""
    print("=" * 60)
    print("  Desktop-Pokemon")
    print("=" * 60)
    print()

    # 创建应用实例
    app = QApplication(sys.argv)

    # 设置应用信息
    app.setApplicationName("Desktop-Pokemon")
    app.setOrganizationName("Desktop-Pokemon")

    # 创建主窗口
    window = PetWindow()
    window.show()

    print()
    print("[INFO] Desktop pet started!")
    print("[TIP] Left-drag to move, click to interact, right-click to exit")
    print()

    # 运行应用
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
