# 📤 Bulk Upload Accounts Feature - Complete Guide

## 🎯 Overview

The **Bulk Upload** feature allows you to add multiple Facebook accounts at once from a `.txt` file. Browsers will open automatically for each account to save sessions, and you can solve CAPTCHAs manually if they appear.

---

## 🚀 Quick Start

### Step 1: Prepare Your Accounts File

Create a `.txt` file with accounts in this format:

```txt
account1@gmail.com:password123
account2@gmail.com:securepass456
account3@gmail.com:mypassword789
```

**Format Rules:**
- ✅ One account per line
- ✅ Format: `email:password`
- ✅ Lines starting with `#` are ignored (comments)
- ✅ Empty lines are ignored
- ✅ Only `.txt` files accepted

**Example with comments:**
```txt
# My Facebook Accounts for Marketplace
# Format: email:password

account1@gmail.com:password123
account2@gmail.com:securepass456

# Testing accounts
testuser@gmail.com:testpass123
```

---

### Step 2: Upload Your File

1. Go to **Accounts** page
2. Click **"Bulk Upload"** button (top right)
3. Click to select your `.txt` file (or drag & drop)
4. Click **"Upload & Login"**
5. Watch browsers open automatically for each account
6. Solve CAPTCHAs manually if they appear
7. Wait for all sessions to save

---

## 🎨 User Interface

### Modal Features:

1. **File Format Instructions**
   - Blue info box with format details
   - Example code snippet
   - Download sample file button

2. **Automation Info**
   - Purple box explaining browser automation
   - CAPTCHA handling info

3. **File Upload Area**
   - Drag & drop zone
   - File name and size display
   - Only accepts `.txt` files

4. **Results Summary**
   - ✅ Created: Successfully added accounts
   - ⚠️ Skipped: Already exist in database
   - ❌ Failed: Invalid format or errors
   - Detailed lists of each category

5. **Auto-close**
   - Modal closes automatically after 5 seconds
   - Accounts list refreshes

---

## 🏗️ Technical Implementation

### Backend API Endpoint

**File:** `accounts/api_views.py`

```python
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bulk_upload_accounts_with_login(request):
    """
    Bulk upload Facebook accounts from a text file.
    Format: email:password (one per line)
    Browser will open for each account to save session.
    """
    # 1. Validate file type (.txt only)
    # 2. Parse file line by line
    # 3. Skip comments (#) and empty lines
    # 4. Create accounts in database
    # 5. Track created/skipped/failed
    # 6. Start browser automation in background thread
    # 7. Return detailed summary
```

**Endpoint:** `POST /api/accounts/bulk-upload/`

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: `file` (File upload)

**Response:**
```json
{
  "message": "Bulk upload completed. Processing 3 accounts...",
  "summary": {
    "created": 3,
    "skipped": 1,
    "failed": 0
  },
  "details": {
    "created_accounts": ["acc1@gmail.com", "acc2@gmail.com"],
    "skipped_accounts": ["existing@gmail.com"],
    "failed_accounts": [
      {
        "line": "invalid-line",
        "error": "Invalid format (use email:password)"
      }
    ]
  }
}
```

---

### Frontend Component

**File:** `components/BulkUploadModal.tsx`

**Key Features:**
- File selection with validation
- Download sample file button
- Format instructions display
- Upload with progress feedback
- Results summary with stats
- Auto-close timer (5 seconds)
- Error handling

**Props:**
```typescript
interface BulkUploadModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void; // Refresh accounts list
}
```

---

### Accounts Page Integration

**File:** `app/dashboard/accounts/page.tsx`

**Changes:**
- Added "Bulk Upload" button next to "Add Account"
- Import BulkUploadModal component
- Added `isBulkUploadOpen` state
- Wire button to open modal
- Pass `fetchAccounts` as success callback

---

## 📊 Processing Flow

```
1. User clicks "Bulk Upload"
   ↓
2. Modal opens with instructions
   ↓
3. User selects .txt file
   ↓
4. User clicks "Upload & Login"
   ↓
5. Frontend sends file to backend
   ↓
6. Backend parses file
   ↓
7. Backend creates accounts in DB
   ↓
8. Backend returns summary immediately
   ↓
9. Frontend shows results
   ↓
10. Backend starts browser automation (background)
    ↓
11. For each account:
    - Open browser
    - Auto-fill credentials
    - Wait for login
    - Handle CAPTCHA (90 sec)
    - Save session
    ↓
12. Modal auto-closes after 5 sec
    ↓
13. Accounts list refreshes
```

