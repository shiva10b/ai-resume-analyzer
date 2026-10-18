import { useState } from "react";
import UploadForm from "./components/UploadForm";
import ResultsPanel from "./components/ResultsPanel";
import { analyzeResume } from "./api/client";
import { FileSearch } from "lucide-react";

export default function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleAnalyze = async (file, jd) => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const data = await analyzeResume(file, jd);
      setResult(data);
    } catch (err) {
      setError(err?.response?.data?.detail || "Unable to analyze resume. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50">
      <header className="border-b border-slate-200 bg-white">
        <div className="max-w-3xl mx-auto px-6 py-4 flex items-center gap-2.5">
          <FileSearch className="w-5 h-5 text-indigo-600" />
          <h1 className="text-sm font-semibold text-slate-900">AI Resume Analyzer</h1>
        </div>
      </header>

      <main className={`${result ? "max-w-5xl" : "max-w-3xl"} mx-auto px-6 py-10 space-y-8`}>
        {!result && !loading && (
          <div className="space-y-1">
            <h2 className="text-xl font-semibold text-slate-900">Analyze your resume</h2>
            <p className="text-sm text-slate-500">
              Upload a resume and paste a job description to get an ATS score and specific improvement suggestions.
            </p>
          </div>
        )}

        {!result && <UploadForm onAnalyze={handleAnalyze} loading={loading} />}

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-xl px-4 py-3">
            <p className="text-sm font-medium text-red-800">Unable to analyze resume</p>
            <p className="text-sm text-red-600 mt-0.5">{error}</p>
          </div>
        )}

        {result && <ResultsPanel result={result} onReset={() => setResult(null)} />}
      </main>

      <footer className="border-t border-slate-200 mt-16">
        <div className="max-w-3xl mx-auto px-6 py-6 text-xs text-slate-400">
          Built with FastAPI, React &amp; Llama 3.1
        </div>
      </footer>
    </div>
  );
}
