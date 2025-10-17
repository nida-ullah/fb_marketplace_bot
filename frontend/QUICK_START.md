# 🚀 Quick Start Guide

## Setup Instructions

### 1. Copy Environment File
```bash
cp .env.local.example .env.local
```

### 2. Start Development Server
```bash
npm run dev
```

### 3. Open Browser
Navigate to: http://localhost:3000

## 🎯 What You'll See

### Landing Page (/)
- Hero section with features
- Call-to-action buttons
- Professional design

### Login Page (/login)
- Email/password form
- Form validation
- Error handling

### Signup Page (/signup)
- Registration form
- Password confirmation
- Validation

### Dashboard (/dashboard)
- Protected route (requires login)
- Stats overview
- Quick action cards
- Sidebar navigation

## ⚠️ Important Notes

### Backend Connection
The frontend expects a Django backend API at:
```
http://localhost:8000/api
```

**If backend is not running**, you'll see:
- Login errors (cannot connect)
- Mock data on dashboard (demo mode)

### Mock Mode
The dashboard shows sample data if the backend API is unavailable. This allows you to:
- View the UI design
- Test navigation
- See the layout

## 🔧 Environment Variables

Edit `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

For production:
```env
NEXT_PUBLIC_API_URL=https://your-domain.com/api
```

## 📝 Default Test Account (when backend is ready)

After setting up the Django backend:
```
Email: test@example.com
Password: password123
```

## 🎨 Pages to Explore

1. **/** - Landing page
2. **/login** - Try logging in
3. **/signup** - Create account form
4. **/dashboard** - Main dashboard (requires auth)

## 🐛 Common Issues

### Port Already in Use
```bash
# Kill process on port 3000
npx kill-port 3000

# Or use different port
npm run dev -- -p 3001
```

### Module Not Found
```bash
npm install
```

### API Connection Failed
- Check if Django backend is running on port 8000
- Verify CORS is configured in Django
- Check `.env.local` API URL

## 🎉 Next Steps

After verifying the frontend works:

1. **Set up Django backend API**
   - Create REST API endpoints
   - Configure CORS
   - Implement JWT authentication

2. **Complete TODO pages**
   - Accounts management
   - Posts management
   - Bulk upload
   - Analytics
   - Settings

3. **Connect to real API**
   - Remove mock data
   - Test authentication flow
   - Verify all CRUD operations

## 📚 Learn More

- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [React Hook Form](https://react-hook-form.com/)
- [TypeScript](https://www.typescriptlang.org/)
