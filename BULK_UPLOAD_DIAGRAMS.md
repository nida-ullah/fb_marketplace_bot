# 📊 Bulk Upload Feature - Visual Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    BULK UPLOAD WORKFLOW                         │
└─────────────────────────────────────────────────────────────────┘

┌───────────────┐
│  User Access  │
│  /bulk-upload/│
└───────┬───────┘
        │
        ▼
┌─────────────────────────┐
│  Bulk Upload Page       │
│  (HTML Form)            │
│  - Instructions         │
│  - File Input           │
│  - Examples             │
└───────┬─────────────────┘
        │
        │ User uploads CSV
        ▼
┌─────────────────────────┐
│  Django View            │
│  bulk_upload_posts()    │
└───────┬─────────────────┘
        │
        │ Validate file
        ▼
┌─────────────────────────┐      ❌ Not CSV
│  File Type Check        │──────────────┐
└───────┬─────────────────┘              │
        │ ✅ Is CSV                       │
        ▼                                 │
┌─────────────────────────┐              │
│  Parse CSV              │              │
│  (csv.DictReader)       │              │
└───────┬─────────────────┘              │
        │                                 │
        │ For each row                    │
        ▼                                 │
┌─────────────────────────────────────┐  │
│  Row Validation Loop                │  │
│                                     │  │
│  ┌──────────────────────┐          │  │
│  │ 1. Check Required    │          │  │
│  │    Fields            │          │  │
│  └──────────┬───────────┘          │  │
│             │                       │  │
│             ▼                       │  │
│  ┌──────────────────────┐          │  │
│  │ 2. Verify Account    │          │  │
│  │    Exists            │          │  │
│  └──────────┬───────────┘          │  │
│             │                       │  │
│             ▼                       │  │
│  ┌──────────────────────┐          │  │
│  │ 3. Validate Price    │          │  │
│  │    (numeric)         │          │  │
│  └──────────┬───────────┘          │  │
│             │                       │  │
│             ▼                       │  │
│  ┌──────────────────────┐          │  │
│  │ 4. Check Image       │          │  │
│  │    Exists            │          │  │
│  └──────────┬───────────┘          │  │
│             │                       │  │
│             ▼                       │  │
│  ┌──────────────────────┐          │  │
│  │ 5. Parse DateTime    │          │  │
│  │    (if provided)     │          │  │
│  └──────────┬───────────┘          │  │
│             │                       │  │
│             ▼                       │  │
│  ┌──────────────────────┐          │  │
│  │ 6. Create Post       │          │  │
│  │    or Log Error      │          │  │
│  └──────────────────────┘          │  │
│                                     │  │
└─────────────┬───────────────────────┘  │
              │                           │
              ▼                           │
┌─────────────────────────┐              │
│  Import Summary         │              │
│  - Success count        │              │
│  - Error count          │              │
│  - Error details        │              │
└───────┬─────────────────┘              │
        │                                 │
        │ ◄───────────────────────────────┘
        │
        ▼
┌─────────────────────────┐
│  Display Results        │
│  - Success message      │
│  - Error messages       │
│  - Redirect to list     │
└─────────────────────────┘


═══════════════════════════════════════════════════════════════════

                    DATA FLOW DIAGRAM

┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│             │       │             │       │             │
│  CSV File   │──────▶│  Validation │──────▶│  Database   │
│             │       │   Logic     │       │  (SQLite)   │
│             │       │             │       │             │
└─────────────┘       └─────────────┘       └─────────────┘
      │                     │                      │
      │                     │                      │
      │                     ▼                      │
      │              ┌─────────────┐              │
      │              │   Errors    │              │
      │              │   Log       │              │
      │              └─────────────┘              │
      │                                            │
      └───────────────────────────────────────────┘
                          │
                          ▼
                  ┌─────────────┐
                  │   Media     │
                  │   Files     │
                  │ (Images)    │
                  └─────────────┘


═══════════════════════════════════════════════════════════════════

                    VALIDATION FLOW

