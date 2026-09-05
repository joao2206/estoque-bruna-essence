import { useState } from 'react'
import type { FormEvent } from 'react'
import { Navigate, useNavigate } from 'react-router'

import { getToken, login } from '../services/auth'

import {
  LockKeyhole,
  LogIn,
  Mail,
} from 'lucide-react'

import './LoginPage.css'

export function LoginPage() {
  const navigate = useNavigate()

  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  if (getToken()) {
    return <Navigate to="/" replace />
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setError('')
    setLoading(true)

    try {
      await login(email, password)
      navigate('/')
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : 'Não foi possível entrar.',
      )
    } finally {
      setLoading(false)
    }
  }

 return (
  <main className="login-page">
    <section className="login-card">
      <div className="login-brand">
        <span>BE</span>
      </div>

      <h1>Estoque Bruna Essence</h1>
      <p>Entre para gerenciar produtos e estoque.</p>

      <form onSubmit={handleSubmit}>
        <label htmlFor="email">E-mail</label>

        <div className="login-input">
          <Mail size={18} />

          <input
            id="email"
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            placeholder="seu@email.com"
            required
          />
        </div>

        <label htmlFor="password">Senha</label>

        <div className="login-input">
          <LockKeyhole size={18} />

          <input
            id="password"
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            placeholder="Digite sua senha"
            required
          />
        </div>

        {error && (
          <div className="login-error">
            {error}
          </div>
        )}

        <button
          className="login-button"
          type="submit"
          disabled={loading}
        >
          <LogIn size={18} />

          {loading ? 'Entrando...' : 'Entrar'}
        </button>
      </form>
    </section>
  </main>
)
}