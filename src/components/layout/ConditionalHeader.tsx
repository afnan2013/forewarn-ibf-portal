'use client'

import { usePathname } from 'next/navigation'
import Header from './Header'

export default function ConditionalHeader() {
  const pathname = usePathname()
  
  // Don't show header on auth pages
  const isAuthPage = pathname?.includes('/login') || pathname?.includes('/register')
  
  if (isAuthPage) {
    return null
  }
  
  return <Header />
}
