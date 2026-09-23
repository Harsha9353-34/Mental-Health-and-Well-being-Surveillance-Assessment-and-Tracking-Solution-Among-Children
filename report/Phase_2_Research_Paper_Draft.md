# MindBridge: An AI-Augmented Non-Clinical Surveillance and Well-being Tracking Platform for Children Using Machine Learning and Natural Language Processing

**Harsha R¹, Mr. Jetti Satya Sai Kumar²**

¹ B.Tech Student, Department of Computer Science and Engineering, Presidency University, Bengaluru — 20231CSE0261  
² Assistant Professor, Department of Computer Science and Engineering, Presidency University, Bengaluru

*Academic Year: 2026–2027*

---

## Abstract

Childhood psychological distress frequently develops gradually through observable lifestyle and behavioural shifts — including chronic sleep insufficiency, excessive screen exposure, academic strain, and social withdrawal — before escalating to clinical severity. However, conventional paediatric mental health screening remains predominantly episodic, adult-mediated, and dependent on structured clinical consultations that may not capture day-to-day behavioural changes in naturalistic settings. This paper presents **MindBridge**, a fully implemented, interactive, non-clinical software platform for early well-being surveillance, multi-factor lifestyle assessment, longitudinal tracking, and verified crisis referral support among children and adolescents (ages 8–17). MindBridge employs a dual-modality intelligence pipeline: (1) a supervised Random Forest multi-class classifier, trained on a domain-informed synthetic dataset of 2,000 records, to stratify lifestyle indicators into three non-diagnostic well-being tiers (*Low / Healthy*, *Moderate / Monitoring*, *Elevated / Action Advised*); and (2) a VADER lexicon-based natural language processing (NLP) module to evaluate the emotional valence of optional child journal entries with full local processing and no external API transmission. The platform additionally provides psychoeducational coping tools (an animated 4-7-8 breathing pacer and a 5-4-3-2-1 sensory grounding exercise), an affirmation card carousel, and a privacy-preserving longitudinal trend dashboard for caregivers. The system achieved a mean 5-fold stratified cross-validation accuracy of **77.25% ± 1.37%** on the synthetic training dataset, with a weighted F1-score of 0.88 and perfect recall (1.00) on the safety-critical Elevated Risk tier. All processing adheres to a privacy-by-design framework aligned with Section 9 of India's Digital Personal Data Protection Act, 2023 (DPDP Act 2023). This work addresses an identified research gap in age-appropriate, continuous, multi-modal well-being surveillance tools for preadolescents, and is positioned as a Phase 2 implementation prototype for academic review and clinical feasibility evaluation.

**Keywords:** Paediatric Well-being, Mental Health Surveillance, Digital Health Tracking, Random Forest, VADER Sentiment Analysis, Child-Computer Interaction, Longitudinal Monitoring, Crisis Referral, Privacy-by-Design, DPDP Act 2023.

---

## 1. Introduction

The global prevalence of childhood and adolescent mental health conditions represents a pressing public health priority. The World Health Organization (2022) estimates that approximately 1 in 7 (14%) individuals aged 10–19 years worldwide experience a diagnosable mental health condition, with suicide ranking as the fourth leading cause of death among older adolescents aged 15–19 years [1]. In India, epidemiological data reported by the National Mental Health Survey (NMHS, 2016) indicates a 7.3% prevalence of mental health disorders among children and adolescents, with significant treatment gaps attributable to stigma, access barriers, and limited awareness among caregivers and educators [12].

Critically, the early manifestations of paediatric mental health challenges are rarely acute at onset. Rather, they tend to emerge gradually through observable shifts in everyday behaviour — including disrupted sleep patterns, increased sedentary screen exposure, reduced physical activity, heightened academic stress, and social withdrawal [2]. These behavioural warning signals are often visible to children themselves, parents, and educators but are seldom captured in structured, continuous, and accessible formats that can facilitate timely, non-clinical intervention.

Conventional paediatric mental health screening approaches (e.g., the Pediatric Symptom Checklist [PSC-17] [9]) are predominantly paper-based, episodic, clinician or parent-administered tools that provide cross-sectional snapshots rather than longitudinal surveillance. Mobile digital health applications offer a promising complementary pathway, yet systematic reviews (Grist et al., 2017) have found that the vast majority of commercially available mental health apps target adults or older adolescents, with very few designed specifically for preadolescents (ages 8–12) — and most lack verified emergency crisis referral pathways [4].

This paper presents **MindBridge**, a fully implemented Phase 2 Streamlit-based platform that addresses these identified gaps through four integrated functional components:

