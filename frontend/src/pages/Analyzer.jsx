import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Layout from '../components/Layout';
import StateMessage from '../components/StateMessage';
import { analyzeText } from '../lib/api';

export default function Analyzer() {
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  async function handleAnalyze() {
    const value = text.trim();
    setError('');
    if (!value) {
      setError('Please enter or paste some text before analyzing.');
      return;
    }
    setLoading(true);
    try {
      const result = await analyzeText(value);
      navigate('/results', { state: { text: value, analysis: result } });
    } catch (err) {
      const message = err.response?.data?.detail || err.message || 'Unable to connect to the OmniRead backend.';
      setError(`Analysis failed: ${message}`);
    } finally {
      setLoading(false);
    }
  }

  return (
    <Layout>
      <section className="mx-auto max-w-5xl px-5 py-10 sm:px-8 sm:py-16">
        <div className="mb-8">
          <p className="text-sm font-semibold uppercase tracking-wider text-indigo-600">Text Analyzer</p>
          <h1 className="mt-2 text-3xl font-bold tracking-tight sm:text-4xl">Understand your text</h1>
          <p className="mt-3 max-w-2xl text-slate-600">Paste a passage below and OmniRead will analyze readability, statistics, difficult words and complex sentences.</p>
        </div>

        {error && <div className="mb-5"><StateMessage type="error" title="Something went wrong">{error}</StateMessage></div>}

        <div className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm sm:p-7">
          <label htmlFor="text-input" className="text-sm font-semibold text-slate-700">Text to analyze</label>
          <textarea
            id="text-input"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Paste or type your text here..."
            className="mt-3 min-h-[340px] w-full resize-y rounded-2xl border border-slate-200 bg-slate-50 p-5 text-base leading-7 text-slate-800 outline-none transition focus:border-indigo-400 focus:bg-white focus:ring-4 focus:ring-indigo-100"
            aria-describedby="text-help"
          />
          <div className="mt-3 flex flex-col justify-between gap-3 sm:flex-row sm:items-center">
            <p id="text-help" className="text-sm text-slate-500">{text.length.toLocaleString()} characters</p>
            <button
              type="button"
              onClick={handleAnalyze}
              disabled={loading}
              className="rounded-xl bg-indigo-600 px-6 py-3 font-semibold text-white transition hover:bg-indigo-700 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {loading ? 'Analyzing…' : 'Analyze Text'}
            </button>
          </div>
        </div>
      </section>
    </Layout>
  );
}
