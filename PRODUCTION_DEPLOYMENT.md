# Production Deployment Guide - Headless Browser Mode

## 🎯 Overview
This guide explains how to configure the bot to run in **headless mode** for production hosting, while keeping it visible during local development.

---

## 🔧 How It Works

### Headless Mode
- **Headless = True** (Production): Browser runs in background, no window opens
- **Headless = False** (Development): Browser window visible, you can see what's happening

### Configuration Method
The bot uses an environment variable: `PLAYWRIGHT_HEADLESS`

---

## 📝 Configuration

### Option 1: Using .env File (Recommended)

1. **Copy the example file**:
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` file**:
   
   **For Local Development** (see browser):
   ```env
   PLAYWRIGHT_HEADLESS=false
   ```
   
   **For Production** (headless):
   ```env
   PLAYWRIGHT_HEADLESS=true
   ```

### Option 2: Environment Variable (Hosting Platforms)

Set the environment variable in your hosting platform:

**Heroku**:
```bash
heroku config:set PLAYWRIGHT_HEADLESS=true
```

**AWS / EC2**:
```bash
export PLAYWRIGHT_HEADLESS=true
```

**Docker**:
```dockerfile
ENV PLAYWRIGHT_HEADLESS=true
```

**Render / Railway / Vercel**:
Add in environment variables section: `PLAYWRIGHT_HEADLESS=true`

### Option 3: No Configuration (Default)

If you don't set anything, it defaults to **headless=true** (production mode).

---

## 🚀 Production Setup

### Step 1: Install Playwright Dependencies

On your production server, install Playwright browsers:

```bash
# Install Python dependencies
pip install -r requirement.txt

# Install Playwright browsers
python -m playwright install chromium

# Install system dependencies (Linux servers)
python -m playwright install-deps
```

### Step 2: Set Environment Variable

```bash
export PLAYWRIGHT_HEADLESS=true
```

Or add to your `.env` file:
```env
PLAYWRIGHT_HEADLESS=true
```

### Step 3: Test It

```bash
# Start Django
python manage.py runserver

# In another terminal, test posting
python manage.py post_to_marketplace
```

**Expected**: No browser window opens, but posting works in background!

---

## 🖥️ Local Development Setup

### Step 1: Create .env File

```bash
cp .env.example .env
```

### Step 2: Edit .env

```env
PLAYWRIGHT_HEADLESS=false
```

### Step 3: Run Django

```bash
python manage.py runserver
```

### Step 4: Test Posting

- Go to Posts page
- Select a pending post
- Click "Start Posting"

**Expected**: Browser window opens, you can see Playwright filling the form! 🎉

---

## 📊 Behavior Comparison

| Mode | Browser Window | Console Window (Windows) | Use Case |
|------|---------------|-------------------------|----------|
| **Headless = false** | ✅ Visible | ✅ Opens | Local development, debugging |
| **Headless = true** | ❌ Hidden | ❌ No console | Production, hosting, automation |

---

## 🐛 Troubleshooting

### Issue 1: Browser opens in production

**Problem**: Browser window opening on server  
**Solution**: Set `PLAYWRIGHT_HEADLESS=true`

```bash
export PLAYWRIGHT_HEADLESS=true
```

### Issue 2: Can't see browser locally

**Problem**: Browser not visible during development  
**Solution**: Set `PLAYWRIGHT_HEADLESS=false` in `.env`

```env
PLAYWRIGHT_HEADLESS=false
```

### Issue 3: Playwright not installed

**Error**: `Executable doesn't exist at ...`  
**Solution**: Install Playwright browsers

```bash
python -m playwright install chromium
python -m playwright install-deps  # Linux only
```

### Issue 4: Permission denied on Linux

**Problem**: Can't run browser on Linux server  
**Solution**: Install system dependencies

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2

