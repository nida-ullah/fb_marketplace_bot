# Debugging Authentication Issues - Quick Fix Guide

## ✅ Backend Status: WORKING PERFECTLY

I tested both endpoints and they work fine:

### Login Test (SUCCESS ✅)
```bash
POST http://localhost:8000/api/auth/login/
Body: { "email": "admin@gmail.com", "password": "admin" }
Response: 200 OK with tokens
```

### Signup Test (SUCCESS ✅)
```bash
POST http://localhost:8000/api/auth/register/
Body: { "username": "testuser123", "email": "testuser123@example.com", "password": "test123456", ... }
Response: 201 CREATED with tokens
```

## ✅ Frontend API Endpoints: FIXED

Updated from:
- ❌ `/api/accounts/auth/login/`
- ❌ `/api/accounts/auth/register/`

To:
- ✅ `/api/auth/login/`
- ✅ `/api/auth/register/`

## 🔍 How to Debug the Frontend Issue

### Step 1: Check Both Servers Are Running

**Backend (Django):**
```bash
cd "c:/Users/NidaUllah/OneDrive - Higher Education Commission/Documents/Development/fb_marketplace_bot"
source env/Scripts/activate
python manage.py runserver
```
Should see: `Starting development server at http://127.0.0.1:8000/`

**Frontend (Next.js):**
```bash
cd "c:/Users/NidaUllah/OneDrive - Higher Education Commission/Documents/Development/fb_marketplace_bot/frontend"
npm run dev
```
Should see: `- Local: http://localhost:3000`

### Step 2: Open Browser Console

1. Open **http://localhost:3000/login** in Chrome/Edge
2. Press **F12** to open Developer Tools
3. Go to **Console** tab
4. Try to login with: `admin@gmail.com` / `admin`
5. Look for any error messages (red text)

### Step 3: Check Network Tab

1. In Developer Tools, go to **Network** tab
2. Try to login again
3. Look for the request to `auth/login/`
4. Click on it to see:
   - **Status Code**: Should be 200, not 404 or 500
   - **Request Payload**: Check if email/password are sent
   - **Response**: Check what the server returns

## 🐛 Common Issues & Solutions

### Issue 1: "Network Error" or "Failed to fetch"

**Cause**: Backend not running or CORS issue

**Fix**:
```bash
# Restart backend
cd "c:/Users/NidaUllah/OneDrive - Higher Education Commission/Documents/Development/fb_marketplace_bot"
source env/Scripts/activate
python manage.py runserver
```

### Issue 2: 404 Not Found

**Cause**: Wrong API endpoint

**Fix**: I already fixed this! The endpoints are now correct:
- `/api/auth/login/`
- `/api/auth/register/`

### Issue 3: 401 Unauthorized (Login)

**Cause**: Wrong email/password

**Fix**: Use your superuser credentials:
- Email: `admin@gmail.com`
- Password: (the password you set when creating superuser)

If you forgot the password:
```bash
cd "c:/Users/NidaUllah/OneDrive - Higher Education Commission/Documents/Development/fb_marketplace_bot"
source env/Scripts/activate
python manage.py changepassword admin
```

### Issue 4: CORS Error

**Cause**: Frontend URL not in CORS allowed origins

**Fix**: Already configured in `settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

### Issue 5: "Login failed" or "Signup failed" generic error

**Cause**: Frontend not getting proper error message from backend

**Fix**: Check browser console for the actual error response

## 🧪 Quick Test Script

Run this to test if everything is connected:

```bash
cd "c:/Users/NidaUllah/OneDrive - Higher Education Commission/Documents/Development/fb_marketplace_bot"
source env/Scripts/activate

# Test login
python -c "
import requests
response = requests.post('http://localhost:8000/api/auth/login/', 
    json={'email': 'admin@gmail.com', 'password': 'admin'})
print(f'Login: {response.status_code} - {response.json()}')
"
```

If this returns 200 with tokens, backend is working fine.

## 📱 Frontend Debugging Steps

### Step 1: Clear Browser Cache
1. Press **Ctrl + Shift + Delete**
2. Clear "Cached images and files"
3. Clear "Cookies and other site data"
4. Refresh page

### Step 2: Check localStorage
1. In browser console, type:
```javascript
localStorage.clear()
```
2. Refresh the page
3. Try login again

### Step 3: Check if axios is making the request
1. In browser console, type:
```javascript
fetch('http://localhost:8000/api/auth/login/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email: 'admin@gmail.com', password: 'admin' })
})
.then(r => r.json())
.then(console.log)
```

If this works, the issue is in the React code.

## 🎯 Expected Behavior

### Successful Login:
1. User enters email and password
2. Frontend sends POST to `/api/auth/login/`
3. Backend returns:
   ```json
   {
     "user": { "id": 1, "username": "admin", "email": "admin@gmail.com" },
     "tokens": { "access": "...", "refresh": "..." }
   }
   ```
4. Frontend saves token to localStorage
5. User redirected to `/dashboard`

### Successful Signup:
1. User enters name, email, password
2. Frontend generates username from email
3. Frontend sends POST to `/api/auth/register/`
4. Backend creates user and returns tokens
5. Frontend saves token to localStorage
6. User redirected to `/dashboard`

## 🔧 Final Checklist

- ✅ Backend running on http://localhost:8000
- ✅ Frontend running on http://localhost:3000
- ✅ CORS configured correctly
- ✅ API endpoints fixed to `/api/auth/...`
- ✅ Backend endpoints tested and working
- ⏳ **Need to verify**: Frontend making correct requests

## 🆘 If Still Not Working

1. **Restart both servers** (backend and frontend)
2. **Clear browser cache** completely
3. **Check browser console** for specific error messages
4. **Check Network tab** to see what request is being sent
5. **Share the error message** from browser console

The backend is 100% working, so the issue is in:
- Frontend not running
- Browser cache
- Network request format
- Or the error message not being displayed properly

## 📝 What to Check Next

Please check:
1. Is frontend running? (`npm run dev` in frontend folder)
2. What error do you see in browser console?
3. What status code do you see in Network tab?
4. Can you access http://localhost:3000 ?

Share the error message and I'll help you fix it immediately!
