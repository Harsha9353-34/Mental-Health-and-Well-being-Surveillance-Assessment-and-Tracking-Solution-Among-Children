# Mental Health and Well-being Surveillance, Assessment and Tracking Solution Among Children

## Project Overview

This project focuses on the design and full implementation of **MindBridge** — an intelligent, child-centered digital platform for early mental health and well-being surveillance, assessment, longitudinal tracking, and verified support referral among children and adolescents.

The platform combines a low-cognitive-load interface (single-tap emoji mood check-ins and an optional reflective journal) with a dual-modality intelligence pipeline: (1) supervised machine learning classification for non-diagnostic lifestyle risk stratification (*Low / Healthy*, *Moderate / Monitoring*, *Elevated / Action Advised*), and (2) natural language processing (NLP) for emotional valence and affective tone scoring. Caregivers receive explainable longitudinal trend dashboards alongside verified emergency crisis referral pathways.

## Student

Harsha R

## USN

20231CSE0261

## Guide

Mr. Jetti Satya Sai Kumar

## University

Presidency University, Bengaluru

## Degree

B.Tech – Computer Science and Engineering

## Academic Year

2026–2027

---

## Phase 1 — Design & Literature Defense (Complete ✅)

- **Literature Review:** Critical survey of 10 peer-reviewed papers and epidemiological surveillance frameworks (WHO, CDC MMWR, JCPP, JMIR, CMPB).
- **Research Gap Analysis:** Formulation of 4 distinct opportunities spanning age-appropriate interaction, multi-modal synthesis, continuous tracking, and crisis integration.
- **Problem Statement & Scope:** Clear boundaries distinguishing non-clinical surveillance from medical diagnosis.
- **System Architecture:** 5-tier architecture design (Presentation, Application Logic, ML/NLP Intelligence, Data Persistence, External Referral).
- **Data Flow Design:** Comprehensive Level 0 and Level 1 DFDs mapping child check-in to role-based analytics.
- **Privacy & Ethics:** Privacy-by-design framework aligned with Section 9 of India's Digital Personal Data Protection Act, 2023 (DPDP Act 2023).

## Phase 2 — Full Application Implementation (Complete ✅)

- **Child Interactive Portal:** Emoji mood picker + lifestyle sliders + optional reflective journal.
- **ML Risk Classifier:** Random Forest (200 trees, StandardScaler, 5-fold CV) — 77.25% CV accuracy, 0.88 weighted F1, perfect recall on Elevated Risk tier.
- **NLP Sentiment Engine:** VADER SentimentIntensityAnalyzer — local processing, no data transmission.
- **Coping Toolkit:** Animated 4-7-8 breathing pacer (HTML/CSS/JS), 5-4-3-2-1 grounding exercise, affirmation cards.
- **Guardian Dashboard:** Longitudinal trend charts, rolling averages, distress alerts — privacy-preserving (no journal text shown).
- **Crisis Referral:** Childline 1098, Tele-MANAS 14416, NIMHANS, iCall TISS.
- **Research Paper Draft:** IEEE-format paper ready for submission.

---

## How to Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Generate synthetic training data (already done — data/synthetic_checkins.csv)
python src/data/generate_dataset.py

# 3. Train the ML classifier (already done — models/risk_classifier.pkl)
python src/ml/train.py

# 4. Launch the Streamlit application
streamlit run app.py
```

Then open http://localhost:8501 in your browser.

---

## Repository Structure

```
/
├── README.md
├── .gitignore
├── requirements.txt                               # Python dependencies
├── app.py                                         # Main Streamlit entry point
│
├── src/
│   ├── data/
│   │   ├── schema.py                              # Feature definitions, mood labels, risk tiers, constants
│   │   └── generate_dataset.py                   # Synthetic 2000-record training data generator
│   ├── ml/
│   │   ├── train.py                               # Random Forest training + 5-fold CV + serialization
│   │   ├── predict.py                             # Inference wrapper (singleton model loading)
│   │   └── explainer.py                           # Feature importance plots + plain-English explanations
│   ├── nlp/
│   │   └── sentiment.py                           # VADER sentiment wrapper
│   ├── ui/
│   │   ├── checkin.py                             # Child check-in page
│   │   ├── coping.py                              # Coping toolkit (breathing + grounding + affirmations)
│   │   ├── dashboard.py                           # Guardian longitudinal dashboard
│   │   └── crisis.py                              # Crisis referral resources page
│   └── utils/
│       ├── storage.py                             # CSV-based check-in history (no PII)
│       └── session.py                             # Streamlit session state management
│
├── models/
│   └── risk_classifier.pkl                       # Serialised sklearn Pipeline (trained)
│
├── data/
│   └── synthetic_checkins.csv                    # Synthetic training dataset (2000 records)
│
├── docs/
│   └── Review_1_Mini_Project_Presentation.pptx  # Phase 1 review presentation
│
├── report/
│   ├── Phase_1_Project_Report.md                 # Complete Phase 1 academic report
│   └── Phase_2_Research_Paper_Draft.md           # IEEE-format research paper draft
│
└── diagrams/
    ├── system_architecture.png                   # 5-tier system architecture diagram
    ├── data_flow_diagram.png                     # End-to-end data flow diagram
    └── mental_health_project_gantt_chart.png     # Phase 1 Gantt chart
