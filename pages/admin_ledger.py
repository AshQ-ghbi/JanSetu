import streamlit as st
import pandas as pd
from datetime import datetime

supabase = st.session_state.get("supabase")

DOMAIN_ICONS = {
    "Agriculture": "🌾",
    "Education":   "🏫",
    "Healthcare":  "🏥",
    "MSME":        "🏪",
    "Rural Access":"📡",
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
# PAGE HEADER
# ════════════════════════════════════════════════════════════

st.markdown("## 🕵️ Solver & Admin Ledger")
st.caption("Real-time Operational Intelligence Dashboard for JanSetu administrators and hackathon judges.")
st.divider()

# Refresh button
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

total_tickets  = len(queries)
active_solvers = sum(1 for s in solvers if s.get("status") == "Active")
paid_queries   = sum(1 for q in queries if q.get("payment_status") == "Paid")
total_revenue  = sum(
    q["solvers"]["fee"]
    for q in queries
    if q.get("payment_status") == "Paid" and q.get("solvers")
)
pending_queries = total_tickets - paid_queries
conversion_rate = round((paid_queries / total_tickets) * 100, 1) if total_tickets > 0 else 0.0


# ════════════════════════════════════════════════════════════
# KPI METRICS ROW
# ════════════════════════════════════════════════════════════

st.markdown("### 📊 Platform KPIs")

m1, m2, m3, m4, m5, m6 = st.columns(6)

with m1:
    st.metric("🎫 Total Tickets", total_tickets)
with m2:
    st.metric("⚡ Active Solvers", active_solvers)
with m3:
    st.metric("💰 Revenue (₹)", f"₹{total_revenue}")
with m4:
    st.metric("✅ Paid Sessions", paid_queries)
with m5:
    st.metric("⏳ Pending", pending_queries)
with m6:
    st.metric("📈 Conversion", f"{conversion_rate}%")

st.divider()


# ════════════════════════════════════════════════════════════
# QUERY DISTRIBUTION
# ════════════════════════════════════════════════════════════

if queries:
    st.markdown("### 🗂️ Query Distribution by Domain")

    domain_counts = {}
    for q in queries:
        d = q.get("ai_category", "Unknown")
        domain_counts[d] = domain_counts.get(d, 0) + 1

    dist_df = pd.DataFrame(
        [{"Domain": f"{DOMAIN_ICONS.get(d,'❓')} {d}", "Queries": c}
         for d, c in sorted(domain_counts.items(), key=lambda x: x[1], reverse=True)]
    )
    st.bar_chart(dist_df.set_index("Domain"))
    st.divider()


# ════════════════════════════════════════════════════════════
# LIVE QUERY LEDGER
# ════════════════════════════════════════════════════════════

st.markdown("### 📋 Live Query Ledger")

if not queries:
    st.info("📭 No queries yet. Submit one from the Citizen Portal!")
else:
    # Build a clean DataFrame
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

        rows.append({
            "ID":          f"#{q.get('id', '?')}",
            "Citizen":     q.get("citizen_name", "—"),
            "Problem":     (q.get("raw_problem") or "")[:60] + ("..." if len(q.get("raw_problem","")) > 60 else ""),
            "Domain":      f"{DOMAIN_ICONS.get(domain,'❓')} {domain}",
            "Solver":      solver_info.get("name", "—"),
            "Fee":         f"₹{solver_info.get('fee','—')}" if solver_info else "—",
            "Status":      "✅ Paid" if status == "Paid" else "⏳ Pending",
            "Submitted":   created_str,
        })

    df = pd.DataFrame(rows)
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "ID":        st.column_config.TextColumn("ID", width="small"),
            "Citizen":   st.column_config.TextColumn("Citizen", width="medium"),
            "Problem":   st.column_config.TextColumn("Problem Preview", width="large"),
            "Domain":    st.column_config.TextColumn("Domain", width="medium"),
            "Solver":    st.column_config.TextColumn("Matched Solver", width="medium"),
            "Fee":       st.column_config.TextColumn("Fee", width="small"),
            "Status":    st.column_config.TextColumn("Payment", width="small"),
            "Submitted": st.column_config.TextColumn("Submitted", width="medium"),
        },
    )
    st.caption(f"Showing {len(queries)} record(s) · Sorted newest first")

st.divider()


# ════════════════════════════════════════════════════════════
# SOLVER REGISTRY
# ════════════════════════════════════════════════════════════

st.markdown("### 🧑‍💼 Verified Solver Registry")

if not solvers:
    st.warning("No solvers found. Please run database_setup.sql in Supabase.")
else:
    # Show as a clean table
    solver_rows = []
    for s in solvers:
        domain = s.get("domain", "—")
        status = s.get("status", "—")
        rating = s.get("rating", 0)
        stars  = "⭐" * int(rating)

        solver_rows.append({
            "Name":     s.get("name", "—"),
            "Domain":   f"{DOMAIN_ICONS.get(domain,'❓')} {domain}",
            "Location": s.get("location", "—"),
            "Rating":   f"{stars}  {rating}/5",
            "Fee":      f"₹{s.get('fee','—')}",
            "Status":   "🟢 Active" if status == "Active" else "🔴 Inactive",
            "Contact":  s.get("contact", "—"),
        })

    solver_df = pd.DataFrame(solver_rows)
    st.dataframe(
        solver_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Name":     st.column_config.TextColumn("Name", width="medium"),
            "Domain":   st.column_config.TextColumn("Domain", width="medium"),
            "Location": st.column_config.TextColumn("Location", width="large"),
            "Rating":   st.column_config.TextColumn("Rating", width="medium"),
            "Fee":      st.column_config.TextColumn("Fee", width="small"),
            "Status":   st.column_config.TextColumn("Status", width="small"),
            "Contact":  st.column_config.TextColumn("Contact", width="medium"),
        },
    )

st.divider()


# ════════════════════════════════════════════════════════════
# REVENUE SUMMARY TABLE
# ════════════════════════════════════════════════════════════

st.markdown("### 💼 Escrow Revenue Summary by Domain")

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
            "Domain":      f"{DOMAIN_ICONS.get(d,'❓')} {d}",
            "Sessions":    sessions,
            "Revenue":     f"₹{revenue}",
            "Avg. Ticket": f"₹{round(revenue/sessions)}",
        })

    # Add total row
    rev_rows.append({
        "Domain":      "🏆 TOTAL",
        "Sessions":    sum(count_by_domain.values()),
        "Revenue":     f"₹{sum(paid_by_domain.values())}",
        "Avg. Ticket": "—",
    })

    rev_df = pd.DataFrame(rev_rows)
    st.dataframe(
        rev_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Domain":      st.column_config.TextColumn("Domain", width="large"),
            "Sessions":    st.column_config.NumberColumn("Sessions", width="small"),
            "Revenue":     st.column_config.TextColumn("Revenue", width="medium"),
            "Avg. Ticket": st.column_config.TextColumn("Avg. Ticket", width="medium"),
        },
    )

st.divider()
st.caption("🔐 Admin Ledger · JanSetu v1.0 · All transactions stored in Supabase PostgreSQL · Data refreshes on every page load.")
