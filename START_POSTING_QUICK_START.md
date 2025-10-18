# Start Posting Feature - Quick Start Guide

## 🚀 How to Use

### Step 1: Create Pending Posts
1. Go to **Posts** page in dashboard
2. Click **"Create Post"** button
3. Fill in post details (title, description, price, image)
4. Select an account
5. Set scheduled time (any time)
6. Save post

### Step 2: Select Posts to Post
1. Check the boxes next to posts you want to publish
2. Bulk actions bar appears at the top
3. "Start Posting" button shows with count

### Step 3: Start Posting
1. Click **"Start Posting (N)"** green button
2. See success message: "Started posting process for N post(s)"
3. Selection clears automatically
4. Posts are being published in background

### Step 4: Verify
1. Wait 30-60 seconds per post
2. Refresh page or wait for auto-refresh
3. Check posts status changed to "Posted" (green badge)

---

## 💡 Tips

- **Select only pending posts** - Posted posts are automatically filtered out
- **No need to wait** - Background process continues even if you close browser
- **Check browser windows** - Playwright will open browser windows for each account
- **One account at a time** - If you have multiple accounts, posting happens sequentially

---

## ⚠️ Important Notes

### Before Using:
1. ✅ Ensure account has active session (green "Active" badge on Accounts page)
2. ✅ Verify post has image uploaded
3. ✅ Check price is valid number
4. ✅ Title and description filled

### During Posting:
- Browser windows will open automatically
- Don't close browser windows manually
- Process takes 30-60 seconds per post
- Check terminal for progress logs

### After Posting:
- Posts will show green "Posted" badge
- Check Facebook Marketplace to verify
- If failed, check terminal logs for errors

---

## 🐛 Common Issues

### "No pending posts found"
- You selected already posted posts
- Select posts with orange "Pending" badge

### "Session not found"
- Account needs to login again
- Go to Accounts page → Click "Update Session"

### Button doesn't appear
- Make sure to select at least one pending post
- Refresh page if bulk actions bar doesn't show

### Posts not getting published
- Check account session is active
- Verify image file exists
- Check terminal/console for errors
- Try posting one post at a time first

---

## 📊 What Happens Behind the Scenes

1. **Frontend** sends post IDs to backend
2. **Backend** filters only pending posts
3. **Subprocess** starts management command
4. **Playwright** opens browser with saved session
5. **Script** navigates to Marketplace create page
6. **Form** is filled with post details
7. **Image** is uploaded
8. **Post** is published to Facebook
9. **Database** marks post as `posted=True`

---

## 🎯 Best Practices

### For Best Results:
- ✅ Test with 1-2 posts first
- ✅ Use active accounts with valid sessions
- ✅ Upload clear, high-quality images
- ✅ Write clear titles and descriptions
- ✅ Set realistic prices
- ✅ Post during business hours

### To Avoid Issues:
- ❌ Don't post too many at once (start with 5-10)
- ❌ Don't close browser windows manually
- ❌ Don't restart backend while posting
- ❌ Don't select already-posted posts
- ❌ Don't use expired sessions

---

## ✅ Success Checklist

Before clicking "Start Posting":
- [ ] Posts are marked as "Pending" (orange badge)
- [ ] Accounts have "Active" session (green badge)
- [ ] Images are uploaded
- [ ] Titles and descriptions are filled
- [ ] Prices are valid numbers
- [ ] Backend server is running
- [ ] Terminal is visible (to see progress)

---

## 🎉 That's It!

You can now:
- ✅ Post multiple items with one click
- ✅ Continue working while posts are published
- ✅ Manage marketplace listings efficiently
- ✅ Scale your Facebook Marketplace presence

**Enjoy automated posting!** 🚀
