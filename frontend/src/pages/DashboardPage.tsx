export function DashboardPage() {
  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1>Painel</h1>
          <p>Acompanhe as principais informações da loja.</p>
        </div>
      </div>

      <section className="welcome-card">
        <h2>Bem-vindo ao Estoque Bruna Essence</h2>
        <p>
          Categorias, produtos e usuários já estão conectados
          ao PostgreSQL.
        </p>
      </section>
    </div>
  )
}