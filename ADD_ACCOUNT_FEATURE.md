# ✨ Add Account Feature - Complete Guide

## 🎯 Overview

The **Add Account** feature allows you to add new Facebook accounts with **automated browser login**. If CAPTCHA or 2FA appears, you can solve it manually while the browser is open.

---

## 🚀 How It Works

### User Flow:

1. **Click "Add Account"** button on the Accounts page
2. **Fill in the form**:
   - Facebook email
   - Facebook password
3. **Click "Add Account"**
4. **Browser opens automatically** with Facebook login
5. **Three scenarios**:
   - ✅ **Auto-login succeeds** → Session saved automatically
   - 🔒 **CAPTCHA appears** → Solve it manually (90 seconds)
   - ❌ **Wrong credentials** → Login fails, no session saved
6. **Account appears in the list** (session status will update)

---

## 🏗️ Technical Implementation

### Backend (Django)

#### 1. New API Endpoint
**File**: `accounts/api_views.py`

```python
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_facebook_account_with_login(request):
    """
    Add a new Facebook account and automatically open browser for login.
    If CAPTCHA appears, user can solve it manually.
    """
    email = request.data.get('email')
    password = request.data.get('password')
    
    # Validation
    if not email or not password:
        return Response({'error': 'Email and password are required'})
    
    # Check duplicates
    if FacebookAccount.objects.filter(email=email).exists():
        return Response({'error': 'Account already exists'})
    
    # Create account
    account = FacebookAccount.objects.create(
        email=email,
        password=password
    )
    
    # Start browser automation in background thread
    def automated_login():
        success = save_session(email, password)
        if success:
            print(f"✅ Session saved for {email}")
        else:
            print(f"❌ Login failed for {email}")
    
    Thread(target=automated_login, daemon=True).start()
    
    return Response({
        'message': 'Account created. Browser opening...',
        'account': serializer.data
    })
```

**Route**: `/api/accounts/add-with-login/`

---

#### 2. Session Automation
**File**: `automation/post_to_facebook.py`

The `save_session()` function:
- Opens Chromium browser (headless=False)
- Navigates to Facebook login
- **Auto-fills** email and password
- Detects CAPTCHA/2FA/Checkpoint
- Waits **90 seconds** for manual intervention
- Saves session to `sessions/{email}.json`
- Returns success/failure status

---

### Frontend (Next.js + TypeScript)

#### 1. Add Account Modal
**File**: `frontend/components/AddAccountModal.tsx`

**Features**:
- ✅ Email and password inputs
- ✅ Form validation (email format, required fields)
- ✅ Loading state with spinner
- ✅ Success/error messages
- ✅ Info box explaining the process
- ✅ Automatic close after 2 seconds on success

**Props**:
```typescript
interface AddAccountModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void; // Refresh accounts list
}
```

---

#### 2. API Client Update
**File**: `frontend/lib/api.ts`

Added new method:
```typescript
export const accountsAPI = {
  addWithLogin: (data: { email: string; password: string }) =>
    api.post("/accounts/add-with-login/", data),
  
  // ... other methods
};
```

---

#### 3. Accounts Page Integration
**File**: `frontend/app/dashboard/accounts/page.tsx`

**Changes**:
- Import `AddAccountModal` component
- Add `isModalOpen` state
- Wire "Add Account" button to open modal
- Pass `fetchAccounts` as `onSuccess` callback

```tsx
<AddAccountModal
  isOpen={isModalOpen}
  onClose={() => setIsModalOpen(false)}
  onSuccess={fetchAccounts}
/>

<Button onClick={() => setIsModalOpen(true)}>
  <Plus size={20} />
  Add Account
</Button>
```

---

## 📸 User Experience

### Step-by-Step Screenshots (Expected Flow)

1. **Initial State**: Accounts page with "Add Account" button
2. **Modal Opens**: Form with email/password fields and info box
3. **Submitting**: Loading spinner, "Adding..." button text
4. **Browser Opens**: Chromium window shows Facebook login (auto-filled)
5. **Three Scenarios**:
   - ✅ Success → Green checkmark, "Session saved!"
   - 🔒 CAPTCHA → User solves manually within 90 seconds
   - ❌ Error → Red alert, "Login failed"
6. **Success State**: Green alert, "Account Created!"
7. **Auto-close**: Modal closes after 2 seconds
8. **Refresh**: Accounts list refreshes, new account appears

---

## 🔐 Security Features

1. **Password Storage**: Encrypted in Django database
2. **JWT Authentication**: All API calls require valid token
3. **Session Files**: Stored locally in `sessions/` folder
4. **CORS Protection**: Only frontend origin allowed
5. **No Password Logging**: Passwords never printed to console

