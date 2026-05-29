import streamlit as st
from datetime import datetime

# ── Supabase client from session state ──────────────────────
supabase = st.session_state.get("supabase")

# ── Domain metadata ─────────────────────────────────────────
DOMAIN_COLORS: dict[str, str] = {
    "Agriculture": "#22C55E",
    "Education":   "#3B82F6",
    "Healthcare":  "#EF4444",
    "MSME":        "#F59E0B",
    "Rural Access":"#8B5CF6",
}
DOMAIN_ICONS: dict[str, str] = {
    "Agriculture": "🌾",
    "Education":   "🏫",
    "Healthcare":  "🏥",
    "MSME":        "🏪",
    "Rural Access":"📡",
}

# ════════════════════════════════════════════════════════════
# SECTION A — DATA LOADERS
# ════════════════════════════════════════════════════════════

def load_solvers() -> list[dict]:
    """Fetch all solvers ordered by domain."""
    try:
        res = (
            supabase.table("solvers")
            .select("*")
            .order("domain")
            .execute()
        )
        return res.data or []
    except Exception as e:
        st.error(f"❌ Could not load solvers: {e}")
        return []


def load_queries() -> list[dict]:
    """Fetch all queries joined with solver name, newest first."""
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


def compute_metrics(solvers: list[dict], queries: list[dict]) -> dict:
    """Derive platform KPI metrics from raw data."""
    total_tickets  = len(queries)
    active_solvers = sum(1 for s in solvers if s.get("status") == "Active")
    total_revenue  = sum(
        q["solvers"]["fee"]
        for q in queries
        if q.get("payment_status") == "Paid"
        and q.get("solvers")
    )
    paid_queries   = sum(1 for q in queries if q.get("payment_status") == "Paid")
    pending        = total_tickets - paid_queries
    conversion     = (
        round((paid_queries / total_tickets) * 100, 1)
        if total_tickets > 0 else 0.0
    )
    return {
        "total_tickets":  total_tickets,
        "active_solvers": active_solvers,
        "total_revenue":  total_revenue,
        "paid_queries":   paid_queries,
        "pending":        pending,
        "conversion":     conversion,
    }


# ════════════════════════════════════════════════════════════
# SECTION B — PAGE HEADER
# ════════════════════════════════════════════════════════════

st.markdown(
    """
    <div style='margin-bottom:0.25rem;'>
        <span style='font-family:"Baloo 2",cursive; font-size:2rem;
                     font-weight:800; color:#000080;'>
            👨‍🏫 Solver & Admin Ledger
        </span>
    </div>
    <div style='font-size:0.92rem; color:#6B7280; margin-bottom:0.5rem;'>
        Real-time operational intelligence dashboard for JanSetu platform
        administrators and hackathon judges.
    </div>
    <div class='tricolor-bar'></div>
    """,
    unsafe_allow_html=True,
)

# ── Refresh control ─────────────────────────────────────────
col_refresh, col_ts = st.columns([1, 3])
with col_refresh:
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.rerun()
with col_ts:
    st.markdown(
        f"<div style='font-size:0.78rem; color:#9CA3AF; padding-top:0.6rem;'>"
        f"Last updated: {datetime.now().strftime('%d %b %Y · %H:%M:%S')}</div>",
        unsafe_allow_html=True,
    )

# ════════════════════════════════════════════════════════════
# SECTION C — LOAD DATA
# ════════════════════════════════════════════════════════════

with st.spinner("Loading platform data…"):
    solvers = load_solvers()
    queries = load_queries()
    metrics = compute_metrics(solvers, queries)

# ════════════════════════════════════════════════════════════
# SECTION D — KPI METRIC CARDS  (Row 1)
# ════════════════════════════════════════════════════════════

st.markdown("### 📊 Platform KPIs")

