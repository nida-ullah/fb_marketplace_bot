# User Registration System - Complete Setup

## ✅ What's Already Available

### Backend (Django)
✅ **Registration API Endpoint**: `/api/accounts/auth/register/`
- Located in: `accounts/api_views.py`
- Accepts: username, email, password, confirm_password, first_name, last_name
- Returns: User data + JWT tokens (access & refresh)
- Permission: `AllowAny` (no authentication required)

✅ **Login API Endpoint**: `/api/accounts/auth/login/`
- Accepts: email or username + password
- Returns: User data + JWT tokens

✅ **User Profile Endpoint**: `/api/accounts/auth/user/`
- Returns: Current authenticated user data
- Requires: JWT token

### Frontend (Next.js)
✅ **Signup Page**: `/signup`
- Located in: `frontend/app/signup/page.tsx`
- Features:
  - Full name input
  - Email validation
  - Password with confirmation
  - Form validation using Zod
  - Error handling
  - Link to login page

✅ **Login Page**: `/login`
- Located in: `frontend/app/login/page.tsx`
- Has "Create account" link to `/signup`

✅ **Authentication Context**: `frontend/context/AuthContext.tsx`
- Provides: login(), signup(), logout() functions
- Handles: JWT token storage, auto-redirect, session persistence

✅ **API Integration**: `frontend/lib/api.ts`
- authAPI.signup() - Register new user
- authAPI.login() - Login existing user
- authAPI.getProfile() - Get user info

## 🔧 Recent Fixes Applied

1. **Fixed API endpoints** - Updated to use correct backend URLs:
   - `/api/accounts/auth/login/`
   - `/api/accounts/auth/register/`
   - `/api/accounts/auth/user/`

2. **Fixed signup parameters** - Backend expects:
   ```typescript
   {
     username: string,        // Auto-generated from email
     email: string,
     password: string,
     confirm_password: string, // Same as password
     first_name: string,      // From name field
     last_name: string        // From name field
   }
   ```

3. **Auto-generate username** - Frontend now splits full name and generates username from email

4. **Better error handling** - Shows specific validation errors (username taken, email exists, etc.)

## 🚀 How to Use

### For New Users (Registration)

1. **Navigate to signup page**:
   ```
   http://localhost:3000/signup
   ```

2. **Fill in the form**:
   - Full Name: e.g., "John Doe"
   - Email: e.g., "john@example.com"
   - Password: minimum 6 characters
   - Confirm Password: must match

3. **Click "Create account"**:
   - Account created in Django database
   - JWT tokens saved to localStorage
   - Auto-redirected to `/dashboard`

### For Existing Users (Login)

1. **Navigate to login page**:
   ```
   http://localhost:3000/login
   ```

2. **Enter credentials**:
   - Email: e.g., "admin@gmail.com"
   - Password: your password

3. **Click "Sign in"**:
   - JWT tokens saved
   - Redirected to dashboard

### Switching Between Pages

- **On Login page**: Click "Create account" link → Goes to `/signup`
- **On Signup page**: Click "Sign in" link → Goes to `/login`

## 🔐 Current Super User

You mentioned you created a superuser. You can login with that:
- URL: `http://localhost:3000/login`
- Email: (your superuser email)
- Password: (your superuser password)

## 📋 Testing Registration

### Test Case 1: New User Registration
```bash
1. Go to http://localhost:3000/signup
2. Enter:
   - Name: "Test User"
   - Email: "test@example.com"
   - Password: "test123"
   - Confirm: "test123"
3. Should redirect to dashboard after successful signup
```

### Test Case 2: Duplicate Email
```bash
1. Try signing up with email that already exists
2. Should show error: "user with this email already exists."
```

### Test Case 3: Password Mismatch
```bash
1. Enter different values in Password and Confirm Password
2. Should show error: "Passwords don't match"
```

## 🛠️ Backend Verification

You can verify user registration in Django admin:

```bash
# Login to Django admin
http://localhost:8000/admin

# Or check via shell
cd c:/Users/NidaUllah/OneDrive\ -\ Higher\ Education\ Commission/Documents/Development/fb_marketplace_bot
source env/Scripts/activate
python manage.py shell

# In Python shell:
from django.contrib.auth.models import User
User.objects.all()  # List all users
User.objects.filter(email='test@example.com')  # Check specific user
```

## 🔄 Authentication Flow

```
User fills signup form
        ↓
Frontend validates (Zod schema)
        ↓
POST /api/accounts/auth/register/
        ↓
Backend validates & creates user
        ↓
Returns JWT tokens + user data
        ↓
Frontend saves to localStorage
        ↓
Auto-redirect to /dashboard
        ↓
User is logged in
```

## 📝 Notes

- **No email verification** currently implemented (users can register immediately)
- **Username auto-generated** from email (part before @)
- **JWT tokens** used for authentication (no sessions)
- **Tokens persist** in localStorage (users stay logged in)
- **Auto-logout** on 401 errors (expired tokens)

## ✨ Next Steps (Optional Enhancements)

If you want to add more features:

1. **Email Verification**
   - Send confirmation email after signup
   - Verify email before allowing login

2. **Password Reset**
   - "Forgot password" link
   - Email with reset token

3. **Social Login**
   - Google OAuth
   - Facebook OAuth

4. **Profile Management**
   - Update user info
   - Change password
   - Upload avatar

5. **User Roles**
   - Admin, Manager, User roles
   - Permission-based access

But for now, **registration is fully functional** and ready to use! 🎉
