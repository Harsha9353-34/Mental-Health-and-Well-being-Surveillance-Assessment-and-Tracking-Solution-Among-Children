import React, { useState } from 'react';
import { 
  PhoneCall, 
  Copy, 
  Check, 
  ShieldAlert, 
  ChevronDown,
  ChevronUp,
  AlertCircle
} from 'lucide-react';

const CRISIS_DATA = [
  {
    name: "Childline / Child Helpline India",
    number: "1098",
    badge: "24/7 Toll-Free",
    desc: "National 24-hour emergency phone outreach service for children in distress. Ministry of Women and Child Development, Government of India."
  },
  {
    name: "Tele-MANAS (Mental Health Helpline)",
    number: "14416",
    alt_number: "1800-891-4416",
    badge: "Government of India",
    desc: "National tele-mental health programme providing round-the-clock psychological first aid and counseling support in 20+ Indian languages."
  },
  {
    name: "NIMHANS Outpatient & Crisis Support",
    number: "+91-80-46110007",
    badge: "Apex Psychiatric Institute",
    desc: "Specialized child & adolescent psychiatric consultations, psychological assessment, and family counseling in Bengaluru, Karnataka."
  },
  {
    name: "iCall Psychosocial Helpline (TISS)",
    number: "+91-9152987821",
    badge: "Mon–Sat, 10 AM–8 PM",
    desc: "Free and confidential telephone and email counseling support operated by the Tata Institute of Social Sciences."
  },
];

const PROTOCOL_STEPS = [
  {
    step: 1,
    title: "Maintain Calm Demeanor & Regulated Presence",
    desc: "Your emotional regulation sets the safety boundary for the child. Avoid raising your voice, displaying panic, or expressing frustration."
  },
  {
    step: 2,
    title: "Ensure Continuous, Uninterrupted Supervision",
    desc: "Never leave a child expressing acute despair or crisis unattended. Maintain continuous physical presence in a quiet, safe environment."
  },
  {
    step: 3,
    title: "Practice Active, Non-Judgmental Listening",
    desc: "Acknowledge feelings without offering immediate dismissals or quick fixes. Say: 'I am here with you, your feelings are important, and we will work through this together.'"
  },
  {
    step: 4,
    title: "Contact Verified National Helplines",
    desc: "Dial Childline (1098) or Tele-MANAS (14416) for guidance from certified counselors trained in crisis de-escalation protocols."
  },
  {
    step: 5,
    title: "Coordinate Clinical Evaluation",
    desc: "Schedule an evaluation with a licensed child psychologist, developmental pediatrician, or psychiatrist. This prototype does not substitute clinical therapy."
  }
];

