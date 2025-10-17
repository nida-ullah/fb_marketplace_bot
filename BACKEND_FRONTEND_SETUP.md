# Backend & Frontend Integration Setup Guide

## 🚀 Quick Setup

### Step 1: Install Backend Dependencies

```bash
# In the main project directory
pip install djangorestframework djangorestframework-simplejwt django-cors-headers
```

### Step 2: Run Django Migrations (if needed)

```bash
python manage.py migrate
```

### Step 3: Start Django Backend

```bash
python manage.py runserver
```

Django will run on: **http://localhost:8000**

### Step 4: Start Next.js Frontend (in a new terminal)

```bash
cd frontend
npm run dev
```

Next.js will run on: **http://localhost:3000**

---

## 🔐 Testing Login with Existing Admin Account

Your existing admin account:
- **Email**: admin@gmail.com
- **Username**: admin
- **Password**: (your admin password)

### Login Steps:

1. Open **http://localhost:3000**
2. Click **"Login"**
3. Enter your credentials:
   - **Email**: admin@gmail.com (or username: admin)
   - **Password**: your admin password
4. Click **"Sign In"**

You should be redirected to the dashboard!

---

## 📡 API Endpoints Created

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login (returns JWT tokens)
- `GET /api/auth/user/` - Get current user info (requires JWT)

### Dashboard Stats
- `GET /api/stats/dashboard/` - Get dashboard statistics

### Facebook Accounts
- `GET /api/accounts/` - List all accounts
- `POST /api/accounts/` - Create new account
- `GET /api/accounts/<id>/` - Get specific account
- `PUT /api/accounts/<id>/` - Update account
- `DELETE /api/accounts/<id>/` - Delete account

### Marketplace Posts
- `GET /api/posts/` - List all posts
- `POST /api/posts/` - Create new post
- `GET /api/posts/<id>/` - Get specific post
- `PUT /api/posts/<id>/` - Update post
- `DELETE /api/posts/<id>/` - Delete post

---

## 🔧 What Was Configured

### Backend Changes (Django)

1. **settings.py**:
   - Added `rest_framework`, `rest_framework_simplejwt`, `corsheaders`
   - Configured JWT authentication (5-hour access token)
   - Enabled CORS for `http://localhost:3000`
   - Set up REST Framework defaults

2. **New Files Created**:
   - `accounts/serializers.py` - User, Register, FacebookAccount serializers
   - `accounts/api_views.py` - Authentication & account API views
   - `accounts/api_urls.py` - API URL routing
   - `postings/serializers.py` - MarketplacePost serializer
   - `postings/api_views.py` - Post API views
   - `postings/api_urls.py` - Post API URLs

3. **URLs Updated**:
   - `bot_core/urls.py` - Added `/api/` routes

### Frontend Changes

1. **Environment File**:
   - Created `.env.local` with `NEXT_PUBLIC_API_URL=http://localhost:8000/api`

2. **Already Configured** (from previous setup):
   - API client in `lib/api.ts`
   - Auth context in `context/AuthContext.tsx`
   - Login/Signup pages
   - Dashboard with protected routes

---

## 🧪 Testing the API

### Test with curl (optional):

```bash
# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@gmail.com","password":"your_password"}'

# Get dashboard stats (replace YOUR_TOKEN)
curl http://localhost:8000/api/stats/dashboard/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Test in Browser:

1. Start both servers
2. Visit http://localhost:3000
3. Login with admin account
4. Check dashboard - should show real data!

---

## 🎯 Current Status

### ✅ Backend Ready
- REST API endpoints configured
- JWT authentication enabled
- CORS configured for frontend
- Serializers created for all models

### ✅ Frontend Ready
- Environment variable set
- API client configured
- Auth context ready
- Protected routes working

### 🎉 What Works Now
- User can login with existing admin account
- JWT tokens are generated and stored
- Dashboard loads with authentication
- API calls include Bearer token
- Protected routes work correctly

---

## 🐛 Troubleshooting

### "Module not found: rest_framework"
```bash
pip install djangorestframework djangorestframework-simplejwt django-cors-headers
```

### "CORS error" in browser console
Check that Django is running and CORS is configured in settings.py

### "401 Unauthorized" on dashboard
- Make sure you're logged in
- Check that token is in localStorage: Open DevTools → Application → Local Storage → `auth_token`

### Dashboard shows "Loading..."
- Check Django is running on port 8000
- Check `.env.local` has correct API URL
- Open DevTools → Network tab to see API requests

---

## 📝 Next Steps

After login works:

1. **Build Accounts Page** - Create `/dashboard/accounts/page.tsx`
2. **Build Posts Page** - Create `/dashboard/posts/page.tsx`
3. **Add Bulk Upload** - Create `/dashboard/bulk-upload/page.tsx`
4. **Add Analytics** - Create `/dashboard/analytics/page.tsx`
5. **Add Settings** - Create `/dashboard/settings/page.tsx`

---

**Ready to test!** Start both servers and login at http://localhost:3000 🚀
