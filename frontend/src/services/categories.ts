import { apiRequest } from './api'
import type { Category } from '../types/category'

export function listCategories(): Promise<Category[]> {
  return apiRequest<Category[]>('/categories')
}

export function createCategory(name: string): Promise<Category> {
  return apiRequest<Category>('/categories', {
    method: 'POST',
    body: JSON.stringify({ name }),
  })
}