export default function CrisisResources() {
  const [copiedNumber, setCopiedNumber] = useState(null);
  const [openStep, setOpenStep] = useState(0);

  const handleCopy = (num) => {
    navigator.clipboard.writeText(num);
    setCopiedNumber(num);
    setTimeout(() => setCopiedNumber(null), 2000);
  };

  return (
    <div className="max-w-3xl mx-auto py-4 space-y-6">
      
      {/* Page Title */}
      <div className="space-y-1">
        <div className="inline-flex items-center gap-1.5 text-xs font-semibold text-rose-700 uppercase tracking-wider">
          <ShieldAlert className="w-3.5 h-3.5 text-rose-600" />
          <span>Emergency Referral Pathways</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
          Crisis Support &amp; Verified Helplines
        </h1>
        <p className="text-xs text-slate-500 leading-relaxed">
          National mental health and emergency resources verified as of September 2026.
        </p>
      </div>

      {/* Immediate Emergency Callout */}
      <div className="p-5 rounded-xl bg-rose-700 text-white flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="space-y-1">
          <div className="flex items-center gap-2 font-bold text-sm">
            <AlertCircle className="w-4 h-4" />
            <span>Immediate Danger / Life-Threatening Crisis</span>
          </div>
          <p className="text-xs text-rose-100">
            Contact National Emergency Services immediately. Toll-free 24/7.
          </p>
        </div>
        <a
          href="tel:112"
          className="px-5 py-2.5 rounded-lg bg-white text-rose-900 font-bold text-xs hover:bg-rose-50 transition-colors self-start sm:self-auto shrink-0"
        >
          Call 112 (Emergency)
        </a>
      </div>

      {/* Verified Helplines Grid */}
      <div className="space-y-3">
        <h3 className="font-semibold text-sm text-slate-900">
          Verified National Helplines (India)
        </h3>
        
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
          {CRISIS_DATA.map((h, i) => (
            <div key={i} className="card-surface p-5 space-y-3 flex flex-col justify-between">
              <div className="space-y-1.5">
                <div className="flex items-center justify-between">
                  <span className="text-[11px] font-medium px-2 py-0.5 rounded bg-slate-100 text-slate-600 border border-slate-200">
                    {h.badge}
                  </span>
                </div>
                <h4 className="font-semibold text-sm text-slate-900">{h.name}</h4>
                <div className="text-xl font-bold font-mono text-slate-900">
                  <a href={`tel:${h.number.replace(/[^0-9+]/g, '')}`} className="hover:underline">
                    {h.number}
                  </a>
                  {h.alt_number && (
                    <span className="text-xs font-normal text-slate-500 ml-1">/ {h.alt_number}</span>
                  )}
                </div>
                <p className="text-xs text-slate-500 leading-relaxed">{h.desc}</p>
              </div>

              <div className="flex items-center gap-2 pt-2 border-t border-slate-100">
                <a
                  href={`tel:${h.number.replace(/[^0-9+]/g, '')}`}
                  className="flex-1 py-1.5 px-3 rounded-lg bg-slate-900 hover:bg-slate-800 text-white font-medium text-xs flex items-center justify-center gap-1.5 transition-colors"
                >
                  <PhoneCall className="w-3 h-3" />
                  <span>Call</span>
                </a>
                <button
                  onClick={() => handleCopy(h.number)}
                  className="py-1.5 px-3 rounded-lg border border-slate-200 hover:bg-slate-50 text-slate-700 text-xs font-medium flex items-center gap-1 transition-colors"
                  title="Copy helpline number"
                >
                  {copiedNumber === h.number ? <Check className="w-3 h-3 text-emerald-600" /> : <Copy className="w-3 h-3" />}
                  <span>{copiedNumber === h.number ? "Copied" : "Copy"}</span>
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Step-by-Step Caregiver Protocol */}
      <div className="card-surface p-6 space-y-4">
        <div>
          <h3 className="font-semibold text-sm text-slate-900">
            Caregiver Crisis Response Protocol
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">
            Sequential guidelines recommended when managing acute pediatric distress.
          </p>
        </div>

        <div className="space-y-2">
          {PROTOCOL_STEPS.map((s, idx) => {
            const isOpen = openStep === idx;
            return (
              <div key={idx} className="border border-slate-200 rounded-lg overflow-hidden">
                <button
                  onClick={() => setOpenStep(isOpen ? -1 : idx)}
                  className="w-full p-3 text-left flex items-center justify-between text-xs font-semibold text-slate-800 hover:bg-slate-50 transition-colors"
                >
                  <span className="flex items-center gap-2">
                    <span className="font-mono text-slate-400">0{s.step}.</span>
                    <span>{s.title}</span>
                  </span>
                  {isOpen ? <ChevronUp className="w-3.5 h-3.5 text-slate-400" /> : <ChevronDown className="w-3.5 h-3.5 text-slate-400" />}
                </button>
                {isOpen && (
                  <div className="px-3 pb-3 text-xs text-slate-600 leading-relaxed border-t border-slate-100 pt-2 bg-slate-50/50">
                    {s.desc}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

    </div>
  );
}
