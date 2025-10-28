# 🔒 Security Analysis: Facebook Account Storage

## Current Implementation Review

### ✅ What You're Doing RIGHT:

1. **Session Files** (`.json` files)
   - ✅ Storing Facebook session cookies in `/sessions/` folder
   - ✅ Contains authentication tokens (not passwords)
   - ✅ Can reuse without re-login
   - ✅ Sessions expire naturally (Facebook manages this)

2. **Session-Based Authentication**
   - ✅ Primary authentication uses session files
   - ✅ Playwright loads session to bypass login
   - ✅ No password needed for posting

### ⚠️ Current Security Issues:

1. **Password Storage in Database** ❌
   ```python
   # accounts/models.py
   password = models.CharField(max_length=255)  # ⚠️ STORED IN PLAIN TEXT!
   ```
   - ❌ **Passwords stored unencrypted** in SQLite database
   - ❌ Anyone with database access sees passwords
   - ❌ If database is leaked, all Facebook accounts compromised

2. **Why You Need Password** ⚠️
   ```python
   # Used only when session expires or doesn't exist
   # automation/post_to_facebook.py - line 45
   if password:
       page.fill('input[name="pass"]', password)  # Re-login
   ```
   - Password needed for initial login
   - Password needed when session expires
   - Password needed to refresh session

---

## 🎯 Security Recommendations

### Option 1: **Encrypt Passwords** (RECOMMENDED)
Keep password in database but encrypt it properly.

#### Implementation:

```python
# 1. Install cryptography package
# pip install cryptography

# 2. Create encryption utility
# accounts/encryption.py
from cryptography.fernet import Fernet
from django.conf import settings
import base64

class PasswordEncryption:
    """Encrypt/Decrypt Facebook passwords"""
    
    @staticmethod
    def get_cipher():
        """Get encryption cipher from settings"""
        key = settings.FACEBOOK_PASSWORD_ENCRYPTION_KEY.encode()
        return Fernet(key)
    
    @staticmethod
    def encrypt(password):
        """Encrypt a password"""
        cipher = PasswordEncryption.get_cipher()
        return cipher.encrypt(password.encode()).decode()
    
    @staticmethod
    def decrypt(encrypted_password):
        """Decrypt a password"""
        cipher = PasswordEncryption.get_cipher()
        return cipher.decrypt(encrypted_password.encode()).decode()


# 3. Update model
# accounts/models.py
from .encryption import PasswordEncryption

class FacebookAccount(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='facebook_accounts')
    email = models.EmailField()
    encrypted_password = models.TextField()  # Changed from password
    session_cookie = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def set_password(self, raw_password):
        """Encrypt and save password"""
        self.encrypted_password = PasswordEncryption.encrypt(raw_password)
    
    def get_password(self):
        """Decrypt and return password"""
        return PasswordEncryption.decrypt(self.encrypted_password)
    
    @property
    def password(self):
        """For backward compatibility"""
        return self.get_password()


# 4. Add encryption key to settings
# bot_core/settings.py
import os
from cryptography.fernet import Fernet

# Generate once and keep secret!
# Run this ONCE: python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
FACEBOOK_PASSWORD_ENCRYPTION_KEY = os.environ.get(
    'FB_PASSWORD_KEY',
    'your-generated-key-here'  # Replace with actual key
)


# 5. Update API views
# accounts/api_views.py
def add_facebook_account_with_login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    account = FacebookAccount.objects.create(
        user=request.user,
        email=email
    )
    account.set_password(password)  # Encrypts before saving
    account.save()
    
    # Use decrypted password for login
    success = save_session(email, account.get_password())
```

**Pros:**
- ✅ Passwords encrypted in database
- ✅ Can still re-login when session expires
- ✅ Minimal code changes
- ✅ Backward compatible

**Cons:**
- ⚠️ Encryption key must be kept secret
- ⚠️ If key is leaked, passwords can be decrypted

---

### Option 2: **Never Store Password** (MOST SECURE)
Only use session files, never store password.

#### Implementation:

```python
# 1. Remove password field from model
# accounts/models.py
class FacebookAccount(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email = models.EmailField()
    # NO PASSWORD FIELD!
    session_cookie = models.TextField(blank=True, null=True)
    session_expires = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


# 2. Update API - one-time password use
# accounts/api_views.py
def add_facebook_account_with_login(request):
    email = request.data.get('email')
    password = request.data.get('password')  # Only used once!
    
    # Create account WITHOUT saving password
    account = FacebookAccount.objects.create(
        user=request.user,
        email=email
    )
    
    # Use password ONLY to create session
    success = save_session(email, password)
    
    if success:
        # Password is discarded after session is created
        return Response({'message': 'Session saved, password not stored'})
    else:
        account.delete()
        return Response({'error': 'Login failed'}, status=400)


# 3. Handle session expiry
def update_account_session(request, pk):
    """When session expires, user must manually re-login"""
    account = FacebookAccount.objects.get(pk=pk)
    
    # User must open browser and login manually
    # We capture the session but never store password
    success = save_session(account.email, password=None)  # Manual login
    
    return Response({'message': 'Please login in the browser window'})
```

**Pros:**
- ✅ **ZERO password storage** - most secure
- ✅ No encryption needed
- ✅ Even if database leaked, passwords safe

**Cons:**
- ❌ Cannot auto-refresh session
- ❌ User must manually re-login when session expires
- ❌ More friction for users

---

### Option 3: **Hybrid Approach** (BALANCED)
Encrypt password, but add option to delete it after successful session.

