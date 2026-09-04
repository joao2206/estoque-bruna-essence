export interface ProductVariant {
  id: number
  company_id: number
  product_id: number
  sku: string
  color: string
  size: string
  cost_price: string
  sale_price: string
  minimum_stock: number
  active: boolean
  created_at: string
  updated_at: string
}

export interface ProductVariantCreate {
  product_id: number
  color: string
  size: string
  cost_price: number
  sale_price: number
  minimum_stock: number
}