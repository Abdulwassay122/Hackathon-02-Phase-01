// src/app/layout.tsx
import type { Metadata } from 'next'
import '../styles/globals.css'
import { AuthProvider } from '../context/AuthContext'
import ToastComponent from '../components/Toast'
import ErrorBoundary from '../components/ErrorBoundary'

export const metadata: Metadata = {
  title: 'Todo App',
  description: 'A full-stack todo application',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <ErrorBoundary>
          <AuthProvider>
            {children}
            <ToastComponent />
          </AuthProvider>
        </ErrorBoundary>
      </body>
    </html>
  )
}