m1, m2, m3, m4, m5, m6 = st.columns(6)
kpis = [
    ("🎫", str(metrics["total_tickets"]),  "Total Tickets"),
    ("⚡", str(metrics["active_solvers"]), "Active Solvers"),
    ("💰", f"₹{metrics['total_revenue']}", "Micro-Revenue"),
    ("✅", str(metrics["paid_queries"]),   "Paid Sessions"),
    ("⏳", str(metrics["pending"]),         "Pending"),
    ("📈", f"{metrics['conversion']}%",    "Conversion"),
]
for col, (icon, value, label) in zip([m1, m2, m3, m4, m5, m6], kpis):
    with col:
        st.markdown(
            f"""
            <div class='metric-card'>
                <div style='font-size:1.4rem;'>{icon}</div>
                <div class='metric-value'>{value}</div>
                <div class='metric-label'>{label}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ════════════════════════════════════════════════════════════
# SECTION E — DOMAIN DISTRIBUTION BAR
# ════════════════════════════════════════════════════════════

st.markdown("<br>", unsafe_allow_html=True)

# Count queries per domain
domain_counts: dict[str, int] = {}
for q in queries:
    d = q.get("ai_category", "Unknown")
    domain_counts[d] = domain_counts.get(d, 0) + 1

if domain_counts:
    st.markdown("### 🗂️ Query Distribution by Domain")

    total_q = sum(domain_counts.values()) or 1
    bar_html = "<div style='display:flex; gap:4px; border-radius:8px; overflow:hidden; height:28px; margin:0.5rem 0 0.3rem;'>"
    for domain, count in sorted(domain_counts.items(),
                                key=lambda x: x[1], reverse=True):
        pct = round((count / total_q) * 100, 1)
        color = DOMAIN_COLORS.get(domain, "#94A3B8")
        icon  = DOMAIN_ICONS.get(domain, "❓")
        bar_html += (
            f"<div style='flex:{pct}; background:{color}; "
            f"display:flex; align-items:center; justify-content:center; "
            f"font-size:0.72rem; font-weight:700; color:white; "
            f"white-space:nowrap; overflow:hidden; padding:0 6px;'>"
            f"{icon} {pct}%</div>"
        )
    bar_html += "</div>"
    st.markdown(bar_html, unsafe_allow_html=True)

    # Legend
    legend_html = "<div style='display:flex; gap:12px; flex-wrap:wrap; margin-bottom:1rem;'>"
    for domain, count in sorted(domain_counts.items(),
                                key=lambda x: x[1], reverse=True):
        color = DOMAIN_COLORS.get(domain, "#94A3B8")
        icon  = DOMAIN_ICONS.get(domain, "❓")
        legend_html += (
            f"<span style='font-size:0.78rem; display:flex; align-items:center; gap:4px;'>"
            f"<span style='width:10px; height:10px; background:{color}; "
            f"border-radius:2px; display:inline-block;'></span>"
            f"{icon} {domain} ({count})</span>"
        )
    legend_html += "</div>"
    st.markdown(legend_html, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# SECTION F — LIVE QUERY LOG
# ════════════════════════════════════════════════════════════

st.markdown("### 📋 Live Query Ledger")

if not queries:
    st.markdown(
        """
        <div style='text-align:center; padding:3rem; color:#9CA3AF;
                    background:white; border-radius:12px;
                    border:1px dashed #E8DDD0;'>
            <div style='font-size:2rem; margin-bottom:0.5rem;'>📭</div>
            <div style='font-size:0.9rem;'>No queries yet. Submit one from the
                Citizen Portal!</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    # Table header
    st.markdown(
        """
        <div style='display:grid;
                    grid-template-columns: 50px 1fr 1fr 110px 100px 130px 90px;
                    gap:8px; padding:0.5rem 1rem;
                    background:#F8FAFC; border-radius:8px 8px 0 0;
                    border:1px solid #E8DDD0;
                    font-size:0.72rem; font-weight:700; color:#9CA3AF;
                    text-transform:uppercase; letter-spacing:0.06em;'>
            <div>#ID</div>
            <div>Citizen</div>
            <div>Problem (truncated)</div>
            <div>AI Domain</div>
            <div>Solver</div>
            <div>Fee</div>
            <div>Status</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for i, q in enumerate(queries):
        solver_info = q.get("solvers") or {}
        solver_name = solver_info.get("name", "—")
        solver_fee  = solver_info.get("fee",  "—")
        solver_fee_str = f"₹{solver_fee}" if solver_fee != "—" else "—"

        domain      = q.get("ai_category", "—")
        d_color     = DOMAIN_COLORS.get(domain, "#94A3B8")
        d_icon      = DOMAIN_ICONS.get(domain, "❓")

        status      = q.get("payment_status", "Pending")
        status_color = "#22C55E" if status == "Paid" else "#EF4444"
        status_bg    = "#F0FDF4" if status == "Paid" else "#FEF2F2"
        status_icon  = "✅" if status == "Paid" else "⏳"

        raw_preview = (q.get("raw_problem") or "")[:55]
        if len(q.get("raw_problem", "")) > 55:
            raw_preview += "…"

        # Created at
        created_raw = q.get("created_at", "")
        try:
            dt = datetime.fromisoformat(created_raw.replace("Z", "+00:00"))
            created_str = dt.strftime("%d %b %H:%M")
        except Exception:
            created_str = created_raw[:16] if created_raw else "—"

        row_bg = "#FFFFFF" if i % 2 == 0 else "#FAFAFA"

        st.markdown(
            f"""
            <div style='display:grid;
                        grid-template-columns: 50px 1fr 1fr 110px 100px 130px 90px;
                        gap:8px; padding:0.65rem 1rem;
                        background:{row_bg};
                        border:1px solid #E8DDD0; border-top:none;
                        font-size:0.82rem; color:#374151;
                        align-items:center;'>
                <div style='font-weight:700; color:#000080;'>
                    #{q.get("id","?")}
                </div>
                <div>
                    <div style='font-weight:600;'>{q.get("citizen_name","—")}</div>
                    <div style='font-size:0.7rem; color:#9CA3AF;'>{created_str}</div>
                </div>
                <div style='font-size:0.78rem; color:#6B7280;
                            font-style:italic; overflow:hidden;
                            text-overflow:ellipsis; white-space:nowrap;'
                     title='{q.get("raw_problem","").replace("'","")}'>
                    {raw_preview}
                </div>
                <div>
                    <span style='background:{d_color}22; color:{d_color};
                                 border:1px solid {d_color}44;
                                 border-radius:20px; padding:2px 10px;
                                 font-size:0.72rem; font-weight:700;
                                 white-space:nowrap;'>
                        {d_icon} {domain}
                    </span>
                </div>
                <div style='font-size:0.8rem; font-weight:500;'>
                    {solver_name}
                </div>
                <div style='font-weight:700; color:#FF6B00;'>
                    {solver_fee_str}
                </div>
                <div>
                    <span style='background:{status_bg}; color:{status_color};
                                 border:1px solid {status_color}44;
                                 border-radius:20px; padding:2px 10px;
                                 font-size:0.72rem; font-weight:700;'>
                        {status_icon} {status}
                    </span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        f"""
        <div style='padding:0.5rem 1rem; background:#F8FAFC;
                    border:1px solid #E8DDD0; border-top:none;
                    border-radius:0 0 8px 8px; font-size:0.75rem;
                    color:#9CA3AF; text-align:right;'>
            Showing {len(queries)} record(s) · Auto-sorted newest first
        </div>
        """,
        unsafe_allow_html=True,
    )

# ════════════════════════════════════════════════════════════
# SECTION G — SOLVER REGISTRY
# ════════════════════════════════════════════════════════════

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### 🧑‍💼 Verified Solver Registry")

if not solvers:
    st.info("No solvers found. Run the database_setup.sql to seed data.")
else:
    cols = st.columns(3)
    for i, solver in enumerate(solvers):
        with cols[i % 3]:
            domain      = solver.get("domain", "Unknown")
            d_color     = DOMAIN_COLORS.get(domain, "#94A3B8")
            d_icon      = DOMAIN_ICONS.get(domain, "❓")
            status      = solver.get("status", "Unknown")
            status_dot  = "🟢" if status == "Active" else "🔴"
            rating      = solver.get("rating", 0)
            stars_full  = "★" * int(rating)
            stars_empty = "☆" * (5 - int(rating))

            st.markdown(
                f"""
                <div style='background:white; border:1px solid #E8DDD0;
                            border-top:4px solid {d_color};
                            border-radius:12px; padding:1.1rem 1.25rem;
                            margin-bottom:1rem;
                            box-shadow:0 2px 10px rgba(0,0,0,0.05);'>
                    <div style='display:flex; justify-content:space-between;
                                align-items:center; margin-bottom:6px;'>
                        <div style='font-family:"Baloo 2",cursive;
                                    font-weight:700; font-size:1rem;
                                    color:#1A1A2E;'>
                            {d_icon} {solver.get("name","—")}
                        </div>
                        <div style='font-size:0.72rem;'>{status_dot} {status}</div>
                    </div>
                    <div style='background:{d_color}15; color:{d_color};
                                border-radius:6px; padding:2px 10px;
                                font-size:0.72rem; font-weight:700;
                                display:inline-block; margin-bottom:8px;'>
                        {domain}
                    </div>
                    <div style='font-size:0.82rem; color:#6B7280; margin-bottom:4px;'>
                        📍 {solver.get("location","—")}
                    </div>
                    <div style='display:flex; justify-content:space-between;
                                align-items:center; margin-top:8px;
                                padding-top:8px; border-top:1px solid #F3F4F6;'>
                        <div style='color:#F59E0B; font-size:0.85rem;
                                    letter-spacing:1px;'>
                            {stars_full}<span style='color:#D1D5DB;'>{stars_empty}</span>
                            <span style='color:#374151; font-size:0.78rem;
                                        margin-left:4px;'>{rating}</span>
                        </div>
                        <div style='font-weight:800; color:#FF6B00;
                                    font-family:"Baloo 2",cursive; font-size:1.1rem;'>
                            ₹{solver.get("fee","—")}
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

# ════════════════════════════════════════════════════════════
# SECTION H — ESCROW SUMMARY TABLE
# ════════════════════════════════════════════════════════════

st.markdown("### 💼 Escrow Micro-Revenue Summary")

paid_by_domain: dict[str, int] = {}
count_by_domain: dict[str, int] = {}
for q in queries:
    if q.get("payment_status") == "Paid" and q.get("solvers"):
        d   = q.get("ai_category", "Unknown")
        fee = q["solvers"].get("fee", 0)
        paid_by_domain[d]   = paid_by_domain.get(d, 0) + fee
        count_by_domain[d]  = count_by_domain.get(d, 0) + 1

if not paid_by_domain:
    st.markdown(
        """
        <div style='background:#FFFBEB; border:1px solid #FDE68A;
                    border-radius:10px; padding:1rem 1.5rem;
                    font-size:0.88rem; color:#92400E;'>
            ⏳ No paid transactions yet. Revenue will appear here once
            citizens confirm payments.
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    total_escrow = sum(paid_by_domain.values())

    # Header
    st.markdown(
        """
        <div style='display:grid; grid-template-columns:2fr 1fr 1fr 1fr;
                    gap:8px; padding:0.5rem 1rem;
                    background:#F8FAFC; border-radius:8px 8px 0 0;
                    border:1px solid #E8DDD0;
                    font-size:0.72rem; font-weight:700; color:#9CA3AF;
                    text-transform:uppercase; letter-spacing:0.06em;'>
            <div>Domain</div>
            <div>Sessions</div>
            <div>Revenue</div>
            <div>Avg. Ticket</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for j, (domain, revenue) in enumerate(
        sorted(paid_by_domain.items(), key=lambda x: x[1], reverse=True)
    ):
        d_color  = DOMAIN_COLORS.get(domain, "#94A3B8")
        d_icon   = DOMAIN_ICONS.get(domain, "❓")
        sessions = count_by_domain.get(domain, 1)
        avg_fee  = round(revenue / sessions, 0)
        row_bg   = "#FFFFFF" if j % 2 == 0 else "#FAFAFA"

        st.markdown(
            f"""
            <div style='display:grid; grid-template-columns:2fr 1fr 1fr 1fr;
                        gap:8px; padding:0.65rem 1rem;
                        background:{row_bg};
                        border:1px solid #E8DDD0; border-top:none;
                        font-size:0.85rem; color:#374151; align-items:center;'>
                <div style='display:flex; align-items:center; gap:8px;'>
                    <span style='width:10px; height:10px; background:{d_color};
                                 border-radius:2px; display:inline-block;'></span>
                    {d_icon} {domain}
                </div>
                <div style='font-weight:600;'>{sessions}</div>
                <div style='font-weight:800; color:#22C55E;'>₹{revenue}</div>
                <div style='color:#6B7280;'>₹{int(avg_fee)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Total row
    st.markdown(
        f"""
        <div style='display:grid; grid-template-columns:2fr 1fr 1fr 1fr;
                    gap:8px; padding:0.65rem 1rem;
                    background:#FFF8F0;
                    border:2px solid #FF6B00; border-top:none;
                    border-radius:0 0 8px 8px;
                    font-size:0.88rem; font-weight:800;
                    color:#1A1A2E; align-items:center;'>
            <div>🏆 TOTAL</div>
            <div>{sum(count_by_domain.values())}</div>
            <div style='color:#FF6B00; font-size:1rem;'>₹{total_escrow}</div>
            <div>—</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ── Admin Footer ─────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(
    """
    <div style='text-align:center; font-size:0.75rem; color:#9CA3AF;
                padding:1rem; border-top:1px solid #E8DDD0;'>
        🔐 Admin Ledger · JanSetu v1.0 · All transactions are immutable
        and stored in Supabase PostgreSQL.
        <br>
        Data refreshes on every page load. Click "Refresh Data" for live pull.
    </div>
    """,
    unsafe_allow_html=True,
)
