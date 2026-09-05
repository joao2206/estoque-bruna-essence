export interface StockItem {
  product_variant_id: number
  sku: string
  product_name: string
  color: string
  size: string
  current_stock: number
  minimum_stock: number
  low_stock: boolean
}