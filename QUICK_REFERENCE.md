# 🚀 Quick Reference - Headless Mode

## One-Line Commands

### Local Development (See Browser)
```bash
export PLAYWRIGHT_HEADLESS=false && python manage.py runserver
```

### Production (Headless)
```bash
export PLAYWRIGHT_HEADLESS=true && python manage.py runserver
```

### Check Current Mode
```bash
echo $PLAYWRIGHT_HEADLESS
```

---

## Installation (Production Server)

```bash
# 1. Install dependencies
pip install -r requirement.txt

# 2. Install Playwright browser
python -m playwright install chromium

# 3. Install system dependencies (Linux only)
python -m playwright install-deps

# 4. Set headless mode
export PLAYWRIGHT_HEADLESS=true

# 5. Run migrations
python manage.py migrate

# 6. Start server
python manage.py runserver
```

---

## Environment Variables

| Value | Mode | Browser | Use Case |
|-------|------|---------|----------|
| `false` | Development | Visible | Local testing |
| `true` | Production | Hidden | Hosting |
| (not set) | Production | Hidden | Default |

---

## Files Modified

- `bot_core/settings.py` → Added headless setting
- `automation/post_to_facebook.py` → Updated browser launches
- `postings/api_views.py` → Fixed path + subprocess flags

---

## Check Logs

```bash
# View logs in real-time
tail -f logs/posting_process.log

# Check last 50 lines
tail -n 50 logs/posting_process.log

# Search for errors
grep "Error\|Failed" logs/posting_process.log
```

---

## What You'll See

### Development Mode (PLAYWRIGHT_HEADLESS=false)
```
🌐 Browser mode: Visible
🌐 Opening Marketplace listing page...
[Browser window opens]
```

### Production Mode (PLAYWRIGHT_HEADLESS=true)
```
🌐 Browser mode: Headless
🌐 Opening Marketplace listing page...
[No browser window]
```

---

## Hosting Platforms

### Heroku
```bash
heroku config:set PLAYWRIGHT_HEADLESS=true
heroku buildpacks:add https://github.com/mxschmitt/heroku-playwright-buildpack
```

### Render
Add to Environment Variables:
```
PLAYWRIGHT_HEADLESS = true
```

### Railway
Add to Variables:
```
PLAYWRIGHT_HEADLESS = true
```

### Docker
```dockerfile
ENV PLAYWRIGHT_HEADLESS=true
RUN python -m playwright install chromium
RUN python -m playwright install-deps
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Browser opens on server | `export PLAYWRIGHT_HEADLESS=true` |
| Can't see browser locally | `export PLAYWRIGHT_HEADLESS=false` |
| "manage.py not found" | Already fixed! |
| "Executable doesn't exist" | `python -m playwright install chromium` |
| Permission denied (Linux) | `python -m playwright install-deps` |

---

## Test Commands

```bash
# Test visible mode
export PLAYWRIGHT_HEADLESS=false
python manage.py post_to_marketplace

# Test headless mode
export PLAYWRIGHT_HEADLESS=true
python manage.py post_to_marketplace

# Test via API
curl -X POST http://localhost:8000/api/posts/start-posting/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"post_ids": [44]}'
```

---

## Status Indicators

✅ Path to manage.py: **FIXED**  
✅ Headless mode: **IMPLEMENTED**  
✅ Environment config: **READY**  
✅ Production ready: **YES**  
✅ Documentation: **COMPLETE**

---

## Quick Links

- **Full Guide**: `PRODUCTION_DEPLOYMENT.md`
- **Summary**: `START_HERE_PRODUCTION.md`
- **Template**: `.env.example`

---

**Need help?** Check logs: `logs/posting_process.log` 📝
