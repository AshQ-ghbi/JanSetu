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

# ── 2. Supabase Connection (cached, runs once) ───────────────
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

# ── 3. Sidebar Brand ─────────────────────────────────────────
with st.sidebar:
    st.markdown("# 🇮🇳 JanSetu")
    st.markdown("**India's Own Problem-Solving OS**")
    st.markdown("*Connecting citizens with verified local experts*")
    st.divider()
    st.markdown("**5 Domains Covered:**")
    st.markdown("🌾 Agriculture")
    st.markdown("🏫 Education")
    st.markdown("🏥 Healthcare")
    st.markdown("🏪 MSME")
    st.markdown("📡 Rural Access")
    st.divider()
    st.caption("🔒 Powered by Beyond Life")
    st.caption("Connect with builders at Github")
    st.caption("JanSetu v1.0 · Cyphersnova Hackathon 2026 by Ashish Kumar")

# ── 4. Page Definitions ──────────────────────────────────────
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

# ── 5. Navigation ─────────────────────────────────────────────
nav = st.navigation({
    "🏠 JanSetu Platform": [citizen_page, admin_page],
})

nav.run()
