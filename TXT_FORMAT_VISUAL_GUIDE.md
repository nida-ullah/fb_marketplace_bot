# 📝 TXT File Format - Visual Guide

## ✅ Correct Format

```
┌─────────────────────────────────────────┐
│ iPhone 13 Pro                           │ ← Line 1: Title
│ Great condition, 256GB storage          │ ← Line 2: Description
│ 699.99                                  │ ← Line 3: Price
│                                         │ ← Line 4: BLANK LINE
│ Samsung TV                              │ ← Line 1: Title
│ 55 inch 4K Smart TV                     │ ← Line 2: Description
│ 450.00                                  │ ← Line 3: Price
│                                         │ ← Line 4: BLANK LINE
│ Gaming Laptop                           │ ← Line 1: Title
│ RTX 3060 16GB RAM                       │ ← Line 2: Description
│ 1200.00                                 │ ← Line 3: Price
└─────────────────────────────────────────┘
```

---

## 🎯 Pattern

Each product follows this exact pattern:

```
[TITLE]           ← Line 1
[DESCRIPTION]     ← Line 2
[PRICE]           ← Line 3
                  ← Line 4 (empty/blank)
```

**Repeat for each product!**

---

## ✅ Real Example

Save this as `products.txt`:

```
iPhone 13
Great condition
699

Samsung TV
55 inch 4K
450

Laptop
Gaming laptop
1200
```

---

## ❌ Common Mistakes

### Mistake 1: No Blank Line
```
iPhone 13
Great condition
699
Samsung TV        ← ❌ Wrong! Need blank line above
55 inch 4K
450
```

### Mistake 2: CSV Format
```
iPhone 13,Great condition,699  ← ❌ Wrong! Not CSV anymore
Samsung TV,55 inch 4K,450      ← ❌ This is the old format
```

### Mistake 3: Extra Blank Lines
```
iPhone 13
Great condition
699

                  ← ❌ Only ONE blank line needed
Samsung TV
```

### Mistake 4: Missing Lines
```
iPhone 13
699               ← ❌ Missing description line!

Samsung TV
```

---

## 📊 Visual Comparison

### ❌ OLD (CSV Format):
```
title,description,price
iPhone 13,Great condition,699
Samsung TV,55 inch 4K,450
```

### ✅ NEW (TXT Format):
```
iPhone 13
Great condition
699

Samsung TV
55 inch 4K
450
```

**Much cleaner!** 🎉

---

## 💡 Pro Tips

### Tip 1: Use Notepad
Just open Notepad and type:
- Product name (Enter)
- Description (Enter)
- Price (Enter)
- Press Enter again for blank line
- Next product...

### Tip 2: Count Lines
Each product = **4 lines** total (including blank)
- 3 lines of data
- 1 blank line

### Tip 3: Price Format
Both work:
- `699` ✅
- `699.99` ✅
- `699.9` ✅

Just numbers, no currency symbol!

### Tip 4: Descriptions
Can include:
- Commas: "Great condition, works perfectly" ✅
- Quotes: 'Like "new" condition' ✅
- Numbers: "256GB, 2 years old" ✅

Everything works!

---

## 📱 Step by Step

### Step 1: Open Notepad
Windows: Press `Windows + R`, type `notepad`, press Enter

### Step 2: Type First Product
```
iPhone 13
```
Press Enter

```
Great condition, 256GB
```
Press Enter

```
699
```
Press Enter TWICE (for blank line)

### Step 3: Type Second Product
```
Samsung TV
```
Press Enter

```
55 inch 4K Smart TV
```
Press Enter

```
450
```
Press Enter TWICE (for blank line)

### Step 4: Continue Pattern
Repeat for all products!

### Step 5: Save
- File → Save As
- Name: `products.txt`
- Save type: Text Documents (*.txt)
- Click Save

### Step 6: Upload in App
Done! 🎉

---

## 🔍 Validation Checklist

Before uploading, check:
- [ ] Each product has EXACTLY 3 lines
- [ ] Blank line after each product's price
- [ ] Prices are just numbers (no $ or currency)
- [ ] No extra blank lines at start/end
- [ ] File saved as `.txt`

---

## 🎯 Quick Reference

**Structure:**
```
Title           (Line 1)
Description     (Line 2)  
Price          (Line 3)
               (Line 4 - blank)
[Repeat]
```

**Example:**
```
Product 1 Name
Product 1 Description
100

Product 2 Name
Product 2 Description
200

Product 3 Name
Product 3 Description
300
```

That's it! 🚀

---

## 📝 Template

Copy and paste this template:

```
Replace with product 1 title
Replace with product 1 description
Replace with product 1 price

Replace with product 2 title
Replace with product 2 description
Replace with product 2 price

Replace with product 3 title
Replace with product 3 description
Replace with product 3 price
```

Just replace the text and you're done!

---

## 🎉 You're Ready!

The TXT format is:
- ✅ Simple
- ✅ Clean
- ✅ Easy to create
- ✅ Hard to mess up

Just remember: **3 lines + blank line** for each product!

Happy posting! 🚀
