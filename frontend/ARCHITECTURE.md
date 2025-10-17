# 🏗️ Frontend Architecture Overview

## 📂 File Structure
```
frontend/
│
├── 📱 app/                          # Next.js App Router
│   ├── 🏠 page.tsx                  # Landing Page (Public)
│   ├── 🎨 layout.tsx                # Root Layout + AuthProvider
│   ├── 🌍 globals.css               # Global Styles
│   │
│   ├── 🔐 login/
│   │   └── page.tsx                 # Login Page
│   │
│   ├── ✍️ signup/
│   │   └── page.tsx                 # Signup Page
│   │
│   └── 📊 dashboard/                # Protected Dashboard
│       ├── layout.tsx               # Dashboard Layout + Sidebar
│       ├── page.tsx                 # Dashboard Home (Stats)
│       │
│       ├── 👥 accounts/             # TODO: Account Management
│       ├── 📝 posts/                # TODO: Post Management
│       ├── 📤 bulk-upload/          # TODO: Bulk Upload
│       ├── 📈 analytics/            # TODO: Analytics
│       └── ⚙️ settings/             # TODO: Settings
│
├── 🧩 components/
│   └── ui/                          # Reusable UI Components
│       ├── Button.tsx               # Button Component
│       ├── Input.tsx                # Input Component
│       ├── Card.tsx                 # Card Component
│       ├── Toast.tsx                # Toast Notifications
│       └── Sidebar.tsx              # Dashboard Sidebar
│
├── 🔄 context/
│   └── AuthContext.tsx              # Authentication State
│
├── 🎣 hooks/
│   └── useAuth.ts                   # Auth Hook
│
├── 🛠️ lib/
│   ├── api.ts                       # API Client + Endpoints
│   └── utils.ts                     # Helper Functions
│
├── 📦 types/
│   └── index.ts                     # TypeScript Interfaces
│
├── 📄 Documentation
│   ├── FRONTEND_README.md           # Full Documentation
│   ├── QUICK_START.md               # Quick Setup Guide
│   └── SETUP_COMPLETE.md            # What Was Built
│
└── ⚙️ Config Files
    ├── package.json                 # Dependencies
    ├── tsconfig.json                # TypeScript Config
    ├── tailwind.config.ts           # Tailwind Config
    ├── next.config.ts               # Next.js Config
    ├── .env.local.example           # Environment Template
    └── eslint.config.mjs            # ESLint Config
```

---

## 🔄 Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                       USER BROWSER                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    NEXT.JS FRONTEND                         │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │               Page Components                         │  │
│  │  • Landing Page (/)                                  │  │
│  │  • Login (/login)                                    │  │
│  │  • Signup (/signup)                                  │  │
│  │  • Dashboard (/dashboard)                            │  │
│  └──────────────────────────────────────────────────────┘  │
│                              │                              │
│                              ▼                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │            AuthContext (State)                        │  │
│  │  • user: User | null                                 │  │
│  │  • isAuthenticated: boolean                          │  │
│  │  • login(), signup(), logout()                       │  │
│  └──────────────────────────────────────────────────────┘  │
│                              │                              │
│                              ▼                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │             API Client (Axios)                        │  │
│  │  • Request Interceptor (add token)                   │  │
│  │  • Response Interceptor (handle 401)                 │  │
│  │  • API endpoints (auth, accounts, posts, stats)      │  │
│  └──────────────────────────────────────────────────────┘  │
│                              │                              │
└──────────────────────────────┼──────────────────────────────┘
                               │
                               │ HTTP/HTTPS
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                  DJANGO BACKEND API                         │
│                                                             │
│  • POST /api/auth/login/                                   │
│  • POST /api/auth/signup/                                  │
│  • GET  /api/auth/profile/                                 │
│  • GET  /api/accounts/                                     │
│  • POST /api/accounts/                                     │
│  • GET  /api/posts/                                        │
│  • POST /api/posts/                                        │
│  • GET  /api/stats/dashboard/                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    SQLite DATABASE                          │
│  • User accounts                                           │
│  • Facebook accounts                                       │
│  • Marketplace posts                                       │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔐 Authentication Flow

