<div align="center">

<img src="https://img.shields.io/badge/🇮🇳-Made%20for%20Bharat-FF6B00?style=for-the-badge&labelColor=000080" />
<img src="https://img.shields.io/badge/Hackathon-Cyphersnova%202026-138808?style=for-the-badge" />
<img src="https://img.shields.io/badge/Status-Live%20Prototype-blue?style=for-the-badge" />

<br/><br/>

 `India's Problem-Solving OS

### *"Connecting 900 Million Rural Citizens with Verified Local Experts — One Problem at a Time"*

<br/>

[![Live App](https://img.shields.io/badge/🚀%20Live%20Demo-jansetu--beyondlife--krashish.streamlit.app-FF6B00?style=for-the-badge&logo=streamlit&logoColor=white)](https://jansetu-beyondlife-krashish.streamlit.app)
&nbsp;
[![GitHub](https://img.shields.io/badge/GitHub-AshQ--ghbi%2FJanSetu-181717?style=for-the-badge&logo=github)](https://github.com/AshQ-ghbi/JanSetu)

<br/>

</div>

---

## 🎯 The Problem We're Solving

> **India has 640,000+ villages. Most citizens have no affordable, trusted access to expert help for everyday problems.**

A farmer in Chhindwara doesn't know why his crops are yellowing. A widow in rural Rajasthan can't navigate pension paperwork. A first-generation student in MP can't afford coaching for board exams.

They all have **one thing in common** — they don't know who to call.

**JanSetu changes that. Instantly.**

---

## 💡 What is JanSetu?

**JanSetu** (जनसेतु — *"Bridge for the People"*) is a **Digital Public Infrastructure (DPI)** platform that:

1. **Listens** to a citizen's problem in Hindi, English, or any local dialect
2. **Classifies** it using an AI NLP engine across 5 critical domains
3. **Matches** them with the highest-rated verified local expert instantly
4. **Connects** them via a ₹10–₹50 escrow-protected UPI micro-payment

No middlemen. No bureaucracy. No internet literacy required beyond a form.

---

## ✨ Live Demo

| Page | What to See |
|------|-------------|
| 👪 **Citizen Portal** | Type a problem in Hindi or English → AI classifies → Expert matched → Pay ₹19 via UPI QR → Get direct contact |
| 🕵️ **Admin Ledger** | Real-time KPIs, query distribution chart, live ledger, solver registry, escrow revenue summary |

**Try these test inputs on the Citizen Portal:**
- `"मेरे खेत में पत्ते पीले पड़ रहे हैं"` → Agriculture expert
- `"My daughter needs Class 10 board exam coaching"` → Education specialist
- `"chest pain and high BP"` → Healthcare worker
- `"GST registration for my small shop"` → MSME advisor
- `"ration card not linked to Aadhaar"` → Rural Access specialist

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     CITIZEN (Mobile)                     │
│              Describes problem in any language           │
└──────────────────────────┬──────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────┐
│               JanSetu — Streamlit Frontend               │
│                                                          │
│   ┌─────────────────┐      ┌──────────────────────────┐ │
│   │  NLP Classifier  │      │     Admin Ledger         │ │
│   │  (Keyword AI)    │      │  KPIs · Ledger · Revenue │ │
│   │  5 Domain Match  │      │  Solver Registry         │ │
│   └────────┬─────────┘      └──────────────────────────┘ │
│              │                                               │
│              ▼                                               │
│   ┌─────────────────┐                                     │
│   │  Solver Matcher  │  → Highest-rated Active Expert        │
│   │  (Supabase SQL)  │                                        │
│   └────────┬─────────┘                                    │
└───────────┼────────────────────────────────────────────┘
         ...  │
          ....▼
┌─────────────────────────────────────────────────────────┐
│              Supabase (PostgreSQL + REST API)                     │
│   solvers table  ·  queries table  ·  payment tracking            │
└──────────────────────────┬──────────────────────────────┘
                                │
                              ..▼
┌─────────────────────────────────────────────────────────┐
│                    UPI Escrow Payment                     │
│         QR Code → GPay / PhonePe / Paytm / BHIM          │
│         Funds held until session complete                 │
└─────────────────────────────────────────────────────────┘
```

---

