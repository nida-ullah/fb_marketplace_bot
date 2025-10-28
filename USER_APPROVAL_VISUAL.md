# 🎯 User Approval System - Visual Summary

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     USER REGISTRATION FLOW                       │
└─────────────────────────────────────────────────────────────────┘

                        NEW USER
                           │
                           ├─► Visits /signup
                           │
                           ├─► Fills Form
                           │   • Name
                           │   • Email  
                           │   • Password
                           │
                           ├─► Clicks "Create Account"
                           │
                           ▼
                    ┌──────────────┐
                    │   BACKEND    │
                    │  API /signup │
                    └──────────────┘
                           │
                           ├─► Creates User
                           │   is_approved = FALSE
                           │
                           ├─► Returns Success
                           │   (No tokens!)
                           │
                           ▼
                    ┌──────────────┐
                    │   FRONTEND   │
                    │ Shows Success│
                    │   Message    │
                    └──────────────┘
                           │
                           ▼
        ╔══════════════════════════════════════════╗
        ║ ✅ Account Created Successfully!         ║
        ║                                          ║
        ║ Your account is pending approval.        ║
        ║ You will be able to login once an        ║
        ║ administrator approves your account.     ║
        ╚══════════════════════════════════════════╝


┌─────────────────────────────────────────────────────────────────┐
│                    LOGIN ATTEMPT (UNAPPROVED)                    │
└─────────────────────────────────────────────────────────────────┘

                    UNAPPROVED USER
                           │
                           ├─► Tries to Login
                           │   /login
                           │
                           ▼
                    ┌──────────────┐
                    │   BACKEND    │
                    │  API /login  │
                    └──────────────┘
                           │
                           ├─► Checks Password ✓
                           │
                           ├─► Checks is_approved
                           │   is_approved = FALSE ✗
                           │
                           ├─► Returns 403 Forbidden
                           │
                           ▼
                    ┌──────────────┐
                    │   FRONTEND   │
                    │ Shows Error  │
                    └──────────────┘
                           │
                           ▼
        ╔══════════════════════════════════════════╗
        ║ ❌ Error                                 ║
        ║                                          ║
        ║ Your account is waiting for              ║
        ║ administrator approval.                  ║
        ║ Please contact the administrator.        ║
        ╚══════════════════════════════════════════╝


┌─────────────────────────────────────────────────────────────────┐
│                      ADMIN APPROVAL PROCESS                      │
└─────────────────────────────────────────────────────────────────┘

                        ADMIN
                           │
                           ├─► Logs into /admin
                           │   Username: admin
                           │   Password: admin
                           │
                           ├─► Navigates to "Users"
                           │
                           ▼
        ╔══════════════════════════════════════════╗
        ║ USERS LIST                               ║
        ║────────────────────────────────────────  ║
        ║ Username    | Email          | Status    ║
        ║────────────────────────────────────────  ║
        ║ admin       | admin@...      | ✓ Approved║
        ║ testuser    | test@...       | ✗ Pending ║
        ║ john        | john@...       | ✗ Pending ║
        ╚══════════════════════════════════════════╝
                           │
                           ├─► Clicks on "testuser"
                           │
                           ▼
        ╔══════════════════════════════════════════╗
        ║ EDIT USER: testuser                      ║
        ║                                          ║
        ║ Username: testuser                       ║
        ║ Email: test@example.com                  ║
        ║                                          ║
        ║ Approval Information:                    ║
        ║ ☑ Is approved                           ║
        ║ Approved at: ________                    ║
        ║ Approved by: ________                    ║
        ║                                          ║
        ║ [Save] [Delete]                          ║
        ╚══════════════════════════════════════════╝
                           │
                           ├─► Checks "Is approved"
                           │
                           ├─► Clicks "Save"
                           │
                           ▼
                    ┌──────────────┐
                    │   DATABASE   │
                    └──────────────┘
                           │
                           ├─► Updates User:
                           │   is_approved = TRUE
                           │   approved_at = NOW
                           │   approved_by = admin
                           │
                           ▼
        ╔══════════════════════════════════════════╗
        ║ ✓ User Approved Successfully!            ║
        ╚══════════════════════════════════════════╝


┌─────────────────────────────────────────────────────────────────┐
│                   LOGIN AFTER APPROVAL                           │
└─────────────────────────────────────────────────────────────────┘

                    APPROVED USER
                           │
                           ├─► Tries to Login
                           │   /login
                           │
                           ▼
                    ┌──────────────┐
                    │   BACKEND    │
                    │  API /login  │
                    └──────────────┘
                           │
                           ├─► Checks Password ✓
                           │
                           ├─► Checks is_approved
                           │   is_approved = TRUE ✓
                           │
                           ├─► Generates JWT Tokens
                           │   • Access Token
                           │   • Refresh Token
                           │
                           ▼
                    ┌──────────────┐
                    │   FRONTEND   │
                    │ Saves Tokens │
                    └──────────────┘
                           │
                           ├─► localStorage.setItem('token', ...)
                           │
                           ├─► Redirects to /dashboard
                           │
                           ▼
        ╔══════════════════════════════════════════╗
        ║ 🎉 DASHBOARD                             ║
        ║                                          ║
        ║ Welcome, testuser!                       ║
        ║                                          ║
        ║ Total Accounts: 0                        ║
        ║ Total Posts: 0                           ║
        ║                                          ║
        ║ [Add Account] [Create Post]              ║
        ╚══════════════════════════════════════════╝
