# 📋 Bulk Upload Quick Reference

## Quick Start (3 Steps)

### 1️⃣ Upload Images
```bash
# Place your images in:
media/posts/iphone.jpg
media/posts/laptop.jpg
media/posts/tv.jpg
```

### 2️⃣ Create CSV File
```csv
account_email,title,description,price,image_filename,scheduled_time
user@example.com,iPhone 13,Great condition,699.99,iphone.jpg,2025-10-16 10:00:00
user@example.com,Laptop,Gaming laptop,1200.00,laptop.jpg,2025-10-16 11:00:00
user@example.com,TV,55 inch Smart TV,450.00,tv.jpg,2025-10-16 12:00:00
```

### 3️⃣ Upload
Go to: `http://localhost:8000/bulk-upload/`

---

## CSV Format

### Required Columns (in order):
1. **account_email** - Must exist in database
2. **title** - Product title (max 255 chars)
3. **description** - Product description
4. **price** - Numeric (e.g., 99.99)
5. **image_filename** - File in media/posts/
6. **scheduled_time** - YYYY-MM-DD HH:MM:SS (optional)

---

## Common Mistakes ❌

| Mistake | Correct |
|---------|---------|
| `image_filename: /media/posts/img.jpg` | `image_filename: img.jpg` |
| `price: $99.99` | `price: 99.99` |
| `scheduled_time: 10/16/2025` | `scheduled_time: 2025-10-16 10:00:00` |
| Missing header row | Always include header row |
| Wrong column order | Follow exact order above |

---

## Testing Checklist ✅

Before uploading your CSV:

- [ ] Images uploaded to `media/posts/` folder
- [ ] Account exists in database
- [ ] Account has saved session
- [ ] CSV has header row
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

## Need Help?

📖 Read full guide: `BULK_UPLOAD_GUIDE.md`
