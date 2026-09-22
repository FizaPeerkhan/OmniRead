import { Link, useLocation } from 'react-router-dom';

export default function Layout({ children }) {
  const location = useLocation();
  return (
    <div className="min-h-screen">
      <header className="border-b border-slate-200 bg-white/90 backdrop-blur">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-5 py-4 sm:px-8">
          <Link to="/" className="flex items-center gap-3" aria-label="OmniRead home">
            <div className="grid h-10 w-10 place-items-center rounded-xl bg-indigo-600 text-lg font-bold text-white shadow-sm">O</div>
            <div>
              <div className="text-lg font-bold tracking-tight">OmniRead</div>
              <div className="text-xs text-slate-500">Complexity Stripped. Clarity Delivered.</div>
            </div>
          </Link>
          {location.pathname !== '/' && (
            <Link to="/analyzer" className="rounded-lg px-3 py-2 text-sm font-medium text-slate-600 hover:bg-slate-100">
              Text Analyzer
            </Link>
          )}
        </div>
      </header>
      <main>{children}</main>
      <footer className="border-t border-slate-200 bg-white">
        <div className="mx-auto max-w-6xl px-5 py-6 text-center text-sm text-slate-500 sm:px-8">
          OmniRead • NLP-powered reading assistance
        </div>
      </footer>
    </div>
  );
}