```
┌─────────┐
│  User   │
└────┬────┘
     │
     │ 1. Opens /login
     ▼
┌─────────────────┐
│  Login Page     │
│  (Form Input)   │
└────┬────────────┘
     │
     │ 2. Submits email + password
     ▼
┌─────────────────────┐
│  AuthContext        │
│  login() function   │
└────┬────────────────┘
     │
     │ 3. POST /api/auth/login/
     ▼
┌──────────────────────┐
│  Django Backend      │
│  Validates           │
└────┬─────────────────┘
     │
     │ 4. Returns { token, user }
     ▼
┌──────────────────────┐
│  AuthContext         │
│  • Store token       │
│  • Store user        │
│  • Set isAuth=true   │
└────┬─────────────────┘
     │
     │ 5. Redirect to /dashboard
     ▼
┌──────────────────────┐
│  Dashboard Layout    │
│  • Check isAuth      │
│  • Render Sidebar    │
└────┬─────────────────┘
     │
     │ 6. Load dashboard
     ▼
┌──────────────────────┐
│  Dashboard Page      │
│  • Fetch stats       │
│  • Display cards     │
└──────────────────────┘
```

---

## 🛡️ Protected Route Logic

```
User navigates to /dashboard
         │
         ▼
┌─────────────────────┐
│  Dashboard Layout   │
│  useAuth() hook     │
└────┬────────────────┘
     │
     ▼
┌──────────────────────────┐
│  Check: isAuthenticated? │
└────┬─────────────────┬───┘
     │                 │
     │ YES             │ NO
     ▼                 ▼
┌─────────┐      ┌──────────────┐
│  Render │      │  Redirect to │
│  Page   │      │  /login      │
└─────────┘      └──────────────┘
```

---

## 🎨 Component Hierarchy

```
App
└── RootLayout (AuthProvider wrapper)
    ├── Landing Page (/)
    │   ├── Header
    │   ├── Hero Section
    │   ├── Features Section
    │   └── Footer
    │
    ├── Login Page (/login)
    │   └── Card
    │       ├── CardHeader
    │       ├── CardContent
    │       │   ├── Input (email)
    │       │   ├── Input (password)
    │       │   └── Button
    │       └── Link to Signup
    │
    ├── Signup Page (/signup)
    │   └── Card
    │       ├── CardHeader
    │       ├── CardContent
    │       │   ├── Input (name)
    │       │   ├── Input (email)
    │       │   ├── Input (password)
    │       │   ├── Input (confirm password)
    │       │   └── Button
    │       └── Link to Login
    │
    └── Dashboard (/dashboard)
        ├── DashboardLayout
        │   ├── Sidebar
        │   │   ├── Logo
        │   │   ├── Navigation Links
        │   │   └── User Profile + Logout
        │   │
        │   └── Main Content Area
        │       └── Dashboard Page
        │           ├── Header
        │           ├── Stats Cards (4x)
        │           │   ├── Card (Total Accounts)
        │           │   ├── Card (Total Posts)
        │           │   ├── Card (Pending Posts)
        │           │   └── Card (Posted Today)
        │           ├── Success Rate Card
        │           └── Quick Actions Card
        │
        ├── Accounts Page (TODO)
        ├── Posts Page (TODO)
        ├── Bulk Upload Page (TODO)
        ├── Analytics Page (TODO)
        └── Settings Page (TODO)
```

---

## 📊 State Management

### Global State (AuthContext)
```typescript
{
  user: User | null,
  loading: boolean,
  isAuthenticated: boolean,
  login: (email, password) => Promise<void>,
  signup: (name, email, password) => Promise<void>,
  logout: () => void
}
```

### Local State (useState)
- Form inputs
- Loading states
- Error messages
- Page-specific data

### Server State (API calls)
- Dashboard stats
- Account lists
- Post lists
- Analytics data

---

## 🚀 API Endpoints Map

