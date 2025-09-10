# Forewarn IBF Portal

A production-ready admin dashboard built with Next.js, designed for managing users and displaying various data insights with role-based access control.

## 🎯 Project Overview

This is an admin portal dashboard that provides:
- **User Management System**: Login, Registration, Password Reset
- **Role-Based Authorization**: SuperAdmin, Admin, Manager, Normal User roles
- **Data Dashboard**: Multiple menus with different status views and analytics
- **Responsive Design**: Built with Tailwind CSS for all screen sizes

## 🛠️ Tech Stack

- **Frontend**: Next.js 15 with App Router
- **Backend**: Next.js API Routes + Server Actions
- **Language**: TypeScript
- **Styling**: Tailwind CSS v4 (CSS-based configuration)
- **UI Components**: Shadcn/ui (headless component library)
- **Icons**: Lucide React
- **Linting**: ESLint
- **Database**: PostgreSQL (recommended) or MySQL
- **ORM**: Prisma (planned)
- **Authentication**: NextAuth.js (planned)
- **Deployment**: Vercel (frontend + backend)

## 🚀 Development Roadmap

### Phase 1: Foundation ✅
- [x] Next.js project setup with TypeScript
- [x] Project structure with App Router
- [x] Tailwind CSS v4 configuration (CSS-based)
- [x] Shadcn/ui component library integration
- [x] Basic header component with responsive design
- [x] Logo component with FOREWARN IBF branding

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

### Prerequisites

- Node.js 18+ 
- npm, yarn, pnpm, or bun

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd forewarn-ibf-portal
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:

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
├── app/                    # App Router pages and layouts
│   ├── layout.tsx         # Root layout with header integration
│   ├── page.tsx           # Home page with feature cards
│   ├── globals.css        # Global styles with Tailwind v4 and theme variables
│   └── favicon.ico        # App icon
├── components/            # Reusable UI components
│   ├── layout/           # Layout-specific components
│   │   ├── Header.tsx    # Main navigation header with Shadcn/ui
│   │   └── Logo.tsx      # FOREWARN IBF logo component
│   └── ui/               # Shadcn/ui components
│       ├── avatar.tsx    # User avatar component
│       ├── badge.tsx     # Status badge component
│       ├── button.tsx    # Button component with variants
│       ├── card.tsx      # Card layout component
│       ├── dropdown-menu.tsx # Dropdown menu component
│       ├── input.tsx     # Form input component
│       ├── sheet.tsx     # Slide-out panel component
│       └── table.tsx     # Data table component
├── lib/                  # Utility functions and configurations
│   └── utils.ts          # Utility functions (clsx, tailwind-merge)
└── types/                # TypeScript type definitions (planned)
```

### Key Features Implemented

- **Responsive Header**: Navigation with search, notifications, and user menu
- **Component Library**: Shadcn/ui components with consistent theming
- **Dark Mode Support**: CSS variables for light/dark theme switching
- **Modern Styling**: Tailwind CSS v4 with CSS-based configuration

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

## 🎨 Styling & Components

### Tailwind CSS v4
This project uses the latest Tailwind CSS v4 with **CSS-based configuration**. Unlike previous versions, there's no `tailwind.config.js` file. Instead, configuration is handled through CSS using the `@theme` directive in `globals.css`.

### Shadcn/ui Integration
We've successfully integrated Shadcn/ui with Tailwind CSS v4, proving compatibility between these cutting-edge technologies. The component library provides:
- Consistent design system with CSS variables
- Accessible components built on Radix UI
- Full TypeScript support
- Customizable theming with light/dark mode support

### Available Components
- Avatar with fallback support
- Badges for status indicators  
- Buttons with multiple variants
- Cards for content layout
- Dropdown menus with keyboard navigation
- Form inputs with validation styles
- Data tables with sorting
- Slide-out sheets for modals

## 📚 Learn More

To learn more about the technologies used in this project:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial
- [Tailwind CSS v4 Documentation](https://tailwindcss.com/docs/v4-beta) - utility-first CSS framework with CSS-based configuration
- [Shadcn/ui Documentation](https://ui.shadcn.com/) - beautifully designed component library
- [Lucide React Icons](https://lucide.dev/) - beautiful & consistent icon toolkit
- [TypeScript Documentation](https://www.typescriptlang.org/docs/) - typed JavaScript

## 🚀 Deployment

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.

## 📝 Development Notes

This README will be updated as we progress through development phases. Each major feature addition or architectural change will be documented here to maintain project clarity and help with onboarding new team members.
