import type { PropsWithChildren } from 'react'
import { Navigate } from 'react-router'

import { getToken } from '../services/auth'

export function ProtectedRoute({ children }: PropsWithChildren) {
  if (!getToken()) {
    return <Navigate to="/login" replace />
  }

  return children
}