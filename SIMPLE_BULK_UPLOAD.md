# 🚀 SIMPLE Bulk Upload Guide

## The EASIEST Way to Upload Multiple Posts with Images

No need for Imgur or URL conversions! Just follow these 3 simple steps:

---

## 📋 Step 1: Prepare Your CSV File

Create a CSV with these columns:

```csv
title,description,price,image_filename
iPhone 13 Pro,Excellent condition 256GB,699.99,iphone.jpg
Samsung TV 55",4K Smart TV like new,450.00,tv.jpg
Gaming Laptop,RTX 3060 16GB RAM,1200.00,laptop.jpg
```

**Columns:**
- `title` - Product name
- `description` - Product details
- `price` - Price (numbers only)
- `image_filename` - Name of the image file (just the filename, not full path)

---

## 📸 Step 2: Prepare Your Images

1. Rename your images with simple names:
   - `iphone.jpg`
   - `tv.jpg`
   - `laptop.jpg`

2. Put ALL images in ONE folder

3. Select all images → Right-click → "Send to" → "Compressed (zipped) folder"

**You now have:**
- ✅ `products.csv` - Your product list
- ✅ `images.zip` - All your product images

---

## ⬆️ Step 3: Upload in the App

1. Click "Create Multiple Posts"
2. Select accounts
3. Upload your CSV file
4. Upload your ZIP file (optional)
5. Click "Upload CSV"

**Done!** ✅

---

## 💡 How It Works

The app automatically:
1. Reads your CSV file
2. Extracts images from the ZIP
3. Matches images by filename
4. Creates posts for each selected account
5. Attaches the correct image to each post

**Example:**
- CSV row says `image_filename: iphone.jpg`
- App finds `iphone.jpg` in the ZIP
- Attaches it to the iPhone post
- Repeats for each account you selected

---

## 🎯 Full Example

### Your Files:

**products.csv:**
```csv
title,description,price,image_filename
iPhone 13 Pro,Like new 256GB,699.99,iphone13.jpg
Samsung Galaxy S22,Mint condition,549.99,samsung.jpg
MacBook Pro,M1 chip 16GB,1299.99,macbook.jpg
```

**images.zip contains:**
```
iphone13.jpg
samsung.jpg
macbook.jpg
```

### Result:

If you select **3 accounts**, the app creates:
- 3 iPhone posts (one per account) with iphone13.jpg
- 3 Samsung posts (one per account) with samsung.jpg  
- 3 MacBook posts (one per account) with macbook.jpg

**Total: 9 posts created!** (3 products × 3 accounts)

---

## ⚠️ Important Notes

1. **Image filenames must match exactly**
   - CSV says `iphone.jpg` → ZIP must contain `iphone.jpg`
   - Case doesn't matter: `iPhone.jpg` = `iphone.jpg`

2. **Supported image formats:**
   - `.jpg` or `.jpeg`
   - `.png`
   - `.gif`
   - `.webp`

3. **ZIP file is optional:**
   - You can upload CSV without images
   - Posts will be created without images
   - You can add images later by editing individual posts

4. **Image not found?**
   - If CSV references an image that's not in the ZIP
   - The app will create the post WITHOUT that image
   - You'll see a warning in the results

---

## 🚫 What You DON'T Need

❌ No Imgur account needed
❌ No URL conversions needed
❌ No Google Drive/OneDrive setup needed
❌ No internet connection needed for images
❌ No complicated steps!

---

## ✅ Benefits

- ⚡ **Fast:** Upload 20 products in 2 minutes
- 🎯 **Simple:** Just CSV + ZIP file
- 🔒 **Private:** Images stay on your server
- 📦 **Organized:** All images in one ZIP
- 🔄 **Flexible:** Images are optional

---

## 📝 Quick Checklist

Before uploading:
- [ ] CSV has required columns: title, description, price
- [ ] Image filenames in CSV match actual filenames
- [ ] All images are in one ZIP file
- [ ] Image names don't have spaces (use underscores: `gaming_laptop.jpg`)
- [ ] At least one account is selected

---

## 🎉 That's It!

The **simplest bulk upload ever:**
1. CSV file with product info
2. ZIP file with images
3. Upload both
4. Done!

No more wrestling with image URLs! 🎊
