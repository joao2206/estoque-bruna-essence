export interface LoginResponse {
  access_token: string
  token_type: string
}

export interface AuthUser {
  id: number
  company_id: number
  name: string
  email: string
  role: string
  active: boolean
}