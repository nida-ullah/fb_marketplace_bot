# Accounts Checkbox & Bulk Delete Feature

## Overview
Added checkbox selection and bulk delete functionality to the Facebook Accounts page, matching the posts page UI improvements.

---

## ✅ Implemented Features

### 1. **Checkbox Selection**
- ✅ Checkbox in table header to select/deselect all accounts
- ✅ Individual checkbox for each account row
- ✅ Visual feedback: selected rows highlighted with blue background
- ✅ Accessible with `aria-label` attributes

### 2. **Bulk Delete**
- ✅ Delete multiple selected accounts at once
- ✅ Bulk actions bar appears when accounts are selected
- ✅ Shows count: "N account(s) selected"
- ✅ "Clear Selection" button to deselect all
- ✅ "Delete N Account(s)" button with confirmation
- ✅ Parallel deletion using `Promise.all()`
- ✅ Success/error alerts with counts
- ✅ Loading state with spinner during deletion

### 3. **Select All/Deselect All**
- ✅ Button in card header to toggle all selections
- ✅ Checkbox in table header for quick access
- ✅ Both methods synchronized

---

## 🎨 UI Components

### Bulk Actions Bar (appears when accounts selected)
```
┌─────────────────────────────────────────────────────────────┐
│ ✓ N account(s) selected                                     │
│ [Clear Selection] [Delete N Account(s)]                     │
└─────────────────────────────────────────────────────────────┘
```
- Blue background (`bg-blue-50`)
- Appears between error messages and stats cards
- Sticky context for user awareness

### Table with Checkboxes
```
┌──────────────────────────────────────────────────────────────┐
│ [✓] | EMAIL | SESSION STATUS | CREATED AT | ACTIONS         │
├──────────────────────────────────────────────────────────────┤
│ [ ] | user@example.com | Active | 10/18/2025 | [Delete]     │
│ [✓] | user2@example.com | No Session | 10/17/2025 | [...]   │
└──────────────────────────────────────────────────────────────┘
```
- Checkbox column (first column, 48px width)
- Header checkbox for "Select All"
- Selected rows have blue background
- Individual checkboxes for each account

---

## 🔧 Technical Implementation

### New State Variables
```typescript
const [selectedAccounts, setSelectedAccounts] = useState<number[]>([]);
const [isDeleting, setIsDeleting] = useState(false);
```

### Handler Functions

#### Bulk Delete with Confirmation
```typescript
const handleBulkDelete = async () => {
  if (selectedAccounts.length === 0) return;
  
  if (!confirm(`Are you sure you want to delete ${selectedAccounts.length} account(s)?`)) {
    return;
  }

  setIsDeleting(true);
  const deletePromises = selectedAccounts.map(id => accountsAPI.delete(id));
  const results = await Promise.allSettled(deletePromises);
  
  const successCount = results.filter(r => r.status === 'fulfilled').length;
  const failCount = results.filter(r => r.status === 'rejected').length;
  
  // Show feedback and refresh
  if (successCount > 0) {
    alert(`Successfully deleted ${successCount} account(s)`);
    setSelectedAccounts([]);
    fetchAccounts();
  }
  
  if (failCount > 0) {
    alert(`Failed to delete ${failCount} account(s)`);
  }
  
  setIsDeleting(false);
};
```

#### Select All Toggle
```typescript
const handleSelectAll = () => {
  if (selectedAccounts.length === accounts.length) {
    setSelectedAccounts([]); // Deselect all
  } else {
    setSelectedAccounts(accounts.map(acc => acc.id)); // Select all
  }
};
```

#### Individual Selection
```typescript
const handleSelectAccount = (id: number) => {
  setSelectedAccounts(prev =>
    prev.includes(id)
      ? prev.filter(accId => accId !== id) // Remove
      : [...prev, id] // Add
  );
};
```

---

## 📋 UI Updates

### 1. Card Header with Select All Button
```tsx
<CardHeader>
  <div className="flex items-center justify-between">
    <CardTitle>All Accounts</CardTitle>
    {accounts.length > 0 && (
      <Button
        variant="outline"
        size="sm"
        onClick={handleSelectAll}
      >
        {selectedAccounts.length === accounts.length
          ? "Deselect All"
          : "Select All"}
      </Button>
    )}
  </div>
</CardHeader>
```

### 2. Bulk Actions Bar
```tsx
{selectedAccounts.length > 0 && (
  <Card className="bg-blue-50 border-blue-200">
    <CardContent className="py-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <CheckCircle className="h-5 w-5 text-blue-600" />
          <span className="font-medium text-blue-900">
            {selectedAccounts.length} account(s) selected
          </span>
        </div>
        <div className="flex gap-2">
          <Button onClick={() => setSelectedAccounts([])}>
            Clear Selection
          </Button>
          <Button onClick={handleBulkDelete} disabled={isDeleting}>
            Delete {selectedAccounts.length} Account(s)
          </Button>
        </div>
      </div>
    </CardContent>
  </Card>
)}
```

