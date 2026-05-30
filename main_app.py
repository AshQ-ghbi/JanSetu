import streamlit as st
from supabase import create_client, Client

# ── 1. Page Config ──────────────────────────────────────────
st.set_page_config(
    page_title="JanSetu — Connecting India",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "**JanSetu** — Connecting Rural Citizens with verified local experts across 5 main domains (Agriculture, Education, Healthcare, MSME & Rural Access)."
    },
)

# ── 2. Global CSS Injection ──────────────────────────────────
st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

/* ── Root tokens ── */
:root {
    --saffron:   #FF6B00;
    --saffron-lt:#FFF3E8;
    --green:     #138808;
    --green-lt:  #E8F5E9;
    --navy:      #000080;
    --navy-lt:   #E8EBF7;
    --gold:      #FFB800;
    --red:       #E63946;
    --bg:        #F5F7FF;
    --card:      #FFFFFF;
    --border:    #E2E8F0;
    --text:      #1A1A2E;
    --muted:     #64748B;
    --radius:    14px;
    --shadow:    0 4px 20px rgba(0,0,128,.08);
    --shadow-lg: 0 8px 40px rgba(0,0,128,.13);
}

/* ── Global reset ── */
html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif !important;
}

/* ── App background ── */
.stApp {
    background: linear-gradient(135deg, #F0F4FF 0%, #FFF8F0 50%, #F0FFF4 100%) !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--navy) 0%, #1a1a6e 60%, #0d0d4a 100%) !important;
    border-right: none !important;
}
[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] .stCaption {
    color: rgba(255,255,255,0.75) !important;
}
[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.15) !important;
}

/* ── Nav links in sidebar ── */
[data-testid="stSidebarNavLink"] {
    border-radius: 10px !important;
    margin: 2px 4px !important;
    transition: all 0.25s ease !important;
    color: rgba(255,255,255,0.85) !important;
}
[data-testid="stSidebarNavLink"]:hover,
[data-testid="stSidebarNavLink"][aria-selected="true"] {
    background: rgba(255,255,255,0.15) !important;
    color: #FFFFFF !important;
    font-weight: 600 !important;
}

/* ── Metric cards ── */
[data-testid="stMetric"] {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1rem 1.25rem !important;
    box-shadow: var(--shadow);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
[data-testid="stMetric"]:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
}
[data-testid="stMetricLabel"] {
    color: var(--muted) !important;
    font-size: 0.72rem !important;
    font-weight: 500 !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
[data-testid="stMetricValue"] {
    color: var(--navy) !important;
    font-weight: 700 !important;
    font-size: 1.35rem !important;
}
[data-testid="stMetricDelta"] svg { display: none; }
[data-testid="stMetricDelta"] > div {
    color: var(--green) !important;
    font-size: 0.75rem !important;
    font-weight: 500 !important;
}

/* ── Buttons ── */
.stButton > button[kind="primary"],
.stFormSubmitButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--saffron) 0%, #e65c00 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    padding: 0.65rem 1.5rem !important;
    box-shadow: 0 4px 15px rgba(255,107,0,.35) !important;
    transition: all 0.25s ease !important;
}
.stButton > button[kind="primary"]:hover,
.stFormSubmitButton > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(255,107,0,.45) !important;
}
.stButton > button:not([kind="primary"]) {
    border-radius: 10px !important;
    border: 1.5px solid var(--border) !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
}
.stButton > button:not([kind="primary"]):hover {
    border-color: var(--saffron) !important;
    color: var(--saffron) !important;
}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    border-radius: 10px !important;
    border: 1.5px solid var(--border) !important;
    font-family: 'Poppins', sans-serif !important;
    font-size: 0.95rem !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
    background: #fff !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--saffron) !important;
    box-shadow: 0 0 0 3px rgba(255,107,0,.12) !important;
}

/* ── Alert boxes ── */
[data-testid="stAlert"] {
    border-radius: var(--radius) !important;
    border: none !important;
    font-size: 0.92rem !important;
}

/* ── DataFrames ── */
[data-testid="stDataFrame"] {
    border-radius: var(--radius) !important;
    border: 1px solid var(--border) !important;
    overflow: hidden !important;
    box-shadow: var(--shadow) !important;
}

