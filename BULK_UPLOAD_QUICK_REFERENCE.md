# 📦 Bulk Upload - Quick Reference Card

## Access
🌐 **URL:** `http://localhost:3000/dashboard/bulk-upload`
📍 **Navigation:** Dashboard → Bulk Upload

---

## CSV Format

### Headers (Required)
```csv
title,description,price,image_url
```

### Example Row
```csv
iPhone 13 Pro,Excellent condition with box,699.99,https://images.unsplash.com/photo-xxx?w=800
```

### Column Rules
| Column | Required | Format | Example |
|--------|----------|--------|---------|
| title | ✅ Yes | Text | "iPhone 13 Pro" |
| description | ✅ Yes | Text | "Excellent condition..." |
| price | ✅ Yes | Number | `699.99` (no $) |
| image_url | ❌ No | URL | `https://...` |

---

## Quick Steps

1. **Download Sample** → Click "Sample CSV" button
2. **Edit CSV** → Add your products
3. **Select Accounts** → Check 1 or more accounts
4. **Upload** → Choose your CSV file
5. **Create** → Click "Upload & Create Posts"

---

## Math

**Formula:** `CSV Rows × Selected Accounts = Total Posts`

**Examples:**
- 5 rows × 1 account = 5 posts
- 5 rows × 3 accounts = 15 posts
- 10 rows × 2 accounts = 20 posts

---

## Image URLs

### Free Sources
- Unsplash: https://unsplash.com
- Pexels: https://pexels.com
- Picsum: https://picsum.photos

### Get URL from Unsplash
1. Find image → Download
2. Right-click → Copy image address
3. Add `?w=800` to end

Example: `https://images.unsplash.com/photo-1234567890?w=800`

---

## Common Errors

| Error | Fix |
|-------|-----|
| "CSV file could not be parsed" | Save as CSV, not Excel |
| "Failed to download image" | Use public, accessible URLs |
| "Invalid price" | Remove $, use numbers only: `99.99` |
| "Missing required fields" | Fill in title, description, price |

---

## Do's & Don'ts

### ✅ DO
- Use sample CSV as template
- Test with 1-2 products first
- Use public image URLs
- Check account has "Active" status
- Price as numbers: `99.99`

### ❌ DON'T
- Add extra columns
- Use currency symbols: `$99.99`
- Use private/blocked URLs
- Upload 1000+ rows at once
- Change column headers

---

## Pro Tips

💡 **Batch Processing:** Split large files into 50-100 row chunks
💡 **Image Optimization:** Add `?w=800` to Unsplash URLs
💡 **Session Check:** Ensure accounts show "✓ Active" badge
💡 **Test First:** Upload 2-3 test products before full batch
💡 **Keep Backup:** Save original CSV before editing

---

## Status Meanings

| Badge | Meaning |
|-------|---------|
| ✓ Active (Green) | Ready to post |
| No Session (Red) | Needs login first |

---

## Results

### Success Message
```
✅ Successfully created 15 posts! (5 post(s) × 3 account(s))
```

### Error Message
```
Row 3: Invalid price '$99.99'
Row 5: Failed to download image (HTTP 404)
```

---

## Need Help?

📖 **Full Guide:** See `BULK_UPLOAD_USER_GUIDE.md`
📄 **Quick Start:** See `BULK_UPLOAD_QUICK_START.md`
📊 **Technical Details:** See `BULK_UPLOAD_IMPLEMENTATION_SUMMARY.md`

---

## Sample CSV Content

```csv
title,description,price,image_url
iPhone 13 Pro,Excellent condition iPhone 13 Pro with 256GB storage. Includes original box and accessories.,699.99,https://images.unsplash.com/photo-1632661674596-df8be070a5c5?w=800
Samsung 55 inch TV,Brand new 55 inch 4K Smart TV with HDR support. Never used.,450.00,https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=800
Gaming Laptop,High performance gaming laptop with RTX 3060 graphics card.,1200.00,https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=800
```

---

**🚀 Ready to upload? Get the sample CSV and start posting!**