## 🌾 5 Domains Covered

| Domain | Icon | Experts Handle |
|--------|------|----------------|
| **Agriculture** | 🌾 | Crop disease, pest control, mandi prices, soil, irrigation, livestock |
| **Education** | 🏫 | Board exam prep, scholarships, admissions, skill development, NEET/JEE |
| **Healthcare** | 🏥 | Symptoms, medicines, Ayushman Bharat, telemedicine, mental health |
| **MSME** | 🏪 | GST, Udyam registration, MUDRA loans, business licensing, exports |
| **Rural Access** | 📡 | Ration card, Aadhaar linking, panchayat schemes, MGNREGA, pension |

---

## 🔐 How the Escrow Model Works

```
Citizen pays ₹10–₹50  →  Held in JanSetu Escrow (UPI)
        │
        ├──► Expert's contact revealed immediately
        │
        └──► Session happens → Citizen confirms → Expert paid
                                      │
                                      └──► If unsatisfied → Refund
```

This **trust layer** is what makes rural citizens actually use the platform — they know their money is safe before they commit to talking to a stranger.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Streamlit (Python) · Poppins font · Custom CSS design system |
| **Database** | Supabase (PostgreSQL) · REST API |
| **AI/NLP** | Custom keyword-based domain classifier (Hindi + English bilingual) |
| **Payments** | UPI Deep Link · QR Code generation (`qrcode[pil]`) |
| **Hosting** | Streamlit Community Cloud |
| **Auth/Secrets** | Streamlit Secrets Manager |

---

## 📁 Project Structure

```
JanSetu/
│
├── main_app.py              # App entry point · global CSS · Supabase init · navigation
│
├── pages/
│   ├── citizen_portal.py    # Citizen-facing UI · NLP classifier · solver match · UPI payment
│   └── admin_ledger.py      # Admin dashboard · KPIs · live ledger · revenue summary
│
├── requirements.txt         # streamlit · supabase · qrcode[pil] · Pillow
├── .devcontainer/           # GitHub Codespaces config (ignored by Streamlit Cloud)
└── README.md
```

---

## 🚀 Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/AshQ-ghbi/JanSetu.git
cd JanSetu

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add Supabase secrets

# 4. Run the app
streamlit run main_app.py
```

---

## 🗄️ Database Schema (Supabase)

```sql
-- Verified local experts
CREATE TABLE solvers (
    id        SERIAL PRIMARY KEY,
    name      TEXT NOT NULL,
    domain    TEXT NOT NULL,          -- Agriculture | Education | Healthcare | MSME | Rural Access
    location  TEXT,
    rating    NUMERIC(2,1) DEFAULT 4.0,
    fee       INTEGER DEFAULT 29,     -- consultation fee in ₹
    status    TEXT DEFAULT 'Active',  -- Active | Inactive
    contact   TEXT                    -- phone number revealed post-payment
);

-- Citizen queries
CREATE TABLE queries (
    id                 SERIAL PRIMARY KEY,
    citizen_name       TEXT,
    raw_problem        TEXT,
    ai_category        TEXT,           -- classified domain
    matched_solver_id  INTEGER REFERENCES solvers(id),
    payment_status     TEXT DEFAULT 'Pending',  -- Pending | Paid
    created_at         TIMESTAMPTZ DEFAULT now()
);
```

---

## 📊 Impact Potential

| Metric | Estimate |
|--------|----------|
| 🇮🇳 Target population | 900M+ rural Indians |
| 🏘️ Villages in India | 640,000+ |
| 📱 UPI users (2025) | 350M+ |
| 💸 Avg. consultation fee | ₹19–₹49 |
| ⚡ Time to expert match | < 3 seconds |
| 🔒 Trust mechanism | Escrow-protected payment |

---

## 👨‍💻 Built By

<div align="center">

**Ashish Kumar** <br/><br/>
*Team Beyond Life*

Cyphersnova Hackathon 2026

*"Technology should serve the last person in the last village first."*

</div>

---

## 📄 License

License — free to use, modify, and build upon for public good.

---

<div align="center">

**⭐ If JanSetu inspires you, star the repo and share it.**

*Built with ❤️ for Bharat · Powered by Streamlit + Supabase*

</div>
