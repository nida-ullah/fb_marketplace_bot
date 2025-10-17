
# 🎉 Bulk Upload Feature - Quick Reference

## ✅ What's Been Added

### New Features:
1. ✅ **"Bulk Upload" button** on Accounts page
2. ✅ **Bulk upload modal** with file format instructions
3. ✅ **Download sample file** button
4. ✅ **Drag & drop** file upload
5. ✅ **Detailed results** (Created/Skipped/Failed counts)
6. ✅ **Automatic browser login** for all accounts
7. ✅ **CAPTCHA handling** (solve manually if appears)

---

## 🚀 How to Use

### 1. Prepare Your File

Create a `.txt` file with this format:

```txt
account1@gmail.com:password123
account2@gmail.com:securepass456
account3@gmail.com:mypassword789
```

**Rules:**
- One account per line
- Format: `email:password`
- Lines starting with `#` are comments (ignored)
- Empty lines are ignored

---

### 2. Upload Your File

1. Go to: **http://localhost:3000/dashboard/accounts**
2. Click **"Bulk Upload"** button (white button, top right)
3. Click **"Download Sample File"** to see example format
4. Select your `.txt` file (or drag & drop)
5. Click **"Upload & Login"**
6. Wait for results to show
7. Browsers will open automatically for each account
8. Solve CAPTCHAs manually if they appear
9. Modal closes automatically after 5 seconds

---

## 📊 What You'll See

### Results Summary:
- ✅ **Created:** Successfully added accounts
- ⚠️ **Skipped:** Already exist in database
- ❌ **Failed:** Invalid format or errors

### After Upload:
- Browsers open one by one for each account
- Email and password auto-filled
- If CAPTCHA appears, you have 90 seconds to solve it
- Sessions save automatically to `sessions/` folder
- Accounts list refreshes automatically

---

## 📁 Sample File

You can download a sample file from the modal, or create one:

**sample_accounts.txt:**
```txt
# My Facebook Accounts
# Format: email:password

account1@gmail.com:password123
account2@gmail.com:securepass456

# Testing accounts
test@gmail.com:testpass789
```

---

## 🔍 Backend Logs

Watch your backend terminal for progress:

```bash
🌐 Opening browser for account1@gmail.com...
✅ Session saved for account1@gmail.com

🌐 Opening browser for account2@gmail.com...
🔒 Captcha/2FA/Checkpoint detected!
👉 Please solve it manually in the browser...
⏳ Waiting 90 seconds for you to complete...
✅ Login successful after solving checkpoint!
✅ Session saved for account2@gmail.com
```

---

## 🎯 Tips

1. **Start Small:** Test with 2-3 accounts first
2. **Monitor Logs:** Keep backend terminal visible
3. **Handle CAPTCHAs:** Don't close browser windows
4. **Check Status:** Refresh accounts page to see session status
5. **Backup File:** Keep your accounts.txt file safe

---

## ⚠️ Common Issues

### "Only .txt files are allowed"
- Make sure file extension is `.txt`

### "Failed to process file"
- Check file format: `email:password`
- Download sample file and use as template

### Accounts showing "Skipped"
- Accounts already exist in database
- Use different emails or delete existing ones

### Browser doesn't open
- Check Playwright is installed: `pip install playwright`
- Install Chromium: `playwright install chromium`

---

## 📋 Quick Test

1. Create `test.txt`:
```txt
test1@gmail.com:pass1
test2@gmail.com:pass2
```

2. Go to Accounts page
3. Click "Bulk Upload"
4. Select `test.txt`
5. Click "Upload & Login"
6. Watch results and browsers!

---

## 🎨 UI Preview

**Accounts Page:**
- Two buttons at top right:
  - "Bulk Upload" (white/outline)
  - "Add Account" (blue)

**Bulk Upload Modal:**
- Title: "Bulk Upload Accounts"
- Blue box: File format instructions with example
- Purple box: Automation process info
- Upload area: Click or drag & drop
- "Download Sample File" link (blue text)
- "Upload & Login" button (blue)

**Results:**
- Green box with stats
- Three cards: Created / Skipped / Failed
- Lists of each category
- Auto-close countdown: "Closing in 5 seconds..."

---

## 📊 File Format Examples

✅ **Valid:**
```txt
user@gmail.com:password123
test.user@domain.com:secure$pass
email@example.com:pass with spaces
# This is a comment
```

❌ **Invalid:**
```txt
userpassword (missing colon)
user@gmail.com (missing password)
:password (missing email)
```

---

## 🚀 Next Steps After Upload

1. **Check Accounts List** - New accounts appear
2. **Verify Session Status** - Green "Active" or Red "No Session"
3. **Wait for Browser Logins** - May take 2-3 minutes per account
4. **Refresh Page** - See updated session statuses
5. **Start Posting** - Use accounts to post to Marketplace

---

## 🔧 Files Changed

### Backend:
- `accounts/api_views.py` - New endpoint
- `accounts/api_urls.py` - New route

### Frontend:
- `components/BulkUploadModal.tsx` - **NEW** component
- `lib/api.ts` - New API method
- `app/dashboard/accounts/page.tsx` - Added button

---

## ✨ Feature Complete!

- ✅ Bulk upload from .txt file
- ✅ File format validation
- ✅ Download sample file
- ✅ Automatic browser login
- ✅ CAPTCHA handling
- ✅ Detailed results summary
- ✅ Auto-refresh accounts list

**Status:** 🎉 **READY TO USE!**

---

**Test it now:** Create a `.txt` file with 2-3 accounts and click "Bulk Upload"! 🚀
