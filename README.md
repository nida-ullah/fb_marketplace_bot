# 🚀 Facebook Marketplace Automation Bot

> **Full-Stack Application** - Modern Next.js Frontend + Django Backend + Playwright Browser Automation

Automated system to post products to Facebook Marketplace with a beautiful web interface. Manage multiple Facebook accounts, create posts, and automate marketplace listings with browser automation.

![Tech Stack](https://img.shields.io/badge/Django-5.2.2-green)
![Tech Stack](https://img.shields.io/badge/Next.js-15.5.6-black)
![Tech Stack](https://img.shields.io/badge/Playwright-1.52.0-blue)
![Tech Stack](https://img.shields.io/badge/TypeScript-5.x-blue)

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Running the Project](#-running-the-project)
- [Usage Guide](#-usage-guide)
- [API Endpoints](#-api-endpoints)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### 🎨 **Modern Web Interface (Next.js Frontend)**
- 🔐 **User Authentication** - JWT-based login/signup system
- 📊 **Dashboard** - Real-time statistics and analytics
- 👥 **Account Management** - Add, view, and manage Facebook accounts
- 📝 **Posts Management** - Create and manage marketplace listings
- 🔄 **Update Sessions** - One-click browser automation to refresh expired sessions
- 📤 **Bulk Upload** - Upload multiple accounts from `.txt` files
- 🎨 **Beautiful UI** - Responsive design with Tailwind CSS
- 🔔 **Real-time Feedback** - Toast notifications for all actions

### ⚙️ **Powerful Backend (Django REST API)**
- 🗄️ **RESTful API** - Complete CRUD operations for accounts and posts
- 🔒 **JWT Authentication** - Secure token-based authentication
- 👤 **User Management** - Django user model with secure passwords
- 📦 **Database** - SQLite (easily switch to PostgreSQL)
- 🌐 **CORS Enabled** - Ready for frontend integration

### 🤖 **Browser Automation (Playwright)**
- 🌐 **Automated Login** - Save Facebook sessions automatically
- 🔄 **Session Reuse** - Login once, reuse sessions forever
- 🛡️ **CAPTCHA Support** - Manual CAPTCHA solving with 90-second timeout
- 🖼️ **Auto-fill Forms** - Automatically fills login credentials
- 📱 **Multiple Accounts** - Manage and automate multiple Facebook accounts
- 🎯 **Smart Detection** - Detects CAPTCHA and waits for manual solving

### 📦 **Bulk Operations**
- 📤 **Bulk Account Upload** - Upload accounts from `.txt` file (one email:password per line)
- 📝 **Bulk Post Upload** - CSV with 3 columns (title, description, price)
- ⚡ **Batch Processing** - Process multiple accounts sequentially

---

## 🛠️ Tech Stack

### **Frontend**
- ⚛️ **Next.js 15.5.6** - React framework with App Router
- 🎨 **Tailwind CSS** - Utility-first CSS framework
- 📘 **TypeScript** - Type-safe development
- 🔗 **Axios** - HTTP client for API calls
- 📋 **React Hook Form** - Form validation
- ✅ **Zod** - Schema validation
- 🎭 **Lucide React** - Beautiful icon library

### **Backend**
- 🐍 **Django 5.2.2** - High-level Python web framework
- 🔌 **Django REST Framework 3.14.0** - Powerful REST API toolkit
- 🔑 **Simple JWT 5.3.0** - JWT authentication
- 🌐 **Django CORS Headers 4.3.1** - Cross-origin resource sharing
- 🎭 **Playwright 1.52.0** - Browser automation
- 🗄️ **SQLite** - Default database (production-ready PostgreSQL support)

---

## 📁 Project Structure

```
fb_marketplace_bot/
│
├── frontend/                    # Next.js Frontend Application
│   ├── app/                    # Next.js App Router
│   │   ├── dashboard/         # Dashboard pages
│   │   │   ├── accounts/      # Accounts management page
│   │   │   ├── posts/         # Posts management page
│   │   │   └── page.tsx       # Dashboard home
│   │   ├── login/             # Login page
│   │   ├── signup/            # Signup page
│   │   └── layout.tsx         # Root layout
│   ├── components/            # React components
│   │   ├── ui/               # Reusable UI components
│   │   ├── AddAccountModal.tsx
│   │   └── BulkUploadModal.tsx
│   ├── lib/                   # Utility functions
│   │   └── api.ts            # API client (Axios)
│   ├── context/              # React Context
│   │   └── AuthContext.tsx   # Authentication context
│   ├── hooks/                # Custom React hooks
│   ├── types/                # TypeScript types
│   ├── package.json
│   └── next.config.ts
│
├── accounts/                   # Django Accounts App
│   ├── models.py             # FacebookAccount model
│   ├── api_views.py          # REST API views
│   ├── api_urls.py           # API routes
│   ├── forms.py
│   └── management/
│       └── commands/
│           └── cleanup_sessions.py
│
├── postings/                   # Django Postings App
│   ├── models.py             # MarketplacePost model
│   ├── api_views.py          # REST API views
│   ├── api_urls.py           # API routes
│   ├── serializers.py        # DRF serializers
│   └── migrations/
│
├── automation/                 # Browser Automation
│   ├── post_to_facebook.py   # Playwright automation logic
│   └── cron.py               # Scheduled tasks
│
├── bot_core/                   # Django Project Settings
│   ├── settings.py           # Main settings
│   ├── urls.py               # URL configuration
│   └── wsgi.py
│
├── sessions/                   # Saved Facebook sessions (.json)
├── media/                      # Uploaded files
│   └── posts/                # Post images
│
├── manage.py                   # Django management script
├── requirements.txt            # Python dependencies
├── db.sqlite3                  # SQLite database
└── README.md                   # This file
```

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- ✅ **Python 3.8+** - [Download](https://www.python.org/downloads/)
- ✅ **Node.js 18+** - [Download](https://nodejs.org/)
- ✅ **Git** - [Download](https://git-scm.com/)
- ✅ **pip** - Python package manager (included with Python)
- ✅ **npm** - Node package manager (included with Node.js)

---

## 🚀 Installation

### **Step 1: Clone the Repository**

```bash
git clone https://github.com/nida-ullah/fb_marketplace_bot.git
cd fb_marketplace_bot
```

---

### **Step 2: Backend Setup (Django)**

#### 2.1 Create Virtual Environment

```bash
# Windows
python -m venv env
env\Scripts\activate

# macOS/Linux
python3 -m venv env
source env/bin/activate
```

#### 2.2 Install Python Dependencies

```bash
pip install -r requirements.txt
```

#### 2.3 Install Playwright Browsers

```bash
playwright install chromium
```

#### 2.4 Create Required Folders

```bash
# Windows
mkdir sessions
mkdir media\posts

# macOS/Linux
mkdir -p sessions media/posts
```

#### 2.5 Run Database Migrations

```bash
python manage.py migrate
```

#### 2.6 Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
# Follow prompts to create admin account
```

---

### **Step 3: Frontend Setup (Next.js)**

#### 3.1 Navigate to Frontend Directory

```bash
cd frontend
```

#### 3.2 Install Node Dependencies

```bash
npm install
```

#### 3.3 Create Environment File

Create a file named `.env.local` in the `frontend/` folder:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

#### 3.4 Go Back to Root Directory

```bash
cd ..
```

---

## 🎮 Running the Project

You need **TWO terminals** running simultaneously:

### **Terminal 1: Django Backend**

```bash
# Navigate to project root
cd fb_marketplace_bot

# Activate virtual environment
# Windows:
env\Scripts\activate
# macOS/Linux:
source env/bin/activate

# Run Django server
python manage.py runserver
```

✅ **Backend running at:** `http://localhost:8000`

---

### **Terminal 2: Next.js Frontend**

```bash
# Navigate to frontend folder
cd fb_marketplace_bot/frontend

# Run Next.js dev server
npm run dev
```

✅ **Frontend running at:** `http://localhost:3000`

---

## 📖 Usage Guide

### 🌐 **Access Points**

- 🎨 **Web App:** http://localhost:3000
- 🔐 **Login/Signup:** Create account at http://localhost:3000/signup
- 🏠 **Dashboard:** http://localhost:3000/dashboard
- 🛠️ **Django Admin:** http://localhost:8000/admin
- 📡 **API:** http://localhost:8000/api

---

### 👤 **1. Create User Account**

1. Visit http://localhost:3000/signup
2. Fill in email, password, and name
3. Click "Sign Up"
4. Login with your credentials

---

### 📱 **2. Add Facebook Accounts**

#### **Method A: Single Account (with Browser Automation)**

1. Go to **Dashboard → Accounts**
2. Click **"Add Account"** button
3. Enter Facebook email and password
4. Click **"Add Account"**
5. ✨ **Browser opens automatically** - complete login (solve CAPTCHA if needed)
6. Session is saved automatically

#### **Method B: Bulk Upload from Text File**

1. Create a `.txt` file with one account per line:
   ```
   email1@example.com:password1
   email2@example.com:password2
   email3@example.com:password3
   ```

2. Go to **Dashboard → Accounts**
3. Click **"Bulk Upload"** button
4. Select your `.txt` file
5. Click **"Upload Accounts"**
6. ✨ **Browser opens for each account** - complete logins sequentially

---

### 🔄 **3. Update Expired Sessions**

When a session expires (shows red "No Session" badge):

1. Go to **Dashboard → Accounts**
2. Find account with **red "No Session"** badge
3. Click **"Update Session"** button
4. ✨ **Browser opens** - complete login
5. Session is refreshed automatically

---

### 📝 **4. Manage Posts**

#### **View All Posts**

1. Go to **Dashboard → Posts**
2. See all marketplace listings with:
   - Post image
   - Title and description
   - Price
   - Account email
   - Posted/Pending status
   - Scheduled time

#### **Filter Posts**

- Click **"All Posts"** - Show everything
- Click **"Posted"** - Show only posted items
- Click **"Pending"** - Show items awaiting posting

#### **Delete Post**

- Click **"Delete"** button on any post card
- Confirm deletion

---

### 🎯 **5. Dashboard Statistics**

The dashboard shows:
- 📊 **Total Accounts** - All Facebook accounts
- ✅ **Active Sessions** - Accounts with valid sessions
- ⏳ **Expired Sessions** - Accounts needing session update
- 📦 **Total Posts** - All marketplace listings
- ✅ **Posted** - Successfully posted items
- ⏳ **Pending** - Items waiting to be posted

---

### 🛠️ **6. Django Admin Panel (Advanced)**

Access at: http://localhost:8000/admin

- ➕ Create posts manually
- 📝 Edit account details
- 🗑️ Bulk delete operations
- 👀 View all database records
- 🔧 Advanced configurations

---

## 📡 API Endpoints

### **Authentication**
```
POST   /api/auth/register/          # Create new user
POST   /api/auth/login/             # Login (returns JWT tokens)
GET    /api/auth/user/              # Get current user info
```

### **Accounts**
```
GET    /api/accounts/               # List all accounts
POST   /api/accounts/add-with-login/ # Add single account + browser login
POST   /api/accounts/bulk-upload/   # Bulk upload from .txt file
POST   /api/accounts/<id>/update-session/ # Update session for account
DELETE /api/accounts/<id>/          # Delete account
```

### **Posts**
```
GET    /api/posts/                  # List all posts
POST   /api/posts/                  # Create new post
GET    /api/posts/<id>/             # Get post detail
PUT    /api/posts/<id>/             # Update post
DELETE /api/posts/<id>/             # Delete post
```

### **Statistics**
```
GET    /api/stats/dashboard/        # Get dashboard statistics
```

---

## 🐛 Troubleshooting

### ❌ **"Port already in use"**

**Django (Port 8000):**
```bash
python manage.py runserver 8001
```

**Next.js (Port 3000):**
```bash
npm run dev -- -p 3001
```

---

### ❌ **"Module not found" errors**

**Backend:**
```bash
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

---

### ❌ **"Cannot connect to backend"**

1. Check Django server is running on port 8000
2. Verify `.env.local` has correct URL:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000/api
   ```
3. Check CORS settings in `bot_core/settings.py`

---

### ❌ **"Database errors"**

Delete database and recreate:
```bash
# Delete database
rm db.sqlite3

# Recreate
python manage.py migrate
python manage.py createsuperuser
```

---

### ❌ **"Playwright browser not found"**

```bash
playwright install chromium
```

---

### ❌ **"Session not saving"**

1. Ensure `sessions/` folder exists
2. Check browser automation completes login
3. Verify no errors in Django console
4. Try manual CAPTCHA solving if prompted

---

## 📝 Important Notes

- 🔐 **Sessions** must be created via browser automation (one-time manual login)
- 🤖 **CAPTCHA** may appear on first login - solve it manually within 90 seconds
- 📁 **Folders** `sessions/` and `media/posts/` must exist
- 🚫 **Don't commit** `env/`, `node_modules/`, `.env.local`, `db.sqlite3` to git
- 🔄 **Two servers** (Django + Next.js) must run simultaneously
- 🛡️ **Facebook** may flag weak/fake accounts - use real accounts

---

## 🎯 What Makes This Project Special?

✅ **Full-Stack** - Complete frontend + backend integration  
✅ **Modern Tech** - Next.js 15, Django 5, TypeScript  
✅ **Browser Automation** - Playwright for Facebook login  
✅ **JWT Auth** - Secure token-based authentication  
✅ **Bulk Operations** - Upload multiple accounts at once  
✅ **Session Management** - Smart session reuse  
✅ **Beautiful UI** - Modern, responsive design  
✅ **RESTful API** - Clean, documented endpoints  
✅ **Type-Safe** - Full TypeScript on frontend  
✅ **Production-Ready** - Easy to deploy  

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

1. 🍴 Fork the repository
2. 🌿 Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. ✅ Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. 📤 Push to the branch (`git push origin feature/AmazingFeature`)
5. 🎉 Open a Pull Request

---

## 📄 License

This project is for educational purposes. Use responsibly and comply with Facebook's Terms of Service.

---

## 👨‍💻 Author

**Nida Ullah**
- GitHub: [@nida-ullah](https://github.com/nida-ullah)
- Repository: [fb_marketplace_bot](https://github.com/nida-ullah/fb_marketplace_bot)

---

## 🙏 Acknowledgments

- Django REST Framework team
- Next.js team
- Playwright team
- Open source community

---

**⭐ If you find this project helpful, please give it a star!**
