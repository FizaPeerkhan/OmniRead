import { Navigate, Route, Routes } from 'react-router-dom';
import Home from './pages/Home';
import Analyzer from './pages/Analyzer';
import Results from './pages/Results';

export default function App() {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/analyzer" element={<Analyzer />} />
        <Route path="/results" element={<Results />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </div>
  );
}
