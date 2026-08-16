import { Route, Routes } from 'react-router'
import ReferenceDetails from './features/references/ReferenceDetails'

import Header from './components/Header'
import ReferenceBrowser from './features/references/ReferenceBrowser'
import NotFoundPage from './pages/NotFoundPage'

function App() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <Header />

      <Routes>
        <Route path="/" element={<ReferenceBrowser />} />
        <Route path="/references/:id" element={<ReferenceDetails />} />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </div>
  )
}

export default App
