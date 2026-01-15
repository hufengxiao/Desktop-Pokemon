"""
宠物窗口模块
实现透明、无边框、可拖拽的桌宠窗口
"""

from PySide6.QtWidgets import QWidget, QLabel, QMenu
from PySide6.QtCore import Qt, QPoint, QTimer
from PySide6.QtGui import QMovie, QCursor
from PIL import Image

from src.config import config
from src.core.resource_loader import ResourceLoader


class PetWindow(QWidget):
    """桌宠窗口类"""

    def __init__(self):
        super().__init__()

        # 初始化资源加载器
        self.resource_loader = ResourceLoader(config.get_pet_sprite_dir())

        # 当前动画状态
        self.current_animation = None
        self.idle_animation = None  # 待机动画
        self.click_animation = None  # 点击动画
        self.click_animation_duration = 2000  # 默认点击动画时长（毫秒）

        # 拖拽相关
        self.dragging = False
        self.drag_position = QPoint()
        self.drag_start_pos = QPoint()  # 记录拖拽起始位置

        # 初始化 UI
        self.init_ui()

        # 加载动画
        self.load_animations()

        # 播放待机动画
        self.play_idle_animation()

    def init_ui(self):
        """初始化用户界面"""
        # 设置窗口标志
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |  # 无边框
            Qt.WindowType.WindowStaysOnTopHint |  # 置顶
            Qt.WindowType.Tool  # 不在任务栏显示
        )

        # 设置背景透明
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # 设置窗口大小
        self.resize(*config.WINDOW_SIZE)

        # 创建标签用于显示动画
        self.animation_label = QLabel(self)
        self.animation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.animation_label.setGeometry(0, 0, *config.WINDOW_SIZE)

        # 设置窗口位置（如果有保存的位置）
        if config.window_x is not None and config.window_y is not None:
            self.move(config.window_x, config.window_y)
        else:
            # 默认位置：屏幕右下角
            screen = self.screen().geometry()
            self.move(
                screen.width() - self.width() - 50,
                screen.height() - self.height() - 100
            )

        # 设置窗口不透明度
        self.setWindowOpacity(config.WINDOW_OPACITY)

        # 设置鼠标形状
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        print("[Window] Window initialized")

    def get_gif_duration(self, gif_path):
        """
        计算 GIF 文件的总播放时长（毫秒）

        Args:
            gif_path: GIF 文件路径

        Returns:
            总时长（毫秒），如果出错返回默认值 2000
        """
        try:
            img = Image.open(gif_path)
            total_duration = 0
            frame_count = 0

            while True:
                try:
                    frame_duration = img.info.get('duration', 100)  # 默认 100ms
                    total_duration += frame_duration
                    frame_count += 1
                    img.seek(img.tell() + 1)
                except EOFError:
                    break

            print(f"[Window] GIF analysis: {frame_count} frames, {total_duration}ms total")
            return total_duration

        except Exception as e:
            print(f"[Window] Warning: Failed to analyze GIF duration: {e}")
            return 2000  # 默认 2 秒

    def load_animations(self):
        """加载所有动画资源"""
        # 列出可用动画
        available_animations = self.resource_loader.list_available_animations()

        if not available_animations:
            print("[Window] Warning: No animation resources found!")
            return

        # 加载待机动画
        idle_path = self.resource_loader.get_animation_path('idle')
        if idle_path:
            self.idle_animation = QMovie(idle_path)
            self.idle_animation.setScaledSize(self.animation_label.size())
            print("[Window] Idle animation loaded")

        # 加载点击动画
        click_path = self.resource_loader.get_animation_path('click')
        if click_path:
            self.click_animation = QMovie(click_path)
            self.click_animation.setScaledSize(self.animation_label.size())
            # 计算点击动画的实际时长
            self.click_animation_duration = self.get_gif_duration(click_path)
            print(f"[Window] Click animation loaded (duration: {self.click_animation_duration}ms)")

    def play_idle_animation(self):
        """播放待机动画"""
        if self.idle_animation:
            self.current_animation = 'idle'
            self.animation_label.setMovie(self.idle_animation)
            self.idle_animation.start()
            print("[Window] Playing idle animation")
        else:
            print("[Window] Warning: Idle animation not loaded")

    def play_click_animation(self):
        """播放点击反馈动画"""
        if self.click_animation:
            self.current_animation = 'click'
            # 停止当前播放的动画
            if self.idle_animation and self.idle_animation.state() == QMovie.MovieState.Running:
                self.idle_animation.stop()

            self.animation_label.setMovie(self.click_animation)
            self.click_animation.start()
            print(f"[Window] Playing click animation (will play for {self.click_animation_duration}ms)")

            # 使用实际计算的动画时长，播放完一次后返回待机
            QTimer.singleShot(self.click_animation_duration, self.on_click_animation_finished)
        else:
            # 如果没有点击动画，直接返回待机
            print("[Window] Warning: Click animation not loaded, using idle")
            self.play_idle_animation()

    def on_click_animation_finished(self):
        """点击动画播放完成后的回调"""
        # 停止点击动画
        if self.click_animation:
            self.click_animation.stop()
        # 返回待机动画
        self.play_idle_animation()

    def mousePressEvent(self, event):
        """鼠标按下事件"""
        if event.button() == Qt.MouseButton.LeftButton:
            # 记录拖拽起始位置
            self.dragging = True
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            self.drag_start_pos = event.globalPosition().toPoint()  # 记录起始全局位置
            event.accept()

        elif event.button() == Qt.MouseButton.RightButton:
            # 右键显示菜单
            self.show_context_menu(event.globalPosition().toPoint())

    def mouseMoveEvent(self, event):
        """鼠标移动事件（拖拽）"""
        if self.dragging and event.buttons() == Qt.MouseButton.LeftButton:
            # 移动窗口
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        """鼠标释放事件"""
        if event.button() == Qt.MouseButton.LeftButton:
            if self.dragging:
                # 结束拖拽
                self.dragging = False

                # 保存窗口位置
                pos = self.pos()
                config.save_config(window_x=pos.x(), window_y=pos.y())

                # 检查是否是点击（鼠标移动距离小于5像素认为是点击）
                release_pos = event.globalPosition().toPoint()
                distance = (release_pos - self.drag_start_pos).manhattanLength()
                if distance < 5:
                    # 触发点击动画
                    self.play_click_animation()

            event.accept()

    def show_context_menu(self, position):
        """显示右键菜单"""
        menu = QMenu(self)

        # 添加菜单项
        exit_action = menu.addAction("退出")

        # 执行菜单并获取选择的动作
        action = menu.exec(position)

        if action == exit_action:
            self.close_application()

    def close_application(self):
        """关闭应用程序"""
        print("[Window] Closing application...")

        # 保存当前位置
        pos = self.pos()
        config.save_config(window_x=pos.x(), window_y=pos.y())

        # 关闭窗口
        self.close()

    def closeEvent(self, event):
        """窗口关闭事件"""
        # 停止所有动画
        if self.idle_animation:
            self.idle_animation.stop()
        if self.click_animation:
            self.click_animation.stop()

        print("[Window] Window closed")
        event.accept()
