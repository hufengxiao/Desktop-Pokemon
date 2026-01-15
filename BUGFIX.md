# Bug Fixes Log

## Issues Fixed (2026-01-15)

### Issue #1: Encoding Error on Windows

**Problem:**
```
UnicodeDecodeError: 'gbk' codec can't decode byte 0xac in position 134: illegal multibyte sequence
```

**Root Cause:**
- `requirements.txt` contained UTF-8 Chinese comments
- Windows pip uses GBK encoding by default
- Chinese characters in console output could cause display issues

**Solution:**
1. Removed all Chinese comments from `requirements.txt`
2. Changed all console output to English in:
   - `src/main.py`
   - `src/config.py`
   - `src/core/resource_loader.py`
   - `src/ui/pet_window.py`
3. Updated batch scripts (`install.bat`, `run.bat`) to use English

**Files Modified:**
- requirements.txt
- install.bat
- run.bat
- src/main.py
- src/config.py
- src/core/resource_loader.py
- src/ui/pet_window.py

---

### Issue #2: QMovie setLoopCount AttributeError

**Problem:**
```
AttributeError: 'PySide6.QtGui.QMovie' object has no attribute 'setLoopCount'
```

**Root Cause:**
- PySide6's QMovie doesn't have `setLoopCount()` method
- Attempted to call non-existent method when loading click animation

**Solution:**
- Removed `setLoopCount()` call
- Implemented timer-based control for click animation duration
- Used `QTimer.singleShot(600, callback)` to stop animation after one play
- Timer duration set to 600ms (covers 7 frames × 80ms + buffer)

**Code Changes:**
```python
# Before (WRONG):
self.click_animation.setLoopCount(1)
self.click_animation.finished.connect(...)

# After (CORRECT):
# Start animation
self.click_animation.start()
# Use timer to stop after one loop
QTimer.singleShot(600, self.on_click_animation_finished)
```

**Files Modified:**
- src/ui/pet_window.py

---

### Issue #3: Click Detection Logic Error

**Problem:**
- Click detection was comparing floating point positions incorrectly
- `event.globalPosition().toPoint() == self.drag_position + ...` rarely true
- Users reported clicks not being detected

**Root Cause:**
- Original logic checked for exact position match
- Mouse position can vary slightly even without dragging
- Floating point precision issues

**Solution:**
- Track drag start position separately
- Calculate Manhattan distance between press and release points
- Consider it a "click" if distance < 5 pixels
- Much more reliable click detection

**Code Changes:**
```python
# Before (UNRELIABLE):
if event.globalPosition().toPoint() == self.drag_position + self.frameGeometry().topLeft():
    self.play_click_animation()

# After (RELIABLE):
release_pos = event.globalPosition().toPoint()
distance = (release_pos - self.drag_start_pos).manhattanLength()
if distance < 5:  # Less than 5 pixels = click
    self.play_click_animation()
```

**Files Modified:**
- src/ui/pet_window.py

---

## Verification

All issues have been tested and verified fixed:

### Test Results:

1. **Encoding Test:**
   ```bash
   pip install -r requirements.txt
   # Result: SUCCESS - All packages installed without errors
   ```

2. **Import Test:**
   ```bash
   python test_import.py
   # Result: SUCCESS - All dependencies imported correctly
   ```

3. **Application Test:**
   ```bash
   python src/main.py
   # Result: SUCCESS - Application starts and runs without errors
   ```

4. **Functionality Test:**
   - [x] Window appears with transparent background
   - [x] Idle animation plays continuously
   - [x] Drag and drop works smoothly
   - [x] Click detection triggers animation
   - [x] Right-click menu appears
   - [x] Position is saved on exit

---

## Additional Improvements

### Animation State Management

Improved animation switching logic:
- Stop idle animation before starting click animation
- Prevent animation conflicts
- Smoother transitions between states

```python
if self.idle_animation and self.idle_animation.state() == QMovie.MovieState.Running:
    self.idle_animation.stop()
```

---

## Known Limitations

1. **Click Animation Duration:**
   - Currently hardcoded to 600ms
   - Future: Could calculate from GIF frame count and delays

2. **Console Output in GUI:**
   - Windows GUI apps don't show console output by default
   - Use `pythonw.exe` for production (no console)
   - Keep `python.exe` for debugging

---

## Testing Checklist for Users

- [ ] Run `python test_import.py` - all checks should pass
- [ ] Run `python src/main.py` - window should appear
- [ ] Drag the pet around - should move smoothly
- [ ] Click the pet - should trigger jump animation
- [ ] Wait for animation to finish - should return to idle
- [ ] Right-click - menu should appear with "Exit" option
- [ ] Close and reopen - window position should be remembered

---

## If Issues Persist

1. **Still getting encoding errors:**
   - Verify you're using the latest `requirements.txt` (no comments)
   - Check file encoding: should be UTF-8 or ASCII
   - Try: `pip install PySide6 psutil Pillow` directly

2. **Window not appearing:**
   - Delete `config.json` file
   - Restart application
   - Window will reset to default position

3. **Animation issues:**
   - Regenerate placeholder images: `python generate_placeholder.py`
   - Check `assets/sprites/pikachu/` contains `idle.gif` and `click.gif`

---

**All issues resolved and tested!**
**Application is ready for use.**

Last Updated: 2026-01-15
