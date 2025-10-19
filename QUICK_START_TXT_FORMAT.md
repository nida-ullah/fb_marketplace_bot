# 🚀 Quick Start Guide - New TXT Format

## ✅ What Changed?

1. **Single Post:** URL option removed - only file upload now
2. **Bulk Upload:** Changed from CSV to TXT format (simpler!)

---

## 📝 Creating TXT File for Bulk Upload

### Format:
Each product needs **3 lines** followed by a **blank line**:

```
Title
Description  
Price

Next Title
Next Description
Next Price
```

### Example:

```txt
iPhone 13 Pro
Excellent condition iPhone 13 Pro with 256GB storage. Includes original box and accessories.
699.99

Samsung 55 inch TV
Brand new 55 inch 4K Smart TV with HDR support. Never used.
450.00

Gaming Laptop
High performance gaming laptop with RTX 3060 graphics card. Perfect for gaming and content creation.
1200.00
```

---

## 🎯 How to Use

### Single Post:
1. Click "Create Post"
2. Fill in title, description, price
3. **Upload image file** (no URL option anymore)
4. Select account(s)
5. Click "Create Post"

### Bulk Upload:
1. Click "Create Multiple Posts"
2. **Download Sample TXT** (see the format)
3. Create your TXT file:
   - Line 1: Product title
   - Line 2: Product description  
   - Line 3: Price (just the number)
   - Line 4: Blank line
   - Repeat for each product
4. **Select images** in the SAME ORDER as products in TXT
5. Upload TXT file
6. Upload images
7. Select accounts
8. Click "Upload TXT"

**Done!** The app matches images automatically:
- 1st image → 1st product
- 2nd image → 2nd product
- etc.

---

## 💡 Tips

### TXT File:
- Use any text editor (Notepad, VS Code, etc.)
- **Must have blank line between products**
- Price should be just the number (e.g., `699.99`)
- Descriptions can be as long as you want
- Can include commas, quotes, anything!

### Images:
- Select in the SAME ORDER as your TXT file
- Use Ctrl+Click to select multiple
- File names don't matter
- Just make sure order matches!

---

## 📋 Complete Example

### 1. Create `products.txt`:
```
iPhone 13
Great condition, works perfectly
699

Samsung TV
55 inch 4K Smart TV
450

Laptop
Gaming laptop with RTX 3060
1200
```

### 2. Have 3 images ready:
- `photo1.jpg` (iPhone)
- `photo2.jpg` (TV)
- `photo3.jpg` (Laptop)

### 3. In the app:
- Upload `products.txt`
- Select images in order: photo1, photo2, photo3
- Select 2 accounts
- Click "Upload TXT"

### 4. Result:
**6 posts created!** (3 products × 2 accounts)

---

## ❓ FAQ

**Q: Why TXT instead of CSV?**
A: TXT is simpler! No column headers, no escaping commas, easier to read and write.

**Q: What if my description has multiple lines?**
A: Keep it on one line in the TXT file. Use spaces or periods instead of line breaks.

**Q: Do I need to name images specifically?**
A: No! Just select them in the same order as your products. The app matches by position.

**Q: Can I still use URL for single posts?**
A: No, URL option is removed. Upload images directly (safer and simpler).

**Q: What if I forget the blank line?**
A: The parser might get confused. Always put a blank line after each product's price!

**Q: Can prices have decimals?**
A: Yes! Use `699.99` or just `699` - both work.

---

## 🎉 Benefits

### Why this is better:
- ✅ **Simpler format** - No CSV headers, no columns
- ✅ **No escaping** - Commas in descriptions? No problem!
- ✅ **Easier to edit** - Just use Notepad
- ✅ **Cleaner structure** - Read top to bottom
- ✅ **Less errors** - Can't mess up column order

---

## 🚨 Common Mistakes

### ❌ Wrong:
```
iPhone 13, Great condition, 699
Samsung TV, 55 inch, 450
```
(This looks like CSV)

### ✅ Correct:
```
iPhone 13
Great condition
699

Samsung TV
55 inch
450
```
(Each product = 3 lines + blank)

---

## 🎊 Ready to Go!

1. Download sample TXT from the app
2. Edit it with your products
3. Upload with images
4. Done! 🚀

**It's that easy!**
