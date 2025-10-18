# Bulk Upload Feature - Quick Start

## 🚀 How to Use in 5 Steps

### 1️⃣ Download Sample CSV
Click the **"Sample CSV"** button to get a template file.

### 2️⃣ Edit the CSV
Open the downloaded file and add your products:

```csv
title,description,price,image_url
iPhone 13 Pro,Excellent condition...,699.99,https://images.unsplash.com/photo-xxx
Samsung TV,Brand new 55 inch...,450.00,https://images.unsplash.com/photo-yyy
Gaming Laptop,High performance...,1200.00,https://images.unsplash.com/photo-zzz
```

**Required columns:**
- `title` - Product name
- `description` - Product details
- `price` - Price (numbers only, e.g., 99.99)

**Optional column:**
- `image_url` - Public URL of product image

### 3️⃣ Select Accounts
Check the boxes for which Facebook accounts to post to.
- Single account = Posts created for that account
- Multiple accounts = Posts duplicated for ALL selected accounts

### 4️⃣ Upload CSV
Click "Select CSV File" and choose your edited file.

### 5️⃣ Create Posts
Click "Upload & Create Posts" and wait for completion.

---

## 📊 Example Results

**Scenario:**
- CSV with 5 products
- Selected 3 Facebook accounts

**Result:**
- ✅ 15 posts created (5 × 3)

---

## 💡 Quick Tips

✅ **DO:**
- Use the sample CSV as a template
- Test with 1-2 products first
- Use image URLs from Unsplash, Pexels, or your website
- Verify accounts have "Active" sessions
- Keep prices as numbers only (99.99, not $99.99)

❌ **DON'T:**
- Don't add extra columns to CSV
- Don't include currency symbols in price
- Don't use private/blocked image URLs
- Don't upload hundreds of rows at once (split into batches)

---

## 🔗 Free Image Sources

- **Unsplash**: https://unsplash.com
- **Pexels**: https://pexels.com  
- **Picsum Photos**: https://picsum.photos

**How to get image URL from Unsplash:**
1. Find image → Click "Download"
2. Right-click → "Copy image address"
3. Add `?w=800` to end of URL for optimal size

Example: `https://images.unsplash.com/photo-1234567890?w=800`

---

## 🐛 Common Issues & Fixes

### "CSV file could not be parsed"
**Fix:** Save as CSV format, not Excel (.xlsx)

### "Failed to download image from URL"
**Fix:** Test URL in browser - must be publicly accessible

### "Invalid price"
**Fix:** Remove $, commas, or text from price column
- ✅ Correct: `99.99`
- ❌ Wrong: `$99.99`

### "Missing required fields"  
**Fix:** Ensure every row has title, description, and price

---

## 📱 Access Bulk Upload

Navigate to: **Dashboard** → **Bulk Upload**

Or direct URL: `http://localhost:3000/dashboard/bulk-upload`

---

## 📖 Need More Help?

See the complete guide: `BULK_UPLOAD_USER_GUIDE.md`

---

**Ready? Download the sample CSV and start bulk uploading!** 🎉
