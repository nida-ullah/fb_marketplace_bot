# Quick Test Guide - Frontend Changes

## 🚀 How to Test Everything

### Prerequisites
1. Backend running: `python manage.py runserver`
2. Frontend running: `cd frontend && npm run dev`
3. At least one Facebook account added
4. Open browser: `http://localhost:3000`

---

## Test 1: Status Badges ✅

### Steps:
1. Go to Dashboard → Posts
2. Create a new post (or use existing ones)
3. **Before posting**: Look for **yellow "⏳ Pending"** badge
4. Click "Start Posting"
5. **During posting**: Watch for **blue "🔄 Posting..."** badge
6. **After success**: See **green "✅ Posted"** badge
7. **If error occurs**: See **red "❌ Failed"** badge with info icon (ℹ️)
8. **Hover over info icon**: Should show error message tooltip

### Expected Result:
- Each post shows appropriate color badge
- Failed posts show error details on hover
- Badges update automatically when status changes

---

## Test 2: Real-Time Progress (SSE) ✅

### Steps:
1. Create 5-10 posts (so you can see progress)
2. Click "Start Posting" button
3. **Immediately watch for**:
   - Progress card appears above posts
   - Green pulsing dot (connection status)
   - Progress bar starts at 0%
   - Statistics show Total/Completed/Failed

4. **While posting**:
   - Progress bar moves smoothly
   - "Currently posting: [title]" updates in real-time
   - Completed count increases
   - Percentage updates live

5. **When finished**:
   - Progress bar reaches 100%
   - Green success message appears
   - Connection closes (dot stops pulsing)
   - Progress card disappears after 2 seconds
   - Posts list auto-refreshes

### Expected Result:
- **No 3-second delays** (old polling is gone)
- Updates happen **instantly**
- Connection stays open during posting
- Auto-closes when done

### Browser Console Check:
Open DevTools Console (F12) and look for:
```
✅ SSE connection established
📊 Progress update: {status: "running", completed_posts: 3, ...}
🏁 Job finished, closing SSE connection
🧹 Cleaning up SSE connection
```

---

## Test 3: Session Persistence (Forever) ✅

### Steps:
1. Add a Facebook account with session
2. Wait 24 hours (or manually change file timestamp)
3. Go to backend: `http://localhost:8000/api/accounts/health-check/`
4. Check response JSON

### Expected Result:
```json
{
  "overall_health": "healthy",
  "accounts": [
    {
      "account_id": 1,
      "email": "test@example.com",
      "session_exists": true,
      "session_valid": true,  // ← Should be TRUE even if old
      "session_age_days": 45.2,  // ← Can be any number
      "health_status": "healthy"  // ← Always healthy if file exists
    }
  ]
}
```

### Manual File Test:
```bash
# Check session file exists
ls sessions/

# Example output:
# test_example_com.json

# File should have "cookies" field
cat sessions/test_example_com.json | grep cookies
```

---

## Test 4: Error Handling ✅

### Steps to Force an Error:
1. Create a post with very long title (>500 characters)
2. Or use an account with expired/invalid session
3. Start posting
4. Watch the failed post

### Expected Result:
- Post shows **red "Failed" badge**
- Info icon (ℹ️) appears next to badge
- Hover shows error message
- Retry count shows if > 0
- Error logged in backend ErrorLog table

### Backend Error Log Check:
```python
# Open Django shell
python manage.py shell

# Check error logs
from postings.models import ErrorLog
ErrorLog.objects.all().values('post_title', 'error_type', 'error_message')
```

---

## Test 5: TypeScript Type Safety ✅

### Steps:
1. Open `frontend/app/dashboard/posts/page.tsx` in VS Code
2. Try typing: `post.` and wait for autocomplete

### Expected IntelliSense:
You should see:
- ✅ status
- ✅ error_message
- ✅ retry_count
- ✅ account (nested object)
- ✅ account.email
- ✅ All other post fields

### Type Error Test:
```typescript
// This should show RED underline (TypeScript error)
post.status = 'invalid_status';

// This should work fine (no error)
post.status = 'pending';
```

---

## Test 6: Performance Comparison ✅

### Old System (Polling):
- Network tab shows HTTP requests every 3 seconds
- Many small requests
- 3-second delay to see updates

### New System (SSE):
1. Open DevTools → Network tab
2. Start posting
3. Look for **"status-stream"** connection (EventSource)
4. Should see **ONE connection** that stays open
5. Updates arrive instantly (no delay)

### Check:
- **Before**: 20 requests/minute
- **After**: 1 persistent connection
- **Speed**: Updates appear instantly

---

## Test 7: Mobile Responsiveness ✅

### Steps:
1. Open DevTools (F12)
2. Toggle device toolbar (Ctrl+Shift+M)
3. Select iPhone or Android device
4. Test all features

### Expected Result:
- Status badges visible
- Progress bar readable
- Statistics cards stack vertically
- Buttons work correctly
- Tooltips show on tap

---

## Common Issues & Fixes

### Issue 1: SSE shows "Disconnected"
**Fix:**
```bash
# Check backend is running
python manage.py runserver

# Check for CORS errors in console
# May need to add EventSource to CORS config
```

### Issue 2: "Connection lost" error
**Fix:**
- Backend crashed - check Django terminal for errors
- Network issue - check internet connection
- Firewall - allow localhost:8000

### Issue 3: Progress stuck at 0%
**Fix:**
```bash
# Check PostingJob is being created
python manage.py shell
from postings.models import PostingJob
PostingJob.objects.all()

# Should see jobs with status 'running'
```

### Issue 4: Types not working
**Fix:**
```bash
cd frontend
npm install  # Reinstall dependencies
# Restart VS Code
```

### Issue 5: Old polling still running
**Fix:**
- Hard refresh browser (Ctrl+Shift+R)
- Clear browser cache
- Check no old setInterval in code

---

## Success Criteria ✅

All features work if:
- ✅ Status badges show correct colors
- ✅ Real-time progress updates instantly
- ✅ SSE connection opens/closes properly
- ✅ Sessions don't expire after 30 days
- ✅ Error messages appear in tooltips
- ✅ TypeScript autocomplete works
- ✅ No console errors
- ✅ Mobile layout works
- ✅ Performance is better than before

---

## Next Steps

Once testing is complete:
1. ✅ **Production Deployment** - Follow VPS setup guide
2. 🔄 **Optional Enhancements** - Add health dashboard, error viewer
3. 📊 **Monitoring** - Track job success rate
4. 🔔 **Notifications** - Add email/browser notifications

---

## Questions?

Check these files for details:
- `FRONTEND_UPDATES_COMPLETE.md` - Full explanation of changes
- `frontend/types/index.ts` - TypeScript interfaces
- `frontend/components/PostingProgress.tsx` - SSE implementation
- `postings/realtime_views.py` - Backend SSE endpoint
