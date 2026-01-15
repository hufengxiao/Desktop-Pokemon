# Desktop-Pokemon - 赛博桌宠

一个跨平台的桌面宠物应用，小怪兽会悬浮在你的桌面上陪伴你工作！

![Version](https://img.shields.io/badge/version-0.1.0--MVP-blue)
![Python](https://img.shields.io/badge/python-3.10+-green)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)

## 功能特性

### MVP 版本（当前）

- 透明无边框窗口，始终置顶在桌面
- 循环播放待机动画（呼吸效果）
- 点击触发反馈动画（跳跃效果）
- 左键拖拽自由移动位置
- 窗口位置自动保存和恢复
- 右键菜单退出应用

### 计划中的功能

详见 [spec.md](spec.md) 查看完整开发路线图：

- 阶段二：状态机、行走动画、系统监控、喂食系统
- 阶段三：多宠物支持、对话气泡、配置面板
- 阶段四：跨平台打包与发布

## 快速开始

### 环境要求

- Python 3.10 或更高版本
- pip（Python 包管理器）

### 安装依赖

```bash
# 克隆或下载本项目后，进入项目目录
cd Desktop-Pokemon

# 安装依赖（推荐使用虚拟环境）
pip install -r requirements.txt
```

### 运行程序

```bash
# 在项目根目录执行
python src/main.py
```

或者在 Windows 上双击运行：
```bash
python src\main.py
```

### 首次运行

首次运行时，程序会使用占位符图像（蓝色圆形小怪兽）。如果你有自己的宠物图像资源：

1. 准备两个 GIF 动画：
   - `idle.gif` - 待机动画（循环播放）
   - `click.gif` - 点击反馈动画（播放一次）

2. 将它们放入 `assets/sprites/pikachu/` 目录，替换现有文件

3. 重新运行程序即可看到你的自定义图像

## 使用指南

### 基础操作

- **移动**：左键按住桌宠拖拽
- **互动**：左键点击触发动画反馈
- **退出**：右键点击选择"退出"

### 配置文件

程序会在根目录自动生成 `config.json` 文件，保存：
- 窗口位置（X、Y 坐标）
- 窗口透明度
- 宠物类型

你可以手动编辑该文件来调整设置。

## 项目结构

```
Desktop-Pokemon/
├── src/                    # 源代码
│   ├── main.py             # 主入口
│   ├── config.py           # 配置管理
│   ├── ui/                 # 界面模块
│   │   └── pet_window.py   # 主窗口
│   ├── core/               # 核心逻辑
│   │   └── resource_loader.py  # 资源加载
│   ├── models/             # 数据模型
│   └── utils/              # 工具函数
├── assets/                 # 资源文件
│   ├── sprites/            # 精灵图/动画
│   │   └── pikachu/
│   │       ├── idle.gif
│   │       └── click.gif
│   ├── sounds/             # 音效（未实现）
│   └── icons/              # 应用图标
├── requirements.txt        # 依赖列表
├── spec.md                 # 项目规划文档
└── README.md               # 本文件
```

## 自定义你的桌宠

### 更换角色

1. 在 `assets/sprites/` 下创建新文件夹（如 `squirtle/`）
2. 放入该角色的动画文件（`idle.gif`, `click.gif`）
3. 修改 `config.json` 中的 `pet_type` 为新文件夹名
4. 重启程序

### 创建新动画

动画文件支持：
- **GIF 格式**：推荐，支持透明背景和帧动画
- **PNG 格式**：静态图像

推荐尺寸：
- 128x128 像素（默认）
- 256x256 像素（高清）

确保使用透明背景（Alpha 通道），否则会有白色/黑色底色。

## 技术说明

### 技术栈

- **GUI 框架**：PySide6（Qt for Python）
- **图像处理**：Pillow（仅用于生成占位符）
- **系统监控**：psutil（未来版本）

### 核心实现

- 使用 `Qt.FramelessWindowHint` 实现无边框窗口
- 使用 `Qt.WindowStaysOnTopHint` 保持窗口置顶
- 使用 `WA_TranslucentBackground` 实现背景透明
- 使用 `QMovie` 播放 GIF 动画
- 使用 `mousePressEvent` 系列实现拖拽和点击

### 平台兼容性

- **Windows**：完全支持（已测试）
- **macOS**：理论支持，窗口置顶可能需要授权
- **Linux**：理论支持，部分桌面环境可能需要配置

## 开发指南

### 开发环境配置

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 生成占位符图像

如果需要重新生成占位符图像：

```bash
python generate_placeholder.py
```

### 代码风格

- 遵循 PEP 8 规范
- 使用中文注释便于理解
- 每个模块包含文档字符串

## 常见问题

### Q: 窗口看不到或位置不对？

删除 `config.json` 文件重启，窗口会重置到默认位置（右下角）。

### Q: 动画不播放或显示空白？

检查 `assets/sprites/pikachu/` 目录下是否有 `idle.gif` 文件，确保文件未损坏。

### Q: 如何让桌宠开机自启动？

- **Windows**：将程序快捷方式放入启动文件夹（`Win+R` 输入 `shell:startup`）
- **macOS**：系统偏好设置 → 用户与群组 → 登录项
- **Linux**：添加到 `~/.config/autostart/`

### Q: CPU 占用过高？

检查 GIF 动画的帧数和尺寸，建议：
- 帧数不超过 30 帧
- 尺寸不大于 256x256
- 每帧延迟不少于 50ms

## 贡献指南

欢迎提交 Issue 和 Pull Request！

在提交 PR 前请确保：
1. 代码符合 PEP 8 规范
2. 添加必要的注释和文档
3. 测试通过

## 许可证

本项目采用 MIT 许可证，详见 LICENSE 文件（待添加）。

## 致谢

- PySide6 团队提供优秀的 Python Qt 绑定
- 所有为开源社区做出贡献的开发者

---

**项目版本**：v0.1.0-MVP
**最后更新**：2026-01-15

如有问题或建议，欢迎提交 Issue！
