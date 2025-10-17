# 🚀 Quick Start Guide - Connect Frontend to Backend

## Step-by-Step Instructions

### ✅ Step 1: Install Backend Packages

Open terminal in the **main project directory** and run:

```bash
pip install -r requirement.txt
```

Or install manually:
```bash
pip install djangorestframework djangorestframework-simplejwt django-cors-headers
```

### ✅ Step 2: Start Django Backend

**Option A - Use the batch script:**
```bash
start_backend.bat
```

**Option B - Manual command:**
```bash
python manage.py runserver
```

✅ Backend should start on: **http://localhost:8000**

---

### ✅ Step 3: Start Next.js Frontend

Open a **NEW terminal** and run:

**Option A - Use the batch script:**
```bash
start_frontend.bat
```

**Option B - Manual commands:**
```bash
cd frontend
npm run dev
```

✅ Frontend should start on: **http://localhost:3000**

---

### ✅ Step 4: Test Login

1. Open browser: **http://localhost:3000**
2. Click **"Login"** button
3. Enter your admin credentials:
   - **Email**: `admin@gmail.com`
   - **Password**: (your admin password)
4. Click **"Sign In"**

✅ You should be redirected to the **Dashboard** with real data!

---

## 🎯 What to Expect

### Landing Page (/)
- Hero section with gradient
- "Get Started" and "Login" buttons
- Features showcase

### Login Page (/login)
- Email and password fields
- Form validation
- Error messages if credentials are wrong

### Dashboard (/dashboard)
- **Total Facebook Accounts** - from your database
- **Total Posts Created** - from your database
- **Pending Posts** - posts with status 'pending'
- **Posted Today** - posts marked as posted
- **Success Rate** - percentage calculation
- Sidebar with navigation
- Your user info displayed

---

## 🔍 Verify Everything Works

### Backend Check:
```bash
# Visit in browser or curl
http://localhost:8000/api/auth/login/
```
Should show: `{"detail":"Method \"GET\" not allowed."}`  
✅ This means the endpoint exists!

### Frontend Check:
- Landing page loads without errors
- Console has no red errors
- Can navigate between pages

### Integration Check:
- Login works with your admin account
- Dashboard shows real statistics
- Network tab shows API calls to `http://localhost:8000/api/`
- No CORS errors in console

---

## 🐛 Troubleshooting

### "Module not found: rest_framework"
```bash
pip install djangorestframework djangorestframework-simplejwt django-cors-headers
```

### "Port 8000 already in use"
```bash
# Find and kill the process
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F
```

### "Port 3000 already in use"
```bash
npx kill-port 3000
```

### "CORS error" in browser console
1. Check Django is running
2. Verify `settings.py` has `corsheaders` in INSTALLED_APPS
3. Verify CORS_ALLOWED_ORIGINS includes `http://localhost:3000`

### Login doesn't work / "Invalid credentials"
```bash
# Reset admin password
python manage.py changepassword admin
```

### Dashboard shows "Loading..." forever
1. Open DevTools (F12)
2. Go to **Network** tab
3. Look for failed API requests
4. Check if Django backend is running
5. Verify `.env.local` has `NEXT_PUBLIC_API_URL=http://localhost:8000/api`

---

## 📂 Files Created/Modified

### Backend:
- ✏️ `bot_core/settings.py` - Added REST, JWT, CORS config
- ✏️ `bot_core/urls.py` - Added API routes
- ✏️ `requirement.txt` - Added new packages
- ✨ `accounts/serializers.py` - NEW
- ✨ `accounts/api_views.py` - NEW
- ✨ `accounts/api_urls.py` - NEW
- ✨ `postings/serializers.py` - NEW
- ✨ `postings/api_views.py` - NEW
- ✨ `postings/api_urls.py` - NEW

### Frontend:
- ✨ `frontend/.env.local` - NEW (API URL)

### Helper Files:
- ✨ `start_backend.bat` - NEW (quick start backend)
- ✨ `start_frontend.bat` - NEW (quick start frontend)
- ✨ `BACKEND_FRONTEND_SETUP.md` - NEW (detailed docs)
- ✨ `INTEGRATION_COMPLETE.md` - NEW (what was done)
- ✨ `QUICK_START_INTEGRATION.md` - NEW (this file)

---

## 🎉 Success!

When everything works:

**Backend Terminal:**
```
Django version 5.2.2, using settings 'bot_core.settings'
Starting development server at http://127.0.0.1:8000/
```

**Frontend Terminal:**
```
✓ Ready on http://localhost:3000
```

**Browser:**
- ✅ Landing page loads
- ✅ Can login with admin account
- ✅ Dashboard shows real data
- ✅ No console errors

---

## 📞 Need Help?

Check these files for more info:
- `INTEGRATION_COMPLETE.md` - Full details of what was built
- `BACKEND_FRONTEND_SETUP.md` - Complete API documentation
- `frontend/README.md` - Frontend documentation

---

**Ready to start?** Run `start_backend.bat` and `start_frontend.bat` now! 🚀
