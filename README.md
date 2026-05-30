# 🇮🇳 JanSetu — Unified Problem-Solving OS for Bharat

> **Hackathon Prototype** · India at a Turning Point · Built in ≤10 hours

JanSetu is a localized **Digital Public Infrastructure (DPI) router** that
instantly connects rural citizens with verified local specialists across 5
national challenge domains — using AI classification, Supabase backend, and
UPI micro-payments.

---

## 🗂️ Project Structure

```
jansetu/
├── main_app.py                  # Streamlit entrypoint + navigation
├── pages/
│   ├── citizen_portal.py        # Citizen-facing UI + payment flow
│   └── admin_ledger.py          # Admin analytics & live query ledger
├── database_setup.sql           # PostgreSQL DDL + seed data (run in Supabase)
├── requirements.txt             # Python dependencies
└── .streamlit/
    └── secrets.toml             # Supabase credentials (template)
```

---

## ⚡ Quick Start (10 minutes)

### Step 1 — Supabase Setup

### Step 2 — Configure Secrets

### Step 3 — Install & Run Locally

### Step 4 — Deploy to Streamlit Cloud (Free)
1. Push this folder to a GitHub repo.
2. Go to [share.streamlit.io](https://share.streamlit.io) → connect repo → set
   `main_app.py` as the entry point.
3. Under **Advanced Settings → Secrets** content.
4. Click **Deploy** — live in ~2 minutes. ✅

---

## 🌟 Feature Highlights

| Feature | Implementation |
|---|---|
| AI Problem Classifier | Keyword-frequency NLP across 5 domains |
| Instant Solver Match | Supabase query filtered by domain + rating |
| UPI QR Payment | `qrcode` library → `upi://pay` deep-link |
| Escrow Flow | Payment status stored in Supabase `queries` table |
| Contact Reveal | Unlocked only after payment confirmation |
| Admin Ledger | Live query log, KPI cards, domain distribution bar |

---

## 🎯 5 Supported Domains

| Domain | Icon | Example Problem |
|---|---|---|
| Agriculture | 🌾 | Pest attack on crops, weather advisory |
| Education | 📚 | Affordable tutoring, board exam prep |
| Healthcare | 🏥 | OPD triage, rural doctor consultation |
| MSME | 🏪 | Micro-loan documentation, GST help |
| Rural Access | 📡 | Digital literacy, scheme enrollment |

---

## 🔧 Tech Stack

- **Frontend**: Streamlit (st.Page + st.navigation multi-page)
- **Backend DB**: Supabase (PostgreSQL + REST API)
- **QR Generation**: `qrcode[pil]` library
- **Payment**: UPI deep-link simulation (no API keys needed)
- **Deployment**: Streamlit Community Cloud (free tier)

---

## 📝 Hackathon Notes

- **Zero cost**: All services used are on free tiers.
- **No payment API**: UPI QR is a client-side deep-link — no Razorpay/Stripe
  tokens needed, works instantly for demo.
- **Language-agnostic**: Classifier handles Hindi + English mixed text.
- **Mobile-friendly**: Responsive CSS grid, large touch targets.

---

*Built with ❤️ for India by Beyond Life· JanSetu v1.0*
