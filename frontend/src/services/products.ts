import { apiRequest } from './api'
import type {
  Product,
  ProductCreate,
} from '../types/product'

export function listProducts(): Promise<Product[]> {
  return apiRequest<Product[]>('/products')
}

export function createProduct(
  product: ProductCreate,
): Promise<Product> {
  return apiRequest<Product>('/products', {
    method: 'POST',
    body: JSON.stringify(product),
  })
}

export function getProduct(productId: number): Promise<Product> {
  return apiRequest<Product>(`/products/${productId}`)
}