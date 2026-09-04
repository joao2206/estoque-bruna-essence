import { useEffect, useState } from 'react'
import type { FormEvent } from 'react'
import { Link, useParams } from 'react-router'

import {
  createProductVariant,
  listProductVariants,
} from '../services/productVariants'
import { getProduct } from '../services/products'
import type { Product } from '../types/product'
import type { ProductVariant } from '../types/productVariant'

const currencyFormatter = new Intl.NumberFormat('pt-BR', {
  style: 'currency',
  currency: 'BRL',
})

export function ProductVariantsPage() {
  const { productId } = useParams()
  const numericProductId = Number(productId)
  const invalidProductId =
    !Number.isInteger(numericProductId) || numericProductId <= 0

  const [product, setProduct] = useState<Product | null>(null)
  const [variants, setVariants] = useState<ProductVariant[]>([])

  const [color, setColor] = useState('')
  const [size, setSize] = useState('')
  const [costPrice, setCostPrice] = useState('')
  const [salePrice, setSalePrice] = useState('')
  const [minimumStock, setMinimumStock] = useState('0')

  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    if (invalidProductId) {
        return
    }

    Promise.all([
        getProduct(numericProductId),
        listProductVariants(numericProductId),
    ])
        .then(([productResponse, variantsResponse]) => {
        setProduct(productResponse)
        setVariants(variantsResponse)
        })
        .catch((error) => {
        setError(
            error instanceof Error
            ? error.message
            : 'Não foi possível carregar o produto.',
        )
        })
        .finally(() => setLoading(false))
    }, [numericProductId, invalidProductId])

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setError('')
    setSaving(true)

    try {
      const variant = await createProductVariant({
        product_id: numericProductId,
        color: color.trim(),
        size: size.trim(),
        cost_price: Number(costPrice),
        sale_price: Number(salePrice),
        minimum_stock: Number(minimumStock),
      })

      setVariants((current) =>
        [...current, variant].sort((a, b) =>
          `${a.color}-${a.size}`.localeCompare(
            `${b.color}-${b.size}`,
          ),
        ),
      )

      setColor('')
      setSize('')
      setCostPrice('')
      setSalePrice('')
      setMinimumStock('0')
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : 'Não foi possível cadastrar a variação.',
      )
    } finally {
      setSaving(false)
    }
  }

  if (invalidProductId) {
    return (
        <div className="page">
        <Link className="back-link" to="/products">
            ← Voltar para produtos
        </Link>

        <div className="form-error">
            Produto inválido.
        </div>
        </div>
    )
  }

  if (loading) {
    return <div className="loading-page">Carregando...</div>
  }

  return (
    <div className="page">
      <Link className="back-link" to="/products">
        ← Voltar para produtos
      </Link>

      <div className="page-header">
        <div>
          <h1>Variações</h1>
          <p>{product?.name ?? 'Produto não encontrado'}</p>
        </div>
      </div>

      <section className="product-form-card">
        <h2>Nova variação</h2>

        <form onSubmit={handleSubmit}>
          <div className="form-field">
            <label htmlFor="variant-color">Cor</label>
            <input
              id="variant-color"
              value={color}
              onChange={(event) => setColor(event.target.value)}
              placeholder="Ex.: Preto"
              required
            />
          </div>

          <div className="form-field">
            <label htmlFor="variant-size">Tamanho</label>
            <input
              id="variant-size"
              value={size}
              onChange={(event) => setSize(event.target.value)}
              placeholder="Ex.: M"
              required
            />
          </div>

          <div className="form-field">
            <label htmlFor="cost-price">Preço de custo</label>
            <input
              id="cost-price"
              type="number"
              min="0"
              step="0.01"
              value={costPrice}
              onChange={(event) => setCostPrice(event.target.value)}
              placeholder="0,00"
              required
            />
          </div>

          <div className="form-field">
            <label htmlFor="sale-price">Preço de venda</label>
            <input
              id="sale-price"
              type="number"
              min="0"
              step="0.01"
              value={salePrice}
              onChange={(event) => setSalePrice(event.target.value)}
              placeholder="0,00"
              required
            />
          </div>

          <div className="form-field">
            <label htmlFor="minimum-stock">Estoque mínimo</label>
            <input
              id="minimum-stock"
              type="number"
              min="0"
              step="1"
              value={minimumStock}
              onChange={(event) =>
                setMinimumStock(event.target.value)
              }
              required
            />
          </div>

          {error && (
            <div className="form-error full-width">{error}</div>
          )}

          <div className="form-actions full-width">
            <button disabled={saving}>
              {saving ? 'Salvando...' : 'Cadastrar variação'}
            </button>
          </div>
        </form>
      </section>

      <section className="table-card">
        <div className="table-toolbar">
          <h2>Variações cadastradas</h2>
        </div>

        {variants.length === 0 ? (
          <p>Nenhuma variação cadastrada.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>SKU</th>
                <th>Cor</th>
                <th>Tamanho</th>
                <th>Custo</th>
                <th>Venda</th>
                <th>Mínimo</th>
              </tr>
            </thead>

            <tbody>
              {variants.map((variant) => (
                <tr key={variant.id}>
                  <td><strong>{variant.sku}</strong></td>
                  <td>{variant.color}</td>
                  <td>{variant.size}</td>
                  <td>
                    {currencyFormatter.format(
                      Number(variant.cost_price),
                    )}
                  </td>
                  <td>
                    {currencyFormatter.format(
                      Number(variant.sale_price),
                    )}
                  </td>
                  <td>{variant.minimum_stock}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>
    </div>
  )
}