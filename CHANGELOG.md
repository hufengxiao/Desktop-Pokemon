# Changelog

All notable changes to Desktop-Pokemon will be documented in this file.

---

## [Unreleased]

### Added (2026-01-15)

#### Automatic GIF Duration Detection

**Feature**: Click animation now plays for its complete duration instead of being cut off early.

**What Changed:**
- Added `get_gif_duration()` method to automatically calculate GIF animation duration
- Click animation duration is now dynamically calculated from the actual GIF file
- Timer automatically adjusts to match animation length

**Technical Details:**
- Uses PIL/Pillow to read GIF frame data
- Calculates total duration by summing all frame delays
- Stores duration in `self.click_animation_duration` variable
- Timer uses actual duration instead of hardcoded 600ms

**Before:**
```python
# Hardcoded duration - didn't match actual GIF
QTimer.singleShot(600, self.on_click_animation_finished)
```

**After:**
```python
# Automatically calculated from GIF
self.click_animation_duration = self.get_gif_duration(click_path)
QTimer.singleShot(self.click_animation_duration, self.on_click_animation_finished)
```

**Example Output:**
```
[Window] GIF analysis: 69 frames, 2070ms total
[Window] Click animation loaded (duration: 2070ms)
[Window] Playing click animation (will play for 2070ms)
```

**Benefits:**
- Click animation plays completely (all 69 frames, ~2.07 seconds)
- No need to manually adjust timing when changing GIF files
- Works with any GIF duration automatically
- Better user experience - animations feel more natural

**Files Modified:**
- `src/ui/pet_window.py`
  - Added `from PIL import Image` import
  - Added `get_gif_duration()` method
  - Added `self.click_animation_duration` variable
  - Updated `load_animations()` to calculate duration
  - Updated `play_click_animation()` to use calculated duration

---

## [0.1.0-MVP] - 2026-01-15

### Initial Release

**Core Features:**
- Transparent frameless window
- Always on top desktop pet
- Idle animation loop (breathing effect)
- Click interaction with animation feedback
- Drag and drop to move window
- Right-click context menu
- Window position persistence
- Placeholder image generation

**Technical Implementation:**
- Python 3.10+ with PySide6 (Qt 6)
- Resource loading system
- Configuration management
- Cross-platform support (Windows/macOS/Linux)

**Bug Fixes:**
- Fixed encoding issues on Windows (UTF-8 vs GBK)
- Fixed QMovie API compatibility
- Fixed click detection logic

**Documentation:**
- Complete README with setup instructions
- Development roadmap (spec.md)
- Testing guide (TEST_GUIDE.md)
- Bug fix log (BUGFIX.md)

---

## Version History

- **v0.1.0-MVP** (2026-01-15) - Initial MVP release
- **Unreleased** - Dynamic animation duration support

---

## Upcoming Features

See `spec.md` for the full development roadmap.

### Phase 2 (Planned)
- State machine system
- Walking animation and movement
- System monitoring (CPU/memory)
- Feeding system

### Phase 3 (Planned)
- Multiple pet support
- Speech bubbles
- Settings GUI
- Data persistence

### Phase 4 (Planned)
- Cross-platform packaging
- Installer creation
- Performance optimization

---

## How to Report Issues

If you encounter any bugs or have feature requests, please:
1. Check existing issues in the project
2. Provide detailed reproduction steps
3. Include your OS and Python version
4. Attach relevant log output

---

**Last Updated**: 2026-01-15
