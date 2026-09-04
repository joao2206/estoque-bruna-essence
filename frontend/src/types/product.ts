export interface Product {
  id: number
  company_id: number
  category_id: number
  name: string
  description: string | null
  brand: string | null
  image_url: string | null
  active: boolean
  created_at: string
  updated_at: string
}

export interface ProductCreate {
  category_id: number
  name: string
  description: string | null
  brand: string | null
  image_url: string | null
}