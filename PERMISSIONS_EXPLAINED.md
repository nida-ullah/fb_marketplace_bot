# 🔐 Django User Permissions - Complete Guide

## Understanding the Permissions Section in Django Admin

When you edit a user in the Django admin panel, you see three important checkboxes under "Permissions":

---

## 1️⃣ Active (is_active)

```
☑ Active
```

**What it means:**
- Controls whether the user account is "enabled" or "disabled"
- Like a master ON/OFF switch for the account

**When CHECKED (☑):**
- ✅ User can login
- ✅ User can access the system
- ✅ Account is "active"

**When UNCHECKED (☐):**
- ❌ User CANNOT login (even with correct password)
- ❌ Account is "deactivated/suspended"
- 💡 Use this to temporarily disable an account without deleting it

**Example Use Cases:**
- Suspend a user temporarily (vacation, investigation)
- Disable account until email is verified
- Soft delete (keep data but prevent access)

---

## 2️⃣ Staff Status (is_staff)

```
☐ Staff status
    Designates whether the user can log into this admin site.
```

**What it means:**
- Controls access to the **Admin Panel** (http://localhost:8000/admin)
- Does NOT control access to your main app (frontend)

**When CHECKED (☑):**
- ✅ User can access admin panel at /admin
- ✅ User is considered "staff member"
- ⚠️ BUT they can only see what you give them permission to see
- 💡 Good for: Customer support, moderators, content managers

**When UNCHECKED (☐):**
- ❌ User CANNOT access admin panel at all
- ✅ User can still use your main app (Facebook marketplace bot)
- 💡 This is the default for regular users

**Example:**
- Regular user (customer): `is_staff = False`
- Support staff: `is_staff = True` (can see admin panel)
- Admin/Owner: `is_staff = True` + `is_superuser = True`

---

## 3️⃣ Superuser Status (is_superuser)

```
☐ Superuser status
    Designates that this user has all permissions without explicitly assigning them.
```

**What it means:**
- The "GOD MODE" checkbox
- User has ALL permissions automatically
- Can do EVERYTHING in the admin panel

**When CHECKED (☑):**
- ✅ Can access admin panel (auto-sets is_staff)
- ✅ Can see ALL models (Users, Facebook Accounts, Posts, etc.)
- ✅ Can add/edit/delete ANYTHING
- ✅ Can approve/reject users
- ✅ Can create other superusers
- ✅ Can change any settings
- ⚠️ **VERY POWERFUL - Use carefully!**

**When UNCHECKED (☐):**
- ❌ User only has specific permissions you assign
- 💡 Better for staff members with limited roles

**Example:**
- You (site owner): `is_superuser = True`
- Admin assistant: `is_superuser = False` but has specific permissions
- Regular users: `is_superuser = False`

---

## 🎯 Common Permission Combinations

### 1. Regular User (Default)
```
☑ Active
☐ Staff status
☐ Superuser status
☐ Is approved  (YOUR CUSTOM FIELD)
```
**Can do:**
- ❌ Cannot access admin panel
- ❌ Cannot login until approved
- Use case: Regular customers

### 2. Approved Regular User
```
☑ Active
☐ Staff status
☐ Superuser status
☑ Is approved  (YOUR CUSTOM FIELD)
```
**Can do:**
- ✅ Can login to main app
- ✅ Can add Facebook accounts
- ✅ Can create posts
- ❌ Cannot access admin panel
- Use case: Normal paying customers

### 3. Support Staff Member
```
☑ Active
☑ Staff status
☐ Superuser status
☑ Is approved
```
**Can do:**
- ✅ Can access admin panel
- ✅ Can view users (if you give permission)
- ❌ Cannot delete users (unless you give permission)
- ❌ Cannot create superusers
- Use case: Customer support, moderators

### 4. Administrator (You!)
```
☑ Active
☑ Staff status
☑ Superuser status
☑ Is approved
```
**Can do:**
- ✅ EVERYTHING!
- ✅ Full control of admin panel
- ✅ Can approve users
- ✅ Can manage all data
- Use case: Site owner, main admin

### 5. Suspended User
```
☐ Active          ← UNCHECKED!
☐ Staff status
☐ Superuser status
☑ Is approved
```
**Can do:**
- ❌ Cannot login (account disabled)
- 💡 Data is preserved
- Use case: Temporarily banned user

---

## 🔍 User Permissions (Groups and User Permissions)

Below the main checkboxes, you see two large boxes:

### Groups
```
Available groups          Chosen groups
────────────────    ⇄    ────────────────
(empty)                   (empty)
```

**What it is:**
- A way to assign permissions to multiple users at once
- Like creating "roles" or "teams"

**Example Groups You Could Create:**
- "Content Moderators" - Can edit posts but not delete
- "Billing Team" - Can view user accounts but not edit
- "Premium Users" - Special permissions for paid users

**How to use:**
1. Create a group in admin (Groups section)
2. Assign permissions to the group
3. Add users to the group
4. All users in group get those permissions automatically

### User Permissions
```
Available user permissions    Chosen user permissions
──────────────────────   ⇄   ──────────────────────
accounts | Can add...         (empty)
accounts | Can change...
accounts | Can delete...
accounts | Can view...
...
```

**What it is:**
- Specific permissions for THIS user only
- Very granular control

**Example Permissions:**
- `accounts | Can add facebook account` - User can create FB accounts
- `accounts | Can change facebook account` - User can edit FB accounts
- `accounts | Can delete facebook account` - User can delete FB accounts
- `accounts | Can view facebook account` - User can see FB accounts

**When to use:**
- Superusers: Don't need any (they have ALL)
- Staff members: Pick specific ones they need
- Regular users: Usually none (they use the main app, not admin)

---

## 🎯 For Your Use Case (Approval System)

### Your Custom Field: "Is approved"
```
☑ Is approved
    Designates whether this user has been approved by admin to login.
```

This is YOUR custom field, separate from Django's built-in ones!

**How it works with Django permissions:**

#### New User Registers:
```
☑ Active            (Django auto-sets this)
☐ Staff status      (Not staff)
☐ Superuser status  (Not superuser)
☐ Is approved       ← YOUR FIELD (starts unchecked)
```
Result: Can't login to main app (blocked by YOUR code)

#### You Approve:
```
☑ Active
☐ Staff status
☐ Superuser status
☑ Is approved       ← YOU CHECK THIS
```
Result: Can now login to main app!

#### Make Someone Staff:
```
☑ Active
☑ Staff status      ← CHECK THIS
☐ Superuser status
☑ Is approved
```
Result: Can access admin panel (limited permissions)

#### Make Someone Admin:
```
☑ Active
☑ Staff status      ← CHECK THIS
☑ Superuser status  ← CHECK THIS
☑ Is approved
```
Result: Full admin access!

---

## 💡 Quick Decision Guide

### "Should I check Staff Status?"
- ✅ YES: If they need to access admin panel
- ❌ NO: Regular users who only use your app

### "Should I check Superuser Status?"
- ✅ YES: Only for trusted admins (you, co-founder)
- ❌ NO: Everyone else (too powerful)

### "Should I check Active?"
- ✅ YES: Almost always (default)
- ❌ NO: Only to suspend/disable account

### "Should I check Is Approved?"
- ✅ YES: To allow them to use your app
- ❌ NO: To keep them in "pending" state

---

## 🔒 Security Best Practices

1. **Minimize Superusers**
   - Only 1-2 people (site owners)
   - Don't create superuser for every admin task

2. **Use Groups for Staff**
   - Create "Support Team" group with limited permissions
   - Add staff members to group
   - Easier to manage than individual permissions

3. **Regular Users Don't Need Admin Access**
   - `is_staff = False` for customers
   - They use your frontend app, not admin panel

4. **Your Approval Field is Separate**
   - Controls login to YOUR app
   - Django's Active controls login to admin
   - Both need to be checked for full access

---

## 📊 Summary Table

| Checkbox | What It Controls | Who Should Have It |
|----------|------------------|-------------------|
| **Active** | Can login at all | Everyone (unless suspended) |
| **Staff Status** | Can access admin panel | Only admins/staff |
| **Superuser** | Has ALL permissions | Only site owners |
| **Is Approved** (yours) | Can use main app | Approved customers only |

---

## 🎯 Your Current Setup

For the user in your screenshot (`test2`):

```
Current Settings:
☑ Active           → Account is enabled
☐ Staff status     → Cannot access admin panel
☐ Superuser status → Not an admin
☑ Is approved      → Can use your app
```

**This is PERFECT for a regular customer!**

They can:
- ✅ Login to your app (http://localhost:3000)
- ✅ Add Facebook accounts
- ✅ Create marketplace posts

They cannot:
- ❌ Access admin panel (http://localhost:8000/admin)
- ❌ See other users' data
- ❌ Approve other users

---

## 🚀 What You Should Do

### For Regular Users (Customers):
```
☑ Active
☐ Staff status
☐ Superuser status
☑ Is approved
```

### For Your Admin Account:
```
☑ Active
☑ Staff status
☑ Superuser status
☑ Is approved
```

### For Future Staff (if needed):
```
☑ Active
☑ Staff status      ← So they can access admin
☐ Superuser status  ← Don't give them full power
☑ Is approved

+ Add to "Support Team" group with specific permissions
```

---

**That's it! The permissions system gives you fine-grained control over who can do what in your system.** 🎉
