import { useEffect, useState } from 'react'

function App() {
  const [status, setStatus] = useState('Conectando...')

  useEffect(() => {
    fetch('http://127.0.0.1:8000/health')
      .then((response) => response.json())
      .then((data) => {
        setStatus(data.status)
      })
      .catch(() => {
        setStatus('Erro ao conectar com a API')
      })
  }, [])

  return (
    <main>
      <h1>Estoque Bruna Essence</h1>

      <p>
        Status da API: <strong>{status}</strong>
      </p>
    </main>
  )
}

export default App