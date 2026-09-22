import { useEffect, useMemo, useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import Layout from '../components/Layout';
import MetricCard from '../components/MetricCard';
import StateMessage from '../components/StateMessage';
import DifficultWordText from '../components/DifficultWordText';
import { simplifyText } from '../lib/api';

function formatReadingTime(seconds) {
  const value = Number(seconds);
  if (!Number.isFinite(value)) return '—';
  if (value < 60) return `${Math.round(value)} sec`;
  return `${Math.floor(value / 60)} min ${Math.round(value % 60)} sec`;
}

function prettyKey(key) {
  return key.replaceAll('_', ' ').replace(/\b\w/g, (c) => c.toUpperCase());
}

export default function Results() {
  const { state } = useLocation();
  const navigate = useNavigate();
  const text = state?.text || '';
  const analysis = state?.analysis;
  const [selectedWord, setSelectedWord] = useState(null);
  const [simplified, setSimplified] = useState(null);
  const [simplifyLoading, setSimplifyLoading] = useState(false);
  const [simplifyError, setSimplifyError] = useState('');
  const [speaking, setSpeaking] = useState(false);

  useEffect(() => {
    if (!analysis || !text) navigate('/analyzer', { replace: true });
  }, [analysis, text, navigate]);

  useEffect(() => () => window.speechSynthesis?.cancel(), []);

  const readability = analysis?.readability || {};
  const stats = analysis?.statistics || {};
  const difficultWords = Array.isArray(analysis?.difficult_words) ? analysis.difficult_words : [];
  const complexSentences = Array.isArray(analysis?.complex_sentences) ? analysis.complex_sentences : [];

  const readabilityMetrics = useMemo(() => Object.entries(readability).filter(([key]) => key !== 'difficulty' && key !== 'reading_time_seconds'), [readability]);

  async function handleSimplify() {
    setSimplifyError('');
    setSimplifyLoading(true);
    try {
      const result = await simplifyText(text);
      setSimplified(result);
    } catch (err) {
      const message = err.response?.data?.detail || err.message || 'Unable to connect to the simplification endpoint.';
      setSimplifyError(`Simplification failed: ${message}`);
    } finally {
      setSimplifyLoading(false);
    }
  }

  function stopSpeech() {
    window.speechSynthesis?.cancel();
    setSpeaking(false);
  }

  function playSpeech() {
    if (!simplified?.simplified_text || !('speechSynthesis' in window)) return;
    stopSpeech();
    const utterance = new SpeechSynthesisUtterance(simplified.simplified_text);
    utterance.onend = () => setSpeaking(false);
    utterance.onerror = () => setSpeaking(false);
    window.speechSynthesis.speak(utterance);
    setSpeaking(true);
  }

  function pauseSpeech() {
    if ('speechSynthesis' in window) window.speechSynthesis.pause();
  }

  function resumeSpeech() {
    if ('speechSynthesis' in window) window.speechSynthesis.resume();
  }

  if (!analysis || !text) return null;

  return (
    <Layout>
      <section className="mx-auto max-w-6xl px-5 py-10 sm:px-8 sm:py-14">
        <div className="mb-8 flex flex-col justify-between gap-4 sm:flex-row sm:items-end">
          <div>
            <p className="text-sm font-semibold uppercase tracking-wider text-indigo-600">Results Dashboard</p>
            <h1 className="mt-2 text-3xl font-bold tracking-tight sm:text-4xl">Your text analysis</h1>
          </div>
          <Link to="/analyzer" className="text-sm font-semibold text-indigo-600 hover:text-indigo-800">Analyze another text →</Link>
        </div>

        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <MetricCard label="Overall difficulty" value={readability.difficulty} hint="Calculated by the backend" />
          <MetricCard label="Words" value={stats.word_count} />
          <MetricCard label="Sentences" value={stats.sentence_count} />
          <MetricCard label="Reading time" value={formatReadingTime(readability.reading_time_seconds)} />
        </div>

        <div className="mt-6 grid gap-6 lg:grid-cols-[1.5fr_1fr]">
          <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <div className="mb-5 flex items-center justify-between gap-4">
              <div><h2 className="text-xl font-bold">Difficult words</h2><p className="mt-1 text-sm text-slate-500">Select a highlighted word for its returned analysis.</p></div>
              <span className="rounded-full bg-amber-50 px-3 py-1 text-sm font-semibold text-amber-700">{difficultWords.length}</span>
            </div>
            <div className="rounded-2xl bg-slate-50 p-5">
              <DifficultWordText text={text} difficultWords={difficultWords} onSelect={setSelectedWord} />
            </div>
            {selectedWord ? (
              <div className="mt-5 rounded-2xl border border-indigo-100 bg-indigo-50/60 p-5">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <h3 className="text-lg font-bold text-indigo-950">{selectedWord.word}</h3>
                  <span className="rounded-full bg-white px-3 py-1 text-xs font-semibold text-indigo-700">{selectedWord.difficulty_level || 'Unknown'} • score {selectedWord.difficulty_score ?? '—'}</span>
                </div>
                <dl className="mt-4 grid gap-3 text-sm sm:grid-cols-2">
                  <div><dt className="font-semibold text-slate-500">Lemma</dt><dd className="mt-1 text-slate-800">{selectedWord.lemma || '—'}</dd></div>
                  <div><dt className="font-semibold text-slate-500">Replacement</dt><dd className="mt-1 text-slate-800">{selectedWord.replacement || 'No replacement returned'}</dd></div>
                  <div><dt className="font-semibold text-slate-500">Zipf frequency</dt><dd className="mt-1 text-slate-800">{selectedWord.zipf_frequency ?? '—'}</dd></div>
                  <div><dt className="font-semibold text-slate-500">Syllables</dt><dd className="mt-1 text-slate-800">{selectedWord.syllables ?? '—'}</dd></div>
                </dl>
                {Array.isArray(selectedWord.reasons) && selectedWord.reasons.length > 0 && (
                  <div className="mt-4"><p className="text-sm font-semibold text-slate-500">Reasons</p><div className="mt-2 flex flex-wrap gap-2">{selectedWord.reasons.map((reason) => <span key={reason} className="rounded-full bg-white px-3 py-1 text-xs text-slate-700">{reason}</span>)}</div></div>
                )}
              </div>
            ) : difficultWords.length > 0 ? <p className="mt-4 text-sm text-slate-500">Choose a highlighted word above to inspect its difficulty details.</p> : <p className="mt-4 text-sm text-slate-500">No difficult words were returned for this text.</p>}
          </section>

          <section className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="text-xl font-bold">Text statistics</h2>
            <div className="mt-5 divide-y divide-slate-100">
              {Object.entries(stats).map(([key, value]) => <div key={key} className="flex items-center justify-between gap-4 py-3 text-sm"><span className="text-slate-500">{prettyKey(key)}</span><span className="font-semibold text-slate-900">{typeof value === 'number' ? value.toLocaleString() : value ?? '—'}</span></div>)}
            </div>
          </section>
        </div>

        <section className="mt-6 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="text-xl font-bold">Readability metrics</h2>
          <div className="mt-5 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
            {readabilityMetrics.map(([key, value]) => <MetricCard key={key} label={prettyKey(key)} value={value} />)}
          </div>
        </section>

        <section className="mt-6 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex items-center justify-between gap-3"><div><h2 className="text-xl font-bold">Complex sentences</h2><p className="mt-1 text-sm text-slate-500">Sentences flagged by the backend analysis.</p></div><span className="rounded-full bg-indigo-50 px-3 py-1 text-sm font-semibold text-indigo-700">{complexSentences.length}</span></div>
          {complexSentences.length ? <div className="mt-5 space-y-4">{complexSentences.map((item, index) => <article key={`${item.sentence}-${index}`} className="rounded-2xl border border-slate-200 p-5"><div className="flex flex-wrap justify-between gap-2"><span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-700">{item.difficulty_level || 'Unknown'} • score {item.difficulty_score ?? '—'}</span><span className="text-xs text-slate-500">{item.word_count ?? '—'} words</span></div><p className="mt-3 leading-7 text-slate-700">{item.sentence}</p>{item.reasons?.length ? <p className="mt-3 text-sm text-slate-500">Reasons: {item.reasons.join(', ')}</p> : null}</article>)}</div> : <p className="mt-5 text-sm text-slate-500">No complex sentences were returned.</p>}
        </section>

        <section className="mt-6 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-center"><div><h2 className="text-xl font-bold">Text simplification</h2></div><button type="button" onClick={handleSimplify} disabled={simplifyLoading} className="rounded-xl bg-indigo-600 px-5 py-3 font-semibold text-white hover:bg-indigo-700 disabled:cursor-not-allowed disabled:opacity-60">{simplifyLoading ? 'Simplifying…' : simplified ? 'Simplify Again' : 'Simplify Text'}</button></div>
          {simplifyError && <div className="mt-5"><StateMessage type="error" title="Simplification unavailable">{simplifyError}</StateMessage></div>}
          {simplified && <div className="mt-6 grid gap-5 lg:grid-cols-2"><div className="rounded-2xl bg-slate-50 p-5"><p className="text-sm font-semibold text-slate-500">Original text</p><p className="reading-text mt-3 whitespace-pre-wrap text-slate-700">{simplified.original_text || text}</p></div><div className="rounded-2xl border border-indigo-100 bg-indigo-50/50 p-5"><p className="text-sm font-semibold text-indigo-700">Simplified text</p><p className="reading-text mt-3 whitespace-pre-wrap text-slate-800">{simplified.simplified_text || 'No simplified text returned.'}</p></div></div>}
          {simplified && <div className="mt-5 grid gap-5 lg:grid-cols-[1fr_auto]"><div><p className="text-sm font-semibold text-slate-600">Word replacements</p><div className="mt-2 flex flex-wrap gap-2">{(simplified.word_replacements || []).filter((item) => item.replacement).map((item, index) => <span key={`${item.word}-${index}`} className="rounded-full bg-slate-100 px-3 py-1.5 text-sm text-slate-700">{item.word} → {item.replacement}</span>)}{!(simplified.word_replacements || []).some((item) => item.replacement) && <span className="text-sm text-slate-500">No replacements returned.</span>}</div></div><div className="rounded-2xl bg-slate-50 p-4 text-sm"><span className="font-semibold">Simplification applied:</span> <span>{simplified.simplification_applied ? 'Yes' : 'No'}</span></div></div>}
          {simplified && <div className="mt-6 border-t border-slate-100 pt-6"><div className="flex flex-wrap gap-3"><button type="button" onClick={playSpeech} disabled={!simplified.simplified_text || !('speechSynthesis' in window)} className="rounded-xl bg-slate-900 px-5 py-3 font-semibold text-white hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-50">▶ Play</button><button type="button" onClick={pauseSpeech} disabled={!speaking} className="rounded-xl border border-slate-200 px-5 py-3 font-semibold text-slate-700 hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-50">Ⅱ Pause</button><button type="button" onClick={resumeSpeech} disabled={!speaking} className="rounded-xl border border-slate-200 px-5 py-3 font-semibold text-slate-700 hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-50">▶ Resume</button><button type="button" onClick={stopSpeech} className="rounded-xl border border-slate-200 px-5 py-3 font-semibold text-slate-700 hover:bg-slate-50">■ Stop</button></div>{!('speechSynthesis' in window) && <p className="mt-3 text-sm text-amber-700">Speech synthesis is not supported by this browser.</p>}</div>}
        </section>
      </section>
    </Layout>
  );
}
