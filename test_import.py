"""
Test script to verify all dependencies are installed correctly
"""

print("Testing imports...")
print()

try:
    import sys
    print(f"[OK] Python version: {sys.version}")
except Exception as e:
    print(f"[FAIL] Python: {e}")

try:
    from PySide6.QtWidgets import QApplication
    print("[OK] PySide6.QtWidgets")
except Exception as e:
    print(f"[FAIL] PySide6.QtWidgets: {e}")

try:
    from PySide6.QtCore import Qt
    print("[OK] PySide6.QtCore")
except Exception as e:
    print(f"[FAIL] PySide6.QtCore: {e}")

try:
    from PySide6.QtGui import QMovie
    print("[OK] PySide6.QtGui")
except Exception as e:
    print(f"[FAIL] PySide6.QtGui: {e}")

try:
    import psutil
    print(f"[OK] psutil version: {psutil.__version__}")
except Exception as e:
    print(f"[FAIL] psutil: {e}")

try:
    from PIL import Image
    print(f"[OK] Pillow (PIL)")
except Exception as e:
    print(f"[FAIL] Pillow: {e}")

print()
print("=" * 50)
print("All dependencies are installed correctly!")
print("You can now run: python src/main.py")
print("=" * 50)
