import { Link } from 'react-router-dom';
import Layout from '../components/Layout';

export default function Home() {
  return (
    <Layout>
      <section className="mx-auto max-w-6xl px-5 py-16 sm:px-8 sm:py-24">
        <div className="max-w-3xl">
          <div className="mb-5 inline-flex rounded-full border border-indigo-100 bg-indigo-50 px-3 py-1 text-sm font-medium text-indigo-700">
            Reading assistance through NLP
          </div>
          <h1 className="text-5xl font-extrabold tracking-tight text-slate-950 sm:text-7xl">OmniRead</h1>
          <p className="mt-5 text-2xl font-semibold text-slate-700 sm:text-3xl">Complexity Stripped. Clarity Delivered.</p>
          <p className="mt-6 max-w-2xl text-lg leading-8 text-slate-600">
            Analyze difficult text, understand its readability, identify challenging words and complex sentences, then simplify the text and listen to the simplified version.
          </p>
          <Link to="/analyzer" className="mt-9 inline-flex items-center rounded-xl bg-indigo-600 px-6 py-3.5 font-semibold text-white shadow-sm transition hover:bg-indigo-700 focus:outline-none focus:ring-4 focus:ring-indigo-200">
            Get Started <span className="ml-2" aria-hidden="true">→</span>
          </Link>
        </div>
      </section>
    </Layout>
  );
}
