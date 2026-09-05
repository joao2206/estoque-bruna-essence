import { useEffect, useState } from 'react'
import { AlertTriangle, Search } from 'lucide-react'

import { listStock } from '../services/stock'
import type { StockItem } from '../types/stock'

import './StockPage.css'

export function StockPage() {
  const [stock, setStock] = useState<StockItem[]>([])
  const [search, setSearch] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    listStock()
      .then(setStock)
      .catch((error) => {
        setError(
          error instanceof Error
            ? error.message
            : 'Não foi possível carregar o estoque.',
        )
      })
      .finally(() => setLoading(false))
  }, [])

  const normalizedSearch = search.trim().toLowerCase()

  const filteredStock = stock.filter((item) => {
    if (!normalizedSearch) {
      return true
    }

    return [
      item.sku,
      item.product_name,
      item.color,
      item.size,
    ].some((value) =>
      value.toLowerCase().includes(normalizedSearch),
    )
  })

  return (
    <div className="page">
      <div className="page-header">
        <h1>Estoque</h1>
        <p>
          Consulte o saldo disponível de cada variação.
        </p>
      </div>

      <section className="table-card">
        <div className="stock-toolbar">
          <div>
            <h2>Posição de estoque</h2>

            {!loading && (
              <span className="stock-count">
                {stock.length}{' '}
                {stock.length === 1 ? 'variação' : 'variações'}
              </span>
            )}
          </div>

          <div className="stock-search">
            <Search size={17} />

            <input
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              placeholder="Buscar produto, SKU, cor..."
            />
          </div>
        </div>

        {error && (
          <div className="stock-error">
            <AlertTriangle size={18} />
            {error}
          </div>
        )}

        {!error && loading ? (
          <p>Carregando estoque...</p>
        ) : !error && filteredStock.length === 0 ? (
          <p>Nenhum item encontrado.</p>
        ) : !error ? (
          <table>
            <thead>
              <tr>
                <th>SKU</th>
                <th>Produto</th>
                <th>Variação</th>
                <th>Saldo</th>
                <th>Mínimo</th>
                <th>Situação</th>
              </tr>
            </thead>

            <tbody>
              {filteredStock.map((item) => (
                <tr key={item.product_variant_id}>
                  <td>
                    <strong className="stock-sku">
                      {item.sku}
                    </strong>
                  </td>

                  <td>{item.product_name}</td>

                  <td>
                    {item.color} / {item.size}
                  </td>

                  <td>
                    <strong>{item.current_stock}</strong>
                  </td>

                  <td>{item.minimum_stock}</td>

                  <td>
                    {item.current_stock === 0 ? (
                      <span className="stock-status stock-empty">
                        Sem estoque
                      </span>
                    ) : item.low_stock ? (
                      <span className="stock-status stock-low">
                        Estoque baixo
                      </span>
                    ) : (
                      <span className="stock-status stock-ok">
                        Normal
                      </span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : null}
      </section>
    </div>
  )
}