### 3. Table Header Checkbox
```tsx
<th className="px-6 py-3 text-left w-12">
  <input
    type="checkbox"
    checked={selectedAccounts.length === accounts.length && accounts.length > 0}
    onChange={handleSelectAll}
    className="h-4 w-4 text-blue-600 rounded border-gray-300 focus:ring-2 focus:ring-blue-500 cursor-pointer"
    aria-label="Select all accounts"
  />
</th>
```

### 4. Row Checkbox & Highlighting
```tsx
<tr 
  className={`hover:bg-gray-50 ${
    selectedAccounts.includes(account.id) ? "bg-blue-50" : ""
  }`}
>
  <td className="px-6 py-4 whitespace-nowrap">
    <input
      type="checkbox"
      checked={selectedAccounts.includes(account.id)}
      onChange={() => handleSelectAccount(account.id)}
      className="h-4 w-4 text-blue-600 rounded border-gray-300 focus:ring-2 focus:ring-blue-500 cursor-pointer"
      aria-label={`Select account ${account.email}`}
    />
  </td>
  {/* Rest of row... */}
</tr>
```

---

## 🎯 User Benefits

### Before
- ❌ Could only delete accounts one by one
- ❌ No way to select multiple accounts
- ❌ Tedious for managing many accounts
- ❌ Confirmation for each individual delete

### After
- ✅ Select multiple accounts with checkboxes
- ✅ "Select All" for mass operations
- ✅ Bulk delete with single confirmation
- ✅ Visual feedback for selections
- ✅ Efficient account management

---

## 🚀 Usage Guide

### Selecting Accounts
1. **Individual**: Click checkbox next to any account
2. **Multiple**: Click checkboxes for desired accounts
3. **All**: 
   - Click "Select All" button in header, OR
   - Click checkbox in table header
4. **Visual Feedback**: Selected rows turn blue

### Bulk Delete
1. Select one or more accounts using checkboxes
2. Bulk actions bar appears at top showing count
3. Click "Delete N Account(s)" button
4. Confirm deletion in popup dialog
5. All selected accounts deleted in parallel
6. Success/error alerts show results
7. Table refreshes automatically

### Clearing Selection
- Click "Clear Selection" in bulk actions bar, OR
- Click "Deselect All" button in header, OR
- Click table header checkbox to toggle off

---

## ✨ Features Comparison

| Feature | Posts Page | Accounts Page |
|---------|-----------|---------------|
| Checkboxes | ✅ | ✅ |
| Select All | ✅ | ✅ |
| Bulk Delete | ✅ | ✅ |
| Bulk Actions Bar | ✅ | ✅ |
| Visual Feedback | ✅ | ✅ |
| Loading States | ✅ | ✅ |
| Success/Error Alerts | ✅ Toast | ✅ Alert |
| Parallel Deletion | ✅ | ✅ |

---

## 🔄 Code Changes

### Files Modified
- `frontend/app/dashboard/accounts/page.tsx` (200+ lines updated)

### New State
```typescript
selectedAccounts: number[]  // IDs of selected accounts
isDeleting: boolean          // Loading state for bulk delete
```

### New Functions
```typescript
handleBulkDelete()      // Delete multiple accounts
handleSelectAll()       // Toggle all selections
handleSelectAccount()   // Toggle individual selection
```

### New UI Elements
1. Checkbox column in table (first column)
2. "Select All" button in card header
3. Checkbox in table header
4. Bulk actions bar (conditional)
5. Selected row highlighting

---

## 🧪 Testing Checklist

- [ ] Select individual accounts using checkboxes
- [ ] Click "Select All" button
- [ ] Click header checkbox to select all
- [ ] Click "Deselect All" button
- [ ] Click header checkbox to deselect all
- [ ] Delete single account via bulk delete
- [ ] Delete multiple accounts (3+) via bulk delete
- [ ] Verify bulk actions bar appears when accounts selected
- [ ] Check blue highlighting on selected rows
- [ ] Test "Clear Selection" button
- [ ] Verify confirmation dialog on bulk delete
- [ ] Check success alert shows correct count
- [ ] Verify table refreshes after deletion
- [ ] Test with no accounts (empty state)
- [ ] Test accessibility (keyboard navigation)

---

## 📝 Notes

- Checkboxes use same styling as posts page for consistency
- Bulk delete uses `Promise.allSettled()` for parallel operations
- Success/error counts shown separately
- Selection state cleared after successful deletion
- Table automatically refreshes to show current accounts
- Accessible with proper `aria-label` attributes
- Consistent with posts page UX patterns

---

## 🎉 Result

The accounts page now has:
1. ✅ **Checkbox selection** for individual and bulk operations
2. ✅ **Bulk delete** functionality with confirmation
3. ✅ **Select All/Deselect All** buttons
4. ✅ **Visual feedback** with blue highlighting
5. ✅ **Bulk actions bar** with clear UI
6. ✅ **Loading states** during operations

Matching the posts page improvements! 🚀