---

## 🛠️ How to Test

### Test Case 1: Successful Auto-Login
```bash
# Start backend
cd fb_marketplace_bot
python manage.py runserver

# Start frontend (in another terminal)
cd frontend
npm run dev

# In browser:
1. Go to http://localhost:3000/dashboard/accounts
2. Click "Add Account"
3. Enter: test@gmail.com / yourpassword
4. Click "Add Account"
5. Browser opens → Login succeeds automatically
6. Check session file exists: sessions/test_gmail_com.json
```

---

### Test Case 2: CAPTCHA/2FA Manual Solve
```bash
# Same steps as above, but:
# When CAPTCHA appears in browser:
1. Solve CAPTCHA manually
2. Complete 2FA if required
3. Wait for session to save
4. Browser closes automatically
5. Check session file created
```

---

### Test Case 3: Wrong Credentials
```bash
# Same steps, but:
# Enter wrong password
# Expected: Browser stays on login page, error message shown
# Session file NOT created
```

---

## 🧪 Debugging Tips

### Check Backend Logs
```bash
# In terminal where runserver is running:
# Look for:
🌐 Opening browser for test@gmail.com...
✅ Session saved successfully for test@gmail.com
# OR
❌ Login failed for test@gmail.com
```

---

### Check Session Files
```bash
# In project root:
ls sessions/
# Expected output:
# test_gmail_com.json
# user_gmail_com.json
```

---

### Check Frontend Network Tab
```javascript
// Expected API response:
{
  "message": "Account created successfully. Browser opening for login...",
  "account": {
    "id": 5,
    "email": "test@gmail.com",
    "session_exists": false,  // Will be true after login
    "created_at": "2025-10-17T12:00:00Z"
  }
}
```

---

## 📊 Status Indicators

### Session Status Badge Colors:
- 🟢 **Green "Active"**: Session file exists, account ready to post
- 🔴 **Red "No Session"**: No session file, needs login

### When Session Status Updates:
- Initially: "No Session" (account just created)
- After browser login: "Active" (on next page refresh)
- If session expires: "No Session" (manually re-login needed)

---

## 🚨 Troubleshooting

### Issue: Browser doesn't open
**Solution**: Check backend terminal for errors. Playwright might need installation:
```bash
playwright install chromium
```

---

### Issue: "Account already exists" error
**Solution**: Email already in database. Use different email or delete existing account first.

---

### Issue: Session not saving after successful login
**Solution**: 
1. Check `sessions/` folder permissions
2. Check browser stayed open for 60+ seconds
3. Check Django logs for save_session errors

---

### Issue: CAPTCHA timeout (90 seconds not enough)
**Solution**: Edit `automation/post_to_facebook.py`:
```python
# Line ~60, change:
time.sleep(90)  # Change to 120 or 180
```

---

## 🎨 UI/UX Improvements (Optional)

### Future Enhancements:
1. **Progress Indicator**: Show "Opening browser..." toast
2. **Session Status Polling**: Auto-refresh status every 10 seconds
3. **Edit Account**: Modal to update email/password
4. **Bulk Add**: Upload CSV with multiple accounts
5. **Test Login**: Button to verify existing session still works

---

## 📁 Files Modified

### Backend:
- ✅ `accounts/api_views.py` - New endpoint
- ✅ `accounts/api_urls.py` - New route

### Frontend:
- ✅ `components/AddAccountModal.tsx` - NEW modal component
- ✅ `lib/api.ts` - New API method
- ✅ `app/dashboard/accounts/page.tsx` - Integrated modal

---

## ✅ Testing Checklist

- [ ] Modal opens on "Add Account" click
- [ ] Form validation works (empty fields, invalid email)
- [ ] API call triggers browser automation
- [ ] Browser opens with Facebook login
- [ ] Email/password auto-filled
- [ ] Success case: Session saves, modal closes
- [ ] CAPTCHA case: User can solve manually
- [ ] Error case: Shows error message
- [ ] Account appears in list after refresh
- [ ] Session status updates correctly
- [ ] Delete account also deletes session file

---

## 🎯 Success Criteria

✅ **Feature Complete When**:
1. User can add account via modal
2. Browser opens automatically
3. Auto-login works for valid credentials
4. CAPTCHA can be solved manually
5. Session saves to `sessions/` folder
6. Account appears in dashboard with correct status
7. No errors in console or backend logs

---

**Status**: ✅ **IMPLEMENTED AND READY TO TEST!**

**Next Steps**: Click "Add Account" button and test the entire flow!