/* ── Dividers ── */
hr {
    border-color: var(--border) !important;
    opacity: 1 !important;
}

/* ── Spinner ── */
[data-testid="stSpinner"] > div {
    color: var(--saffron) !important;
}

/* ── Form container ── */
[data-testid="stForm"] {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.5rem !important;
    box-shadow: var(--shadow);
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #f1f5f9; }
::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--navy); }

/* ── Caption ── */
.stCaption {
    color: var(--muted) !important;
    font-size: 0.78rem !important;
}

/* ── bar chart ── */
[data-testid="stVegaLiteChart"] {
    border-radius: var(--radius);
    border: 1px solid var(--border);
    box-shadow: var(--shadow);
    overflow: hidden;
}

/* ── Heading colours ── */
h1, h2, h3 { color: var(--navy) !important; font-family: 'Poppins', sans-serif !important; }
h4, h5, h6 { color: var(--text) !important; font-family: 'Poppins', sans-serif !important; }
</style>
""", unsafe_allow_html=True)


# ── 3. Supabase Connection (cached, runs once) ───────────────
@st.cache_resource(show_spinner="Connecting to JanSetu database...")
def get_supabase() -> Client:
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except KeyError as e:
        st.error(f"⚠️ Missing secret: {e}. Add SUPABASE_URL and SUPABASE_KEY to your secrets.")
        st.stop()
    except Exception as e:
        st.error(f"❌ Database connection error: {e}")
        st.stop()

# Store in session state so all pages can access it
if "supabase" not in st.session_state:
    st.session_state["supabase"] = get_supabase()


# ── 4. Sidebar Brand ─────────────────────────────────────────
with st.sidebar:
    # Hero logo area
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0 0.5rem 0;'>
        <div style='font-size:2.8rem; margin-bottom:4px;'>🇮🇳</div>
        <div style='font-size:1.6rem; font-weight:800; color:#FFFFFF; letter-spacing:0.02em;'>JanSetu</div>
        <div style='font-size:0.78rem; color:rgba(255,255,255,0.65); font-weight:400; letter-spacing:0.05em; text-transform:uppercase;'>
            India's Problem-Solving OS
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("<div style='font-size:0.7rem; font-weight:600; color:rgba(255,255,255,0.5); text-transform:uppercase; letter-spacing:0.1em; margin-bottom:8px;'>5 Domains Covered</div>", unsafe_allow_html=True)

    domains = [
        ("🌾", "Agriculture",  "#4CAF50"),
        ("🏫", "Education",    "#2196F3"),
        ("🏥", "Healthcare",   "#E91E63"),
        ("🏪", "MSME",         "#FF9800"),
        ("📡", "Rural Access", "#9C27B0"),
    ]
    for icon, label, color in domains:
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:8px;padding:5px 8px;margin:2px 0;border-radius:8px;background:rgba(255,255,255,0.07);">'
            f'<span style="font-size:1.1rem;">{icon}</span>'
            f'<span style="font-size:0.88rem;font-weight:500;color:rgba(255,255,255,0.9);">{label}</span>'
            f'</div>',
            unsafe_allow_html=True
        )

    st.divider()

    st.markdown("""
    <div style='text-align:center; padding-bottom:6px;'>
        <div style='font-size:0.72rem; color:rgba(255,255,255,0.45);'>🔒 Powered by Beyond Life</div>
        <div style='font-size:0.72rem; color:rgba(255,255,255,0.45); margin-top:3px;'>JanSetu v1.0 · Cyphersnova Hackathon 2026</div>
        <div style='font-size:0.72rem; color:rgba(255,255,255,0.55); margin-top:3px; font-weight:500;'>by Ashish Kumar</div>
    </div>
    """, unsafe_allow_html=True)


# ── 5. Page Definitions ──────────────────────────────────────
citizen_page = st.Page(
    "pages/citizen_portal.py",
    title="Citizen Portal",
    icon="👪",
    default=True,
)

admin_page = st.Page(
    "pages/admin_ledger.py",
    title="Solver & Admin Ledger",
    icon="🕵️",
)

# ── 6. Navigation ─────────────────────────────────────────────
nav = st.navigation({
    "🏠 JanSetu Platform": [citizen_page, admin_page],
})

nav.run()