CSV Row Data
    │
    ├──▶ account_email ──▶ Exists in DB? ──┐
    │                                       │
    ├──▶ title ──────────▶ Not empty? ─────┤
    │                                       │
    ├──▶ description ───▶ Not empty? ─────┤
    │                                       ├──▶ ALL VALID? ──▶ CREATE POST
    ├──▶ price ─────────▶ Numeric? ────────┤                        │
    │                                       │                        ▼
    ├──▶ image_filename ▶ File exists? ───┤                 ┌──────────────┐
    │                                       │                 │ MarketPlace  │
    └──▶ scheduled_time ▶ Valid format? ──┘                 │    Post      │
                                                             └──────────────┘
         ❌ ANY INVALID? ──▶ LOG ERROR
                                │
                                ▼
                         Row skipped,
                         continue to next


═══════════════════════════════════════════════════════════════════

                    ERROR HANDLING FLOW

┌─────────────────────────┐
│  Processing Row 5       │
└───────┬─────────────────┘
        │
        ▼
┌─────────────────────────┐
│  Validation Error?      │
└───────┬─────────┬───────┘
        │ Yes     │ No
        │         │
        ▼         ▼
┌─────────────┐  ┌─────────────┐
│  Log Error  │  │ Create Post │
│  with       │  │  Success    │
│  Row Number │  └──────┬──────┘
└──────┬──────┘         │
       │                │
       │                ▼
       │         ┌──────────────┐
       │         │ success_count│
       │         │     + 1      │
       │         └──────────────┘
       │
       ▼
┌──────────────┐
│ error_count  │
│    + 1       │
└──────────────┘
       │
       ▼
Continue to Next Row


═══════════════════════════════════════════════════════════════════

                    USER JOURNEY MAP

1. User Journey (Success Path):

   Start ──▶ Upload Page ──▶ Select CSV ──▶ Click Upload
     │
     ▼
   Processing ──▶ Validation ──▶ Posts Created
     │
     ▼
   Success Message ──▶ Redirect to Post List ──▶ View Posts


2. User Journey (Error Path):

   Start ──▶ Upload Page ──▶ Select CSV ──▶ Click Upload
     │
     ▼
   Processing ──▶ Validation ──▶ Errors Found
     │
     ▼
   Error Messages ──▶ Fix CSV ──▶ Re-upload


═══════════════════════════════════════════════════════════════════

                    COMPONENT INTERACTION

┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND                                │
│                                                                 │
│  ┌─────────────────┐      ┌─────────────────┐                 │
│  │  Post List      │◀────▶│  Bulk Upload    │                 │
│  │  Page           │      │  Page           │                 │
│  └─────────────────┘      └────────┬────────┘                 │
│                                     │                           │
└─────────────────────────────────────┼───────────────────────────┘
                                      │
                                      │ POST request
                                      │
┌─────────────────────────────────────┼───────────────────────────┐
│                         BACKEND     ▼                           │
│                                                                 │
│  ┌──────────────────────────────────────────────────┐          │
│  │           bulk_upload_posts() View               │          │
│  └───────────┬──────────────────────────────────────┘          │
│              │                                                  │
│              ├──▶ BulkPostUploadForm (forms.py)               │
│              │                                                  │
│              ├──▶ CSV Parsing Logic                           │
│              │                                                  │
│              ├──▶ FacebookAccount.objects.get()               │
│              │                                                  │
│              ├──▶ File System Check (os.path.exists)          │
│              │                                                  │
│              └──▶ MarketplacePost.objects.create()            │
│                                                                 │
└─────────────────────────────────────┬───────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                         DATABASE                                │
│                                                                 │
│  ┌─────────────────┐      ┌─────────────────┐                 │
│  │  FacebookAccount│      │ MarketplacePost │                 │
│  │  Table          │      │  Table          │                 │
│  └─────────────────┘      └─────────────────┘                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════

                    FILE SYSTEM INTERACTION

