import React, { useState } from 'react';
import { 
  Heart, 
  Moon, 
  Smartphone, 
  Activity, 
  BookOpen, 
  Send, 
  Lock, 
  AlertTriangle,
  ArrowRight,
  CheckCircle2,
  RefreshCw,
  Info
} from 'lucide-react';
import { submitCheckIn } from '../api';

const MOODS = [
  { score: 6, label: "😄 Joyful", title: "Joyful", emoji: "😄", desc: "Happy, energetic, motivated" },
  { score: 5, label: "😌 Calm", title: "Calm", emoji: "😌", desc: "Relaxed, balanced, content" },
  { score: 4, label: "😐 Neutral", title: "Neutral", emoji: "😐", desc: "Neither particularly up nor down" },
  { score: 3, label: "😟 Worried", title: "Worried", emoji: "😟", desc: "Uneasy, apprehensive, anxious" },
  { score: 2, label: "😢 Sad", title: "Sad", emoji: "😢", desc: "Low mood, tearful, withdrawn" },
  { score: 1, label: "😤 Frustrated", title: "Frustrated", emoji: "😤", desc: "Irritable, overwhelmed, angry" },
];

const STRESS_LABELS = {
  1: "Level 1: No Stress",
  2: "Level 2: Mild Strain",
  3: "Level 3: Moderate Stress",
  4: "Level 4: High Stress",
  5: "Level 5: Severe Overwhelm",
};