```

## Technology Stack

| Component | Technology |
|---|---|
| Web Framework | Streamlit ≥ 1.35 |
| ML Library | scikit-learn ≥ 1.4 (Random Forest + StandardScaler) |
| NLP Library | vaderSentiment ≥ 3.3.2 (VADER) |
| Data Processing | pandas ≥ 2.1, NumPy ≥ 1.26 |
| Visualisation | Plotly ≥ 5.20 |
| Model Serialisation | joblib ≥ 1.3 |
| Language | Python 3.11 |

## Disclaimer

This is an academic engineering prototype and is **NOT** a medical diagnostic system. Machine learning (ML) and natural language processing (NLP) outputs are non-clinical computational estimates and do not replace professional medical or psychiatric evaluation. If a child exhibits persistent distress or acute crisis, consultation with a qualified pediatrician, licensed child psychologist, or verified emergency child helpline is required.

**Emergency Helplines (India):** Childline **1098** | Tele-MANAS **14416** | Emergency **112**


## Project Overview

This project focuses on the conceptualization, architectural design, and preliminary specification of an intelligent, child-centered digital platform for early mental health and well-being surveillance, assessment, longitudinal tracking, and verified support referral among children and adolescents. 

Emerging pediatric emotional distress often manifests through observable lifestyle and behavioral shifts (such as chronic sleep insufficiency, high sedentary screen exposure, academic strain, and social withdrawal). The proposed solution combines an engaging, low-cognitive-load interface (single-tap emoji mood check-ins and an optional reflective journal) with a dual-modality intelligence pipeline: (1) supervised machine learning classification for non-diagnostic lifestyle risk stratification (*Low / Healthy*, *Moderate / Monitoring*, *Elevated / Action Advised*), and (2) natural language processing (NLP) for emotional valence and affective tone scoring. The platform bridges early distress surveillance with immediate, non-clinical psychoeducational calming tools (visual 4-7-8 breathing pacers and grounding exercises) and provides caregivers with explainable longitudinal trend dashboards alongside verified emergency crisis referral pathways.

## Students

| Name | USN |
|---|---|
| Harsha R | 20231CSE0261 |
| ARJUN M | 20231CSE0277 |
| ABHISHEK MR | 20231CSE0268 |

## Guide

Mr. Jetti Satya Sai Kumar

## University

Presidency University

## Degree

B.Tech – Computer Science and Engineering

## Project Phase

Phase 1 – Major Project Design & Literature Defense

## Domain

Applied Artificial Intelligence, Health Informatics, Human-Computer Interaction

## Phase 1 Contents

- **Literature Review:** Critical survey of 10 peer-reviewed papers and epidemiological surveillance frameworks (WHO, CDC MMWR, JCPP, JMIR, CMPB).
- **Research Gap Analysis:** Formulation of 4 distinct opportunities spanning age-appropriate interaction, multi-modal synthesis, continuous tracking, and crisis integration.
- **Problem Statement & Scope:** Clear boundaries distinguishing non-clinical surveillance from medical diagnosis.
- **System Architecture:** 5-tier architecture design (Presentation, Application Logic, ML/NLP Intelligence, Data Persistence, External Referral).
- **Data Flow Design:** Comprehensive Level 0 and Level 1 DFDs mapping child check-in to role-based analytics.
- **Privacy & Ethics:** Privacy-by-design framework aligned with Section 9 of India's Digital Personal Data Protection Act, 2023 (DPDP Act 2023).
- **Expected System Outputs:** Specifications for child check-in, ML risk tiers, NLP indicators, coping tools, guardian dashboard, and crisis resources.
- **Project Timeline:** 24-week Work Breakdown Structure (WBS) and milestone roadmap across Phase 1 and Phase 2.

## Repository Structure

```
/
├── README.md                                             # Main project overview and academic metadata
├── .gitignore                                            # Git ignore rules for environments and temporary files
│
├── docs/
│   └── Phase_1_Project_Report_Harsha_R_20231CSE0261.docx # Final university-submission-ready Word report
├── report/
│   └── Phase_1_Project_Report.md                         # Complete academic Phase 1 report in Markdown format
└── diagrams/
    ├── system_architecture.png                           # Publication-quality 5-tier system architecture diagram
    └── data_flow_diagram.png                             # End-to-end data flow and decision-support pipeline diagram
```

### Folder Purpose Description:
* **`docs/`**: Contains the official, submission-ready Microsoft Word document (`.docx`) compiled with Presidency University cover page, formatted tables, embedded high-resolution figures, callout disclaimer boxes, and academic typography.
* **`report/`**: Contains the complete master academic Phase 1 project report in GitHub-flavored Markdown for web viewing and version tracking.
* **`diagrams/`**: Houses high-resolution (300 DPI) system architecture and data flow diagrams embedded within the project documentation.

## Disclaimer

This is an academic engineering prototype and is **NOT** a medical diagnostic system. Machine learning (ML) and natural language processing (NLP) outputs are non-clinical computational estimates and do not replace professional medical or psychiatric evaluation. If a child exhibits persistent distress or acute crisis, consultation with a qualified pediatrician, licensed child psychologist, or verified emergency child helpline is required.
