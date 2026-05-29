import streamlit as st
from supabase import create_client, Client

# ── 1. Global Page Config (must be first Streamlit call) ────
st.set_page_config(
    page_title="JanSetu — Connecting India",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com/jansetu",
        "Report a bug": None,
        "About": (
            "**JanSetu** | Unified Problem-Solving OS for Bharat\n\n"
            "Connecting citizens with verified local specialists across "
            "Agriculture, Education, Healthcare, MSME & Rural Access.\n\n"
            "_Built for India at a Cyphersnova Hackathon by Beyond Life_"
        ),
    },
)

# ── 2. Inject Global CSS Theme ──────────────────────────────
st.markdown(
    """
    <style>
    /* ── Google Fonts ── */
    @import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@400;600;700;800&family=Noto+Sans:wght@400;500;600&display=swap');

    /* ── Root Variables ── */
    :root {
        --saffron:  #FF6B00;
        --green:    #138808;
        --navy:     #000080;
        --white:    #FFFFFF;
        --cream:    #FFF8F0;
        --card-bg:  #FFFFFF;
        --border:   #E8DDD0;
        --text:     #1A1A2E;
        --muted:    #6B7280;
        --success:  #22C55E;
        --danger:   #EF4444;
    }

    /* ── Base ── */
    html, body, [class*="css"] {
        font-family: 'Noto Sans', sans-serif;
        color: var(--text);
    }
    .main { background: var(--cream); }
    .block-container { padding: 1.5rem 2rem 3rem; max-width: 1100px; }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #000080 0%, #0A0A5C 100%);
        border-right: 3px solid var(--saffron);
    }
    section[data-testid="stSidebar"] * { color: #FFFFFF !important; }
    section[data-testid="stSidebar"] .stRadio label { font-size: 0.95rem; }

    /* ── Header Brand ── */
    .brand-header {
        font-family: 'Baloo 2', cursive;
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #FF6B00 30%, #FFAB00 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.1;
        margin: 0;
    }
    .brand-tagline {
        font-size: 0.9rem;
        color: var(--muted);
        margin-top: 4px;
        letter-spacing: 0.03em;
    }

    /* ── Metric Cards ── */
    .metric-card {
        background: var(--card-bg);
        border: 1px solid var(--border);
        border-top: 4px solid var(--saffron);
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        text-align: center;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        transition: transform 0.2s;
    }
    .metric-card:hover { transform: translateY(-3px); }
    .metric-value {
        font-family: 'Baloo 2', cursive;
        font-size: 2.2rem;
        font-weight: 800;
        color: var(--saffron);
    }
    .metric-label {
        font-size: 0.8rem;
        color: var(--muted);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-top: 4px;
    }

    /* ── Solver Card ── */
    .solver-card {
        background: linear-gradient(135deg, #fff 70%, #FFF3E0 100%);
        border: 1px solid var(--border);
        border-left: 5px solid var(--saffron);
        border-radius: 14px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(255,107,0,0.10);
        margin-top: 1rem;
    }
    .solver-name {
        font-family: 'Baloo 2', cursive;
        font-size: 1.4rem;
        font-weight: 700;
        color: var(--navy);
    }
    .solver-domain-badge {
        display: inline-block;
        padding: 3px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-left: 8px;
        background: var(--saffron);
        color: white;
    }

    /* ── Domain Tag Pills ── */
    .domain-agriculture { background: #D4EDDA; color: #155724; }
    .domain-education   { background: #CCE5FF; color: #004085; }
    .domain-healthcare  { background: #F8D7DA; color: #721C24; }
    .domain-msme        { background: #FFF3CD; color: #856404; }
    .domain-rural       { background: #E2D9F3; color: #4A235A; }

    /* ── Status Badge ── */
    .status-paid    { color: var(--success); font-weight: 700; }
    .status-pending { color: var(--danger);  font-weight: 700; }

    /* ── QR Section ── */
    .qr-box {
        background: white;
        border: 2px dashed var(--saffron);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
    }

    /* ── Divider ── */
    .tricolor-bar {
        height: 4px;
        background: linear-gradient(90deg, #FF6B00 33%, #FFFFFF 33%, #FFFFFF 66%, #138808 66%);
        border-radius: 2px;
        margin: 1rem 0 1.5rem;
    }

    /* ── Button overrides ── */
    .stButton > button {
        font-family: 'Baloo 2', cursive;
        font-weight: 600;
        border-radius: 10px;
        transition: all 0.2s;
    }
    .stButton > button:hover { transform: translateY(-1px); box-shadow: 0 4px 14px rgba(0,0,0,0.15); }

    /* ── Form inputs ── */
    .stTextInput input, .stTextArea textarea {
        border-radius: 10px;
        border: 1.5px solid var(--border);
        font-family: 'Noto Sans', sans-serif;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: var(--saffron);
        box-shadow: 0 0 0 3px rgba(255,107,0,0.15);
    }

    /* ── Info/Warning boxes ── */
    .info-box {
        background: #EFF6FF;
        border-left: 4px solid #3B82F6;
        border-radius: 0 8px 8px 0;
        padding: 0.75rem 1rem;
        font-size: 0.9rem;
        margin: 0.5rem 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── 3. Supabase Client — cached singleton ───────────────────
@st.cache_resource(show_spinner="Connecting to JanSetu Database…")
def get_supabase() -> Client:
    """Return a cached Supabase client using secrets."""
    try:
        url: str = st.secrets["SUPABASE_URL"]
        key: str = st.secrets["SUPABASE_KEY"]
        client: Client = create_client(url, key)
        return client
    except KeyError as e:
        st.error(
            f"⚠️ Missing Streamlit secret: {e}. "
            "Add SUPABASE_URL and SUPABASE_KEY to `.streamlit/secrets.toml`."
        )
        st.stop()
    except Exception as e:
        st.error(f"❌ Could not connect to Supabase: {e}")
        st.stop()


# Store client in session state for pages
if "supabase" not in st.session_state:
    st.session_state["supabase"] = get_supabase()

# ── 4. Sidebar Brand Block ───────────────────────────────────
with st.sidebar:
    st.markdown(
        """
        <div style='padding: 1rem 0 0.5rem; text-align:center;'>
            <div style='font-size:2.8rem;'>🇮🇳</div>
            <div style='font-family:"Baloo 2",cursive; font-size:1.6rem;
                        font-weight:800; color:#FF6B00; line-height:1.1;'>
                JanSetu
            </div>
            <div style='font-size:0.72rem; color:#CBD5E1; letter-spacing:0.08em;
                        margin-top:2px; text-transform:uppercase;'>
                Unified Problem-Solving OS for Bharat
            </div>
        </div>
        <hr style='border-color:#FF6B00; margin:0.8rem 0;'>
        """,
        unsafe_allow_html=True,
    )

# ── 5. Page Definitions & Navigation ────────────────────────
citizen_page = st.Page(
    "pages/citizen_portal.py",
    title="Citizen Portal",
    icon="🙋‍♂️",
    default=True,
)

admin_page = st.Page(
    "pages/admin_ledger.py",
    title="Solver & Admin Ledger",
    icon="👨‍🏫",
)

nav = st.navigation(
    {
        "🏠 Platform": [citizen_page, admin_page],
    }
)

# ── 6. Sidebar Footer ────────────────────────────────────────
with st.sidebar:
    st.markdown(
        """
        <div style='position:fixed; bottom:1.5rem; left:0; width:17rem;
                    text-align:center; font-size:0.7rem; color:#94A3B8;'>
            <div style='margin-bottom:4px;'>🔒 Powered by Supabase + Streamlit</div>
            <div>JanSetu v1.0 · Cyphersnova Hackathon 2026</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ── 7. Run navigation ────────────────────────────────────────
nav.run()
