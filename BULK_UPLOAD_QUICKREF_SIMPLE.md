# 📋 Bulk Upload Quick Reference (SIMPLIFIED)

## Quick Start (3 Steps)

### 1️⃣ Upload Images
```bash
# Place your images in:
media/posts/iphone.jpg
media/posts/laptop.jpg
media/posts/tv.jpg
```

### 2️⃣ Create CSV File (SIMPLER FORMAT!)
```csv
account_email,title,description,price,image_filename
user@example.com,iPhone 13,Great condition,699.99,iphone.jpg
user@example.com,Laptop,Gaming laptop,1200.00,laptop.jpg
user@example.com,TV,55 inch Smart TV,450.00,tv.jpg
```

### 3️⃣ Upload
Go to: `http://localhost:8000/bulk-upload/`

---

## CSV Format (SIMPLIFIED!)

### Required Columns (5 only):
1. **account_email** - Must exist in database
2. **title** - Product title (max 255 chars)
3. **description** - Product description
4. **price** - Numeric (e.g., 99.99)
5. **image_filename** - File in media/posts/

**✅ NO SCHEDULING NEEDED!** All posts are scheduled for immediate posting.

---

## Example CSV

```csv
account_email,title,description,price,image_filename
user@example.com,iPhone 13 Pro,Excellent condition iPhone,699.99,iphone13.jpg
user@example.com,Samsung TV,55 inch 4K Smart TV,450.00,tv.jpg
user@example.com,Gaming Laptop,High performance laptop,1200.00,laptop.jpg
```

---

## Common Mistakes ❌

| Mistake | Correct |
|---------|---------|
| `image_filename: /media/posts/img.jpg` | `image_filename: img.jpg` |
| `price: $99.99` | `price: 99.99` |
| Missing header row | Always include header row |
| Wrong column order | Follow exact order above |
| **Adding scheduled_time column** | **NOT NEEDED - all posts auto-scheduled!** |

---

## Testing Checklist ✅

Before uploading your CSV:

- [ ] Images uploaded to `media/posts/` folder
- [ ] Account exists in database
- [ ] Account has saved session
- [ ] CSV has header row (5 columns only!)
- [ ] All required columns present
- [ ] Prices are numeric (no $ symbol)
- [ ] Image filenames match exactly
- [ ] Tested with 2-3 rows first

---

## Quick Access

- **Bulk Upload Page:** `http://localhost:8000/bulk-upload/`
- **Post List:** `http://localhost:8000/`
- **Create Single Post:** `http://localhost:8000/create/`
- **Django Admin:** `http://localhost:8000/admin/`

---

## Sample CSV Download

Use `sample_bulk_upload.csv` in the project root as a template!

---

## What Changed from Before?

### ❌ REMOVED:
- `scheduled_time` column - NOT NEEDED ANYMORE!
- DateTime parsing and validation
- Scheduling complexity

### ✅ SIMPLIFIED:
- Only 5 columns required (was 6)
- All posts auto-scheduled for immediate posting
- Simpler CSV format
- Less room for errors!

---

## Need Help?

📖 All posts will be scheduled for immediate posting when you run:
```bash
python manage.py post_to_marketplace
```

---

**Last Updated:** October 15, 2025  
**Version:** 2.0 (Simplified)  
**Format:** 5 columns only - NO scheduling column needed!
