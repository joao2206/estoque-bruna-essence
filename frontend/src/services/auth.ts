import type { AuthUser, LoginResponse } from '../types/auth'

const API_URL =
  import.meta.env.VITE_API_URL ?? 'http://127.0.0.1:8000'

const TOKEN_KEY = 'estoque_bruna_token'

export async function login(
  email: string,
  password: string,
): Promise<LoginResponse> {
  const response = await fetch(`${API_URL}/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password }),
  })

  const data = await response.json()

  if (!response.ok) {
    throw new Error(data.detail ?? 'Não foi possível entrar.')
  }

  localStorage.setItem(TOKEN_KEY, data.access_token)

  return data
}

export async function getCurrentUser(): Promise<AuthUser> {
  const token = getToken()

  const response = await fetch(`${API_URL}/auth/me`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })

  if (!response.ok) {
    throw new Error('Sessão inválida ou expirada.')
  }

  return response.json()
}

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY)
}

export function logout(): void {
  localStorage.removeItem(TOKEN_KEY)
}