```

---

## Database Schema

```
┌─────────────────────────────────────────────────────────────┐
│                     CustomUser Model                         │
├─────────────────────────────────────────────────────────────┤
│ id              : Integer (Primary Key)                     │
│ username        : String (Unique)                           │
│ email           : String (Unique)                           │
│ password        : String (Hashed)                           │
│ first_name      : String                                    │
│ last_name       : String                                    │
│ is_staff        : Boolean                                   │
│ is_superuser    : Boolean                                   │
│ date_joined     : DateTime                                  │
│ last_login      : DateTime                                  │
│────────────────────────────────────────────────────────────│
│ is_approved     : Boolean (DEFAULT: False) ⭐              │
│ approved_at     : DateTime (Null)          ⭐              │
│ approved_by     : ForeignKey → CustomUser  ⭐              │
│ rejection_reason: Text (Null)              ⭐              │
└─────────────────────────────────────────────────────────────┘

⭐ = New fields added for approval system
```

---

## API Endpoints

```
┌──────────────────────────────────────────────────────────────┐
│ POST /api/auth/signup/                                       │
├──────────────────────────────────────────────────────────────┤
│ Request:                                                     │
│ {                                                            │
│   "username": "testuser",                                    │
│   "email": "test@example.com",                               │
│   "password": "password123",                                 │
│   "confirm_password": "password123",                         │
│   "first_name": "Test",                                      │
│   "last_name": "User"                                        │
│ }                                                            │
├──────────────────────────────────────────────────────────────┤
│ Response (201 Created):                                      │
│ {                                                            │
│   "success": true,                                           │
│   "message": "Account created successfully! Your account...", │
│   "user": {                                                  │
│     "username": "testuser",                                  │
│     "email": "test@example.com",                             │
│     "is_approved": false                                     │
│   }                                                          │
│ }                                                            │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ POST /api/auth/login/                                        │
├──────────────────────────────────────────────────────────────┤
│ Request:                                                     │
│ {                                                            │
│   "email": "test@example.com",                               │
│   "password": "password123"                                  │
│ }                                                            │
├──────────────────────────────────────────────────────────────┤
│ Response if NOT APPROVED (403 Forbidden):                    │
│ {                                                            │
│   "error": "Account pending approval",                       │
│   "message": "Your account is waiting for admin approval...",│
│   "is_approved": false                                       │
│ }                                                            │
├──────────────────────────────────────────────────────────────┤
│ Response if APPROVED (200 OK):                               │
│ {                                                            │
│   "user": {                                                  │
│     "id": 2,                                                 │
│     "username": "testuser",                                  │
│     "email": "test@example.com",                             │
│     "is_approved": true                                      │
│   },                                                         │
│   "tokens": {                                                │
│     "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",                 │
│     "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."                   │
│   }                                                          │
│ }                                                            │
└──────────────────────────────────────────────────────────────┘
```

---

## Admin Panel Actions

```
╔══════════════════════════════════════════════════════════════╗
║                    BULK APPROVE USERS                         ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  [ ] admin       | admin@gmail.com       | ✓ Approved       ║
║  [✓] testuser    | test@example.com      | ✗ Pending        ║
║  [✓] john        | john@test.com         | ✗ Pending        ║
║  [✓] sarah       | sarah@test.com        | ✗ Pending        ║
║                                                              ║
║  Actions: [Approve selected users ▼] [Go]                   ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║  Result: 3 user(s) have been approved successfully.          ║
╚══════════════════════════════════════════════════════════════╝
```

---

## State Transitions

```
┌──────────────┐     Admin          ┌──────────────┐
│              │    Approves         │              │
│  UNAPPROVED  ├────────────────────►│   APPROVED   │
│              │                     │              │
│ is_approved  │                     │ is_approved  │
│   = false    │     Admin           │   = true     │
│              │◄────────────────────┤              │
└──────────────┘    Rejects          └──────────────┘
                                            │
                                            │ Can Login
                                            │ Gets Tokens
                                            │ Access Dashboard
                                            ▼
                                     ┌──────────────┐
                                     │    ACTIVE    │
                                     │     USER     │
                                     └──────────────┘
```

---

## Key Features Implemented

✅ **Custom User Model**
   - Extended AbstractUser with approval fields
   - Tracks approval status, timestamp, and approver

✅ **Registration Flow**
   - Creates user with is_approved=False
   - Returns success message (no tokens)
   - Shows approval pending notice

✅ **Login Protection**
   - Checks is_approved before generating tokens
   - Returns 403 if not approved
   - Clear error message to user

✅ **Admin Panel**
   - Color-coded approval status
   - Individual and bulk approval actions
   - Audit trail (who approved, when)
   - Search and filter capabilities

✅ **Frontend Updates**
   - Success message on signup
   - Error handling on login
   - Disabled form after successful signup

✅ **Security**
   - No tokens for unapproved users
   - Cannot access protected endpoints
   - Admin-only approval capability

---

**Status**: ✅ Fully Implemented and Tested
**Date**: October 28, 2025
