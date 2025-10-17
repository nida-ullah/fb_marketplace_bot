# Facebook Marketplace Bot - Frontend

A modern Next.js 14 frontend application for managing Facebook Marketplace automation.

## 🚀 Features

- **Authentication System**: Login, signup with JWT tokens
- **Dashboard**: Overview with stats and analytics
- **Account Management**: Manage multiple Facebook accounts
- **Post Management**: Create, edit, and schedule marketplace posts
- **Bulk Upload**: Upload multiple posts via CSV
- **Responsive Design**: Mobile-friendly interface
- **Protected Routes**: Secure dashboard pages

## 🛠️ Tech Stack

- **Next.js 14** (App Router)
- **TypeScript**
- **Tailwind CSS**
- **React Hook Form** + **Zod** (Form validation)
- **Axios** (API calls)
- **Lucide React** (Icons)

## 📋 Prerequisites

- Node.js 18+ installed
- Backend API running (Django backend on port 8000)

## 🔧 Installation

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Create environment file**:
   ```bash
   cp .env.local.example .env.local
   ```

3. **Update `.env.local`** with your backend API URL:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000/api
   ```

## 🚀 Running the Application

### Development Mode
```bash
npm run dev
```

Visit: http://localhost:3000

### Production Build
```bash
npm run build
npm start
```

## 📁 Project Structure

```
frontend/
├── app/
│   ├── dashboard/          # Dashboard pages (protected)
│   │   ├── layout.tsx      # Dashboard layout with sidebar
│   │   ├── page.tsx        # Dashboard home
│   │   ├── accounts/       # Account management (TODO)
│   │   ├── posts/          # Post management (TODO)
│   │   ├── bulk-upload/    # Bulk upload interface (TODO)
│   │   ├── analytics/      # Analytics page (TODO)
│   │   └── settings/       # Settings page (TODO)
│   ├── login/
│   │   └── page.tsx        # Login page
│   ├── signup/
│   │   └── page.tsx        # Signup page
│   ├── layout.tsx          # Root layout with AuthProvider
│   ├── page.tsx            # Landing page
│   └── globals.css         # Global styles
├── components/
│   └── ui/                 # Reusable UI components
│       ├── Button.tsx
│       ├── Input.tsx
│       ├── Card.tsx
│       ├── Toast.tsx
│       └── Sidebar.tsx
├── context/
│   └── AuthContext.tsx     # Authentication context
├── hooks/
│   └── useAuth.ts          # Auth hook
├── lib/
│   ├── api.ts              # API client & endpoints
│   └── utils.ts            # Utility functions
└── types/
    └── index.ts            # TypeScript types
```

## 🔐 Authentication Flow

1. User signs up or logs in
2. Backend returns JWT token
3. Token stored in `localStorage`
4. Token sent with every API request
5. Protected routes check authentication
6. Token validated on backend

## 🎨 Pages

### Public Pages
- **/** - Landing page with features and CTA
- **/login** - User login
- **/signup** - User registration

### Protected Pages (Dashboard)
- **/dashboard** - Overview with stats
- **/dashboard/accounts** - Manage Facebook accounts (TODO)
- **/dashboard/posts** - View and manage posts (TODO)
- **/dashboard/bulk-upload** - Bulk upload interface (TODO)
- **/dashboard/analytics** - Analytics and reports (TODO)
- **/dashboard/settings** - User settings (TODO)

## 🔄 API Integration

The frontend connects to the Django backend API. Update the API URL in `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

### API Endpoints Used
- `POST /api/auth/login/` - User login
- `POST /api/auth/signup/` - User registration
- `GET /api/auth/profile/` - Get user profile
- `GET /api/accounts/` - List Facebook accounts
- `POST /api/accounts/` - Create account
- `GET /api/posts/` - List marketplace posts
- `POST /api/posts/` - Create post
- `GET /api/stats/dashboard/` - Dashboard statistics

## 🎯 Next Steps (TODO)

### Immediate Tasks
1. **Create Account Management Page** (`/dashboard/accounts`)
   - List all Facebook accounts
   - Add new account form
   - Delete account functionality
   - Session status indicator

2. **Create Post Management Page** (`/dashboard/posts`)
   - List all posts with filters
   - Create new post form
   - Edit/delete posts
   - Post status tracking

3. **Create Bulk Upload Page** (`/dashboard/bulk-upload`)
   - CSV file upload
   - Account selection
   - Upload progress
   - Error handling

4. **Create Analytics Page** (`/dashboard/analytics`)
   - Charts and graphs
   - Success rate metrics
   - Account performance
   - Export reports

5. **Create Settings Page** (`/dashboard/settings`)
   - User profile management
   - Password change
   - API key management
   - Notification preferences

### Backend Requirements
The Django backend needs to implement REST API endpoints for:
- User authentication (JWT tokens)
- CRUD operations for accounts and posts
- Stats/analytics endpoints
- Bulk upload handling

## 🎨 Styling

The app uses Tailwind CSS with custom components. Color scheme:
- Primary: Blue (`blue-600`)
- Success: Green (`green-600`)
- Warning: Yellow (`yellow-600`)
- Error: Red (`red-600`)

## 📱 Responsive Design

- Mobile-first approach
- Sidebar collapses on mobile
- Responsive grid layouts
- Touch-friendly buttons

## 🔒 Security

- JWT tokens for authentication
- Protected routes with redirect
- HTTPS in production (recommended)
- XSS protection with React
- CSRF tokens (handled by Django backend)

## 🐛 Troubleshooting

### API Connection Issues
```bash
# Check if backend is running
curl http://localhost:8000/api/

# Check CORS settings in Django backend
```

### Build Errors
```bash
# Clear cache and rebuild
rm -rf .next node_modules
npm install
npm run dev
```

## 📄 License

MIT

## 👥 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 📞 Support

For issues and questions, please open an issue on GitHub.