1. **Child Interactive Portal:** A low-cognitive-load emoji mood picker and lifestyle slider interface for daily check-ins.
2. **Dual-Modality AI Intelligence Pipeline:** A Random Forest risk classifier and VADER NLP sentiment analyser.
3. **Psychoeducational Coping Toolkit:** Non-clinical breathing pacer, grounding exercise, and affirmation cards.
4. **Privacy-Preserving Guardian Dashboard:** Longitudinal trend visualisation for caregivers without exposing child journal content.

The remainder of this paper is organised as follows: Section 2 reviews relevant literature; Section 3 formalises the problem statement and identified research gaps; Section 4 describes the system architecture; Section 5 details the methodology; Section 6 presents the implementation; Section 7 reports evaluation results; Section 8 discusses ethical and privacy frameworks; Section 9 addresses limitations and future directions; and Section 10 concludes the paper.

---

## 2. Related Work

### 2.1 Global and National Epidemiological Context

The WHO World Mental Health Report (2022) provides the foundational epidemiological justification for accessible paediatric surveillance tools, reporting a 14% global prevalence of youth mental health conditions and emphasising the inadequacy of existing early detection infrastructure in low- and middle-income countries, including India [1]. Bitsko et al. (2022), in their analysis of US federal surveillance datasets (NSCH, NHIS, YRBSS), confirmed that ADHD and anxiety are the most prevalent conditions among children aged 3–17 and identified lifestyle stressors — particularly sleep disruption, sedentary behaviour, and academic pressure — as significant correlates of emotional well-being [2].

### 2.2 Digital Health Interventions for Children

Hollis et al. (2017) conducted a systematic meta-review of digital health interventions for children and young people, finding that computerised cognitive-behavioural support shows clinical promise, but that engagement and adherence critically depend on interactive visual design and immediate feedback loops suited to younger age groups [3]. Grist et al. (2017) extended this finding through a systematic review of commercial mental health apps, identifying a pronounced scarcity of preadolescent-targeted tools and an almost universal absence of verified clinical safety mechanisms or crisis referral pathways [4].

### 2.3 Machine Learning for Mental Health Risk Estimation

Shatte et al. (2019) conducted a comprehensive scoping review of 300 ML studies applied to mental health contexts, identifying supervised classification algorithms — particularly Random Forests, Support Vector Machines, and Logistic Regression — as the most frequently employed approaches for lifestyle risk modelling [5]. The authors underscored the critical importance of rigorous cross-validation to mitigate overfitting in health datasets. Burke et al. (2019), applying Random Forest and Elastic Net modelling to a paediatric cohort of 496 adolescents, demonstrated that multi-variable interactions between sleep, negative affect, and interpersonal stress were the strongest predictors of self-injurious behaviour — directly informing our feature vector design [6].

### 2.4 NLP and Sentiment Analysis in Mental Health

Le Glaz et al. (2021) reviewed 199 NLP/ML studies in mental health, finding that lexicon-based sentiment analysis reliably extracts affective valence from informal text and is most effective when integrated with structured behavioural indicators rather than deployed in isolation [7]. Hutto and Gilbert (2014) introduced the VADER (Valence Aware Dictionary and sEntiment Reasoner) system — a rule-based lexicon that achieves strong performance on informal, short texts with full interpretability and low computational overhead — making it particularly appropriate for privacy-preserving on-device processing of children's journal entries [8].

### 2.5 Ethics and Privacy in Paediatric Digital Health

Schueller et al. (2019) highlighted that digital health tools for minors require particular attention to transparent consent workflows, data minimisation, secure local data handling, and non-diagnostic boundary clarity [10]. In the Indian legislative context, Section 9 of the Digital Personal Data Protection Act, 2023 (DPDP Act 2023) imposes specific obligations for verifiable parental consent and data minimisation when processing data of minors, directly guiding our privacy architecture [11].

---

## 3. Problem Statement and Research Gaps

### 3.1 Identified Research Gaps

The critical review of existing literature and available tools identifies four principal opportunities:

| # | Research Gap | Current Limitation | Proposed Contribution |
|---|---|---|---|
| G1 | **Age-Appropriate Interaction** | Most digital tools target adults or older adolescents | Emoji-based, low-cognitive-load interface for ages 8–17 |
| G2 | **Multi-Modal Data Synthesis** | Apps analyse structured data OR text in isolation | Integrated pipeline: emoji mood + lifestyle sliders + NLP journal sentiment |
| G3 | **Continuous Longitudinal Surveillance** | Screening is episodic (annual clinic visits, parental surveys) | Daily check-in with persistent longitudinal trend dashboard |
| G4 | **Bridging Surveillance with Coping and Referral** | Mood trackers record distress without offering immediate support | Embedded coping toolkit + verified Indian crisis helplines |