# Or use Playwright's installer
python -m playwright install-deps
```

---

## 📁 File Changes Summary

### 1. `bot_core/settings.py`
Added:
```python
# Playwright Configuration
PLAYWRIGHT_HEADLESS = os.getenv('PLAYWRIGHT_HEADLESS', 'true').lower() == 'true'
```

### 2. `automation/post_to_facebook.py`
Added helper function:
```python
def get_headless_mode():
    """Get headless mode from settings, defaulting to True for production"""
    try:
        return settings.PLAYWRIGHT_HEADLESS
    except Exception:
        return os.getenv('PLAYWRIGHT_HEADLESS', 'true').lower() == 'true'
```

Updated all browser launches:
```python
headless_mode = get_headless_mode()
print(f"🌐 Browser mode: {'Headless' if headless_mode else 'Visible'}")
browser = p.chromium.launch(headless=headless_mode)
```

### 3. `postings/api_views.py`
Updated subprocess creation:
```python
# Only show console window if not in headless mode
headless = os.getenv('PLAYWRIGHT_HEADLESS', 'true').lower() == 'true'
if not headless:
    creation_flags = subprocess.CREATE_NEW_CONSOLE
```

---

## 🎯 Quick Start Commands

### Local Development
```bash
# 1. Set environment
echo "PLAYWRIGHT_HEADLESS=false" > .env

# 2. Run server
python manage.py runserver

# 3. Open frontend
cd frontend && npm run dev

# 4. Test posting (browser will be visible)
```

### Production Deployment
```bash
# 1. Set environment
export PLAYWRIGHT_HEADLESS=true

# 2. Install dependencies
pip install -r requirement.txt
python -m playwright install chromium
python -m playwright install-deps

# 3. Run migrations
python manage.py migrate

# 4. Collect static files
python manage.py collectstatic --noinput

# 5. Start server
gunicorn bot_core.wsgi:application --bind 0.0.0.0:8000
```

---

## 🔍 Verification

### Check Current Mode

Add this to your posting logs:

```python
headless_mode = get_headless_mode()
print(f"🌐 Browser mode: {'Headless' if headless_mode else 'Visible'}")
```

**In logs you'll see**:
- `🌐 Browser mode: Visible` → Development mode (browser opens)
- `🌐 Browser mode: Headless` → Production mode (background)

---

## ✅ Testing Checklist

### Local Development Test
- [ ] Created `.env` file with `PLAYWRIGHT_HEADLESS=false`
- [ ] Started Django server
- [ ] Selected pending post
- [ ] Clicked "Start Posting"
- [ ] Browser window opened ✅
- [ ] Can see Playwright filling form ✅
- [ ] Post published successfully ✅

### Production Test
- [ ] Set `PLAYWRIGHT_HEADLESS=true` on server
- [ ] Installed Playwright: `python -m playwright install chromium`
- [ ] Installed system deps: `python -m playwright install-deps`
- [ ] Started server
- [ ] Triggered posting via API
- [ ] No browser window opened ✅
- [ ] Logs show "Browser mode: Headless" ✅
- [ ] Post published successfully ✅
- [ ] Checked `logs/posting_process.log` for output ✅

---

## 🎉 Summary

✅ **Headless mode configured**: Browser runs in background when hosted  
✅ **Development mode available**: Can see browser locally by setting `PLAYWRIGHT_HEADLESS=false`  
✅ **Easy switching**: Just change one environment variable  
✅ **Default behavior**: Runs headless (production-ready)  
✅ **Logging works**: All output written to `logs/posting_process.log`  

**Your bot is now ready for production hosting!** 🚀

---

## 📚 Related Files

- `.env.example` - Environment variable template
- `bot_core/settings.py` - Django settings with headless configuration
- `automation/post_to_facebook.py` - Playwright script with headless support
- `postings/api_views.py` - API endpoint that triggers posting
- `logs/posting_process.log` - Real-time posting logs

---

## 💡 Best Practices

1. **Always use `.env` file** in development
2. **Never commit `.env`** to git (add to `.gitignore`)
3. **Set environment variables** in production (don't use `.env` file)
4. **Monitor logs** via `logs/posting_process.log`
5. **Test locally first** with visible browser before deploying
6. **Install Playwright dependencies** on production server
7. **Use process manager** (systemd, supervisor, pm2) in production

---

**Need help?** Check the logs at `logs/posting_process.log` for detailed output! 📝
