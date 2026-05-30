import streamlit as st
import pandas as pd
from datetime import datetime

supabase = st.session_state.get("supabase")

DOMAIN_ICONS = {
    "Agriculture": "🌾",
    "Education":   "🏫",
    "Healthcare":  "🏥",
    "MSME":        "🏪",
    "Rural Access": "📡",
}

DOMAIN_COLORS = {
    "Agriculture": "#4CAF50",
    "Education":   "#2196F3",
    "Healthcare":  "#E91E63",
    "MSME":        "#FF9800",
    "Rural Access": "#9C27B0",
}

# ════════════════════════════════════════════════════════════
# DATA LOADERS
# ════════════════════════════════════════════════════════════

def load_solvers():
    try:
        res = supabase.table("solvers").select("*").order("domain").execute()
        return res.data or []
    except Exception as e:
        st.error(f"❌ Could not load solvers: {e}")
        return []


def load_queries():
    try:
        res = (
            supabase.table("queries")
            .select("*, solvers(name, domain, fee)")
            .order("created_at", desc=True)
            .execute()
        )
        return res.data or []
    except Exception as e:
        st.error(f"❌ Could not load queries: {e}")
        return []


# ════════════════════════════════════════════════════════════
# PAGE HEADER — HERO BANNER
# ════════════════════════════════════════════════════════════

