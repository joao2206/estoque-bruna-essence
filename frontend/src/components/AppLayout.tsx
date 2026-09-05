import { useEffect, useState } from 'react'
import { NavLink, Outlet, useNavigate,} from 'react-router'
import { getCurrentUser, logout,} from '../services/auth'
import type { AuthUser } from '../types/auth'
import { LayoutDashboard, Tags, Package, Warehouse, ShoppingBag, LogOut,} from 'lucide-react'
import './AppLayout.css'

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
            <LayoutDashboard size={18} />
            <span>Painel</span>
        </NavLink>

        <NavLink to="/categories">
            <Tags size={18} />
            <span>Categorias</span>
        </NavLink>

        <NavLink to="/products">
            <Package size={18} />
            <span>Produtos</span>
        </NavLink>

        <span className="disabled-link">
            <Warehouse size={18} />
            <span>Estoque</span>
        </span>

        <span className="disabled-link">
            <ShoppingBag size={18} />
            <span>Vendas</span>
        </span>
        </nav>

        <div className="sidebar-user">
          <div>
            <strong>{user.name}</strong>
            <small>{user.role}</small>
          </div>

          <button onClick={handleLogout}>
            <LogOut size={18} />
            <span>Sair</span>
          </button>
        </div>
      </aside>

      <main className="app-content">
        <Outlet />
      </main>
    </div>
  )
}