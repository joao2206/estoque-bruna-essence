import { apiRequest } from './api'
import type {
  ProductVariant,
  ProductVariantCreate,
} from '../types/productVariant'

export function listProductVariants(
  productId: number,
): Promise<ProductVariant[]> {
  return apiRequest<ProductVariant[]>(
    `/product-variants?product_id=${productId}`,
  )
}

export function createProductVariant(
  variant: ProductVariantCreate,
): Promise<ProductVariant> {
  return apiRequest<ProductVariant>('/product-variants', {
    method: 'POST',
    body: JSON.stringify(variant),
  })
}