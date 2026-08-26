# Mental Health and Well-being Surveillance, Assessment and Tracking Solution Among Children

## Project Overview

This project focuses on the conceptualization, architectural design, and preliminary specification of an intelligent, child-centered digital platform for early mental health and well-being surveillance, assessment, longitudinal tracking, and verified support referral among children and adolescents. 

Emerging pediatric emotional distress often manifests through observable lifestyle and behavioral shifts (such as chronic sleep insufficiency, high sedentary screen exposure, academic strain, and social withdrawal). The proposed solution combines an engaging, low-cognitive-load interface (single-tap emoji mood check-ins and an optional reflective journal) with a dual-modality intelligence pipeline: (1) supervised machine learning classification for non-diagnostic lifestyle risk stratification (*Low / Healthy*, *Moderate / Monitoring*, *Elevated / Action Advised*), and (2) natural language processing (NLP) for emotional valence and affective tone scoring. The platform bridges early distress surveillance with immediate, non-clinical psychoeducational calming tools (visual 4-7-8 breathing pacers and grounding exercises) and provides caregivers with explainable longitudinal trend dashboards alongside verified emergency crisis referral pathways.

## Student

Harsha R

## USN

20231CSE0261

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
│
├── report/
│   └── Phase_1_Project_Report.md                         # Complete academic Phase 1 report in Markdown format
│
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