```python
class FacebookAccount(models.Model):
    email = models.EmailField()
    encrypted_password = models.TextField(blank=True, null=True)  # Optional
    session_cookie = models.TextField(blank=True, null=True)
    password_deleted = models.BooleanField(default=False)
    
    def delete_password(self):
        """Remove password after session is established"""
        self.encrypted_password = None
        self.password_deleted = True
        self.save()
```

**Pros:**
- ✅ Secure by default (encrypted)
- ✅ Option to delete password after session created
- ✅ User choice (keep for auto-refresh or delete for security)

---

## 🔐 Additional Security Enhancements

### 1. Protect Session Files
```python
# Make sure sessions/ folder has proper permissions
import os
import stat

sessions_dir = 'sessions'
if not os.path.exists(sessions_dir):
    os.makedirs(sessions_dir, mode=0o700)  # Only owner can read/write
else:
    os.chmod(sessions_dir, 0o700)

# Set permissions on each session file
for session_file in os.listdir(sessions_dir):
    file_path = os.path.join(sessions_dir, session_file)
    os.chmod(file_path, 0o600)  # Only owner can read/write
```

### 2. Add .gitignore for Sessions
```bash
# .gitignore
sessions/*.json
!sessions/.gitkeep
db.sqlite3
*.pyc
```

### 3. Database Encryption (SQLite)
```python
# For production: Use SQLCipher instead of SQLite
# pip install sqlcipher3

# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'sqlcipher3',  # Instead of sqlite3
        'NAME': BASE_DIR / 'db.sqlite3',
        'OPTIONS': {
            'passphrase': os.environ.get('DB_PASSWORD')
        }
    }
}
```

### 4. Session Validation
```python
def is_session_valid(email):
    """Check if session file exists and is recent"""
    import json
    from datetime import datetime, timedelta
    
    session_file = f"sessions/{email.replace('@', '_').replace('.', '_')}.json"
    
    if not os.path.exists(session_file):
        return False
    
    # Check file age (Facebook sessions expire ~60 days)
    file_age = datetime.now() - datetime.fromtimestamp(os.path.getmtime(session_file))
    if file_age > timedelta(days=50):  # Refresh before expiry
        return False
    
    # Check if session contains required cookies
    with open(session_file, 'r') as f:
        session_data = json.load(f)
        cookies = session_data.get('cookies', [])
        has_auth_cookie = any(c['name'] in ['c_user', 'xs'] for c in cookies)
        return has_auth_cookie
```

### 5. Input Sanitization
```python
# accounts/serializers.py
from django.core.validators import EmailValidator
import re

class FacebookAccountSerializer(serializers.ModelSerializer):
    def validate_email(self, value):
        """Validate Facebook email format"""
        validator = EmailValidator()
        validator(value)
        return value.lower().strip()
    
    def validate_password(self, value):
        """Basic password validation"""
        if len(value) < 6:
            raise serializers.ValidationError("Password too short")
        # Don't allow SQL injection characters
        dangerous_chars = ["'", '"', ";", "--", "/*", "*/"]
        if any(char in value for char in dangerous_chars):
            raise serializers.ValidationError("Invalid characters in password")
        return value
```

### 6. Audit Logging
```python
# Create audit log model
class SecurityAudit(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    action = models.CharField(max_length=100)  # 'login', 'add_account', 'delete_account'
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.JSONField(default=dict)
    
    class Meta:
        ordering = ['-timestamp']

# Log sensitive actions
def log_security_event(request, action, details=None):
    SecurityAudit.objects.create(
        user=request.user,
        action=action,
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', ''),
        details=details or {}
    )

# Use in views
def add_facebook_account_with_login(request):
    # ... create account ...
    log_security_event(request, 'add_facebook_account', {
        'email': account.email,
        'success': True
    })
```

---

## 📋 Implementation Priority

### High Priority (Do Now):
1. ✅ **Encrypt passwords** in database (Option 1)
2. ✅ **Secure session files** (proper permissions)
3. ✅ **Add .gitignore** for sessions and database
4. ✅ **Input validation** on email/password

### Medium Priority:
1. **Session validation** before use
2. **Audit logging** for admin actions
3. **Environment variables** for encryption keys

### Low Priority (Production):
1. Database encryption (SQLCipher)
2. Two-factor authentication
3. Session timeout/auto-logout

---

## 🎯 My Recommendation

**Go with Option 1: Encrypt Passwords**

**Why:**
- ✅ Best balance of security and functionality
- ✅ Can auto-refresh sessions when they expire
- ✅ Minimal user friction
- ✅ Passwords protected even if database leaked
- ✅ Easy to implement

**Implementation Steps:**
1. Install cryptography: `pip install cryptography`
2. Generate encryption key (one-time)
3. Update model to use encrypted_password
4. Create migration
5. Encrypt existing passwords
6. Store key in environment variable (not in code!)

---

## 🔑 Generate Encryption Key

```bash
# Run this ONCE to generate a key:
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"

# Output example: gAAAAABhc6_Q8yN2...
# Add to .env file:
FB_PASSWORD_KEY=gAAAAABhc6_Q8yN2...

# NEVER commit this key to Git!
```

---

## Summary

**Current Status:**
- ⚠️ Passwords stored in plain text
- ✅ Session files used for authentication
- ⚠️ Session files not gitignored

**Recommended Actions:**
1. Encrypt passwords ← **START HERE**
2. Secure session files
3. Add proper validation
4. Implement audit logging

**Result:**
- 🔒 Passwords encrypted
- 🔒 Sessions protected
- 🔒 Full audit trail
- 🔒 Production-ready security

Would you like me to implement the password encryption for you?
