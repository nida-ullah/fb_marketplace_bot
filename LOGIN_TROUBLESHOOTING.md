# 🔍 Login Issue - Troubleshooting Guide

## ✅ Both Servers Are Running!

- **Backend:** http://127.0.0.1:8000 ✅
- **Frontend:** http://localhost:3000 ✅

## Common Login Issues & Solutions

### Issue 1: No User Account Exists

**Solution:** Create a superuser in Django

```bash
# Open a new terminal in the project root
cd c:/Users/NidaUllah/OneDrive\ -\ Higher\ Education\ Commission/Documents/Development/fb_marketplace_bot

# Activate virtual environment
source env/Scripts/activate

# Create superuser
python manage.py createsuperuser

# Enter:
# Email: your@email.com
# Password: your_password
# Password (again): your_password
```

### Issue 2: CORS Error

**Symptoms:** Browser console shows CORS policy error

**Solution:** Already configured in `bot_core/settings.py` with:
- `CORS_ALLOW_ALL_ORIGINS = True` (development)
- `CORS_ALLOW_CREDENTIALS = True`

### Issue 3: Wrong API Endpoint

**Check:**
1. Frontend expects: `/api/auth/login/`
2. Backend should have this route configured

**Verify backend routes:**
```bash
python manage.py show_urls | grep login
```

### Issue 4: Token Authentication Not Working

**Check AuthContext:**
- Saves token to `localStorage.setItem("token", tokens.access)`
- Axios interceptor adds: `Authorization: Bearer ${token}`

## 🧪 Test Steps

### Step 1: Open Browser Console
1. Open http://localhost:3000/login
2. Press F12 to open DevTools
3. Go to Console tab

### Step 2: Try to Login
1. Enter email and password
2. Click Login
3. Watch for errors in console

### Step 3: Check Network Tab
1. Go to Network tab in DevTools
2. Click Login
3. Look for `/api/auth/login/` request
4. Check the response:
   - **200 OK** = Success
   - **400 Bad Request** = Wrong credentials
   - **404 Not Found** = Backend route missing
   - **500 Server Error** = Backend error

## 🔧 Quick Fixes

### Fix 1: Create Test User

```bash
# In Django shell
python manage.py shell

from django.contrib.auth import get_user_model
User = get_user_model()

# Create user
user = User.objects.create_user(
    email='test@example.com',
    password='test123456'
)
print(f"User created: {user.email}")
```

### Fix 2: Check Django Backend Logs

When you try to login, watch the terminal running `python manage.py runserver` for errors like:
- `404 Not Found` - Route doesn't exist
- `500 Internal Server Error` - Backend crash
- Authentication errors

### Fix 3: Test Backend Directly

Use curl or Postman to test the login endpoint:

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123456"}'
```

Expected response:
```json
{
  "tokens": {
    "access": "eyJ0eXAiOiJKV1QiLCJ...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJ..."
  },
  "user": {
    "id": 1,
    "email": "test@example.com"
  }
}
```

## 📋 Checklist

- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] User account created (superuser or regular user)
- [ ] CORS configured in Django settings
- [ ] Auth routes exist in Django URLs
- [ ] Browser console shows no errors
- [ ] Network tab shows 200 OK response

## 🎯 Most Likely Issue

**You don't have a user account yet!**

Run this command:
```bash
cd c:/Users/NidaUllah/OneDrive\ -\ Higher\ Education\ Commission/Documents/Development/fb_marketplace_bot
source env/Scripts/activate
python manage.py createsuperuser
```

Then try logging in with those credentials!

## 📝 Default Test Credentials

If you want to use default credentials, create user with:
- **Email:** `admin@example.com`
- **Password:** `admin123`

```python
# In Django shell
from django.contrib.auth import get_user_model
User = get_user_model()
user = User.objects.create_superuser(
    email='admin@example.com',
    password='admin123'
)
```

---

**Need more help?** Tell me:
1. What error message you see in the browser console
2. What the backend terminal shows when you try to login
3. Did you create a user account?