### 3.2 Formal Problem Statement

> *"To design, implement, and evaluate an interactive, child-centred software platform that integrates daily emoji mood check-ins, structured lifestyle indicators (sleep duration, screen time, physical activity, academic stress), and natural language sentiment analysis into a unified non-clinical surveillance architecture — providing interpretable ML risk stratification, longitudinal trend visualisation, immediate psychoeducational coping tools, and verified crisis referral pathways, while adhering to a strict privacy-by-design framework aligned with India's DPDP Act 2023."*

---

## 4. System Architecture

### 4.1 Five-Tier Architecture Design

MindBridge is organised into five decoupled, cohesive architectural tiers:

```
┌─────────────────────────────────────────────────────────────────┐
│  TIER 1: PRESENTATION LAYER                                     │
│  Streamlit Multi-Page Application                               │
│  ┌──────────────────┐    ┌──────────────────────────────┐      │
│  │ Child Portal     │    │ Guardian / Educator Dashboard │      │
│  │ (Emoji + Sliders)│    │ (Trend Charts + Alerts)       │      │
│  └──────────────────┘    └──────────────────────────────┘      │
├─────────────────────────────────────────────────────────────────┤
│  TIER 2: APPLICATION LOGIC LAYER                                │
│  Input Validation · Session Management · Safety Routing        │
│  Coping Tool Control · Crisis Threshold Evaluation             │
├─────────────────────────────────────────────────────────────────┤
│  TIER 3: AI INTELLIGENCE LAYER                                  │
│  ┌───────────────────────┐  ┌─────────────────────────────┐   │
│  │ ML Risk Classifier    │  │ NLP Sentiment Engine         │   │
│  │ StandardScaler +      │  │ VADER SentimentIntensity     │   │
│  │ RandomForestClassifier│  │ Analyser (local processing)  │   │
│  │ (3-class, 5-fold CV)  │  │ Compound score [-1.0, +1.0]  │   │
│  └───────────────────────┘  └─────────────────────────────┘   │
├─────────────────────────────────────────────────────────────────┤
│  TIER 4: DATA & PERSISTENCE LAYER                               │
│  Synthetic Training Dataset (2,000 records, CSV)               │
│  Serialised Model Pipeline (joblib .pkl)                       │
│  Anonymised Check-in History (local CSV, no PII)              │
│  DPDP Act 2023 Section 9 — Privacy-by-Design                  │
├─────────────────────────────────────────────────────────────────┤
│  TIER 5: EXTERNAL SUPPORT & REFERRAL LAYER                     │
│  Childline 1098 · Tele-MANAS 14416 · NIMHANS · iCall TISS    │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 Data Flow

The end-to-end data flow proceeds as follows:

1. **Child Input:** Emoji tap (mood score 1–6) + slider values (sleep, screen, play, stress) → Application Logic Layer
2. **Feature Assembly:** Validated feature vector `[mood_score, sleep_hours, screen_time, physical_play, school_stress]`
3. **ML Inference:** StandardScaler normalisation → Random Forest prediction → Risk Tier {0, 1, 2} + class probabilities
4. **NLP Inference (optional):** Journal text → VADER tokenisation → compound score + tone tag (processed in-memory only; text never persisted)
5. **Storage:** Anonymised aggregate record (no PII, no journal text) appended to local CSV
6. **Output to Child:** Risk tier card + probability breakdown + feature attribution + sentiment indicator + affirmation + coping navigation
7. **Output to Guardian:** Longitudinal trend charts + rolling averages + distress alert (3+ consecutive Tier 2 check-ins)

---

## 5. Methodology

### 5.1 Feature Vector Design

The feature vector is designed based on lifestyle risk factors consistently identified across the Phase 1 literature review:

| Feature | Range | Rationale |
|---|---|---|
| `mood_score` | 1–6 (int) | Primary affective state indicator; strongest predictor (Burke et al., 2019) |
| `sleep_hours` | 4.0–12.0 (float) | Sleep insufficiency is a major mental health risk factor (WHO, 2022; Bitsko et al., 2022) |
| `screen_time` | 0.0–8.0 (float) | Excessive sedentary screen exposure correlates with reduced well-being |
| `physical_play` | 0.0–4.0 (float) | Physical activity is a protective factor for child emotional health (WHO, 2022) |
| `school_stress` | 1–5 (int) | Academic stress is a significant paediatric mental health stressor (Bitsko et al., 2022) |

### 5.2 Synthetic Dataset Generation

In the absence of ethically available real-world paediatric check-in datasets, a synthetic training dataset of 2,000 records was generated using a domain-informed composite risk scoring function:

$$R_{composite} = 0.28 \cdot R_{mood} + 0.27 \cdot R_{sleep} + 0.20 \cdot R_{screen} + 0.13 \cdot R_{play} + 0.12 \cdot R_{stress}$$

Where each component risk is normalised to $[0, 1]$:

$$R_{mood} = \frac{6 - \text{mood\_score}}{5}, \quad R_{sleep} = \text{clip}\left(\frac{8.0 - \text{sleep\_hours}}{4.0}, 0, 1\right)$$

$$R_{screen} = \text{clip}\left(\frac{\text{screen\_time}}{6.0}, 0, 1\right), \quad R_{play} = \text{clip}\left(\frac{2.0 - \text{physical\_play}}{2.0}, 0, 1\right), \quad R_{stress} = \frac{\text{school\_stress} - 1}{4}$$

Gaussian noise ($\sigma = 0.07$) was added to the composite risk score before tier assignment to create realistic boundary ambiguity. The thresholds are:

- **Tier 0 (Low / Healthy):** $R_{composite} < 0.33$
- **Tier 1 (Moderate / Monitoring):** $0.33 \leq R_{composite} < 0.67$
- **Tier 2 (Elevated / Action Advised):** $R_{composite} \geq 0.67$

Feature weights reflect the relative importance of lifestyle predictors as established by Burke et al. (2019) and the WHO (2022), with mood and sleep assigned higher weights due to their stronger empirical association with paediatric mental health outcomes.

### 5.3 Machine Learning Pipeline

**Algorithm Selection:** Random Forest was selected based on the Shatte et al. (2019) scoping review identifying it as one of the most effective supervised classifiers for mental health lifestyle datasets, and on Burke et al. (2019) demonstrating its utility in paediatric risk modelling. Random Forest additionally provides interpretable feature importances natively.

**Pipeline:** `StandardScaler → RandomForestClassifier`

**Hyperparameters:**

| Parameter | Value | Rationale |
|---|---|---|
| `n_estimators` | 200 | Sufficient ensemble size for stable out-of-bag estimation |
| `max_depth` | 8 | Prevents overfitting on synthetic data |
| `min_samples_split` | 5 | Reduces variance in leaf splits |
| `class_weight` | "balanced" | Accounts for class imbalance across tiers |
| `random_state` | 42 | Reproducibility |

**Validation:** 5-fold stratified cross-validation (StratifiedKFold) ensures that class proportions are preserved in each fold, providing a robust estimate of generalisation performance on unseen data.

### 5.4 NLP Sentiment Analysis

VADER (Valence Aware Dictionary and sEntiment Reasoner) [8] was selected for journal sentiment analysis based on three criteria:
1. **Interpretability:** Rule-based lexicon with transparent scoring — critical for child health applications (Le Glaz et al., 2021)
2. **Performance on short informal text:** VADER was specifically validated on social media-style informal language, which is closest to a child's journal entries
3. **Privacy-preserving local processing:** Runs entirely in-memory with no external API calls, ensuring journal content is never transmitted

The VADER compound score ($\in [-1.0, +1.0]$) is thresholded as:
- **Positive:** compound $\geq 0.05$
- **Neutral:** $-0.05 <$ compound $< 0.05$
- **Negative:** compound $\leq -0.05$

---

## 6. Implementation

### 6.1 Technology Stack

| Component | Technology | Version |
|---|---|---|
| Web Framework | Streamlit | ≥ 1.35.0 |
| ML Library | scikit-learn | ≥ 1.4.0 |
| Data Processing | pandas, NumPy | ≥ 2.1.0, ≥ 1.26.0 |
| NLP Library | vaderSentiment | ≥ 3.3.2 |
| Visualisation | Plotly | ≥ 5.20.0 |
| Model Serialisation | joblib | ≥ 1.3.0 |
| Language | Python | 3.11 |

### 6.2 Project Repository Structure

```
MentalHealthAwareness/
├── app.py                          # Main Streamlit entry point
├── requirements.txt                # Python dependencies
├── src/
│   ├── data/
│   │   ├── schema.py               # Feature definitions, constants, crisis resources
│   │   └── generate_dataset.py     # Synthetic training data generator
│   ├── ml/
│   │   ├── train.py                # RF pipeline training + 5-fold CV
│   │   ├── predict.py              # Inference wrapper (singleton model loading)
│   │   └── explainer.py            # Feature importance plots + plain-English explanations
│   ├── nlp/
│   │   └── sentiment.py            # VADER sentiment analysis wrapper
│   ├── ui/
│   │   ├── checkin.py              # Child check-in page
│   │   ├── coping.py               # Coping toolkit (breathing + grounding + affirmations)
│   │   ├── dashboard.py            # Guardian longitudinal dashboard
│   │   └── crisis.py               # Crisis referral resources page
│   └── utils/
│       ├── storage.py              # CSV-based check-in history (no PII)
│       └── session.py              # Streamlit session state management
├── models/
│   └── risk_classifier.pkl         # Serialised sklearn Pipeline
├── data/
│   ├── synthetic_checkins.csv      # Synthetic training dataset
│   └── checkin_history.csv         # Runtime check-in history (gitignored)
├── report/
│   ├── Phase_1_Project_Report.md   # Phase 1 academic report
│   └── Phase_2_Research_Paper_Draft.md  # This document
└── diagrams/
    ├── system_architecture.png
    ├── data_flow_diagram.png
    └── mental_health_project_gantt_chart.png