```
Authentication:
  POST   /api/auth/login/       → Login user
  POST   /api/auth/signup/      → Register user
  POST   /api/auth/logout/      → Logout user
  GET    /api/auth/profile/     → Get user info

Accounts:
  GET    /api/accounts/         → List all FB accounts
  POST   /api/accounts/         → Add new FB account
  DELETE /api/accounts/:id/     → Remove FB account
  POST   /api/accounts/bulk/    → Bulk upload accounts

Posts:
  GET    /api/posts/            → List all posts
  POST   /api/posts/            → Create new post
  PUT    /api/posts/:id/        → Update post
  DELETE /api/posts/:id/        → Delete post
  POST   /api/posts/bulk/       → Bulk upload posts

Stats:
  GET    /api/stats/dashboard/  → Dashboard statistics
```

---

## 🎯 Page Status

| Page | Path | Status | Description |
|------|------|--------|-------------|
| Landing | `/` | ✅ Complete | Hero, features, CTA |
| Login | `/login` | ✅ Complete | Form with validation |
| Signup | `/signup` | ✅ Complete | Registration form |
| Dashboard | `/dashboard` | ✅ Complete | Stats overview |
| Accounts | `/dashboard/accounts` | ⏳ TODO | Manage FB accounts |
| Posts | `/dashboard/posts` | ⏳ TODO | Manage posts |
| Bulk Upload | `/dashboard/bulk-upload` | ⏳ TODO | CSV upload |
| Analytics | `/dashboard/analytics` | ⏳ TODO | Charts & reports |
| Settings | `/dashboard/settings` | ⏳ TODO | User settings |

---

## 🔧 Technology Decisions

### Why Next.js?
- Server-side rendering (SEO)
- File-based routing
- Built-in optimization
- Great developer experience

### Why TypeScript?
- Type safety
- Better IDE support
- Catch errors early
- Self-documenting code

### Why Tailwind CSS?
- Utility-first approach
- Fast development
- Consistent design
- Easy responsive design

### Why React Hook Form + Zod?
- Performance (minimal re-renders)
- Great validation
- Type-safe schemas
- Easy error handling

---

## 📈 Performance Optimizations

- ✅ Code splitting (automatic with Next.js)
- ✅ Image optimization (Next.js Image component)
- ✅ Font optimization (next/font)
- ✅ Lazy loading (React.lazy for future pages)
- ✅ API response caching (can be added)
- ✅ Static generation where possible

---

## 🛠️ Development Workflow

```bash
# 1. Make changes to code
vim app/dashboard/page.tsx

# 2. Hot reload updates browser automatically
# (no restart needed)

# 3. Check terminal for errors
# (TypeScript errors show immediately)

# 4. Test in browser
open http://localhost:3000

# 5. Commit changes
git add .
git commit -m "feat: update dashboard"
git push
```

---

## 🎨 Design Tokens

### Colors
- Primary: `#2563eb` (blue-600)
- Success: `#16a34a` (green-600)
- Warning: `#ca8a04` (yellow-600)
- Danger: `#dc2626` (red-600)
- Gray: `#6b7280` (gray-500)

### Typography
- Font: Geist Sans (default)
- Mono: Geist Mono
- Sizes: text-sm, text-base, text-lg, text-xl, text-2xl, text-3xl

### Spacing
- Small: `p-4` (16px)
- Medium: `p-6` (24px)
- Large: `p-8` (32px)
- XL: `p-12` (48px)

### Border Radius
- Small: `rounded` (4px)
- Medium: `rounded-lg` (8px)
- Large: `rounded-xl` (12px)
- Full: `rounded-full`

---

## 📱 Responsive Breakpoints

```css
/* Mobile First Approach */
default:  /* < 640px  */ Mobile
sm:       /* ≥ 640px  */ Small tablets
md:       /* ≥ 768px  */ Tablets
lg:       /* ≥ 1024px */ Laptops
xl:       /* ≥ 1280px */ Desktops
2xl:      /* ≥ 1536px */ Large screens
```

### Dashboard Layout
- **Mobile**: Sidebar hidden, full-width content
- **Tablet+**: Sidebar visible (256px), remaining space for content

---

This architecture provides a solid foundation for a scalable, maintainable frontend application! 🚀
