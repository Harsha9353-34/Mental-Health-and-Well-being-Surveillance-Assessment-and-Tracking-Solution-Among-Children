import React, { useState, useEffect } from 'react';
import { 
  Wind, 
  Eye, 
  Hand, 
  Ear, 
  Sparkles, 
  Shuffle, 
  CheckCircle2, 
  RotateCcw,
  Play, 
  Square, 
  Smile,
  ShieldCheck
} from 'lucide-react';

const AFFIRMATION_LIST = [
  "You are brave, strong, and capable of navigating difficult moments.",
  "Your feelings are valid. Giving yourself time to process is healthy.",
  "Each day presents a fresh opportunity to reset and progress.",
  "You are supported, valued, and not alone.",
  "Seeking support from a trusted adult is a sign of courage and strength.",
  "Focus on one calm breath at a time. The present moment is manageable.",
  "Small, consistent steps forward constitute meaningful progress.",
  "Difficult emotions are temporary; your resilience is enduring.",
  "Treat yourself with patience and kindness today.",
  "You have handled challenging situations before and will overcome this too.",
];

const GROUNDING_DATA = [
  { count: 5, icon: Eye, title: "5 Visual Anchors", desc: "Acknowledge 5 distinct objects in your immediate visual field." },
  { count: 4, icon: Hand, title: "4 Tactile Sensations", desc: "Notice 4 different textures you can touch right now." },
  { count: 3, icon: Ear, title: "3 Auditory Signals", desc: "Listen carefully and distinguish 3 separate sounds in the environment." },
  { count: 2, icon: Sparkles, title: "2 Olfactory Notes", desc: "Identify 2 scents or aromas around you." },
  { count: 1, icon: Smile, title: "1 Taste / Sensation", desc: "Notice any taste present in your mouth or take a sip of water." },
];