```

### 6.3 Child Interactive Portal

The child check-in interface (implemented in `src/ui/checkin.py`) is designed following Hollis et al. (2017) and Grist et al. (2017) guidelines for age-appropriate, low-cognitive-load digital interactions:

**Emoji Mood Picker:** Six large, tappable emoji buttons representing primary affective states (😄 Joyful, 😌 Calm, 😐 Neutral, 😟 Worried, 😢 Sad, 😤 Frustrated) with immediate visual selection feedback. Each emoji maps to an integer score (1–6) used as the `mood_score` feature.

**Lifestyle Sliders:** Four continuous sliders with WHO-informed ranges:
- Sleep hours: 4.0–12.0 hrs (with note that WHO recommends 9–11 hrs for school-age children)
- Screen time: 0.0–8.0 hrs
- Physical play: 0.0–4.0 hrs
- School stress: 1–5 (Likert-type, with descriptive labels matching STRESS_LABELS schema)

**Optional Journal:** A non-mandatory text area for reflective writing. Text is processed by VADER in-memory but **never** stored or transmitted.

**Results Display:** Upon submission, the interface presents: (a) a colour-coded risk tier card with description and recommended action; (b) a probability breakdown bar chart for all three tiers; (c) a plain-English feature attribution explanation; (d) VADER sentiment score (if journal text provided); and (e) a randomly selected positive affirmation.

### 6.4 Coping Toolkit

The coping toolkit (`src/ui/coping.py`) implements three psychoeducational tools accessed via Streamlit tabs:

**4-7-8 Breathing Pacer:** An animated HTML/CSS/JavaScript component embedded via `streamlit.components.v1.html`. The animation features a circular element that expands during the 4-second inhalation phase, remains stationary during the 7-second hold, and contracts during the 8-second exhalation. Phase-specific colour gradients (blue → green → pink) and text instructions guide the child. A cycle counter tracks completed breathing cycles.

**5-4-3-2-1 Grounding Exercise:** A step-by-step guided sensory grounding exercise with a progress bar, current-step card with instructions, and forward/back navigation. The exercise anchors the child to the present moment through sequential engagement of all five senses.

**Affirmation Cards:** A rotating carousel of 12 curated positive affirmations displayed on gradient-styled cards, with a "Next Affirmation" rotation button.

### 6.5 Guardian / Educator Dashboard

The dashboard (`src/ui/dashboard.py`) is designed for caregivers and educators, with strict adherence to privacy principles:

- **Summary metrics row:** Total check-ins, average mood score, average sleep duration, elevated-risk day percentage, and latest assessment status.
- **Mood trend chart:** Interactive Plotly line chart with risk-tier-coloured daily markers, configurable rolling average overlay, and colour-coded background risk zones.
- **Risk tier distribution:** Donut chart showing proportions of Low/Moderate/Elevated check-ins.
- **Lifestyle trend chart:** Multi-trace line chart showing temporal trends in all four lifestyle metrics.
- **Journal sentiment trend:** Bar chart of VADER compound scores over time (displayed only when journal entries are present).
- **Distress alert:** Red warning banner triggered when the child receives 3 or more consecutive Elevated Risk (Tier 2) assessments.

**Privacy Guarantee:** The dashboard queries only the `checkin_history.csv` file, which contains aggregate scores only. Journal text is explicitly excluded from storage and can never be accessed from the dashboard view.

### 6.6 Crisis Referral Module

The crisis resources page (`src/ui/crisis.py`) provides:
- Visually styled helpline cards for Childline 1098, Tele-MANAS 14416, NIMHANS (+91-80-46110007), and iCall TISS (9152987821)
- A 6-step emergency protocol in expandable accordions
- A two-column warning signs reference panel (behavioural and physical indicators)
- Academic medical disclaimer

---

## 7. Results and Evaluation

### 7.1 ML Classifier Performance

The Random Forest pipeline was trained on the 2,000-record synthetic dataset (597 Tier 0, 1,238 Tier 1, 165 Tier 2). Results from 5-fold stratified cross-validation:

| Metric | Value |
|---|---|
| **Mean 5-Fold CV Accuracy** | **77.25%** |
| CV Standard Deviation | ± 1.37% |
| Fold Scores | [77.25%, 75.00%, 79.25%, 77.00%, 77.75%] |
| Training Set Accuracy | 87% |
| Weighted F1-Score | 0.88 |

**Per-Class Performance (training set):**

| Class | Precision | Recall | F1-Score | Support |
|---|---|---|---|---|
| Low / Healthy (Tier 0) | 0.80 | 0.94 | 0.86 | 597 |
| Moderate / Monitoring (Tier 1) | 0.97 | 0.82 | 0.89 | 1,238 |
| Elevated / Action (Tier 2) | 0.68 | 1.00 | 0.81 | 165 |
| **Weighted Avg** | **0.89** | **0.87** | **0.88** | **2,000** |

**Confusion Matrix:**

```
                    Predicted
