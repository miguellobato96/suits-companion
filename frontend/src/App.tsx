import { Route, Routes } from 'react-router'

import Header from './components/Header'
import ReferenceBrowser from './features/references/ReferenceBrowser'
import NotFoundPage from './pages/NotFoundPage'

function App() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <Header />

      <Routes>
        <Route path="/" element={<ReferenceBrowser />} />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </div>
  )
}

export default App
