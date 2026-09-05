import { Link } from 'react-router'
import {
  Boxes,
  Package,
  Tags,
  Warehouse,
} from 'lucide-react'

import './DashboardPage.css'

export function DashboardPage() {
  return (
    <div className="page">
      <div className="page-header">
        <h1>Painel</h1>
        <p>Acompanhe as principais informações da loja.</p>
      </div>

      <section className="dashboard-welcome">
        <div>
          <h2>Bem-vindo ao Estoque Bruna Essence</h2>
          <p>
            Gerencie o catálogo e acompanhe o estoque da loja em um só lugar.
          </p>
        </div>

        <div className="dashboard-welcome-icon">
          <Boxes size={26} />
        </div>
      </section>

      <h2 className="dashboard-section-title">Acesso rápido</h2>

      <section className="dashboard-shortcuts">
        <Link to="/categories" className="dashboard-shortcut">
          <div className="dashboard-shortcut-icon">
            <Tags size={21} />
          </div>

          <div>
            <strong>Categorias</strong>
            <small>Organize as categorias da loja</small>
          </div>
        </Link>

        <Link to="/products" className="dashboard-shortcut">
          <div className="dashboard-shortcut-icon">
            <Package size={21} />
          </div>

          <div>
            <strong>Produtos</strong>
            <small>Cadastre e consulte produtos</small>
          </div>
        </Link>

        <Link to="/stock" className="dashboard-shortcut">
          <div className="dashboard-shortcut-icon">
            <Warehouse size={21} />
          </div>

          <div>
            <strong>Estoque</strong>
            <small>Consulte os saldos disponíveis</small>
          </div>
        </Link>
      </section>
    </div>
  )
}