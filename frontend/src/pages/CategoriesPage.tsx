import { useEffect, useState } from 'react'
import type { FormEvent } from 'react'

import {
  createCategory,
  listCategories,
} from '../services/categories'
import type { Category } from '../types/category'
import { Plus, Tags } from 'lucide-react'
import './CategoriesPage.css'

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
        <h1>Categorias</h1>
        <p>Organize os produtos por categoria.</p>
        </div>

        <section className="category-form-card">
        <div className="category-card-header">
            <div className="category-card-icon">
            <Tags size={20} />
            </div>

            <div>
            <h2>Nova categoria</h2>
            <p>Crie uma categoria para organizar seus produtos.</p>
            </div>
        </div>

        <form className="category-form" onSubmit={handleSubmit}>
            <div className="category-field">
            <label htmlFor="category-name">Nome da categoria</label>

            <input
                id="category-name"
                value={name}
                onChange={(event) => setName(event.target.value)}
                placeholder="Ex.: Fitness"
                maxLength={100}
            />
            </div>

            <button disabled={saving}>
            <Plus size={18} />
            {saving ? 'Salvando...' : 'Adicionar'}
            </button>
        </form>

        {error && <div className="form-error">{error}</div>}
        </section>

        <section className="table-card">
        <div className="category-list-header">
            <h2>Categorias cadastradas</h2>

            {!loading && (
            <span className="category-count">
                {categories.length}
            </span>
            )}
        </div>

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