## CIRA : Cyber Incident Response Assistant

> An AI-powered Cyber First Response Platform that helps cybercrime victims understand what happened, preserve critical evidence, and take the right actions before reporting.

---

## 🚨 Problem

Cybercrime victims often panic, lose valuable evidence, delay reporting, or don't know what to do immediately after an incident.

This reduces the chances of:

* Financial recovery
* Successful investigation
* Evidence preservation
* Timely reporting

Many victims struggle to identify:

* What type of cybercrime occurred
* Which evidence is important
* What actions should be taken first
* Where and how to report the incident

---

## 💡 Solution

CIRA acts as an AI Case Officer.

The platform guides victims through a structured conversation, identifies the likely cybercrime category, collects relevant information, and generates a personalized incident response plan.

Users receive:

* Incident classification
* Immediate response actions
* Evidence preservation guidance
* Reporting resources
* Case timeline
* Investigation-ready summary

---

## ✨ Key Features

### 🤖 AI Incident Understanding

Users describe what happened in natural language.

CIRA:

* Understands the incident
* Identifies likely cybercrime category
* Maps incidents to official reporting categories

---

### 🕵️ Conversational Case Intake

Instead of long forms, CIRA asks:

* Context-aware follow-up questions
* One question at a time
* Similar to speaking with a cybercrime officer

---

### 📂 Evidence Preservation Guidance

Provides evidence checklists based on incident type.

Examples:

* Screenshots
* Transaction IDs
* Phone numbers
* URLs
* Chat logs
* Email headers

---

### ⚡ Incident Response Playbooks

Category-specific response guides including:

* Immediate Actions
* Containment Steps
* Evidence Preservation
* Reporting Guidance
* Recovery Recommendations

---

### 📋 Automated Case Timeline

Generates:

```text
Time → Event
```

Example:

```text
14 Jun 2026 - Received suspicious job offer

14 Jun 2026 - Paid registration fee

14 Jun 2026 - Communication stopped

14 Jun 2026 - Fraud identified
```

---

### 📄 Investigation Summary

Creates an editable case summary suitable for:

* Personal records
* Police reporting
* Cyber Crime Portal submissions

---

### ☎ Official Reporting Resources

Provides verified resources such as:

* Cyber Helpline 1930
* National Cyber Crime Reporting Portal
* Official awareness resources

---

## 🎯 Supported Incident Categories

### Online & Social Media Related Crime

* Online Job Fraud
* Profile Hacking
* Fake / Impersonation Profiles
* Email Phishing
* Online Shopping Fraud
* Matrimonial Fraud

### Online Financial Fraud

* UPI Fraud
* Internet Banking Fraud
* E-Wallet Fraud
* Vishing / Fraud Calls
* SIM Swap Fraud

### Hacking & Unauthorized Access

* Email Hacking
* Data Breach
* Website Hacking
* Unauthorized Access

### Ransomware

* Ransomware Incidents

### Cryptocurrency Crime

* Crypto Investment Fraud
* Fraudulent Trading Platforms

---

## 🏗 Architecture

```text
User
    │
    ▼
AI Incident Understanding
    │
    ▼
Category Classification
    │
    ▼
Rule Engine
    │
    ├── Follow-up Questions
    ├── Evidence Checklist
    ├── Response Playbook
    └── Reporting Guidance
    │
    ▼
Timeline Generator
    │
    ▼
Case Summary Generator
    │
    ▼
Investigation Package
```

---

## 🛠 Tech Stack

### Frontend

* Streamlit

### Backend

* Python

### AI Layer

* Groq (Llama 3.3 70B)
* Rule Engine

### Data

* JSON Playbooks
* Category Mapping
* Evidence Templates

### Future Integrations

* Whisper Speech-to-Text
* RAG Knowledge Base
* PDF Report Generation
* Threat Intelligence Feeds

---

## 🚀 Future Roadmap

### V2

* Voice Reporting (Hindi + English)
* Speech-to-Text Incident Reporting
* PDF Investigation Reports

### V3

* Anonymous Trend Analytics
* Scam Pattern Detection
* Victim Support Recommendations

### V4

* Police Investigation Dashboard
* Investigation Assistance Tools
* Case Correlation Engine

---

## 🔒 Privacy

CIRA is designed with privacy in mind.

* No mandatory user accounts
* Minimal data retention
* User-controlled information
* Evidence stored only when required

---

## 🌍 Vision

To become the first place victims turn to immediately after experiencing a cybercrime—helping citizens preserve evidence, reduce panic, improve reporting quality, and support faster cybercrime response.

**"If you've been a victim of cybercrime, CIRA helps you know what to do next."**