---

## 🧪 Testing Guide

### Test Case 1: Valid File Upload

**Prepare file:** `test_accounts.txt`
```txt
test1@gmail.com:password1
test2@gmail.com:password2
test3@gmail.com:password3
```

**Steps:**
1. Go to Accounts page
2. Click "Bulk Upload"
3. Select `test_accounts.txt`
4. Click "Upload & Login"
5. Check results: "3 Created, 0 Skipped, 0 Failed"
6. Watch 3 browsers open sequentially
7. Modal auto-closes after 5 seconds
8. Verify 3 new accounts in the list

**Expected Backend Logs:**
```bash
🌐 Opening browser for test1@gmail.com...
✅ Session saved for test1@gmail.com
🌐 Opening browser for test2@gmail.com...
✅ Session saved for test2@gmail.com
🌐 Opening browser for test3@gmail.com...
✅ Session saved for test3@gmail.com
```

---

### Test Case 2: Duplicate Accounts

**Prepare file:** `duplicates.txt`
```txt
existing@gmail.com:password
new@gmail.com:password
```

**Steps:**
1. Add `existing@gmail.com` manually first
2. Upload `duplicates.txt`
3. Check results: "1 Created, 1 Skipped, 0 Failed"
4. Verify skipped list shows `existing@gmail.com`

---

### Test Case 3: Invalid Format

**Prepare file:** `invalid.txt`
```txt
valid@gmail.com:password123
invalid-line-no-colon
another@gmail.com:pass456
missing@gmail.com:
```

**Steps:**
1. Upload `invalid.txt`
2. Check results: "2 Created, 0 Skipped, 2 Failed"
3. Verify failed list shows:
   - `invalid-line-no-colon` - Invalid format
   - `missing@gmail.com:` - Email or password empty

---

### Test Case 4: With Comments

**Prepare file:** `with_comments.txt`
```txt
# Production Accounts
account1@gmail.com:pass1

# Testing Accounts
account2@gmail.com:pass2

# This is ignored
```

**Steps:**
1. Upload file
2. Check results: "2 Created"
3. Verify comments were ignored

---

### Test Case 5: CAPTCHA Handling

**Prepare file with real account that will trigger CAPTCHA:**
```txt
youraccount@gmail.com:yourpassword
```

**Steps:**
1. Upload file
2. Browser opens
3. CAPTCHA appears
4. Solve CAPTCHA manually within 90 seconds
5. Verify session saves successfully
6. Check backend logs: "✅ Login successful after solving checkpoint!"

---

## 🎯 File Format Validation

### Valid Examples:
```txt
✅ user@gmail.com:password123
✅ test.user@domain.com:complex$pass#123
✅ email@subdomain.example.com:pass with spaces
✅ # This is a comment
✅ 
```

### Invalid Examples:
```txt
❌ userpassword (missing colon)
❌ user@gmail.com (missing password)
❌ :password123 (missing email)
❌ user@gmail.com: (empty password)
❌ :user@gmail.com (colon at start)
```

---

## 🔐 Security Features

1. **JWT Authentication Required**
   - All API calls require valid authentication token
   
2. **File Type Validation**
   - Only `.txt` files accepted
   - Prevents malicious file uploads

3. **Password Encryption**
   - Passwords stored encrypted in database
   - Never logged to console

4. **Duplicate Prevention**
   - Checks existing emails before creating
   - Skips duplicates automatically

5. **Error Isolation**
   - One invalid line doesn't stop entire upload
   - Failed accounts reported separately

---

## 📈 Performance Considerations

### Sequential Browser Automation
- Browsers open **one at a time** (not parallel)
- Prevents system resource overload
- Each login waits 90 seconds max for CAPTCHA

### Background Processing
- File parsing happens immediately
- Browser automation runs in background thread
- Frontend receives response instantly
- User can continue working while logins happen

### Recommended Limits
- **Max accounts per upload:** 50
- **Max file size:** 10 KB
- **Timeout per account:** 90 seconds

---

## 🚨 Troubleshooting

### Issue: "Only .txt files are allowed"
**Solution:** Make sure file extension is `.txt`, not `.doc`, `.csv`, or other formats.

---

### Issue: "Failed to process file"
**Solution:** 
1. Check file encoding (should be UTF-8)
2. Verify format: `email:password`
3. Remove special characters from file
4. Download sample file and use as template

---

### Issue: All accounts showing "Skipped"
**Solution:** All accounts already exist in database. Delete them first or use different emails.