export default function CheckIn({ setActiveTab }) {
  const [selectedMood, setSelectedMood] = useState(null);
  const [sleepHours, setSleepHours] = useState(8.5);
  const [screenTime, setScreenTime] = useState(2.0);
  const [physicalPlay, setPhysicalPlay] = useState(1.5);
  const [schoolStress, setSchoolStress] = useState(2);
  const [journalText, setJournalText] = useState("");

  const [loading, setLoading] = useState(false);
  const [assessment, setAssessment] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedMood) {
      setError("Please select the emoji that best reflects your current state.");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const payload = {
        mood_score: selectedMood.score,
        mood_label: selectedMood.label,
        sleep_hours: parseFloat(sleepHours),
        screen_time: parseFloat(screenTime),
        physical_play: parseFloat(physicalPlay),
        school_stress: parseInt(schoolStress),
        journal_text: journalText.trim(),
      };

      const result = await submitCheckIn(payload);
      setAssessment(result);
    } catch (err) {
      setError(err.message || "Unable to submit check-in. Ensure the backend service is running.");
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setAssessment(null);
    setSelectedMood(null);
    setJournalText("");
    setError(null);
  };

  return (
    <div className="max-w-3xl mx-auto py-4 space-y-8">
      
      {/* Page Title */}
      <div className="space-y-1">
        <div className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-500 uppercase tracking-wider">
          <Heart className="w-3.5 h-3.5 text-slate-400" />
          <span>Daily Self-Report Protocol</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
          Child Well-being Check-in
        </h1>
        <p className="text-xs text-slate-500 leading-relaxed">
          Record your current mood and lifestyle factors. All inputs are evaluated non-clinically.
        </p>
      </div>

      {error && (
        <div className="p-3.5 rounded-lg bg-rose-50 border border-rose-200 text-rose-800 text-xs font-medium flex items-center gap-2">
          <AlertTriangle className="w-4 h-4 text-rose-600 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {!assessment ? (
        <form onSubmit={handleSubmit} className="space-y-6">
          
          {/* Section 1: Mood Selection */}
          <div className="card-surface p-6 space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="font-semibold text-sm text-slate-900">
                1. Affective Mood State
              </h3>
              {selectedMood && (
                <span className="text-xs font-medium px-2 py-0.5 rounded bg-slate-100 text-slate-800 border border-slate-200">
                  Selected: {selectedMood.label}
                </span>
              )}
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2.5">
              {MOODS.map((m) => {
                const isSelected = selectedMood?.score === m.score;
                return (
                  <button
                    key={m.score}
                    type="button"
                    onClick={() => setSelectedMood(m)}
                    className={`p-3 rounded-xl border text-center transition-all flex flex-col items-center justify-between min-h-[110px] ${
                      isSelected
                        ? 'border-slate-900 bg-slate-50 ring-1 ring-slate-900 font-semibold'
                        : 'border-slate-200 hover:border-slate-300 hover:bg-slate-50/50'
                    }`}
                  >
                    <span className="text-3xl my-1">{m.emoji}</span>
                    <div>
                      <div className="font-medium text-xs text-slate-900">{m.title}</div>
                      <div className="text-[10px] text-slate-500 line-clamp-1">{m.desc}</div>
                    </div>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Section 2: Lifestyle Parameters */}
          <div className="card-surface p-6 space-y-5">
            <h3 className="font-semibold text-sm text-slate-900">
              2. Behavioral &amp; Lifestyle Parameters
            </h3>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-5 text-xs">
              
              {/* Sleep Hours */}
              <div className="p-3.5 rounded-lg bg-slate-50 border border-slate-200/80 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-medium text-slate-700 flex items-center gap-1.5">
                    <Moon className="w-3.5 h-3.5 text-slate-500" />
                    <span>Sleep Last Night</span>
                  </span>
                  <span className="font-mono font-semibold text-slate-900">{sleepHours} hrs</span>
                </div>
                <input
                  type="range"
                  min="4.0"
                  max="12.0"
                  step="0.5"
                  value={sleepHours}
                  onChange={(e) => setSleepHours(e.target.value)}
                  className="w-full accent-slate-800 cursor-pointer"
                />
                <div className="flex justify-between text-[10px] text-slate-400">
                  <span>4h (Insufficient)</span>
                  <span>9–11h ideal</span>
                  <span>12h</span>
                </div>
              </div>

              {/* Screen Time */}
              <div className="p-3.5 rounded-lg bg-slate-50 border border-slate-200/80 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-medium text-slate-700 flex items-center gap-1.5">
                    <Smartphone className="w-3.5 h-3.5 text-slate-500" />
                    <span>Screen Exposure</span>
                  </span>
                  <span className="font-mono font-semibold text-slate-900">{screenTime} hrs</span>
                </div>
                <input
                  type="range"
                  min="0.0"
                  max="8.0"
                  step="0.5"
                  value={screenTime}
                  onChange={(e) => setScreenTime(e.target.value)}
                  className="w-full accent-slate-800 cursor-pointer"
                />
                <div className="flex justify-between text-[10px] text-slate-400">
                  <span>0h</span>
                  <span>&le; 2h recommended</span>
                  <span>8h+</span>
                </div>
              </div>

              {/* Physical Play */}
              <div className="p-3.5 rounded-lg bg-slate-50 border border-slate-200/80 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-medium text-slate-700 flex items-center gap-1.5">
                    <Activity className="w-3.5 h-3.5 text-slate-500" />
                    <span>Physical Activity / Play</span>
                  </span>
                  <span className="font-mono font-semibold text-slate-900">{physicalPlay} hrs</span>
                </div>
                <input
                  type="range"
                  min="0.0"
                  max="4.0"
                  step="0.5"
                  value={physicalPlay}
                  onChange={(e) => setPhysicalPlay(e.target.value)}
                  className="w-full accent-slate-800 cursor-pointer"
                />
                <div className="flex justify-between text-[10px] text-slate-400">
                  <span>0h (Sedentary)</span>
                  <span>&ge; 1h recommended</span>
                  <span>4h</span>
                </div>
              </div>

              {/* School Stress */}
              <div className="p-3.5 rounded-lg bg-slate-50 border border-slate-200/80 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-medium text-slate-700 flex items-center gap-1.5">
                    <BookOpen className="w-3.5 h-3.5 text-slate-500" />
                    <span>Academic / School Strain</span>
                  </span>
                  <span className="font-medium text-slate-800">{STRESS_LABELS[schoolStress]}</span>
                </div>
                <input
                  type="range"
                  min="1"
                  max="5"
                  step="1"
                  value={schoolStress}
                  onChange={(e) => setSchoolStress(e.target.value)}
                  className="w-full accent-slate-800 cursor-pointer"
                />
                <div className="flex justify-between text-[10px] text-slate-400">
                  <span>1 (Minimal)</span>
                  <span>3 (Moderate)</span>
                  <span>5 (Extreme)</span>
                </div>
              </div>

            </div>
          </div>

          {/* Section 3: Reflective Journal */}
          <div className="card-surface p-6 space-y-3">
            <div className="flex items-center justify-between">
              <h3 className="font-semibold text-sm text-slate-900">
                3. Reflective Journal Entry <span className="text-xs text-slate-400 font-normal">(Optional)</span>
              </h3>
              <div className="flex items-center gap-1 text-[11px] text-slate-500 bg-slate-100 px-2 py-0.5 rounded">
                <Lock className="w-3 h-3 text-slate-400" />
                <span>Encrypted In-Memory Only</span>
              </div>
            </div>

            <p className="text-xs text-slate-500 leading-relaxed">
              Express your feelings freely. Text is parsed for linguistic valence using VADER NLP 
              and is <strong>never written to disk or shared with guardians</strong> (DPDP Act 2023, Section 9).
            </p>

            <textarea
              rows="3"
              value={journalText}
              onChange={(e) => setJournalText(e.target.value)}
              placeholder="Reflect on your day: What went well? What caused concern or stress?"
              className="w-full p-3.5 rounded-lg bg-white border border-slate-300 focus:border-slate-600 focus:ring-1 focus:ring-slate-600 outline-none text-xs text-slate-800 placeholder:text-slate-400 transition-colors resize-none"
            />
          </div>

          {/* Submit Action */}
          <div className="pt-2">
            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 rounded-lg bg-slate-900 hover:bg-slate-800 text-white font-medium text-xs transition-colors disabled:opacity-50 flex items-center justify-center gap-2"
            >
              {loading ? (
                <>
                  <RefreshCw className="w-4 h-4 animate-spin" />
                  <span>Computing Multi-Modal Risk Inference...</span>
                </>
              ) : (
                <>
                  <Send className="w-4 h-4" />
                  <span>Submit Daily Check-in</span>
                </>
              )}
            </button>
          </div>

        </form>
      ) : (
        /* Professional Clinical Results Card */
        <div className="space-y-6">
          
          {/* Main Tier Classification Banner */}
          <div className={`p-6 rounded-xl border ${
            assessment.risk_tier === 0 
              ? 'bg-emerald-50 border-emerald-300 text-emerald-900' 
              : assessment.risk_tier === 1 
              ? 'bg-amber-50 border-amber-300 text-amber-900' 
              : 'bg-rose-50 border-rose-300 text-rose-900'
          }`}>
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-black/10 pb-4">
              <div>
                <span className="text-[10px] font-bold uppercase tracking-wider block opacity-75">
                  ML Stratification Result
                </span>
                <div className="text-xl font-bold mt-0.5">
                  {assessment.risk_label}
                </div>
              </div>
              <div className="px-2.5 py-1 rounded bg-white/90 border border-current text-[11px] font-mono font-semibold self-start sm:self-auto">
                Confidence: {(assessment.confidence * 100).toFixed(1)}%
              </div>
            </div>

            <div className="pt-4 space-y-2 text-xs">
              <p className="font-medium leading-relaxed">{assessment.description}</p>
              <div className="p-3 rounded-lg bg-white/80 border border-black/5 font-normal">
                <strong>Action Guidance:</strong> {assessment.action}
              </div>
            </div>
          </div>

          {/* Model Explanation */}
          <div className="card-surface p-6 space-y-4">
            <h3 className="font-semibold text-sm text-slate-900">
              Factor Attribution &amp; Multi-Class Probabilities
            </h3>
            
            <p className="text-xs text-slate-600 leading-relaxed">
              <strong>Computational Summary:</strong> {assessment.factor_explanation}
            </p>

            <div className="space-y-2.5 pt-1 text-xs">
              {Object.entries(assessment.probabilities).map(([tierName, prob]) => (
                <div key={tierName} className="space-y-1">
                  <div className="flex justify-between text-[11px]">
                    <span className="text-slate-600">{tierName}</span>
                    <span className="font-mono font-medium text-slate-900">{(prob * 100).toFixed(1)}%</span>
                  </div>
                  <div className="w-full bg-slate-100 rounded h-1.5 overflow-hidden">
                    <div 
                      className="bg-slate-700 h-1.5 rounded"
                      style={{ width: `${prob * 100}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* NLP Sentiment Valence (if journal present) */}
          {assessment.sentiment && journalText.trim() && (
            <div className="card-surface p-6 space-y-3">
              <h3 className="font-semibold text-sm text-slate-900">
                Text Sentiment Valence (VADER Lexicon)
              </h3>
              <div className="p-3.5 rounded-lg bg-slate-50 border border-slate-200 flex items-center justify-between text-xs">
                <div>
                  <span className="font-semibold text-slate-800">{assessment.sentiment.tone_tag} Affective Valence</span>
                  <div className="text-[11px] text-slate-500">Processed locally with rule-based lexicon</div>
                </div>
                <span className="font-mono font-bold text-slate-800 bg-white px-2 py-0.5 rounded border">
                  Compound: {assessment.sentiment.compound}
                </span>
              </div>
            </div>
          )}

          {/* Affirmation Strip */}
          <div className="p-4 rounded-xl bg-slate-100 border border-slate-200 text-xs text-slate-700">
            <span className="font-semibold block mb-0.5 text-slate-800">Supportive Reflection:</span>
            "{assessment.affirmation}"
          </div>

          {/* Navigation Action Buttons */}
          <div className="flex flex-wrap items-center justify-between gap-3 pt-2">
            <button
              onClick={handleReset}
              className="px-4 py-2 rounded-lg border border-slate-300 hover:bg-slate-50 text-slate-700 font-medium text-xs transition-colors"
            >
              ← Record Another Entry
            </button>

            <div className="flex items-center gap-2">
              <button
                onClick={() => setActiveTab('coping')}
                className="px-4 py-2 rounded-lg bg-slate-900 hover:bg-slate-800 text-white font-medium text-xs transition-colors"
              >
                Coping Exercises →
              </button>

              {assessment.risk_tier >= 2 && (
                <button
                  onClick={() => setActiveTab('crisis')}
                  className="px-4 py-2 rounded-lg bg-rose-600 hover:bg-rose-700 text-white font-medium text-xs transition-colors"
                >
                  Emergency Contacts
                </button>
              )}
            </div>
          </div>

        </div>
      )}

    </div>
  );
}
