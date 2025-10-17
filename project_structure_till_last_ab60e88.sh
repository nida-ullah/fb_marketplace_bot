Based on my analysis of your project, here's a comprehensive step-by-step explanation:

🤖 Facebook Marketplace Automation Bot - Complete Explanation
Project Overview
You're building an automated bot that posts products to Facebook Marketplace using Django (web framework) and Playwright (browser automation). This eliminates manual posting and allows you to manage multiple Facebook accounts and schedule posts from a web interface.

🏗️ Architecture & Components
1. Technology Stack
Backend Framework: Django 5.2.2 (Python web framework)
Database: SQLite (stores accounts, posts, sessions)
Browser Automation: Playwright (controls Chrome/Chromium to interact with Facebook)
Image Handling: Pillow (image processing library)
2. Django Apps Structure
Your project has 3 main apps:

a) accounts App
Purpose: Manages Facebook accounts

Key Model (FacebookAccount):

Features:

Add accounts via Django admin or bulk upload
Stores credentials securely in database
Auto-deletes session files when account is removed
b) postings App
Purpose: Manages marketplace listings

Key Model (MarketplacePost):

Features:

Create single posts via admin
Bulk upload via CSV file
Track posting status
c) automation App
Purpose: Handles browser automation logic

Core File: post_to_facebook.py contains:

Session saving - Login once and save cookies
Auto-posting - Fill out Facebook Marketplace forms automatically
📋 Step-by-Step Workflow
STEP 1: Add Facebook Accounts
Two Methods:

Method A: Manual (Django Admin)

Go to http://localhost:8000/admin
Navigate to Accounts > Facebook accounts
Click "Add" and enter email + password
Save
Method B: Bulk Upload

Create accounts.txt file:
Upload via bulk upload interface
System creates database entries automatically
STEP 2: Save Login Sessions
Why? Facebook requires login. Instead of logging in every time, you save the session once.

How it works:

What happens:

Playwright opens a real Chrome browser
Goes to Facebook login page
Auto-fills email & password (if provided)
Waits for you to handle 2FA/CAPTCHA manually
After successful login, saves cookies/session to sessions/your_email_gmail_com.json
Next time: Bot uses this session file - no re-login needed!
Session Storage:

Files stored in sessions folder
JSON format containing authentication cookies
Persists across multiple posts
STEP 3: Create Posts
Three Methods:

A) Single Post (Django Admin)
Admin → Postings > Marketplace posts
Fill in:
Account (select from saved accounts)
Title, description, price
Upload image
Set scheduled_time (set to past/now for immediate posting)
Save
B) Bulk Upload (Simple CSV)
Create CSV with 3 columns only:

Visit http://localhost:8000/bulk-upload/

Select accounts to post from

Upload CSV

Posts created instantly in database with posted=False

C) Advanced Bulk Upload (with Image URLs)
CSV can include optional image_url column:

Bot downloads images automatically!

STEP 4: Execute Automated Posting
Command:

What happens internally:

Query Database:

For each post:

Load account's saved session from sessions
Open browser with saved session (auto-logged in!)
Navigate to facebook.com/marketplace/create/item
Fill Form Automatically:

Update Database:

Mark posted = True
Post won't be processed again
🔐 Session Management System
Session Lifecycle:
Cleanup Features:
Auto-cleanup on account deletion:

Orphaned session cleanup:

Runs when viewing bulk upload page
Removes session files for deleted accounts
🎯 Key Features You've Implemented
1. Multi-Account Support
Store unlimited Facebook accounts
Each post can use different account
Session saved per account
2. Bulk Operations
Upload 100s of accounts at once
Upload 100s of posts via CSV
Multiply posts across accounts (1 post × 5 accounts = 5 listings)
3. Smart Form Filling
The bot intelligently handles Facebook's dynamic form:

Locates input fields even when HTML structure changes
Multiple fallback strategies (text selector, role selector, keyboard navigation)
Debug screenshots on failure
Skips location field (assumes VPN/proxy handles region)
4. Error Handling
Validates CSV data before creating posts
Shows detailed error messages per row
Takes screenshots when posting fails
Checks for CAPTCHA/2FA and waits for manual intervention
5. Scheduling
Set scheduled_time for future posting
Management command only posts when time is reached
Can be automated with cron jobs
📁 Important Files
File	Purpose
db.sqlite3	Database (accounts + posts)
sessions/*.json	Saved login sessions
posts	Uploaded product images
accounts.txt	Bulk account import format
sample_bulk_upload.csv	CSV template for posts
post_to_facebook.py	Core automation logic
manage.py	Django command runner
🚀 Typical Usage Flow
🎓 What You're Learning
Web Scraping/Automation: Using Playwright to control browsers
Django Framework: Models, admin, forms, views, management commands
Database Design: Relationships (ForeignKey), queries, migrations
File Handling: CSV parsing, image uploads, session storage
API Integration: Downloading images from URLs
Background Processing: Threading for async session creation
Production Considerations: Security warnings about storing passwords
⚠️ Current Limitations & Future Improvements
Limitations:

Passwords stored in plain text (should use encryption)
Fixed category/condition (Furniture/New)
No location selection
Headless mode might trigger detection
Sessions expire after ~30-60 days
Potential Enhancements:

Add category/condition selection in admin
Location targeting
Proxy rotation
Captcha solving service integration
Schedule posts with cron/celery
Real-time posting status dashboard
This is a real-world automation project that demonstrates how businesses automate repetitive tasks. You're essentially building a tool that could handle marketplace posting for an e-commerce business managing hundreds of products across multiple accounts! 🎉

Claude Sonnet 4.5 • 1x