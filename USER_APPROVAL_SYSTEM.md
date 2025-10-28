# User Approval System - Complete Guide

## 🎯 What Was Implemented

A **manual user approval system** where:
1. ✅ New users can register but cannot login immediately
2. ✅ They see a message: "Account created successfully! Your account is pending approval..."
3. ✅ Admin manually reviews and approves users in the admin panel
4. ✅ Only approved users can login and access the platform

---

## 🔧 Technical Changes Made

### 1. **Custom User Model** (`accounts/models.py`)
- Extended Django's `AbstractUser` with approval fields:
  - `is_approved` - Boolean flag (default: False)
  - `approved_at` - DateTime when approved
  - `approved_by` - ForeignKey to admin who approved
  - `rejection_reason` - Text field for rejection notes
- Methods: `approve()` and `reject()`

### 2. **Updated API Views** (`accounts/api_views.py`)
- **Register endpoint**: 
  - Creates user with `is_approved=False`
  - Returns success message instead of tokens
  - No automatic login
  
- **Login endpoint**:
  - Checks `is_approved` status before allowing login
  - Returns 403 Forbidden if not approved
  - Shows helpful error message

### 3. **Admin Panel** (`accounts/admin.py`)
- Custom `CustomUserAdmin` with:
  - Color-coded approval status (✓ Green / ✗ Red)
  - Bulk actions: "Approve selected users" and "Reject selected users"
  - Approval information section in user detail page
  - Auto-tracking of who approved and when

### 4. **Frontend Updates**
- **Signup Page** (`frontend/app/signup/page.tsx`):
  - Shows success message with approval notice
  - Disables form after successful registration
  - Provides link to login page
  
- **Auth Context** (`frontend/context/AuthContext.tsx`):
  - Handles approval response from backend
  - Shows appropriate error message on login attempt

---

## 📖 How To Use

### For Regular Users (Registration):

1. **Go to signup page**: `http://localhost:3000/signup`
2. **Fill out the form**: Name, Email, Password, Confirm Password
3. **Submit the form**
4. **See success message**: 
   ```
   Account Created Successfully!
   Your account is pending approval. 
   You will be able to login once an administrator approves your account.
   ```
5. **Wait for admin approval**

### For Admin (Approval Process):

1. **Login to admin panel**: `http://localhost:8000/admin`
   - Username: `admin`
   - Password: `admin`

2. **Navigate to Users**: Click "Users" in the sidebar

3. **View pending users**: Look for users with "✗ Pending" status

4. **Approve a user** (Individual):
   - Click on the user's username
   - Check the "Is approved" checkbox
   - Click "Save"
   - User will see `approved_at` timestamp and your username in `approved_by`

5. **Approve multiple users** (Bulk):
   - Select multiple users with checkboxes
   - Choose "Approve selected users" from Actions dropdown
   - Click "Go"
   - Success message appears

6. **Reject/Unapprove a user**:
   - Select user(s)
   - Choose "Reject/unapprove selected users" from Actions
   - Click "Go"

### For Approved Users (Login):

1. **Go to login page**: `http://localhost:3000/login`
2. **Enter email and password**
3. **Successfully login** and access dashboard

### If User Tries to Login Before Approval:

```
Error: Your account is waiting for administrator approval. 
Please contact the administrator.
```

---

## 🗄️ Database Changes

### Migration Applied:
- Created fresh database with `CustomUser` model
- Removed old migrations
- Applied new migrations with approval fields

### Superuser Created:
```
Username: admin
Password: admin
Email: admin@gmail.com
is_approved: True (auto-approved)
```

---

## 🎨 Admin Panel Features

### User List View Shows:
- Username
- Email
- First Name / Last Name
- **Approval Status** (color-coded)
- Is Staff
- Date Joined

### Filters Available:
- Approval Status
- Staff Status
- Superuser Status
- Date Joined

### Search:
- Username
- Email
- First Name
- Last Name

### Bulk Actions:
1. Approve selected users
2. Reject/unapprove selected users

---

## 🔒 Security Features

1. **No tokens issued** until approved
2. **Cannot login** if `is_approved=False`
3. **Audit trail**: Tracks who approved and when
4. **Rejection reasons**: Can document why user was rejected
5. **Admin-only actions**: Only superusers can approve

---

## 🚀 Production Deployment Recommendations

### 1. **Email Notifications**:
```python
# When user registers (add to register view):
from django.core.mail import send_mail

send_mail(
    'Account Pending Approval',
    'Your account has been created and is waiting for admin approval.',
    'from@example.com',
    [user.email],
)

# When admin approves (add to approve method):
send_mail(
    'Account Approved!',
    'Your account has been approved. You can now login.',
    'from@example.com',
    [user.email],
)
```

### 2. **Admin Notifications**:
```python
# Notify admins when new user registers
from django.contrib.auth import get_user_model

superusers = get_user_model().objects.filter(is_superuser=True)
admin_emails = [admin.email for admin in superusers]

send_mail(
    'New User Registration',
    f'{user.email} has registered and needs approval.',
    'from@example.com',
    admin_emails,
)
```

### 3. **Security Settings**:
```python
# settings.py
SESSION_COOKIE_SECURE = True  # Only send over HTTPS
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
```

---

## 📊 Monitoring Users as Site Owner

You can see all registered users and their status:

```python
# In Django shell or create admin API endpoint
from accounts.models import CustomUser

# Total registered users
total_users = CustomUser.objects.count()

# Pending approval
pending = CustomUser.objects.filter(is_approved=False).count()

# Approved users
approved = CustomUser.objects.filter(is_approved=True).count()

# Recently registered (last 7 days)
from django.utils import timezone
from datetime import timedelta

week_ago = timezone.now() - timedelta(days=7)
recent = CustomUser.objects.filter(date_joined__gte=week_ago).count()
```

---

## ✅ Testing Checklist

- [x] New user can register
- [x] Registration shows success message
- [x] User cannot login before approval
- [x] Login shows "pending approval" error
- [x] Admin can see pending users in admin panel
- [x] Admin can approve individual user
- [x] Admin can bulk approve users
- [x] Approved user can login successfully
- [x] Admin can reject/unapprove users
- [x] Approval timestamp and admin are tracked

---

## 🔄 Reverting Changes (If Needed)

If you want to go back to automatic approval:

1. **Set all users as approved**:
```python
python manage.py shell -c "
from accounts.models import CustomUser
CustomUser.objects.all().update(is_approved=True)
"
```

2. **Change default in model** (optional):
```python
# accounts/models.py
is_approved = models.BooleanField(default=True)  # Change to True
```

3. **Update register view** (optional):
```python
# Return tokens immediately after registration
refresh = RefreshToken.for_user(user)
return Response({
    'user': UserSerializer(user).data,
    'tokens': {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
})
```

---

## 📝 Next Steps (Optional Enhancements)

1. **Add email verification** before approval
2. **Create admin dashboard** showing approval statistics
3. **Add user roles** (e.g., Premium, Basic)
4. **Implement approval workflow** (e.g., requires 2 admins)
5. **Add expiration** for pending accounts (auto-delete after 30 days)
6. **Create API endpoint** for admins to approve from frontend
7. **Build admin notification system** in frontend

---

## 🎯 Summary

✅ **Users register** → See "Pending Approval" message  
✅ **Cannot login** → "Account waiting for approval" error  
✅ **Admin approves** → Via Django admin panel  
✅ **User can login** → Full access to platform  

**Current Status**: Fully implemented and working! 🚀
