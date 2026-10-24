import { useMemo, useState } from "react";
import { Activity, ArrowUpRight, Check, ChevronDown, CircleHelp, Clipboard, FileText, Fingerprint, Gauge, LockKeyhole, RotateCcw, ScanText, ShieldCheck, Sparkles, Upload, WandSparkles } from "lucide-react";

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";
const sampleText = "When I started volunteering at the community library, I thought my job would mostly involve arranging books. Instead, I met people who came in every week just to use the computers, print a form, or ask for help understanding a letter. One afternoon, an older man brought a notice he had received in the post. He was worried because he could not understand the deadline. We read it together, called the office listed on the letter, and wrote down the next steps. It took less than twenty minutes, but he thanked me as if I had done something huge. That day changed how I saw the library. It was not only a place for books; it was a place where people could ask for help without feeling embarrassed.";

function Metric({ label, value, suffix = "" }) {
  return <div className="metric"><span>{label}</span><strong>{value}{suffix}</strong></div>;
}

function ScoreRing({ score }) {
  return <div className="score-ring" style={{ "--score": score }}><div className="score-inner"><strong>{score}%</strong><span>AI-like score</span></div></div>;
}

export default function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [showAll, setShowAll] = useState(false);
  const [apiOnline, setApiOnline] = useState(null);

  const wordCount = useMemo(() => (text.trim().match(/[\p{L}\p{N}'-]+/gu) || []).length, [text]);
  const canAnalyze = wordCount >= 40 && wordCount <= 5000;

  async function analyze() {
    setLoading(true); setError(""); setResult(null);
    try {
      const response = await fetch(`${API_URL}/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.detail || "Could not analyze this text.");
      setResult(payload); setApiOnline(true);
    } catch (e) {
      setError(e.message === "Failed to fetch"
        ? "Can't reach the local analyzer. Start the FastAPI backend on port 8000, then try again."
        : e.message);
      setApiOnline(false);
    } finally { setLoading(false); }
  }

  function reset() { setText(""); setResult(null); setError(""); setShowAll(false); }
  function copyReport() {
    if (!result) return;
    const report = [
      "HUMANCHECK — WRITING PATTERN REPORT",
      `AI-like score: ${result.ai_like_score}%`,
      `Human-like score: ${result.human_like_score}%`,
      `Method: ${result.method}`,
      result.summary,
      "",
      "Signals:", ...result.signals.map((s) => `- ${s}`),
      "",
      "Limitations:", ...result.limitations.map((s) => `- ${s}`),
    ].join("\n");
    navigator.clipboard.writeText(report);
  }

  const metrics = result?.metrics;
  const visibleSentences = result?.sentences?.slice(0, showAll ? 80 : 5) || [];

  return (
    <div className="app-shell">
      <header className="topbar">
        <a className="brand" href="#"><span className="brand-mark"><Fingerprint size={22} /></span><span>human<span className="brand-accent">check</span><small>WRITING PATTERN ANALYZER</small></span></a>
        <div className="top-actions"><span className="local-pill"><span className="status-dot" /> LOCAL-FIRST</span><a className="github-link" href="https://github.com/ranjiths112007/Codomax-Digital-Solutions-AI-ML-Internship-" target="_blank" rel="noreferrer">Project repo <ArrowUpRight size={15}/></a></div>
      </header>

      <main>
        <section className="hero">
          <div className="eyebrow"><Sparkles size={14}/> A clearer look at the words</div>
          <h1>Look closer.<br/><span>Understand the writing.</span></h1>
          <p className="hero-copy">Explore writing patterns that may resemble AI-generated or human-written text. A useful signal for review — never a verdict on authorship.</p>
          <div className="trust-row"><span><LockKeyhole size={15}/> Text stays on your local setup</span><span><ShieldCheck size={15}/> No paid API key</span><span><Activity size={15}/> Pattern-based insights</span></div>
        </section>

        <section className="workspace">
          <div className="input-panel panel">
            <div className="panel-heading"><div><span className="step-label">01 / INPUT</span><h2>Bring your text</h2></div><button className="text-button" onClick={reset}><RotateCcw size={14}/> Clear</button></div>
            <p className="subtext">Paste a passage, essay, article, or draft. For a more meaningful analysis, use at least 40 words.</p>
            <div className="editor-wrap">
              <textarea value={text} onChange={(e) => setText(e.target.value)} placeholder="Paste your text here…&#10;&#10;Your words are analyzed by the local backend. They are not saved by this app." maxLength={30000} aria-label="Text to analyze" />
              <div className="editor-footer"><span>{wordCount.toLocaleString()} words <i>·</i> {text.length.toLocaleString()} characters</span><button className="sample-button" onClick={() => { setText(sampleText); setResult(null); setError(""); }}><FileText size={14}/> Try sample text</button></div>
            </div>
            <div className="privacy-note"><LockKeyhole size={16}/><div><strong>Private by design</strong><p>Analysis runs through your local backend. Don't expose this development server publicly with private text.</p></div></div>
            {error && <div className="error-box" role="alert">{error}</div>}
            <button className="analyze-button" disabled={!canAnalyze || loading} onClick={analyze}>{loading ? <><span className="spinner"/> Analyzing patterns…</> : <><ScanText size={18}/> Analyze writing <ArrowUpRight size={16}/></>}</button>
            <div className="input-footnote">{wordCount < 40 ? `${40 - wordCount} more words needed` : wordCount > 5000 ? "Please keep the input under 5,000 words." : "Ready to analyze"} <span>•</span> Results may be wrong</div>
          </div>

          <div className="results-panel panel">
            <div className="panel-heading"><div><span className="step-label">02 / ANALYSIS</span><h2>Your report</h2></div><span className={apiOnline === false ? "api-status offline" : "api-status"}><span className="status-dot"/>{apiOnline === false ? "OFFLINE" : "LOCAL ANALYZER"}</span></div>
            {!result ? <div className="empty-state"><div className="empty-illustration"><Gauge size={30}/><span><Sparkles size={14}/></span></div><h3>Your analysis starts here</h3><p>Paste at least 40 words and run the analyzer. Your score, writing metrics, and sentence-level cues will appear here.</p><div className="empty-checks"><span><Check size={15}/> AI-like / human-like estimate</span><span><Check size={15}/> Sentence pattern cues</span><span><Check size={15}/> Readable explanation</span></div></div> : <div className="report-content">
              <div className="score-layout"><ScoreRing score={result.ai_like_score}/><div className="score-copy"><span className="result-kicker">PATTERN ESTIMATE</span><h3>{result.ai_like_score >= 65 ? "More AI-like signals" : result.ai_like_score <= 35 ? "More human-like signals" : "A mixed pattern"}</h3><p>{result.summary}</p><div className="score-legend"><span><i className="legend-ai"/> AI-like <strong>{result.ai_like_score}%</strong></span><span><i className="legend-human"/> Human-like <strong>{result.human_like_score}%</strong></span></div></div></div>
              <div className="warning-note"><CircleHelp size={17}/><p><strong>Not an authorship verdict.</strong> These scores are not calibrated probabilities. Writing style alone cannot prove whether a person or AI wrote a passage.</p></div>
              <div className="report-section-title"><h3>Writing profile</h3><span>{metrics.word_count} words analyzed</span></div>
              <div className="metrics-grid"><Metric label="Sentences" value={metrics.sentence_count}/><Metric label="Avg. sentence" value={metrics.average_sentence_length} suffix=" words"/><Metric label="Sentence variation" value={metrics.sentence_length_variation}/><Metric label="Vocabulary diversity" value={metrics.vocabulary_diversity} suffix="%"/><Metric label="Repeated word ratio" value={metrics.repeated_word_ratio} suffix="%"/><Metric label="Transition phrases" value={metrics.transition_phrase_count}/></div>
              <div className="signals-block"><h3><WandSparkles size={17}/> What shaped this result</h3>{result.signals.map((signal, i) => <div className="signal-item" key={i}><span>{String(i + 1).padStart(2, "0")}</span><p>{signal}</p></div>)}</div>
              <div className="sentences-block"><div className="report-section-title"><h3>Sentence scanner</h3><span>Pattern cues, not proof</span></div>{visibleSentences.map((sentence) => <div className="sentence-row" key={sentence.index}><div className={sentence.heuristic_score >= 60 ? "sentence-indicator ai" : sentence.heuristic_score <= 40 ? "sentence-indicator human" : "sentence-indicator mixed"}></div><div className="sentence-body"><p>{sentence.text}</p><span>{sentence.pattern_signal}</span></div></div>)}{result.sentences.length > 5 && <button className="show-more" onClick={() => setShowAll(!showAll)}>{showAll ? "Show fewer sentences" : `Show all ${result.sentences.length} sentences`} <ChevronDown size={15}/></button>}</div>
              <div className="method-row"><div><span className="step-label">METHOD</span><strong>{result.method === "local-ml-model" ? "Local ML model" : "Writing-pattern fallback"}</strong><p>{result.method === "local-ml-model" ? `Model: ${result.model_id}` : "Model unavailable; simple style heuristics were used."}</p></div><button className="secondary-button" onClick={copyReport}><Clipboard size={15}/> Copy report</button></div>
              <details className="limitations"><summary>Read limitations and responsible-use notes</summary><ul>{result.limitations.map((item, i) => <li key={i}>{item}</li>)}</ul></details>
            </div>}
          </div>
        </section>

        <section className="how-section"><div className="section-intro"><span className="step-label">DESIGNED FOR RESPONSIBLE REVIEW</span><h2>Signals, not labels.</h2><p>Human writing is varied. AI writing is varied too. The goal is to help you inspect patterns, not decide someone's credibility from a percentage.</p></div><div className="principles"><article><span className="principle-icon"><ScanText size={20}/></span><h3>Inspect the patterns</h3><p>Explore sentence rhythm, repeated wording, vocabulary variety, and transition phrases.</p></article><article><span className="principle-icon"><LockKeyhole size={20}/></span><h3>Keep it local</h3><p>No paid inference API. The model runs on your own machine after its weights are downloaded.</p></article><article><span className="principle-icon"><CircleHelp size={20}/></span><h3>Stay thoughtful</h3><p>Use the report as one clue among many. Never treat the score as evidence by itself.</p></article></div></section>
      </main>
      <footer><a className="footer-brand" href="#"><Fingerprint size={18}/> humancheck</a><span>Built for learning, transparency, and better writing conversations.</span><span className="footer-right">NO API KEY · LOCAL-FIRST · HUMAN-CENTERED</span></footer>
    </div>
  );
}
