import { useEffect, useState } from 'react'
import {
  NavLink,
  Outlet,
  useNavigate,
} from 'react-router'

import {
  getCurrentUser,
  logout,
} from '../services/auth'
import type { AuthUser } from '../types/auth'

export function AppLayout() {
  const navigate = useNavigate()
  const [user, setUser] = useState<AuthUser | null>(null)

  useEffect(() => {
    getCurrentUser()
      .then(setUser)
      .catch(() => {
        logout()
        navigate('/login')
      })
  }, [navigate])

  function handleLogout() {
    logout()
    navigate('/login')
  }

  if (!user) {
    return <div className="loading-page">Carregando...</div>
  }

  return (
    <div className="app-layout">
      <aside className="sidebar">
        <div className="sidebar-brand">
          <span>BE</span>

          <div>
            <strong>Bruna Essence</strong>
            <small>Controle de estoque</small>
          </div>
        </div>

        <nav>
          <NavLink to="/" end>
            Painel
          </NavLink>

          <NavLink to="/categories">
            Categorias
          </NavLink>

          <NavLink to="/products">
            Produtos
          </NavLink>
          <span className="disabled-link">Estoque</span>
          <span className="disabled-link">Vendas</span>
        </nav>

        <div className="sidebar-user">
          <div>
            <strong>{user.name}</strong>
            <small>{user.role}</small>
          </div>

          <button onClick={handleLogout}>Sair</button>
        </div>
      </aside>

      <main className="app-content">
        <Outlet />
      </main>
    </div>
  )
}