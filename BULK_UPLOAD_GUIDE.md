# 📦 Bulk Post Upload Feature

## Overview
The Bulk Post Upload feature allows you to import multiple marketplace posts at once using a CSV file. This is perfect for dropshippers, inventory managers, or anyone who needs to post many products quickly.

## Features
✅ Upload multiple posts via CSV file  
✅ Automatic validation of data  
✅ Detailed error reporting  
✅ Image validation  
✅ Account verification  
✅ Flexible scheduling  
✅ Import summary  

## How to Use

### Step 1: Prepare Your Images
1. Navigate to the `media/posts/` folder in your project
2. Upload all product images you want to use
3. Note down the exact filenames (e.g., `product1.jpg`, `iphone.png`)

### Step 2: Create Your CSV File
Create a CSV file with the following columns:

| Column Name | Required | Description | Example |
|-------------|----------|-------------|---------|
| account_email | ✅ Yes | Facebook account email (must exist in database) | `user@example.com` |
| title | ✅ Yes | Post title (max 255 characters) | `iPhone 13 Pro` |
| description | ✅ Yes | Product description | `Excellent condition...` |
| price | ✅ Yes | Product price (numeric) | `699.99` |
| image_filename | ✅ Yes | Image filename from media/posts/ | `iphone13.jpg` |
| scheduled_time | ❌ No | When to post (YYYY-MM-DD HH:MM:SS) | `2025-10-16 10:00:00` |

### Step 3: Format Your CSV

**Example CSV Content:**
```csv
account_email,title,description,price,image_filename,scheduled_time
user@example.com,iPhone 13 Pro,Excellent condition iPhone,699.99,iphone13.jpg,2025-10-16 10:00:00
user@example.com,Samsung TV,55 inch 4K Smart TV,450.00,tv.jpg,2025-10-16 11:00:00
user@example.com,Gaming Laptop,High performance laptop,1200.00,laptop.jpg,2025-10-16 12:00:00
```

**Important Notes:**
- First row MUST be the header with column names
- Don't add extra columns
- Keep column names exactly as shown
- Use commas (`,`) as separators
- Enclose text with commas in quotes (e.g., `"Laptop, like new"`)

### Step 4: Upload via Web Interface

1. **Access the Bulk Upload Page:**
   - Visit: `http://localhost:8000/bulk-upload/`
   - Or click "📦 Bulk Upload" button on the posts list page
   - Or access from Django Admin

2. **Upload Your CSV:**
   - Click "Choose File" and select your CSV
   - Click "📤 Upload CSV"
   - Wait for processing

3. **Review Results:**
   - ✅ Success count will be shown
   - ❌ Errors will be listed with row numbers
   - Successfully imported posts appear in the post list

## Validation Rules

### Account Validation
- ✅ Account email must exist in the database
- ✅ Account must have a valid session saved
- ❌ Posts will fail if account doesn't exist

### Title Validation
- ✅ Cannot be empty
- ✅ Maximum 255 characters
- ❌ Will fail if missing

### Description Validation
- ✅ Cannot be empty
- ✅ No length limit
- ❌ Will fail if missing

### Price Validation
- ✅ Must be a valid number
- ✅ Can have decimals (e.g., 99.99)
- ✅ Must be positive or zero
- ❌ Will fail if negative or non-numeric

### Image Validation
- ✅ File must exist in `media/posts/` folder
- ✅ Supports: JPG, JPEG, PNG, GIF
- ❌ Will fail if file not found

### Scheduled Time (Optional)
- ✅ If empty, post is scheduled for immediate posting
- ✅ Accepted formats:
  - `YYYY-MM-DD HH:MM:SS` (e.g., `2025-10-16 14:30:00`)
  - `YYYY-MM-DD HH:MM` (e.g., `2025-10-16 14:30`)
  - `YYYY-MM-DD` (e.g., `2025-10-16`)
- ✅ Times in the past will post immediately
- ❌ Will fail if format is incorrect

## Error Handling

### Common Errors and Solutions

| Error Message | Cause | Solution |
|---------------|-------|----------|
| `Account 'email@example.com' not found` | Email doesn't exist in database | Add account via admin first |
| `Image file 'image.jpg' not found` | Image not in media/posts/ | Upload image to correct folder |
| `Invalid price '99.99x'` | Price contains non-numeric characters | Use only numbers and decimal point |
| `Missing required fields` | One or more columns are empty | Fill all required fields |
| `Invalid datetime format` | Scheduled time in wrong format | Use: YYYY-MM-DD HH:MM:SS |

### Error Report Format
When errors occur, you'll see:
```
❌ 2 error(s) occurred:
Row 3: Account 'test@example.com' not found
Row 5: Image file 'missing.jpg' not found in media/posts/
```

## Advanced Usage

### Bulk Import from Inventory System
If you have an inventory management system, export data in the required CSV format:

```python
# Python script example
import csv
from datetime import datetime, timedelta

products = [
    {"title": "Product 1", "description": "...", "price": 99.99, "image": "p1.jpg"},
    {"title": "Product 2", "description": "...", "price": 149.99, "image": "p2.jpg"},
]

with open('bulk_import.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['account_email', 'title', 'description', 'price', 'image_filename', 'scheduled_time'])
    
    for i, product in enumerate(products):
        scheduled = (datetime.now() + timedelta(hours=i)).strftime('%Y-%m-%d %H:%M:%S')
        writer.writerow([
            'user@example.com',
            product['title'],
            product['description'],
            product['price'],
            product['image'],
            scheduled
        ])
```

### Stagger Posts Over Time
To avoid posting all items at once, set different scheduled_time values:
```csv
account_email,title,description,price,image_filename,scheduled_time
user@example.com,Item 1,Description,99.99,item1.jpg,2025-10-16 10:00:00
user@example.com,Item 2,Description,99.99,item2.jpg,2025-10-16 11:00:00
user@example.com,Item 3,Description,99.99,item3.jpg,2025-10-16 12:00:00
```

### Multiple Accounts
You can mix posts for different accounts in one CSV:
```csv
account_email,title,description,price,image_filename,scheduled_time
account1@example.com,Item A,Description,99.99,itemA.jpg,2025-10-16 10:00:00
account2@example.com,Item B,Description,149.99,itemB.jpg,2025-10-16 10:00:00
account1@example.com,Item C,Description,199.99,itemC.jpg,2025-10-16 11:00:00
```

## Limitations

1. **Category & Condition:**
   - Category defaults to "Furniture"
   - Condition defaults to "New"
   - These are hardcoded in the automation (not changed by this feature)

2. **Image Upload:**
   - Images must be uploaded to `media/posts/` folder manually BEFORE CSV import
   - CSV only references the filename, doesn't upload images

3. **File Size:**
   - Large CSV files (1000+ rows) may take time to process
   - Consider breaking into smaller batches

4. **Validation:**
   - All validation happens during upload
   - Invalid rows are skipped, valid rows are imported

## Best Practices

### ✅ DO:
- Test with a small CSV file first (2-3 rows)
- Use the provided `sample_bulk_upload.csv` as a template
- Upload images before creating CSV
- Double-check account emails exist in database
- Use consistent filename conventions
- Back up your CSV file before uploading

### ❌ DON'T:
- Don't use special characters in filenames
- Don't leave required fields empty
- Don't use relative paths for images
- Don't upload CSV files with thousands of rows at once
- Don't reuse the same CSV without checking results

## Troubleshooting

### Problem: "Account not found" error
**Solution:** Go to Django admin → Accounts → Add the Facebook account first

### Problem: "Image file not found" error
**Solution:** 
1. Check the filename spelling exactly matches
2. Ensure image is in `media/posts/` folder
3. Check file extension (jpg vs jpeg)

### Problem: "Invalid datetime format" error
**Solution:** Use format `2025-10-16 14:30:00` (YYYY-MM-DD HH:MM:SS)

### Problem: CSV won't upload
**Solution:**
1. Ensure file extension is `.csv`
2. Check file isn't corrupted
3. Try opening in text editor to verify format
4. Save as UTF-8 encoding

### Problem: Posts created but not posting
**Solution:** 
1. Run `python manage.py post_to_marketplace`
2. Check scheduled_time is in the past
3. Verify account has valid session

## Access Points

### Web Interface:
- Direct URL: `http://localhost:8000/bulk-upload/`
- From Posts List: Click "📦 Bulk Upload" button
- From Create Post: Link at bottom

### Django Admin:
- Go to Postings → Marketplace posts
- Access custom link (if implemented)

## Files Modified

This feature adds/modifies:
- ✅ `postings/forms.py` - Added `BulkPostUploadForm`
- ✅ `postings/views.py` - Added `bulk_upload_posts` view
- ✅ `postings/urls.py` - Added `/bulk-upload/` route
- ✅ `postings/admin.py` - Enhanced with search/filters
- ✅ `postings/templates/postings/bulk_upload_posts.html` - New template
- ✅ `postings/templates/postings/post_list.html` - Added bulk upload button
- ✅ `sample_bulk_upload.csv` - Sample template file

## No Changes to Automation

**Important:** This feature does NOT modify the posting automation:
- ✅ Category still defaults to "Furniture"
- ✅ Condition still defaults to "New"
- ✅ All automation logic remains unchanged
- ✅ Only adds a way to create multiple posts at once

## Support

If you encounter issues:
1. Check this documentation
2. Verify your CSV format matches examples
3. Test with the provided sample CSV
4. Check Django logs for detailed errors

---

**Last Updated:** October 15, 2025  
**Version:** 1.0  
**Compatible with:** FB Marketplace Bot v1.0+