---

### Issue: Browser doesn't open
**Solution:**
1. Check backend terminal for errors
2. Verify Playwright installed: `pip install playwright`
3. Install Chromium: `playwright install chromium`

---

### Issue: Sessions not saving
**Solution:**
1. Check browser completes login
2. Verify `sessions/` folder exists
3. Check folder permissions
4. Look at backend logs for specific errors

---

### Issue: Modal closes too fast
**Solution:** Edit `BulkUploadModal.tsx` line ~89:
```typescript
setTimeout(() => {
  onSuccess();
  handleClose();
}, 5000); // Change to 10000 for 10 seconds
```

---

## 💡 Best Practices

### 1. Start Small
- Test with 2-3 accounts first
- Verify process works
- Then upload larger batches

### 2. Monitor Backend Logs
- Keep terminal open
- Watch for success/error messages
- Check session file creation

### 3. Handle CAPTCHAs Promptly
- Don't ignore browser windows
- Solve CAPTCHAs within 90 seconds
- Keep browser tabs open until completion

### 4. Use Comments in Files
- Document account purposes
- Group accounts by category
- Add dates for tracking

### 5. Backup Your File
- Keep copy of accounts file
- Don't delete after upload
- May need for re-upload later

---

## 📁 Files Modified/Created

### Backend:
- ✅ `accounts/api_views.py` - Added `bulk_upload_accounts_with_login()`
- ✅ `accounts/api_urls.py` - Added `/accounts/bulk-upload/` route

### Frontend:
- ✅ `components/BulkUploadModal.tsx` - **NEW** modal component (330+ lines)
- ✅ `lib/api.ts` - Added `bulkUpload()` method
- ✅ `app/dashboard/accounts/page.tsx` - Added "Bulk Upload" button

### Documentation:
- ✅ `BULK_UPLOAD_FEATURE.md` - This complete guide

---

## ✅ Feature Checklist

### UI/UX:
- [x] Bulk Upload button on Accounts page
- [x] Modal with file format instructions
- [x] Download sample file button
- [x] Drag & drop file upload
- [x] File validation (.txt only)
- [x] Upload progress indicator
- [x] Results summary with stats
- [x] Detailed success/skip/fail lists
- [x] Auto-close after 5 seconds
- [x] Responsive design

### Backend:
- [x] File upload endpoint
- [x] Parse .txt file format
- [x] Handle comments and empty lines
- [x] Create accounts in database
- [x] Check for duplicates
- [x] Validate email:password format
- [x] Background browser automation
- [x] Sequential login processing
- [x] Session file saving
- [x] Detailed response with summary

### Error Handling:
- [x] Invalid file type rejection
- [x] Malformed line detection
- [x] Empty email/password validation
- [x] Duplicate account skipping
- [x] Individual account error tracking
- [x] Clear error messages

---

## 🎬 Demo Flow

1. **Click "Bulk Upload"** → Modal opens
2. **Click "Download Sample File"** → `sample_accounts.txt` downloaded
3. **Edit sample file** → Add your accounts
4. **Select file** → Drag/drop or click to browse
5. **Click "Upload & Login"** → File uploads
6. **Watch results** → Stats display (Created/Skipped/Failed)
7. **Browsers open** → Automatic login for each account
8. **Modal closes** → After 5 seconds
9. **List refreshes** → New accounts appear with status

---

## 📊 Success Metrics

✅ **Feature is working when:**
1. Modal opens on "Bulk Upload" click
2. File format instructions are clear
3. Sample file downloads correctly
4. File validation prevents invalid uploads
5. Results show correct counts
6. Browsers open for each account
7. Sessions save to `sessions/` folder
8. Skipped/failed accounts are listed
9. Modal auto-closes and refreshes list
10. All accounts appear with correct status

---

## 🚀 What's Next?

After testing bulk upload, you might want to:

1. **Add Progress Indicator** - Show "Processing account 2/5..."
2. **Session Status Polling** - Auto-refresh status every 10 seconds
3. **CSV Support** - Allow CSV files in addition to TXT
4. **Bulk Delete** - Select multiple accounts to delete
5. **Export Accounts** - Download accounts as TXT file
6. **Validation Preview** - Show parsed accounts before uploading

---

**Status**: ✅ **FULLY IMPLEMENTED AND READY TO TEST!**

**Quick Test:** 
1. Create a file: `test.txt` with 2-3 accounts
2. Click "Bulk Upload" button
3. Upload file and watch the magic! 🎉
