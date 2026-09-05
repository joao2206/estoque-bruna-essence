import { apiRequest } from './api'
import type { StockItem } from '../types/stock'

export function listStock(): Promise<StockItem[]> {
  return apiRequest<StockItem[]>('/stock')
}