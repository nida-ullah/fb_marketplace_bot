# Bulk Upload Feature - Complete Guide

## 🎯 Overview

The Bulk Upload feature allows you to create multiple marketplace posts simultaneously for multiple Facebook accounts using a CSV file. This dramatically speeds up the process of listing products across your Facebook accounts.

## 🚀 Quick Start

### Access the Feature
1. Navigate to **Dashboard** → **Bulk Upload** 
2. Or visit: `http://localhost:3000/dashboard/bulk-upload`

### Basic Workflow
1. **Download Sample CSV** - Click the "Sample CSV" button
2. **Edit the CSV** - Fill in your product details
3. **Select Accounts** - Choose which Facebook accounts to post to
4. **Upload & Create** - Upload your CSV file

## 📋 CSV File Format

### Required Columns

| Column | Description | Example | Required |
|--------|-------------|---------|----------|
| `title` | Product name/title | "iPhone 13 Pro - 256GB" | ✅ Yes |
| `description` | Detailed product description | "Excellent condition..." | ✅ Yes |
| `price` | Price in dollars (numbers only) | "699.99" | ✅ Yes |
| `image_url` | Public URL of product image | "https://..." | ❌ Optional |

### Sample CSV Content

```csv
title,description,price,image_url
iPhone 13 Pro,Excellent condition iPhone 13 Pro with 256GB storage. Includes original box and accessories.,699.99,https://images.unsplash.com/photo-1632661674596-df8be070a5c5?w=800
Samsung 55 inch TV,Brand new 55 inch 4K Smart TV with HDR support. Never used.,450.00,https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?w=800
Gaming Laptop,High performance gaming laptop with RTX 3060 graphics card. Perfect for gaming and content creation.,1200.00,https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=800
Vintage Camera,Classic film camera in mint condition. Great for collectors.,150.00,
```

## 🔧 Detailed Instructions

### Step 1: Download Sample CSV

Click the **"Sample CSV"** button in the interface to download a pre-formatted template with example data.

**What you get:**
- Properly formatted CSV with correct column headers
- 3 sample products with real image URLs
- Ready to edit and customize

### Step 2: Prepare Your CSV File

#### Using Excel:
1. Open the downloaded sample CSV in Excel
2. Keep the first row (headers) unchanged
3. Replace sample data with your products
4. Save as **CSV (Comma delimited) (*.csv)**

#### Using Google Sheets:
1. Upload the sample CSV to Google Sheets
2. Edit your product data
3. Download as **CSV (.csv)**

#### Important CSV Rules:
- ✅ Keep column headers exactly as: `title,description,price,image_url`
- ✅ Use plain text (no special formatting)
- ✅ Enclose text with commas in quotes (e.g., "Camera, Lens, Bag")
- ✅ Price must be numbers only (e.g., 99.99, not $99.99)
- ❌ Don't use formulas
- ❌ Don't add extra columns

### Step 3: Add Product Images

You have **two options** for images:

#### Option A: Use Image URLs (Recommended for Bulk Upload)
```csv
title,description,price,image_url
Product Name,Description here,99.99,https://example.com/image.jpg
```

**Where to get image URLs:**
- **Unsplash**: https://unsplash.com (free high-quality images)
- **Pexels**: https://pexels.com (free stock photos)
- **Your website**: Upload to your server and use the URL
- **Image hosting**: Imgur, Cloudinary, etc.

**Getting URL from Unsplash:**
1. Find an image on unsplash.com
2. Click "Download" → Right-click → "Copy image address"
3. Add `?w=800` to the end for optimal size
4. Paste into your CSV

#### Option B: Leave Image URL Empty
```csv
title,description,price,image_url
Product Name,Description here,99.99,
```
Posts will be created without images (you can add them later).

### Step 4: Select Facebook Accounts

**Single Account:**
- Check one account checkbox
- All CSV posts will be created for this account

**Multiple Accounts:**
- Check multiple account checkboxes
- Each CSV post will be duplicated for ALL selected accounts
- Example: 5 CSV rows × 3 accounts = 15 total posts

**Select All:**
- Click "Select All" button
- All accounts will be checked at once

