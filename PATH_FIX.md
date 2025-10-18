# Path Fix - manage.py Not Found Error

## 🐛 Problem
The posting process was failing with this error:
```
can't open file 'C:\\Users\\NidaUllah\\OneDrive - Higher Education Commission\\Documents\\Development\\manage.py': [Errno 2] No such file or directory
```

**Wrong Path**: `C:\...\Development\manage.py`  
**Correct Path**: `C:\...\Development\fb_marketplace_bot\manage.py`

---

## ✅ Solution

### Root Cause
In `postings/api_views.py`, the path calculation was going up **3 levels** instead of **2 levels**:

**Before** (Wrong):
```python
project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(__file__)))
```

This went:
1. `postings/api_views.py`
2. ↑ `postings/` 
3. ↑ `fb_marketplace_bot/` 
4. ↑ `Development/` ❌ (Too far!)

**After** (Correct):
```python
# __file__ is in postings/api_views.py
# Go up 2 levels: postings/ -> fb_marketplace_bot/
project_root = os.path.dirname(os.path.dirname(__file__))
```

This goes:
1. `postings/api_views.py`
2. ↑ `postings/`
3. ↑ `fb_marketplace_bot/` ✅ (Correct!)

---

## 📝 What Was Changed

**File**: `postings/api_views.py`

### Change 1: Fixed Path Calculation
```python
# Get the project root directory (where manage.py is)
# __file__ is in postings/api_views.py
# Go up 2 levels: postings/ -> fb_marketplace_bot/
project_root = os.path.dirname(os.path.dirname(__file__))
manage_py_path = os.path.join(project_root, 'manage.py')
```

### Change 2: Added Debug Logging
Now the log file shows the calculated paths for debugging:
```python
with open(log_file, 'a', encoding='utf-8') as log:
    log.write(f"\n\n=== Starting posting process at {timezone.now()} ===\n")
    log.write(f"Project root: {project_root}\n")
    log.write(f"manage.py path: {manage_py_path}\n")
    log.write(f"Command: {' '.join(command)}\n")
    log.write(f"Post IDs: {post_ids_str}\n\n")
```

---

## 🧪 Verification

Tested the path calculation:
```bash
$ python -c "import os; file_path = os.path.join(os.getcwd(), 'postings', 'api_views.py'); project_root = os.path.dirname(os.path.dirname(file_path)); print('Project root:', project_root); print('manage.py path:', os.path.join(project_root, 'manage.py')); print('Exists:', os.path.exists(os.path.join(project_root, 'manage.py')))"
```

**Output**:
```
Project root: C:\Users\NidaUllah\OneDrive - Higher Education Commission\Documents\Development\fb_marketplace_bot
manage.py path: C:\Users\NidaUllah\OneDrive - Higher Education Commission\Documents\Development\fb_marketplace_bot\manage.py
Exists: True
```

✅ **Path is correct!**

---

## 🎯 Next Steps

1. **Restart Django server** (if running):
   ```bash
   python manage.py runserver
   ```

2. **Test posting again**:
   - Go to Posts page
   - Select a pending post
   - Click "Start Posting"
   - Check logs viewer

3. **Expected log output** (now with debug info):
   ```
   === Starting posting process at 2025-10-18 ... ===
   Project root: C:\...\fb_marketplace_bot
   manage.py path: C:\...\fb_marketplace_bot\manage.py
   Command: C:\...\python.exe C:\...\manage.py post_to_marketplace --post-ids 44
   Post IDs: 44
   
   Checking for posts to publish...
   Publishing specific posts: [44]
   Found 1 posts to publish
   ...
   ```

---

## 📊 File Structure Reference

```
fb_marketplace_bot/              ← project_root (where manage.py is)
├── manage.py                    ← Target file
├── postings/
│   ├── api_views.py            ← Current file (__file__)
│   ├── models.py
│   └── management/
│       └── commands/
│           └── post_to_marketplace.py
├── logs/
│   └── posting_process.log
└── ...
```

**Path calculation**:
- `__file__` = `C:\...\fb_marketplace_bot\postings\api_views.py`
- `os.path.dirname(__file__)` = `C:\...\fb_marketplace_bot\postings\`
- `os.path.dirname(os.path.dirname(__file__))` = `C:\...\fb_marketplace_bot\` ✅

---

## ✨ Summary

**Status**: ✅ Fixed

**Error**: `manage.py` not found (wrong path)  
**Cause**: Path calculation went up 3 levels instead of 2  
**Fix**: Removed extra `os.path.dirname()` call  
**Bonus**: Added debug logging to show calculated paths

**Now it works!** 🚀

Try posting again - the browser should open now! 🎉
