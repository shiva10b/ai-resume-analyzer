import { useState } from "react";
import { UploadCloud, FileText, Loader2 } from "lucide-react";

export default function UploadForm({ onAnalyze, loading }) {
  const [file, setFile] = useState(null);
  const [jd, setJd] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!file || !jd.trim()) return;
    onAnalyze(file, jd);
  };

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-2xl mx-auto bg-white rounded-2xl shadow-sm border border-slate-200 p-8 space-y-6">
      <div>
        <label className="block text-sm font-medium text-slate-700 mb-2">Resume (PDF or DOCX)</label>
        <label className="flex flex-col items-center justify-center gap-2 border-2 border-dashed border-slate-300 rounded-xl p-8 cursor-pointer hover:border-indigo-400 hover:bg-indigo-50/50 transition-colors">
          <input
            type="file"
            accept=".pdf,.docx"
            className="hidden"
            onChange={(e) => setFile(e.target.files[0])}
          />
          {file ? (
            <>
              <FileText className="w-8 h-8 text-indigo-500" />
              <span className="text-sm text-slate-700 font-medium">{file.name}</span>
            </>
          ) : (
            <>
              <UploadCloud className="w-8 h-8 text-slate-400" />
              <span className="text-sm text-slate-500">Click to upload your resume</span>
            </>
          )}
        </label>
      </div>

      <div>
        <label className="block text-sm font-medium text-slate-700 mb-2">Job Description</label>
        <textarea
          value={jd}
          onChange={(e) => setJd(e.target.value)}
          rows={8}
          placeholder="Paste the job description here..."
          className="w-full rounded-xl border border-slate-300 p-4 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-400 resize-none"
        />
      </div>

      <button
        type="submit"
        disabled={!file || !jd.trim() || loading}
        className="w-full flex items-center justify-center gap-2 bg-indigo-600 text-white font-medium py-3 rounded-xl hover:bg-indigo-700 disabled:bg-slate-300 disabled:cursor-not-allowed transition-colors"
      >
        {loading ? (
          <>
            <Loader2 className="w-4 h-4 animate-spin" /> Analyzing...
          </>
        ) : (
          "Analyze Resume"
        )}
      </button>
    </form>
  );
}
