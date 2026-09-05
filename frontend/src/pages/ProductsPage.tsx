import { useEffect, useState } from 'react'
import type { FormEvent } from 'react'

import { listCategories } from '../services/categories'
import {
  createProduct,
  listProducts,
} from '../services/products'
import type { Category } from '../types/category'
import type { Product } from '../types/product'
import { Link } from 'react-router'
import {
  Layers,
  PackagePlus,
  Plus,
  Search,
} from 'lucide-react'

import './ProductsPage.css'

export function ProductsPage() {
  const [products, setProducts] = useState<Product[]>([])
  const [categories, setCategories] = useState<Category[]>([])

  const [categoryId, setCategoryId] = useState('')
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [brand, setBrand] = useState('')
  const [search, setSearch] = useState('')

  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    Promise.all([
      listProducts(),
      listCategories(),
    ])
      .then(([productsResponse, categoriesResponse]) => {
        setProducts(productsResponse)
        setCategories(categoriesResponse)
      })
      .catch((error) => setError(error.message))
      .finally(() => setLoading(false))
  }, [])

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setError('')

    if (!categoryId) {
      setError('Selecione uma categoria.')
      return
    }

    setSaving(true)

    try {
      const product = await createProduct({
        category_id: Number(categoryId),
        name: name.trim(),
        description: description.trim() || null,
        brand: brand.trim() || null,
        image_url: null,
      })

      setProducts((current) =>
        [...current, product].sort((a, b) =>
          a.name.localeCompare(b.name),
        ),
      )

      setCategoryId('')
      setName('')
      setDescription('')
      setBrand('')
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : 'Não foi possível cadastrar o produto.',
      )
    } finally {
      setSaving(false)
    }
  }

  function getCategoryName(categoryId: number) {
    return (
      categories.find((category) => category.id === categoryId)
        ?.name ?? 'Sem categoria'
    )
  }

  const filteredProducts = products.filter((product) =>
    product.name.toLowerCase().includes(search.toLowerCase()),
  )

  return (
    <div className="page">
        <div className="page-header">
        <h1>Produtos</h1>
        <p>Cadastre e organize os produtos comercializados pela loja.</p>
        </div>

        <section className="product-form-card products-form-card">
        <div className="product-card-header">
            <div className="product-card-icon">
            <PackagePlus size={21} />
            </div>

            <div>
            <h2>Novo produto</h2>
            <p>Cadastre um modelo antes de adicionar suas variações.</p>
            </div>
        </div>

        <form className="products-form" onSubmit={handleSubmit}>
            <div className="form-field">
            <label htmlFor="product-name">Nome</label>

            <input
                id="product-name"
                value={name}
                onChange={(event) => setName(event.target.value)}
                placeholder="Ex.: Conjunto Luna"
                minLength={2}
                maxLength={150}
                required
            />
            </div>

            <div className="form-field">
            <label htmlFor="product-category">Categoria</label>

            <select
                id="product-category"
                value={categoryId}
                onChange={(event) => setCategoryId(event.target.value)}
                required
            >
                <option value="">Selecione</option>

                {categories.map((category) => (
                <option key={category.id} value={category.id}>
                    {category.name}
                </option>
                ))}
            </select>
            </div>

            <div className="form-field">
            <label htmlFor="product-brand">Marca</label>

            <input
                id="product-brand"
                value={brand}
                onChange={(event) => setBrand(event.target.value)}
                placeholder="Ex.: Bruna Essence"
                maxLength={100}
            />
            </div>

            <div className="form-field full-width">
            <label htmlFor="product-description">Descrição</label>

            <textarea
                id="product-description"
                value={description}
                onChange={(event) => setDescription(event.target.value)}
                placeholder="Descrição opcional do produto"
                rows={3}
            />
            </div>

            {error && (
            <div className="form-error full-width">
                {error}
            </div>
            )}

            <div className="form-actions full-width">
            <button
                className="product-submit"
                disabled={saving}
            >
                <Plus size={18} />

                {saving ? 'Salvando...' : 'Cadastrar produto'}
            </button>
            </div>
        </form>
        </section>

        <section className="table-card">
        <div className="product-list-header">
            <div className="product-list-title">
            <h2>Produtos cadastrados</h2>

            {!loading && (
                <span className="product-count">
                {filteredProducts.length}
                </span>
            )}
            </div>

            <div className="product-search">
            <Search size={17} />

            <input
                value={search}
                onChange={(event) => setSearch(event.target.value)}
                placeholder="Buscar produto"
            />
            </div>
        </div>

        {loading ? (
            <p>Carregando produtos...</p>
        ) : filteredProducts.length === 0 ? (
            <p>Nenhum produto encontrado.</p>
        ) : (
            <table>
            <thead>
                <tr>
                <th>Produto</th>
                <th>Categoria</th>
                <th>Marca</th>
                <th>Status</th>
                <th>Ações</th>
                </tr>
            </thead>

            <tbody>
                {filteredProducts.map((product) => (
                <tr key={product.id}>
                    <td>
                    <strong>{product.name}</strong>

                    {product.description && (
                        <small className="table-description">
                        {product.description}
                        </small>
                    )}
                    </td>

                    <td>
                    {getCategoryName(product.category_id)}
                    </td>

                    <td>{product.brand ?? '—'}</td>

                    <td>
                    <span className="status-active">
                        Ativo
                    </span>
                    </td>

                    <td>
                    <Link
                        className="product-action"
                        to={`/products/${product.id}/variants`}
                    >
                        <Layers size={15} />
                        Variações
                    </Link>
                    </td>
                </tr>
                ))}
            </tbody>
            </table>
        )}
        </section>
    </div>
    )
}