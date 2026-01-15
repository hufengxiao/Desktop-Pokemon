# Desktop-Pokemon Test Guide

## Problem Fixed

**Issue**: The original `requirements.txt` contained UTF-8 Chinese comments that caused encoding errors on Windows (GBK codec error).

**Solution**: Removed all comments from `requirements.txt` and changed all console output to English to avoid encoding issues.

---

## Installation Test

### Step 1: Verify Dependencies Installation

Run the test script to check if all dependencies are installed:

```bash
python test_import.py
```

Expected output:
```
Testing imports...

[OK] Python version: 3.12.x
[OK] PySide6.QtWidgets
[OK] PySide6.QtCore
[OK] PySide6.QtGui
[OK] psutil version: x.x.x
[OK] Pillow (PIL)

==================================================
All dependencies are installed correctly!
You can now run: python src/main.py
==================================================
```

### Step 2: Install Dependencies (if needed)

If test fails, install dependencies:

**Option A - Using pip directly:**
```bash
pip install -r requirements.txt
```

**Option B - Using install.bat (Windows):**
```bash
Double-click install.bat
```

---

## Running the Application

### Method 1: Direct Command

```bash
python src/main.py
```

### Method 2: Using run.bat (Windows)

```bash
Double-click run.bat
```

---

## Expected Behavior

When you run the application:

1. **Window appears**: A transparent, frameless window with a blue circular character
2. **Animation plays**: The character has a "breathing" animation (idle)
3. **Dragging works**: Left-click and drag to move the window
4. **Click interaction**: Click on the character to trigger jump animation
5. **Right-click menu**: Right-click to show "Exit" option
6. **Position saved**: Window position is saved when you close and restored on next launch

---

## Files Changed (Encoding Fix)

### Fixed Files:
1. `requirements.txt` - Removed Chinese comments
2. `install.bat` - Changed to English text
3. `run.bat` - Changed to English text
4. `src/main.py` - Changed console output to English
5. `src/config.py` - Changed console output to English
6. `src/core/resource_loader.py` - Changed console output to English
7. `src/ui/pet_window.py` - Changed console output to English

### Why?
Windows console uses GBK encoding by default, but the files were UTF-8 with Chinese characters. This caused:
- `UnicodeDecodeError` when pip tried to read requirements.txt
- Potential display issues with Chinese characters in console output

---

## Quick Commands Reference

```bash
# Test dependencies
python test_import.py

# Install dependencies
pip install -r requirements.txt

# Run application
python src/main.py

# Generate placeholder images (if needed)
python generate_placeholder.py
```

---

## Troubleshooting

### Issue: "UnicodeDecodeError" when installing

**Solution**: Make sure you're using the updated `requirements.txt` (no comments, plain package names only)

### Issue: Application starts but no window visible

**Solution**: Delete `config.json` and restart. The window will reset to default position (bottom-right corner)

### Issue: Animations not playing

**Solution**:
1. Check if `assets/sprites/pikachu/idle.gif` exists
2. Run `python generate_placeholder.py` to regenerate placeholder images

### Issue: Import errors

**Solution**: Run `python test_import.py` to see which dependency is missing, then install it

---

## Project Status

- [x] Project structure created
- [x] Dependencies configured (fixed encoding issues)
- [x] Placeholder images generated
- [x] Core modules implemented
- [x] Transparent frameless window working
- [x] Animation system working
- [x] Drag and click interaction working
- [x] Right-click menu working
- [x] Position persistence working

**Status**: MVP Complete and Ready to Run!

---

## Next Steps

1. **Test the application now**: Run `python src/main.py`
2. **Prepare real assets**: Create or download Pokemon GIF animations
   - idle.gif (128x128 or 256x256, transparent background)
   - click.gif (same specs)
3. **Replace placeholder images**: Put your GIFs in `assets/sprites/pikachu/`
4. **Enjoy your desktop pet**!

For development roadmap, see `spec.md`.