**Account Status:**
- ✅ **Active** (Green badge): Account has active session, ready to post
- ❌ **No Session** (Red badge): Account needs login (posts created but won't auto-post)

### Step 5: Upload and Create

1. Click **"Select CSV File"** button
2. Choose your prepared CSV file
3. File name and size will be displayed
4. Click **"Upload & Create Posts"** button
5. Wait for processing (may take a few seconds for large files)

## 📊 Results & Feedback

### Success Message
```
✅ Successfully created 15 posts! (5 post(s) × 3 account(s))
```

**Stats shown:**
- **Posts Created**: Total number of posts created
- **From CSV**: Number of CSV rows × Number of accounts

### Error Messages

#### CSV Format Errors
```
Row 2: Missing required fields (title, description, or price)
Row 3: Invalid price '99.99$' - could not convert string to float
Row 5: Failed to download image (HTTP 404)
```

**Common fixes:**
- Ensure all required columns have values
- Price must be numbers only (no $, commas, or text)
- Image URLs must be publicly accessible
- Check for typos in column headers

#### Upload Errors
```
❌ Please upload a CSV file
❌ Please select at least one account
❌ Error processing CSV file: ...
```

## 🎓 Examples & Use Cases

### Example 1: Single Account, Multiple Products

**Scenario:** You have one Facebook account and 10 products to list.

**CSV:** 10 rows (one per product)
**Accounts Selected:** 1 account
**Result:** 10 posts created

### Example 2: Multiple Accounts, Same Products

**Scenario:** You want to post the same 5 products to 4 different Facebook accounts.

**CSV:** 5 rows (one per product)
**Accounts Selected:** 4 accounts
**Result:** 20 posts created (5 × 4)

### Example 3: Bulk Product Launch

**Scenario:** New product line of 50 items, posting to 3 regional accounts.

**CSV:** 50 rows
**Accounts Selected:** 3 accounts
**Result:** 150 posts created (50 × 3)

## ✅ Best Practices

### CSV Preparation
1. **Test with small file first** - Upload 2-3 products before full batch
2. **Verify image URLs** - Open URLs in browser to ensure they work
3. **Use consistent pricing** - Same currency and decimal places
4. **Keep descriptions concise** - Facebook has character limits
5. **Proofread carefully** - Errors multiply across accounts

### Image URLs
1. **Use reliable sources** - Unsplash, Pexels, or your own server
2. **Optimize image size** - Add `?w=800` to Unsplash URLs
3. **Test accessibility** - Ensure URLs work in incognito/private mode
4. **Use HTTPS** - Secure URLs (https://) are preferred
5. **Avoid redirects** - Direct image URLs work best

### Account Management
1. **Check session status** - Ensure accounts have active sessions
2. **Don't overload** - Don't create hundreds of posts at once
3. **Stagger uploads** - Space out large batches to avoid flags
4. **Monitor results** - Check that posts are created correctly
5. **Update sessions** - Refresh sessions before large uploads

## 🐛 Troubleshooting

### "CSV file could not be parsed"
- **Cause:** Invalid CSV format
- **Fix:** Ensure file is saved as CSV, not Excel (.xlsx)
- **Check:** Open in text editor, should see comma-separated values

### "Failed to download image from URL"
- **Cause:** Image URL is inaccessible or incorrect
- **Fix:** 
  - Test URL in browser
  - Ensure URL is public (not behind login)
  - Use direct image URLs, not webpage URLs

### "Invalid price"
- **Cause:** Price contains non-numeric characters
- **Fix:** Remove $, commas, or text from price column
- **Correct:** `99.99`
- **Incorrect:** `$99.99`, `99.99 USD`, `Ninety-nine`

### "Missing required fields"
- **Cause:** Empty cells in required columns
- **Fix:** Ensure every row has title, description, and price
- **Note:** image_url can be empty

### Posts created but not posting
- **Cause:** Account has "No Session" status
- **Fix:** 
  1. Go to Accounts page
  2. Click "Update Session" for the account
  3. Complete Facebook login
  4. Posts will auto-post after session is active

## 📈 Performance Tips

### For Large Uploads (100+ rows)

1. **Split into batches**
   - Upload 50-100 rows at a time
   - Wait for completion before next batch

2. **Use image URLs**
   - Faster than uploading files
   - Less bandwidth usage

3. **Pre-verify data**
   - Check all URLs work before upload
   - Validate prices and formatting
   - Remove duplicate rows

4. **Monitor server load**
   - Don't upload during peak hours
   - Allow time between large batches

## 🔒 Security & Privacy

- All CSV files are processed server-side
- Image URLs are downloaded and stored on your server
- Original URLs are not stored
- Files are not cached or logged
- HTTPS recommended for all image URLs

## 📱 Mobile Support

The bulk upload page is **not optimized** for mobile devices. For best experience:
- Use desktop/laptop computer
- Use tablet in landscape mode
- Prepare CSV on computer before accessing page

## 🆘 Support & Help

### Need Help?
1. Download sample CSV to see correct format
2. Test with 1-2 products first
3. Check error messages carefully
4. Verify account sessions are active

### Common Questions

**Q: Can I upload images from my computer?**
A: Not in bulk upload. Use image URLs or upload individual posts with local images.

**Q: What's the maximum file size?**
A: No hard limit, but recommend under 100 rows for performance.

**Q: Can I schedule posts for later?**
A: Currently, all bulk uploaded posts are scheduled for immediate posting.

**Q: Can I edit posts after bulk upload?**
A: Yes, go to Posts page and edit individual posts.

**Q: What happens if some rows have errors?**
A: Valid rows are created, error rows are skipped with detailed error messages.

## 📝 Summary

**Bulk Upload allows you to:**
- ✅ Upload multiple products at once via CSV
- ✅ Create posts for multiple accounts simultaneously
- ✅ Use image URLs from the web
- ✅ Save time on repetitive posting
- ✅ Scale your marketplace presence

**Remember:**
- Download sample CSV first
- Test with small batch
- Verify image URLs work
- Check account sessions active
- Review results after upload

---

**Ready to start? Download the sample CSV and give it a try!** 🚀
