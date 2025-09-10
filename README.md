# Forewarn IBF Portal

A production-ready admin dashboard built with Next.js, designed for managing users and displaying various data insights with role-based access control.

## 🎯 Project Overview

This is an admin portal dashboard that provides:
- **User Management System**: Login, Registration, Password Reset
- **Role-Based Authorization**: SuperAdmin, Admin, Manager, Normal User roles
- **Data Dashboard**: Multiple menus with different status views and analytics
- **Responsive Design**: Built with Tailwind CSS for all screen sizes

## 🛠️ Tech Stack

- **Frontend**: Next.js 14 with App Router
- **Backend**: Next.js API Routes + Server Actions
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Linting**: ESLint
- **Database**: PostgreSQL (recommended) or MySQL
- **ORM**: Prisma (planned)
- **Authentication**: NextAuth.js (planned)
- **Deployment**: Vercel (frontend + backend)

## 🚀 Development Roadmap

### Phase 1: Foundation ✅
- [x] Next.js project setup with TypeScript
- [x] Project structure with App Router
- [x] Tailwind CSS configuration

### Phase 2: User Management (In Progress)
- [ ] Authentication pages (Login, Register, Forgot Password)
- [ ] User registration flow
- [ ] Password reset functionality
- [ ] Form validation and error handling

### Phase 3: Authorization System
- [ ] Role-based access control
- [ ] User roles: SuperAdmin, Admin, Manager, Normal User
- [ ] Protected routes and middleware
- [ ] Permission-based component rendering

### Phase 4: Dashboard Implementation
- [ ] Dashboard layout with sidebar navigation
- [ ] Multiple data views and status pages
- [ ] Charts and analytics components
- [ ] Real-time data integration

## 🏃‍♂️ Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `src/app/page.tsx`. The page auto-updates as you edit the file.

## 📁 Project Structure

```
src/
├── app/                 # App Router pages and layouts
│   ├── layout.tsx      # Root layout
│   ├── page.tsx        # Home page
│   └── globals.css     # Global styles
├── components/         # Reusable UI components (planned)
├── lib/               # Utility functions and configurations (planned)
└── types/             # TypeScript type definitions (planned)
```

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

## 📚 Learn More

To learn more about Next.js and the technologies used in this project:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial
- [Tailwind CSS Documentation](https://tailwindcss.com/docs) - utility-first CSS framework
- [TypeScript Documentation](https://www.typescriptlang.org/docs/) - typed JavaScript

## 🚀 Deployment

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.

## 📝 Development Notes

This README will be updated as we progress through development phases. Each major feature addition or architectural change will be documented here to maintain project clarity and help with onboarding new team members.