export default function CopingToolkit() {
  const [activeSubTab, setActiveSubTab] = useState('breathing');

  // Breathing state
  const [isBreathing, setIsBreathing] = useState(false);
  const [breathPhase, setBreathPhase] = useState('idle'); // 'inhale', 'hold', 'exhale'
  const [timerCount, setTimerCount] = useState(4);
  const [completedCycles, setCompletedCycles] = useState(0);

  // Grounding state
  const [groundingChecked, setGroundingChecked] = useState({});

  // Affirmations state
  const [currentAffirmationIndex, setCurrentAffirmationIndex] = useState(0);

  // Minimalist 4-7-8 Breathing Timer Loop
  useEffect(() => {
    let interval = null;
    if (!isBreathing) {
      setBreathPhase('idle');
      setTimerCount(4);
      return;
    }

    setBreathPhase('inhale');
    setTimerCount(4);

    let currentPhase = 'inhale';
    let timeLeft = 4;

    interval = setInterval(() => {
      timeLeft -= 1;
      setTimerCount(timeLeft);

      if (timeLeft <= 0) {
        if (currentPhase === 'inhale') {
          currentPhase = 'hold';
          timeLeft = 7;
          setBreathPhase('hold');
          setTimerCount(7);
        } else if (currentPhase === 'hold') {
          currentPhase = 'exhale';
          timeLeft = 8;
          setBreathPhase('exhale');
          setTimerCount(8);
        } else if (currentPhase === 'exhale') {
          currentPhase = 'inhale';
          timeLeft = 4;
          setBreathPhase('inhale');
          setTimerCount(4);
          setCompletedCycles((c) => c + 1);
        }
      }
    }, 1000);

    return () => clearInterval(interval);
  }, [isBreathing]);

  const toggleGroundingItem = (stepIndex, itemIndex) => {
    const key = `${stepIndex}-${itemIndex}`;
    setGroundingChecked((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  const resetGrounding = () => setGroundingChecked({});

  const shuffleAffirmation = () => {
    setCurrentAffirmationIndex((prev) => (prev + 1) % AFFIRMATION_LIST.length);
  };

  return (
    <div className="max-w-3xl mx-auto py-4 space-y-6">
      
      {/* Header */}
      <div className="space-y-1">
        <div className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-500 uppercase tracking-wider">
          <Wind className="w-3.5 h-3.5 text-slate-400" />
          <span>Non-Clinical Coping Protocol</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
          Psychoeducational Coping Toolkit
        </h1>
        <p className="text-xs text-slate-500 leading-relaxed">
          Structured behavioral grounding and breathing exercises designed to regulate the parasympathetic nervous system.
        </p>
      </div>

      {/* Clean Segmented Control */}
      <div className="flex border-b border-slate-200">
        <div className="flex gap-4">
          <button
            onClick={() => setActiveSubTab('breathing')}
            className={`pb-2.5 text-xs font-semibold border-b-2 transition-colors ${
              activeSubTab === 'breathing'
                ? 'border-slate-900 text-slate-900'
                : 'border-transparent text-slate-500 hover:text-slate-800'
            }`}
          >
            4-7-8 Breathing Pacer
          </button>
          <button
            onClick={() => setActiveSubTab('grounding')}
            className={`pb-2.5 text-xs font-semibold border-b-2 transition-colors ${
              activeSubTab === 'grounding'
                ? 'border-slate-900 text-slate-900'
                : 'border-transparent text-slate-500 hover:text-slate-800'
            }`}
          >
            5-4-3-2-1 Sensory Grounding
          </button>
          <button
            onClick={() => setActiveSubTab('affirmations')}
            className={`pb-2.5 text-xs font-semibold border-b-2 transition-colors ${
              activeSubTab === 'affirmations'
                ? 'border-slate-900 text-slate-900'
                : 'border-transparent text-slate-500 hover:text-slate-800'
            }`}
          >
            Cognitive Affirmations
          </button>
        </div>
      </div>

      {/* TAB 1: BREATHING PACER (Clinical & Minimalist, No Neon Blur) */}
      {activeSubTab === 'breathing' && (
        <div className="card-surface p-8 text-center space-y-6">
          <div className="max-w-md mx-auto space-y-1">
            <h3 className="text-base font-bold text-slate-900">4-7-8 Parasympathetic Regulation</h3>
            <p className="text-xs text-slate-500 leading-relaxed">
              Dr. Andrew Weil's rhythmic breathing framework: Inhale (4s) → Hold (7s) → Exhale (8s).
            </p>
          </div>

          {/* Minimalist Concentric Scale Circle (Apple Health / Linear style) */}
          <div className="py-6 flex items-center justify-center">
            <div className="relative w-56 h-56 flex items-center justify-center">
              
              {/* Outer guide ring */}
              <div className="absolute inset-0 rounded-full border border-slate-200" />
              
              {/* Animated scaling target circle */}
              <div
                className={`rounded-full flex flex-col items-center justify-center transition-all duration-700 ease-out border ${
                  breathPhase === 'inhale'
                    ? 'w-48 h-48 bg-slate-900 border-slate-900 text-white'
                    : breathPhase === 'hold'
                    ? 'w-48 h-48 bg-slate-800 border-slate-800 text-white'
                    : breathPhase === 'exhale'
                    ? 'w-28 h-28 bg-slate-100 border-slate-300 text-slate-800'
                    : 'w-36 h-36 bg-slate-50 border-slate-200 text-slate-600'
                }`}
              >
                <span className="text-[11px] font-mono uppercase tracking-wider opacity-80">
                  {breathPhase === 'inhale' && "Inhale"}
                  {breathPhase === 'hold' && "Hold"}
                  {breathPhase === 'exhale' && "Exhale"}
                  {breathPhase === 'idle' && "Ready"}
                </span>
                <span className="text-4xl font-mono font-bold my-0.5">
                  {isBreathing ? timerCount : "4·7·8"}
                </span>
                <span className="text-[10px] opacity-75">
                  {isBreathing ? (breathPhase === 'exhale' ? "through mouth" : "through nose") : "Start"}
                </span>
              </div>

            </div>
          </div>

          {/* Controls */}
          <div className="space-y-2 pt-2">
            <button
              onClick={() => setIsBreathing(!isBreathing)}
              className={`px-6 py-2.5 rounded-lg text-xs font-medium transition-colors inline-flex items-center gap-2 ${
                isBreathing
                  ? 'bg-rose-600 hover:bg-rose-700 text-white'
                  : 'bg-slate-900 hover:bg-slate-800 text-white'
              }`}
            >
              {isBreathing ? (
                <>
                  <Square className="w-3.5 h-3.5 fill-current" />
                  <span>Stop Session</span>
                </>
              ) : (
                <>
                  <Play className="w-3.5 h-3.5 fill-current" />
                  <span>Begin 4-7-8 Breathing</span>
                </>
              )}
            </button>

            {completedCycles > 0 && (
              <p className="text-xs text-slate-500 font-medium">
                Completed cycles: <span className="font-mono text-slate-900 font-bold">{completedCycles}</span>
              </p>
            )}
          </div>
        </div>
      )}

      {/* TAB 2: 5-4-3-2-1 GROUNDING */}
      {activeSubTab === 'grounding' && (
        <div className="space-y-4">
          <div className="card-surface p-5 flex items-center justify-between">
            <div>
              <h3 className="font-bold text-sm text-slate-900">5-4-3-2-1 Sensory Grounding Technique</h3>
              <p className="text-xs text-slate-500 mt-0.5">
                Cognitive behavioral method to decouple acute stress loops by systematically engaging sensory channels.
              </p>
            </div>
            <button
              onClick={resetGrounding}
              className="flex items-center gap-1 px-2.5 py-1.5 text-xs font-medium rounded border border-slate-200 hover:bg-slate-50 text-slate-600"
            >
              <RotateCcw className="w-3 h-3" />
              <span>Reset</span>
            </button>
          </div>

          <div className="space-y-3">
            {GROUNDING_DATA.map((step, sIdx) => {
              const Icon = step.icon;
              return (
                <div key={sIdx} className="card-surface p-4 space-y-2.5">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2 font-semibold text-xs text-slate-900">
                      <Icon className="w-4 h-4 text-slate-500" />
                      <span>{step.title}</span>
                    </div>
                    <span className="text-[11px] font-mono text-slate-400">Step {sIdx + 1} of 5</span>
                  </div>
                  <p className="text-xs text-slate-500">{step.desc}</p>
                  
                  <div className="flex flex-wrap gap-2 pt-1">
                    {Array.from({ length: step.count }).map((_, itemIdx) => {
                      const isDone = groundingChecked[`${sIdx}-${itemIdx}`];
                      return (
                        <button
                          key={itemIdx}
                          onClick={() => toggleGroundingItem(sIdx, itemIdx)}
                          className={`px-3 py-1 rounded text-xs font-medium border transition-colors flex items-center gap-1.5 ${
                            isDone 
                              ? 'bg-slate-900 border-slate-900 text-white' 
                              : 'bg-white border-slate-200 text-slate-600 hover:border-slate-300'
                          }`}
                        >
                          <CheckCircle2 className={`w-3.5 h-3.5 ${isDone ? 'text-white' : 'text-slate-300'}`} />
                          <span>Anchor #{itemIdx + 1}</span>
                        </button>
                      );
                    })}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* TAB 3: POSITIVE AFFIRMATIONS */}
      {activeSubTab === 'affirmations' && (
        <div className="card-surface p-8 text-center space-y-6">
          <div className="max-w-md mx-auto space-y-1">
            <h3 className="text-base font-bold text-slate-900">Cognitive Self-Affirmation</h3>
            <p className="text-xs text-slate-500 leading-relaxed">
              Evidence-based cognitive restructuring prompts to support emotional resilience.
            </p>
          </div>

          <div className="max-w-lg mx-auto p-8 rounded-xl bg-slate-50 border border-slate-200 space-y-3">
            <span className="text-[11px] font-mono text-slate-400 uppercase tracking-widest block">
              Prompt #{currentAffirmationIndex + 1}
            </span>
            <p className="text-base sm:text-lg font-semibold text-slate-900 leading-relaxed">
              "{AFFIRMATION_LIST[currentAffirmationIndex]}"
            </p>
          </div>

          <div className="pt-2">
            <button
              onClick={shuffleAffirmation}
              className="px-5 py-2.5 rounded-lg bg-slate-900 hover:bg-slate-800 text-white font-medium text-xs transition-colors inline-flex items-center gap-2"
            >
              <Shuffle className="w-3.5 h-3.5" />
              <span>Next Supportive Prompt</span>
            </button>
          </div>
        </div>
      )}

    </div>
  );
}
