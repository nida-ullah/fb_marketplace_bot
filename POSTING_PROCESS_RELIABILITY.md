# Posting Process Reliability Guide

## Current Behavior

### ✅ What Works:
- Posting runs in background via `subprocess.Popen()`
- Closing the **browser/frontend** does NOT stop posting
- Process is independent of your browser session
- Logs are written to `logs/posting_process.log`

### ❌ Limitations:
- If you close the **Django backend server**, posting STOPS
- No automatic retry if a post fails
- No recovery if server crashes mid-posting
- Dependent on your computer staying awake

---

## How to Ensure Posting Completes

### Option 1: Keep Backend Running (Current Setup)
**What to do:**
1. Start posting from frontend
2. Close browser if you want ✅
3. **Keep the backend terminal open** ⚠️
4. **Keep computer awake** ⚠️

**Pros:**
- No changes needed
- Works with current setup

**Cons:**
- Must keep backend running
- Computer can't sleep
- No recovery from crashes

---

### Option 2: Run as Detached Background Service (Recommended)

**For Windows:**
Use Task Scheduler or NSSM (Non-Sucking Service Manager)

**For Linux/Mac:**
Use systemd, supervisor, or PM2

**Steps:**
1. Install supervisor:
   ```bash
   pip install supervisor
   ```

2. Create supervisord config:
   ```ini
   [program:posting_worker]
   command=/path/to/python manage.py post_to_marketplace --post-ids %(ENV_POST_IDS)s
   directory=/path/to/fb_marketplace_bot
   autostart=false
   autorestart=true
   stderr_logfile=/path/to/logs/posting_worker.err.log
   stdout_logfile=/path/to/logs/posting_worker.out.log
   ```

**Pros:**
- ✅ Runs independently of terminal
- ✅ Auto-restart on failure
- ✅ Can close everything safely

**Cons:**
- Requires additional setup

---

### Option 3: Use Celery (Best for Production)

**Install:**
```bash
pip install celery redis
```

**Benefits:**
- ✅ Proper task queue
- ✅ Built-in retry logic
- ✅ Survives server restarts
- ✅ Can monitor progress
- ✅ Can pause/resume tasks
- ✅ Distributed workers

**How it works:**
```python
# Instead of subprocess.Popen()
from tasks import post_to_facebook_task

# Queue the task
result = post_to_facebook_task.delay(post_ids)

# Task runs in background worker
# Even if Django server restarts, task continues!
```

---

## Current Process Flow

```
User clicks "Start Posting"
         ↓
API: /api/posts/start-posting/
         ↓
subprocess.Popen() launches
         ↓
python manage.py post_to_marketplace --post-ids 1,2,3
         ↓
For each post:
  1. Load session
  2. Open Playwright browser
  3. Login to Facebook
  4. Post item
  5. Mark post.posted = True
  6. Close browser
         ↓
All posts processed
         ↓
Process exits
```

---

## What Happens in Each Scenario

### Scenario 1: You close the browser
```
✅ Posting CONTINUES
Why: Frontend is just a UI, backend is independent
```

### Scenario 2: You close the backend terminal
```
❌ Posting STOPS
Why: subprocess.Popen() creates child process
     Child dies when parent (Django) dies
```

### Scenario 3: Computer goes to sleep
```
❌ Posting PAUSES
Why: All processes freeze when computer sleeps
Result: May timeout or fail when waking up
```

### Scenario 4: Internet disconnects during posting
```
❌ Current post FAILS
✅ Process continues to next post
Result: Some posts fail, others may succeed
```

### Scenario 5: Server crashes mid-posting
```
❌ All posting STOPS
Result: Posts that were marked "posted=True" are done
        Posts still "posted=False" remain pending
        Can restart posting for pending posts
```

---

## How to Check if Posting is Still Running

### Method 1: Check the log file
```bash
# On Windows
type logs\\posting_process.log

# On Linux/Mac
tail -f logs/posting_process.log
```

### Method 2: Check running processes
```bash
# Windows
tasklist | findstr python

# Linux/Mac
ps aux | grep post_to_marketplace
```

### Method 3: Check database
```bash
python manage.py shell

>>> from postings.models import MarketplacePost
>>> MarketplacePost.objects.filter(posted=False).count()
# If this number decreases, posting is still running
```

---

## Recommendations

### For Development (Current Setup):
✅ **Keep backend terminal open** while posting
✅ **Don't put computer to sleep**
✅ Close browser if needed - posting continues
✅ Monitor logs to see progress

### For Production:
1. ✅ **Use Celery + Redis** for proper task queue
2. ✅ **Run Django as a service** (systemd/supervisor)
3. ✅ **Add retry logic** for failed posts
4. ✅ **Add health checks** to resume failed batches
5. ✅ **Use headless mode** (Playwright headless=True)
6. ✅ **Run on a server/VPS** not your local computer

---

## Quick Test

To test if posting survives browser closure:

1. Start posting a batch of posts
2. Immediately close your browser
3. Wait 30 seconds
4. Reopen browser and check posts page
5. You should see some posts marked as "Posted"

To test if posting survives backend closure:

1. Start posting
2. Close the Django backend terminal
3. Wait 30 seconds
4. Restart backend and check posts
5. Posting will have STOPPED (some posts may be done)

---

## Future Improvements

### Add Process Status Tracking:

Create a `PostingJob` model to track progress:

```python
class PostingJob(models.Model):
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True)
    total_posts = models.IntegerField()
    completed_posts = models.IntegerField(default=0)
    failed_posts = models.IntegerField(default=0)
    status = models.CharField(max_length=20)  # running, completed, failed
```

### Add Real-time Progress Updates:

Use WebSockets to send live updates to frontend:
- "Posting 3 of 10..."
- "Post #5 completed successfully"
- "Post #7 failed: Session expired"

### Add Automatic Resume:

On server restart, check for incomplete jobs and resume:
```python
# On startup
incomplete_jobs = PostingJob.objects.filter(status='running')
for job in incomplete_jobs:
    resume_posting(job)
```

---

## Summary

**Current Answer to Your Question:**

> "If I start posting and close the browser, will posting continue?"

✅ **YES** - Posting continues if you close the **browser**
❌ **NO** - Posting stops if you close the **backend server**

**Best Practice:**
- For now: Keep backend terminal open until posting completes
- For production: Use Celery + Redis for robust background tasks
- Monitor: Check `logs/posting_process.log` for progress
- Recovery: Pending posts (posted=False) can be re-posted anytime
