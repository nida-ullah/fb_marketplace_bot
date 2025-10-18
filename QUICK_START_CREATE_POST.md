# 🚀 Quick Start - Create Post Feature

## How to Test Right Now

### 1️⃣ Make sure both servers are running:

**Terminal 1 (Backend):**
```bash
cd fb_marketplace_bot
python manage.py runserver
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

### 2️⃣ Navigate to the create post page:

Open browser: **http://localhost:3000/dashboard/create-post**

Or:
- Click "Create Post" in the sidebar
- Or go to Posts page and click "Create Post" button

### 3️⃣ Fill out the form:

1. **Select Accounts**: Check one or more Facebook accounts
   - You can click "Select All Accounts" to select all at once

2. **Enter Post Details**:
   - Title: "iPhone 13 Pro Max"
   - Description: "Brand new iPhone in excellent condition..."
   - Price: "899.99"

3. **Add Image** (Optional - you can skip this):
   - Upload a file, OR
   - Paste an image URL like: `https://example.com/phone.jpg`

4. **Click "Create Post(s)"**

### 4️⃣ What happens:

- You'll see "Creating Posts..." message
- After a few seconds, you'll get a success message
- You'll be redirected to the Posts page
- You'll see multiple posts created (one for each selected account)

---

## Example Test Data

```
Title: Gaming Laptop - High Performance
Description: Dell Gaming Laptop with RTX 3060, 16GB RAM, 512GB SSD. Excellent condition, barely used.
Price: 1299.99
Image: (optional)
```

```
Title: Office Chair - Ergonomic Design
Description: Herman Miller Aeron office chair, adjustable, great for long work hours. Like new condition.
Price: 450.00
Image: (optional)
```

```
Title: PlayStation 5 Console
Description: PS5 Digital Edition with 2 controllers and 5 games. Perfect working condition.
Price: 549.99
Image: (optional)
```

---

## Quick API Test (Optional)

If you want to test the API directly:

```bash
curl -X POST http://localhost:8000/api/posts/create-for-accounts/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "account_ids=[1,2,3]" \
  -F "title=Test Product" \
  -F "description=Test Description" \
  -F "price=99.99"
```

---

## Troubleshooting

### "No accounts found"
- Make sure you have added Facebook accounts first
- Go to /dashboard/accounts and add at least one account

### "Please select at least one account"
- You need to check at least one checkbox under Facebook Accounts

### "Failed to create posts"
- Check backend console for errors
- Make sure both servers are running
- Check that you're logged in

### Form validation errors
- Fill all required fields (marked with *)
- Price must be a number greater than 0
- At least one account must be selected

---

## Where to Find Your Posts

After creating posts:
1. Go to **Dashboard > Posts** (http://localhost:3000/dashboard/posts)
2. You'll see your posts in a grid layout
3. Each post shows:
   - Title and description
   - Price
   - Account email it belongs to
   - Status (Posted/Pending)
   - Created time

---

## What's Created in the Database

When you create posts for 3 accounts:
```
MarketplacePost #1
  - account_id: 1 (account1@gmail.com)
  - title: "Your Title"
  - description: "Your Description"
  - price: 99.99
  - scheduled_time: NOW
  - posted: False

MarketplacePost #2
  - account_id: 2 (account2@gmail.com)
  - title: "Your Title" (same)
  - description: "Your Description" (same)
  - price: 99.99 (same)
  - scheduled_time: NOW
  - posted: False

MarketplacePost #3
  - account_id: 3 (account3@gmail.com)
  - title: "Your Title" (same)
  - description: "Your Description" (same)
  - price: 99.99 (same)
  - scheduled_time: NOW
  - posted: False
```

All posts are identical except for the account they belong to.

---

## Next: Auto-Posting (Future)

Currently, posts are created with `posted: False`. To actually post them to Facebook Marketplace, you'll need to:

1. Run the automation script:
```bash
python manage.py post_to_marketplace
```

2. Or set up a cron job to auto-post pending posts

This will use the Playwright automation to actually post to Facebook.

---

**Ready to go! 🎉**

Navigate to: **http://localhost:3000/dashboard/create-post**