st.markdown("""
<div style="
    background: linear-gradient(135deg, #1a1a6e 0%, #000080 50%, #2d0080 100%);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
">
    <div style="font-size:2rem; font-weight:800; color:#FFFFFF; margin-bottom:4px;">
        🕵️ Solver &amp; Admin Ledger
    </div>
    <div style="font-size:0.92rem; color:rgba(255,255,255,0.75); max-width:600px;">
        Real-time Operational Intelligence Dashboard for JanSetu administrators and hackathon judges.
    </div>
    <div style="margin-top:1rem; display:flex; gap:10px; flex-wrap:wrap;">
        <span style="background:rgba(255,255,255,0.12);color:#fff;font-size:0.72rem;font-weight:600;padding:4px 12px;border-radius:20px;">📊 Live KPIs</span>
        <span style="background:rgba(255,255,255,0.12);color:#fff;font-size:0.72rem;font-weight:600;padding:4px 12px;border-radius:20px;">📋 Query Ledger</span>
        <span style="background:rgba(255,255,255,0.12);color:#fff;font-size:0.72rem;font-weight:600;padding:4px 12px;border-radius:20px;">🧑‍💼 Solver Registry</span>
        <span style="background:rgba(255,255,255,0.12);color:#fff;font-size:0.72rem;font-weight:600;padding:4px 12px;border-radius:20px;">💼 Escrow Summary</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Refresh row
col_btn, col_time = st.columns([1, 3])
with col_btn:
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.rerun()
with col_time:
    st.caption(f"Last updated: {datetime.now().strftime('%d %b %Y · %H:%M:%S')}")

# ════════════════════════════════════════════════════════════
# LOAD DATA
# ════════════════════════════════════════════════════════════

with st.spinner("Loading platform data..."):
    solvers = load_solvers()
    queries = load_queries()

total_tickets   = len(queries)
active_solvers  = sum(1 for s in solvers if s.get("status") == "Active")
paid_queries    = sum(1 for q in queries if q.get("payment_status") == "Paid")
total_revenue   = sum(
    q["solvers"]["fee"]
    for q in queries
    if q.get("payment_status") == "Paid" and q.get("solvers")
)
pending_queries = total_tickets - paid_queries
conversion_rate = round((paid_queries / total_tickets) * 100, 1) if total_tickets > 0 else 0.0


# ════════════════════════════════════════════════════════════
# KPI METRICS ROW
# ════════════════════════════════════════════════════════════

st.markdown("""
<div style="font-size:1.1rem; font-weight:700; color:#1A1A2E; margin-bottom:0.75rem;">
    📊 Platform KPIs
</div>
""", unsafe_allow_html=True)

m1, m2, m3, m4, m5, m6 = st.columns(6)

with m1:
    st.metric("🎫 Total Tickets", total_tickets)
with m2:
    st.metric("⚡ Active Solvers", active_solvers)
with m3:
    st.metric("💰 Revenue (₹)", f"₹{total_revenue:,}")
with m4:
    st.metric("✅ Paid Sessions", paid_queries)
with m5:
    st.metric("⏳ Pending", pending_queries)
with m6:
    st.metric("📈 Conversion", f"{conversion_rate}%")

st.markdown("<br>", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# QUERY DISTRIBUTION
# ════════════════════════════════════════════════════════════

if queries:
    st.markdown("""
<div style="font-size:1.1rem; font-weight:700; color:#1A1A2E; margin-bottom:0.75rem;">
    🗂️ Query Distribution by Domain
</div>
""", unsafe_allow_html=True)

    domain_counts = {}
    for q in queries:
        d = q.get("ai_category", "Unknown")
        domain_counts[d] = domain_counts.get(d, 0) + 1

    dist_df = pd.DataFrame(
        [
            {
                "Domain": f"{DOMAIN_ICONS.get(d, '❓')} {d}",
                "Queries": c,
            }
            for d, c in sorted(domain_counts.items(), key=lambda x: x[1], reverse=True)
        ]
    )
    st.bar_chart(dist_df.set_index("Domain"))
    st.markdown("<br>", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# LIVE QUERY LEDGER
# ════════════════════════════════════════════════════════════

st.markdown("""
<div style="font-size:1.1rem; font-weight:700; color:#1A1A2E; margin-bottom:0.75rem;">
    📋 Live Query Ledger
</div>
""", unsafe_allow_html=True)

if not queries:
    st.info("📭 No queries yet. Submit one from the Citizen Portal!")
else:
    rows = []
    for q in queries:
        solver_info = q.get("solvers") or {}
        created_raw = q.get("created_at", "")
        try:
            dt = datetime.fromisoformat(created_raw.replace("Z", "+00:00"))
            created_str = dt.strftime("%d %b %Y  %H:%M")
        except Exception:
            created_str = created_raw[:16] if created_raw else "—"

        domain = q.get("ai_category", "—")
        status = q.get("payment_status", "Pending")
        raw    = q.get("raw_problem") or ""

        rows.append({
            "ID":        f"#{q.get('id', '?')}",
            "Citizen":   q.get("citizen_name", "—"),
            "Problem":   raw[:60] + ("…" if len(raw) > 60 else ""),
            "Domain":    f"{DOMAIN_ICONS.get(domain, '❓')} {domain}",
            "Solver":    solver_info.get("name", "—"),
            "Fee":       f"₹{solver_info.get('fee', '—')}" if solver_info else "—",
            "Status":    "✅ Paid" if status == "Paid" else "⏳ Pending",
            "Submitted": created_str,
        })

    df = pd.DataFrame(rows)
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "ID":        st.column_config.TextColumn("ID",             width="small"),
            "Citizen":   st.column_config.TextColumn("Citizen",        width="medium"),
            "Problem":   st.column_config.TextColumn("Problem Preview", width="large"),
            "Domain":    st.column_config.TextColumn("Domain",         width="medium"),
            "Solver":    st.column_config.TextColumn("Matched Solver", width="medium"),
            "Fee":       st.column_config.TextColumn("Fee",            width="small"),
            "Status":    st.column_config.TextColumn("Payment",        width="small"),
            "Submitted": st.column_config.TextColumn("Submitted",      width="medium"),
        },
    )
    st.caption(f"Showing {len(queries)} record(s) · Sorted newest first")

st.markdown("<br>", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# SOLVER REGISTRY
# ════════════════════════════════════════════════════════════

st.markdown("""
<div style="font-size:1.1rem; font-weight:700; color:#1A1A2E; margin-bottom:0.75rem;">
    🧑‍💼 Verified Solver Registry
</div>
""", unsafe_allow_html=True)

if not solvers:
    st.warning("No solvers found. Please run database_setup.sql in Supabase.")
else:
    solver_rows = []
    for s in solvers:
        domain = s.get("domain", "—")
        status = s.get("status", "—")
        rating = s.get("rating", 0)
        stars  = "⭐" * int(rating)

        solver_rows.append({
            "Name":     s.get("name", "—"),
            "Domain":   f"{DOMAIN_ICONS.get(domain, '❓')} {domain}",
            "Location": s.get("location", "—"),
            "Rating":   f"{stars}  {rating}/5",
            "Fee":      f"₹{s.get('fee', '—')}",
            "Status":   "🟢 Active" if status == "Active" else "🔴 Inactive",
            "Contact":  s.get("contact", "—"),
        })

    solver_df = pd.DataFrame(solver_rows)
    st.dataframe(
        solver_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Name":     st.column_config.TextColumn("Name",     width="medium"),
            "Domain":   st.column_config.TextColumn("Domain",   width="medium"),
            "Location": st.column_config.TextColumn("Location", width="large"),
            "Rating":   st.column_config.TextColumn("Rating",   width="medium"),
            "Fee":      st.column_config.TextColumn("Fee",      width="small"),
            "Status":   st.column_config.TextColumn("Status",   width="small"),
            "Contact":  st.column_config.TextColumn("Contact",  width="medium"),
        },
    )

st.markdown("<br>", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# REVENUE SUMMARY TABLE
# ════════════════════════════════════════════════════════════

st.markdown("""
<div style="font-size:1.1rem; font-weight:700; color:#1A1A2E; margin-bottom:0.75rem;">
    💼 Escrow Revenue Summary by Domain
</div>
""", unsafe_allow_html=True)

paid_by_domain  = {}
count_by_domain = {}
for q in queries:
    if q.get("payment_status") == "Paid" and q.get("solvers"):
        d   = q.get("ai_category", "Unknown")
        fee = q["solvers"].get("fee", 0)
        paid_by_domain[d]  = paid_by_domain.get(d, 0) + fee
        count_by_domain[d] = count_by_domain.get(d, 0) + 1

if not paid_by_domain:
    st.info("⏳ No paid transactions yet. Revenue will appear here once citizens confirm payments.")
else:
    rev_rows = []
    for d, revenue in sorted(paid_by_domain.items(), key=lambda x: x[1], reverse=True):
        sessions = count_by_domain.get(d, 1)
        rev_rows.append({
            "Domain":       f"{DOMAIN_ICONS.get(d, '❓')} {d}",
            "Sessions":     sessions,
            "Revenue":      f"₹{revenue:,}",
            "Avg. Ticket":  f"₹{round(revenue / sessions):,}",
        })

    # Total row
    rev_rows.append({
        "Domain":      "🏆 TOTAL",
        "Sessions":    sum(count_by_domain.values()),
        "Revenue":     f"₹{sum(paid_by_domain.values()):,}",
        "Avg. Ticket": "—",
    })

    rev_df = pd.DataFrame(rev_rows)
    st.dataframe(
        rev_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Domain":      st.column_config.TextColumn("Domain",      width="large"),
            "Sessions":    st.column_config.NumberColumn("Sessions",   width="small"),
            "Revenue":     st.column_config.TextColumn("Revenue",     width="medium"),
            "Avg. Ticket": st.column_config.TextColumn("Avg. Ticket", width="medium"),
        },
    )

# Footer
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style="
    text-align:center;
    font-size:0.75rem;
    color:#94A3B8;
    padding: 1rem 0 0.5rem;
    border-top: 1px solid #E2E8F0;
">
    🔐 Admin Ledger · JanSetu v1.0 · All transactions stored in
    <strong>Supabase PostgreSQL</strong> · Data refreshes on every page load.
</div>
""", unsafe_allow_html=True)
