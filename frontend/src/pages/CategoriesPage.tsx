import { useEffect, useState } from 'react'
import type { FormEvent } from 'react'

import {
  createCategory,
  listCategories,
} from '../services/categories'
import type { Category } from '../types/category'

export function CategoriesPage() {
  const [categories, setCategories] = useState<Category[]>([])
  const [name, setName] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    listCategories()
      .then(setCategories)
      .catch((error) => setError(error.message))
      .finally(() => setLoading(false))
  }, [])

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()

    if (!name.trim()) {
      return
    }

    setError('')
    setSaving(true)

    try {
      const category = await createCategory(name.trim())

      setCategories((current) =>
        [...current, category].sort((a, b) =>
          a.name.localeCompare(b.name),
        ),
      )

      setName('')
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : 'Não foi possível cadastrar a categoria.',
      )
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1>Categorias</h1>
          <p>Organize os produtos por categoria.</p>
        </div>
      </div>

      <section className="category-form-card">
        <form onSubmit={handleSubmit}>
          <div>
            <label htmlFor="category-name">
              Nova categoria
            </label>

            <input
              id="category-name"
              value={name}
              onChange={(event) => setName(event.target.value)}
              placeholder="Ex.: Fitness"
              maxLength={100}
            />
          </div>

          <button disabled={saving}>
            {saving ? 'Salvando...' : 'Adicionar'}
          </button>
        </form>

        {error && <div className="form-error">{error}</div>}
      </section>

      <section className="table-card">
        {loading ? (
          <p>Carregando categorias...</p>
        ) : categories.length === 0 ? (
          <p>Nenhuma categoria cadastrada.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Nome</th>
                <th>Status</th>
              </tr>
            </thead>

            <tbody>
              {categories.map((category) => (
                <tr key={category.id}>
                  <td>{category.name}</td>
                  <td>
                    <span className="status-active">Ativa</span>
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