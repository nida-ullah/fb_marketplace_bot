# 📱 Managing Multiple Facebook Accounts

This guide explains how to add and test new Facebook accounts for the marketplace bot.

## Quick Start

### Option 1: Full Setup (Recommended) 
**Add account + save session + test posting**

```bash
python add_new_account.py
```

This interactive script will:
1. ✅ Save Facebook session (browser login)
2. ✅ Add account to database
3. ✅ Test posting (optional)
4. ✅ Save test post to database (optional)

### Option 2: Session Only
**Just save the session**

```bash
python save_new_session.py
```

This is faster if you just want to save a session without testing.

---

## Step-by-Step Process

### 1. Save Account Session

**What is a session?**
- A session file stores your Facebook login cookies
- This allows the bot to post without logging in each time
- Sessions expire after some time (weeks/months)

**How to save:**

```bash
# Option A: Use the full script
python add_new_account.py

# Option B: Use the quick script
python save_new_session.py

# Option C: Use Django shell
python manage.py shell
>>> from automation.post_to_facebook import save_session
>>> save_session("your_email@gmail.com")
```

When prompted:
1. Enter the Facebook account email
2. A browser will open
3. Log in to Facebook manually
4. Wait 60 seconds for the session to save
5. Browser will close automatically

**Session files are saved in:** `sessions/`

Example: `sessions/your_email_gmail_com.json`

### 2. Add Account to Database

**Using Django Admin:**
```bash
# Start the development server
python manage.py runserver

# Visit: http://localhost:8000/admin/
# Navigate to: Accounts → Facebook accounts → Add
# Enter email and password (password is for reference)
```

**Using the script:**
```bash
python add_new_account.py
# It will prompt you to add the account automatically
```

### 3. Create a Test Post

**Using Django Admin:**
1. Go to http://localhost:8000/admin/
2. Navigate to: Postings → Marketplace posts → Add
3. Fill in:
   - Account: Select your account
   - Title: "Test Product"
   - Description: "Test description"
   - Price: 100
   - Image: Upload an image
   - Scheduled time: Set to current time
   - Posted: Leave unchecked

**Using add_new_account.py:**
- The script will guide you through creating a test post

### 4. Test Posting

**Run the posting command:**
```bash
python manage.py post_to_marketplace
```

This will:
1. ✅ Find all unpublished posts scheduled for now or earlier
2. ✅ Post them to Facebook Marketplace
3. ✅ Mark them as posted in the database

**Watch the output for:**
- ✅ Clicked on Category dropdown
- ✅ Selected Category: Furniture
- ✅ Clicked on Condition dropdown  
- ✅ Selected Condition: New (via role)
- ✅ Posted successfully!

---

## Managing Multiple Accounts

### List Current Sessions

```bash
# List all saved sessions
ls sessions/

# Windows
dir sessions\
```

### Check Accounts in Database

```bash
python manage.py shell
```

```python
from accounts.models import FacebookAccount

# List all accounts
for account in FacebookAccount.objects.all():
    print(f"Email: {account.email}")

# Check specific account
account = FacebookAccount.objects.get(email="your_email@gmail.com")
print(account)
```

### Re-save Session (if expired)

```bash
python save_new_session.py
# Enter the same email to overwrite
```

Or:

```bash
python manage.py shell
```

```python
from automation.post_to_facebook import save_session
save_session("your_email@gmail.com")  # Will overwrite existing
```

---

## Troubleshooting

### ❌ Session not found error

**Problem:** `Session not found. Run save_session('email') first.`

**Solution:**
```bash
python save_new_session.py
# OR
python add_new_account.py
```

### ❌ Account not found in database

**Problem:** Account doesn't exist in Django database

**Solution:**
```bash
# Use the script
python add_new_account.py

# OR add via admin
python manage.py runserver
# Visit: http://localhost:8000/admin/accounts/facebookaccount/add/
```

### ❌ Session expired

**Problem:** Bot can't log in, even with session file

**Solution:** Re-save the session
```bash
python save_new_session.py
# Enter the same email to overwrite
```

### ❌ Image not found

**Problem:** Image path doesn't exist

**Solution:** 
- Upload images to `media/posts/` folder
- Or provide absolute path to existing image

### ❌ "Could not select Condition: New"

**Problem:** Dropdown selection failed

**Solution:** 
- The script tries 3 different methods automatically
- Check `error_screenshot.png` to see what went wrong
- Session might be expired - try re-saving

---

## Best Practices

1. **Session Management**
   - Save sessions in a secure location
   - Don't commit session files to Git (they contain login cookies)
   - Re-save sessions every few weeks/months

2. **Multiple Accounts**
   - Use different accounts for different regions/markets
   - Don't post too frequently from one account (avoid spam detection)
   - Keep track of which accounts are active

3. **Testing**
   - Always test with a new account before using in production
   - Use the test scripts before scheduling real posts
   - Monitor the console output for errors

4. **Scheduling**
   - Spread out posts over time (don't post all at once)
   - Set appropriate scheduled times
   - Check "posted" status in admin to track what's been published

---

## Quick Reference

| Task | Command |
|------|---------|
| Save session only | `python save_new_session.py` |
| Full setup + test | `python add_new_account.py` |
| List superusers | `python manage.py check_superuser` |
| Post to marketplace | `python manage.py post_to_marketplace` |
| Django admin | `python manage.py runserver` |
| Django shell | `python manage.py shell` |

---

## Files Overview

- `add_new_account.py` - Interactive setup for new accounts
- `save_new_session.py` - Quick session saving
- `check_superuser.py` - Manage Django superusers
- `sessions/` - Stored Facebook login sessions
- `media/posts/` - Images for marketplace posts
- `automation/post_to_facebook.py` - Core posting logic

---

Need help? Check the console output for detailed error messages! 🚀
