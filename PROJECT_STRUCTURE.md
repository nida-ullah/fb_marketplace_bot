# Facebook Marketplace Bot - Production Files

## 📁 Project Structure (Clean)

```
fb_marketplace_bot/
├── accounts/                    # Django app for Facebook accounts
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py              # FacebookAccount model
│   ├── tests.py
│   └── views.py
│
├── automation/                  # Core automation logic
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── cron.py                 # Cron job configurations
│   ├── models.py
│   ├── post_to_facebook.py    # Main posting automation
│   ├── tests.py
│   └── views.py
│
├── bot_core/                    # Django project settings
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py            # Main configuration
│   ├── urls.py                # URL routing
│   └── wsgi.py
│
├── postings/                    # Django app for marketplace posts
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py              # MarketplacePost model
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   ├── management/
│   │   └── commands/
│   │       └── post_to_marketplace.py  # Main command
│   ├── migrations/
│   └── templates/
│       └── postings/
│           ├── create_post.html
│           └── post_list.html
│
├── media/                       # Uploaded media files
│   └── posts/                  # Product images
│
├── sessions/                    # Facebook session files
│   └── *.json                  # Session cookies
│
├── templates/                   # Base templates
│   └── base.html
│
├── manage.py                    # Django management script
├── db.sqlite3                   # Database
├── requirement.txt              # Python dependencies
├── README.md                    # Main documentation
├── .gitignore                   # Git ignore rules
│
├── add_new_account.py          # Utility: Add new Facebook account
└── save_new_session.py         # Utility: Save Facebook session
```

## 🚀 Core Production Files

### 1. **Main Automation**
- `automation/post_to_facebook.py` - Core logic for posting to Facebook Marketplace
  - `save_session(email)` - Save Facebook session
  - `login_and_post(...)` - Post to marketplace

### 2. **Django Management Command**
- `postings/management/commands/post_to_marketplace.py` - Command to process scheduled posts
  - Usage: `python manage.py post_to_marketplace`

### 3. **Utility Scripts**
- `save_new_session.py` - Interactive script to save new Facebook sessions
- `add_new_account.py` - Interactive script to add account and test posting

### 4. **Models**
- `accounts/models.py` - FacebookAccount model
- `postings/models.py` - MarketplacePost model

## 📝 Usage

### Save a New Facebook Session
```bash
python save_new_session.py
```

### Add New Account (with optional test post)
```bash
python add_new_account.py
```

### Post Scheduled Items
```bash
python manage.py post_to_marketplace
```

### Run Django Server
```bash
python manage.py runserver
```

### Access Admin Panel
```bash
# Create superuser first (if not exists)
python manage.py createsuperuser

# Then visit: http://localhost:8000/admin
```

## 🗑️ Removed Files (Cleanup)

The following test and documentation files have been removed:

### Test Files Removed:
- ❌ `post_test.py` - Old test file
- ❌ `save_session_test.py` - Old test file  
- ❌ `test_marketplace_form.py` - Debug tool
- ❌ `check_superuser.py` - Utility script

### Documentation Files Removed:
- ❌ `FIXES_APPLIED.md`
- ❌ `FIX_SUMMARY.md`
- ❌ `PUBLISH_BUTTON_FIX.md`
- ❌ `ACCOUNT_MANAGEMENT.md`

### Screenshot Files Removed:
- ❌ `error_screenshot.png`
- ❌ `test_inspection.png`
- ❌ `publish_button_missing.png`

### Management Commands Removed:
- ❌ `accounts/management/commands/check_superuser.py`

## ✅ What's Left

Only production-ready files remain:
- ✅ Core Django apps (accounts, postings, automation)
- ✅ Working automation scripts
- ✅ Utility scripts for account management
- ✅ Main documentation (README.md)
- ✅ Database and sessions
- ✅ Django default files (manage.py, settings, etc.)

## 🔧 Dependencies

Install from `requirement.txt`:
```bash
pip install -r requirement.txt
```

Main dependencies:
- Django 5.2.2
- Playwright 1.52.0
- Pillow 11.2.1

## 📦 Features

✅ Save Facebook sessions via Playwright  
✅ Schedule posts with title, description, price, image  
✅ Auto-post to Facebook Marketplace  
✅ Multi-account support  
✅ Django admin interface  
✅ Robust error handling  
✅ Multiple fallback strategies for button detection  

## 🛡️ Production Ready

The codebase is now clean and production-ready with:
- No test/debug code in production files
- Clean project structure
- Proper error handling
- Documentation for usage
- Utility scripts for common tasks

---

Last cleaned: October 14, 2025
