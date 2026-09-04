import { getToken, logout } from './auth'

const API_URL =
  import.meta.env.VITE_API_URL ?? 'http://127.0.0.1:8000'

export async function apiRequest<T>(
  path: string,
  options: RequestInit = {},
): Promise<T> {
  const headers = new Headers(options.headers)
  const token = getToken()

  if (token) {
    headers.set('Authorization', `Bearer ${token}`)
  }

  if (options.body) {
    headers.set('Content-Type', 'application/json')
  }

  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers,
  })

  if (response.status === 401) {
    logout()
    window.location.href = '/login'
    throw new Error('Sua sessão expirou.')
  }

  const data = await response.json().catch(() => null)

  if (!response.ok) {
    throw new Error(data?.detail ?? 'Ocorreu um erro.')
  }

  return data
}