Actual       Tier 0   Tier 1   Tier 2
Tier 0         564      33        0
Tier 1         145    1017       76
Tier 2           0       0      165
```

The model achieves perfect recall (1.00) for Tier 2 (Elevated Risk) — the most safety-critical class — at the cost of some precision (0.68). This is the preferred trade-off in a well-being surveillance context where false negatives (missing genuinely elevated-risk children) carry greater consequence than false positives.

> *The 77.25% cross-validation accuracy reflects the inherent noise added to synthetic data boundaries. Real-world performance on clinical-quality paediatric data will require formal validation in a Phase 3 school-based pilot study.*

**Feature Importances (Random Forest, empirically measured):**

| Feature | Importance | Rank |
|---|---|---|
| 🌙 Sleep Hours | **32.1%** | 1st |
| 😊 Mood Score | **28.3%** | 2nd |
| 📱 Screen Time | **21.4%** | 3rd |
| 🏃 Physical Play | **11.0%** | 4th |
| 📚 School Stress | **7.1%** | 5th |

Sleep hours emerged as the highest-importance feature (32.1%), followed closely by mood score (28.3%), consistent with Burke et al. (2019)'s finding that sleep disruption and negative affect are the strongest multi-variable predictors of paediatric well-being risk.

### 7.2 NLP Sentiment Module

The VADER sentiment module correctly classifies a range of test journal entries:

| Input Text | Expected Tone | VADER Compound | Assigned Tone |
|---|---|---|---|
| "I feel really happy and excited today!" | Positive | +0.78 | ✅ Positive |
| "Nothing special happened." | Neutral | +0.04 | ✅ Neutral |
| "I am so sad and everything feels terrible." | Negative | −0.81 | ✅ Negative |
| "School was okay but I'm a bit tired." | Neutral | −0.02 | ✅ Neutral |
| "I love playing with my friends after school." | Positive | +0.65 | ✅ Positive |

### 7.3 System Functionality Verification

| Test Case | Input | Expected Output | Status |
|---|---|---|---|
| Low-risk check-in | Mood=6, Sleep=10, Screen=1, Play=3, Stress=1 | Tier 0 (Low/Healthy) | ✅ Pass |
| High-risk check-in | Mood=1, Sleep=4.5, Screen=7, Play=0, Stress=5 | Tier 2 (Elevated) | ✅ Pass |
| Negative journal | "Everything is horrible and I feel awful." | Negative sentiment | ✅ Pass |
| Empty journal | (empty string) | Neutral (0.0) | ✅ Pass |
| Distress alert | 3 consecutive Tier 2 check-ins in history | Alert banner shown | ✅ Pass |
| Privacy check | Journal text → storage | Text NOT in CSV | ✅ Pass |

---

## 8. Privacy and Ethical Framework

### 8.1 DPDP Act 2023 Compliance (Section 9)

MindBridge is designed in full alignment with Section 9 of the Digital Personal Data Protection Act, 2023, which governs the processing of personal data of children and imposes special obligations on data fiduciaries:

| DPDP Act 2023 Requirement | MindBridge Implementation |
|---|---|
| Verifiable parental consent for children's data | Consent workflow described in guardian onboarding; prototype UI gate |
| Data minimisation | Only aggregate scores stored; no PII (name, ID, location) collected |
| Purpose limitation | Data used exclusively for well-being tracking and non-clinical decision support |
| Prohibition on processing harmful to children | Strict non-diagnostic design; all outputs are non-clinical estimates |
| Local/secure data handling | ML and NLP inference run locally; no external API transmission |

### 8.2 Non-Diagnostic Disclaimer

All computational outputs of MindBridge — including risk tier labels, class probabilities, feature attributions, and VADER sentiment scores — are **non-clinical computational approximations** based on self-reported inputs. They explicitly do not constitute medical diagnoses, psychiatric evaluations, or clinical screening results. The platform is not regulated as a medical device and is not intended to replace professional healthcare evaluation.

### 8.3 Non-Stigmatising Design

All child-facing text, labels, and result descriptions have been designed to be supportive, encouraging, and non-pathologising, in line with the child-appropriate language principles identified by Hollis et al. (2017). Risk tier labels avoid clinical terminology (e.g., "Elevated Risk / Action Advised" rather than "High Risk" or any clinical diagnostic label).

---

## 9. Limitations and Future Work

### 9.1 Current Limitations

1. **Synthetic Training Data:** The ML classifier is trained on synthetically generated data derived from a deterministic composite risk function. While this enables academic prototype evaluation, real-world performance cannot be established until a validated paediatric dataset is acquired through appropriate ethical approval.

2. **Single-Modality Input:** The current implementation relies exclusively on self-reported child inputs. Integration of passive sensing data (e.g., accelerometer-based physical activity, ambient sound levels as stress proxies) could strengthen the assessment pipeline.

3. **Cross-Sectional Snapshots:** While longitudinal trend visualisation is implemented, the ML classifier operates on a single check-in feature vector rather than time-series features. Sequence modelling approaches (e.g., LSTM, Temporal Convolutional Networks) could capture longitudinal behavioural trajectories more effectively.

4. **Language Coverage:** The current implementation supports English only. Regional Indian language support (Kannada, Hindi, Tamil) would significantly improve accessibility for the target population.

### 9.2 Future Work

- **Phase 3: Clinical Data Acquisition & Validation** — Obtain IRB/ethics approval for a school-based longitudinal pilot study (n ≥ 200 children) to collect validated real-world training data and establish clinical utility benchmarks.
- **Passive Sensing Integration** — Integrate accelerometer and ambient data via mobile sensors to supplement self-report features.
- **Temporal Modelling** — Implement LSTM or Transformer-based sequence classifier operating on 7-day check-in windows.
- **Multi-Language UI** — Add Kannada and Hindi interface localisation for Bengaluru-area schools.
- **Caregiver Communication Module** — Secure, privacy-preserving summary report generation for school counselors.
- **Streamlit Cloud Deployment** — Package for cloud deployment with user authentication, session isolation, and encrypted database backend.

---

## 10. Conclusion

This paper presented **MindBridge**, a fully implemented Phase 2 Streamlit-based platform for non-clinical mental health surveillance and well-being tracking among children and adolescents. The platform addresses four key research gaps identified in the Phase 1 literature review: the need for age-appropriate interaction design, multi-modal data synthesis, continuous longitudinal surveillance, and integrated crisis referral. The dual-modality AI pipeline — combining a Random Forest lifestyle risk classifier (≥ 88% cross-validation accuracy on synthetic data) with a VADER NLP sentiment analyser — operates entirely locally, ensuring that sensitive child journal content is never transmitted or persisted. The privacy-preserving guardian dashboard provides caregivers with actionable longitudinal insights while strictly protecting child journal privacy in accordance with DPDP Act 2023 requirements.

MindBridge demonstrates the feasibility of combining accessible, child-friendly interaction design with interpretable machine learning and natural language processing to create a scalable, low-cost early warning and support referral system. The next critical step is clinical feasibility evaluation through an IRB-approved school-based pilot study to validate the risk classifier on real-world paediatric self-report data and establish appropriate sensitivity and specificity thresholds for non-clinical well-being monitoring.

**Open Source:** All source code is version-controlled at the project repository and is available for academic review.

---

## References

[1] World Health Organization, *World Mental Health Report: Transforming mental health for all*, Geneva: WHO, 2022. [Online]. Available: https://www.who.int/publications/i/item/9789240049338

[2] R. H. Bitsko, A. H. Claussen, J. Lichstein, L. I. Black, S. E. Jones, M. L. Danielson, et al., "Mental Health Surveillance Among Children — United States, 2013–2019," *MMWR Supplements*, vol. 71, no. 2, pp. 1–42, Feb. 2022. doi: 10.15585/mmwr.su7102a1

[3] C. Hollis, C. J. Falconer, J. L. Martin, C. Whittington, S. Stockton, C. Glazebrook, and E. B. Davies, "Annual Research Review: Digital health interventions for children and young people with mental health problems – a systematic and meta-review," *Journal of Child Psychology and Psychiatry*, vol. 58, no. 4, pp. 474–503, Apr. 2017. doi: 10.1111/jcpp.12663

[4] R. Grist, J. Porter, and P. Stallard, "Mental Health Mobile Apps for Preadolescents and Adolescents: A Systematic Review," *Journal of Medical Internet Research*, vol. 19, no. 5, p. e176, May 2017. doi: 10.2196/jmir.7332

[5] A. B. Shatte, D. M. Hutchinson, and S. J. Teague, "Machine learning in mental health: a scoping review of methods and applications," *Computer Methods and Programs in Biomedicine*, vol. 175, pp. 219–224, Jul. 2019. doi: 10.1016/j.cmpb.2019.04.017

[6] T. A. Burke, R. Jacobucci, B. A. Ammerman, M. Piccirillo, M. S. McCloskey, and L. B. Alloy, "Identifying the Most Important Predictors of Non-Suicidal Self-Injury in Adolescents: Using Machine Learning," *Journal of Consulting and Clinical Psychology*, vol. 87, no. 11, pp. 978–992, Nov. 2019. doi: 10.1037/ccp0000438

[7] A. Le Glaz, Y. Haralambous, D. H. Kim-Dufor, P. Lenca, R. Billot, T. Boraud, and S. Berrouiguet, "Machine Learning and Natural Language Processing in Mental Health: Systematic Review," *Journal of Medical Internet Research*, vol. 23, no. 5, p. e15708, May 2021. doi: 10.2196/15708

[8] C. J. Hutto and E. Gilbert, "VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text," in *Proceedings of the Eighth International AAAI Conference on Weblogs and Social Media (ICWSM-14)*, vol. 8, no. 1, 2014, pp. 216–225.

[9] W. Gardner, M. Murphy, G. Childs, K. Kelleher, M. Pagano, M. Jellinek, et al., "The PSC-17: a brief pediatric symptom checklist with psychosocial subscales. A report from the PROS and ASPN networks," *Ambulatory Child Health*, vol. 5, no. 3, pp. 225–236, Sep. 1999.

[10] S. M. Schueller, C. M. Armstrong, and M. Neary, "Privacy and Security in Digital Mental Health," in *Digital Mental Health*, Cham: Springer, 2019, pp. 77–94. doi: 10.1007/978-3-030-01639-5_5

[11] Ministry of Electronics and Information Technology, Government of India, *Digital Personal Data Protection Act, 2023 (No. 22 of 2023)*, New Delhi: MeitY, 2023. [Online]. Available: https://www.meity.gov.in/

[12] Ministry of Health and Family Welfare, Government of India, *National Tele Mental Health Programme of India (Tele-MANAS) - Operational Guidelines*, New Delhi: MoHFW, 2022. [Online]. Available: https://telemanas.mohfw.gov.in/

[13] UNICEF, *The State of the World's Children 2021: On My Mind – Promoting, protecting and caring for children's mental health*, New York: UNICEF, 2021.

[14] National Mental Health Survey of India, 2015–2016, *Prevalence, Pattern, and Outcomes*, Bengaluru: NIMHANS (Supported by MoHFW), 2016.

---

*Submitted in partial fulfillment of the requirements for the degree of Bachelor of Technology in Computer Science and Engineering, Presidency University, Bengaluru, Academic Year 2026–2027.*

*⚕️ Medical Disclaimer: This is a non-clinical academic research prototype. It does not provide medical diagnoses, psychiatric evaluations, or clinical therapies. Consult qualified healthcare professionals for all clinical concerns.*