User's Computer                Server
    │                            │
    │ 1. Prepare CSV            │
    │    and Images              │
    │                            │
    │ 2. Upload Images           │
    ├──────────────────────────▶│
    │                            │ Save to:
    │                            │ media/posts/
    │                            │
    │ 3. Upload CSV              │
    ├──────────────────────────▶│
    │                            │ Parse CSV
    │                            │ Validate each row
    │                            │ Check images exist
    │                            │ Create posts
    │                            │
    │ 4. Receive Results         │
    │◀───────────────────────────┤
    │                            │
    │ 5. View Posts              │
    │◀──────────────────────────▶│
    │                            │


═══════════════════════════════════════════════════════════════════

                    SUCCESS SCENARIO

CSV File:
┌─────────────────────────────────────────────────────────────────┐
│ account_email,title,description,price,image_filename,scheduled  │
│ user@ex.com,Product 1,Desc 1,99.99,img1.jpg,2025-10-16 10:00  │
│ user@ex.com,Product 2,Desc 2,149.99,img2.jpg,2025-10-16 11:00 │
│ user@ex.com,Product 3,Desc 3,199.99,img3.jpg,2025-10-16 12:00 │
└─────────────────────────────────────────────────────────────────┘
                        │
                        ▼
               ┌─────────────────┐
               │  Validation     │
               │  All ✅ Pass    │
               └────────┬────────┘
                        │
                        ▼
               ┌─────────────────┐
               │  Create 3 Posts │
               └────────┬────────┘
                        │
                        ▼
               ┌─────────────────┐
               │  Success! ✅    │
               │  3 posts        │
               │  imported       │
               └─────────────────┘


═══════════════════════════════════════════════════════════════════

                    ERROR SCENARIO

CSV File:
┌─────────────────────────────────────────────────────────────────┐
│ account_email,title,description,price,image_filename,scheduled  │
│ user@ex.com,Product 1,Desc 1,99.99,img1.jpg,2025-10-16 10:00  │ ✅
│ fake@ex.com,Product 2,Desc 2,149.99,img2.jpg,2025-10-16 11:00 │ ❌
│ user@ex.com,Product 3,Desc 3,bad,missing.jpg,2025-10-16 12:00 │ ❌
└─────────────────────────────────────────────────────────────────┘
                        │
                        ▼
               ┌─────────────────┐
               │  Validation     │
               │  Row 1: ✅      │
               │  Row 2: ❌      │
               │  Row 3: ❌      │
               └────────┬────────┘
                        │
                        ▼
               ┌─────────────────────────────┐
               │  Result:                    │
               │  ✅ 1 post imported         │
               │  ❌ 2 errors:               │
               │  - Row 2: Account not found│
               │  - Row 3: Invalid price &  │
               │    Image not found         │
               └─────────────────────────────┘


═══════════════════════════════════════════════════════════════════

                    INTEGRATION WITH EXISTING SYSTEM

┌─────────────────────────────────────────────────────────────────┐
│                  EXISTING SYSTEM (UNCHANGED)                    │
│                                                                 │
│  ┌─────────────────┐      ┌──────────────────────────┐        │
│  │  Single Post    │      │  Automation              │        │
│  │  Creation       │      │  (post_to_facebook.py)   │        │
│  └─────────────────┘      └──────────────────────────┘        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Both create same
                              │ MarketplacePost objects
                              │
┌─────────────────────────────┼─────────────────────────────────┐
│          NEW FEATURE        ▼                                  │
│                                                                 │
│  ┌─────────────────────────────────────────┐                  │
│  │  Bulk Upload (CSV)                      │                  │
│  │  - Creates multiple posts at once       │                  │
│  │  - Same database structure              │                  │
│  │  - Compatible with existing automation  │                  │
│  └─────────────────────────────────────────┘                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  MarketplacePost│
                    │  Database Table │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Automation     │
                    │  Posts to FB    │
                    └─────────────────┘


═══════════════════════════════════════════════════════════════════
```

## Legend

- ▶ : Process flow
- ─ : Connection
- ✅ : Success / Valid
- ❌ : Error / Invalid
- │ : Vertical flow
- ┌─┐ : Box/Container
- └─┘ : Box end

---

**Diagram Created:** October 15, 2025  
**Version:** 1.0
