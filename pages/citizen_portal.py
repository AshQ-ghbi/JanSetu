import io
import streamlit as st

# ── Lazy imports (installed via requirements.txt) ────────────
try:
    import qrcode
    from qrcode.image.pil import PilImage
    QR_AVAILABLE = True
except ImportError:
    QR_AVAILABLE = False

# ── Supabase client from session state ──────────────────────
supabase = st.session_state.get("supabase")

# ════════════════════════════════════════════════════════════
# SECTION A — NLP CLASSIFIER
# ════════════════════════════════════════════════════════════

DOMAIN_KEYWORDS: dict[str, list[str]] = {
    "Agriculture": [
        "crop", "pest", "farming", "kisan", "fasal", "weather", "rain",
        "drought", "fertilizer", "kheti", "soil", "harvest", "insect",
        "blight", "mandi", "wheat", "rice", "cotton", "soybean", "irrigation",
        "seeds", "pesticide", "weed", "locust", "fungus", "agri",
    ],
    "Education": [
        "study", "school", "exam", "tutor", "student", "learn", "marks",
        "class", "teacher", "padhai", "book", "coaching", "math", "science",
        "english", "board", "neet", "jee", "degree", "college", "scholarship",
        "homework", "assignment", "syllabus", "cbse", "ncert",
    ],
    "Healthcare": [
        "doctor", "fever", "pain", "hospital", "medicine", "sick", "ill",
        "health", "opd", "treatment", "clinic", "dawa", "bukhar", "blood",
        "sugar", "diabetes", "bp", "cough", "cold", "child", "baby",
        "pregnant", "delivery", "nurse", "ayushman", "vaccine", "injection",
    ],
    "MSME": [
        "loan", "business", "shop", "udyog", "mudra", "msme", "registration",
        "gst", "invoice", "credit", "bank", "startup", "trade", "sell",
        "market", "entrepreneur", "license", "subsidy", "export", "import",
        "goods", "manufacturing", "capital", "finance", "account",
    ],
    "Rural Access": [
        "internet", "village", "gaon", "connectivity", "digital", "wifi",
        "mobile", "sim", "network", "signal", "csc", "e-governance",
        "certificate", "ration", "aadhar", "pension", "scheme", "sarkari",
        "jan dhan", "pm kisan", "electricity", "bijli", "road", "panchayat",
    ],
}

DOMAIN_COLORS: dict[str, str] = {
    "Agriculture": "#22C55E",
    "Education":   "#3B82F6",
    "Healthcare":  "#EF4444",
    "MSME":        "#F59E0B",
    "Rural Access":"#8B5CF6",
}

DOMAIN_ICONS: dict[str, str] = {
    "Agriculture": "🌾",
    "Education":   "📚",
    "Healthcare":  "🏥",
    "MSME":        "🏪",
    "Rural Access":"📡",
}


def classify_problem(text: str) -> str:
    """
    Keyword-frequency NLP classifier.
    Scores each domain by counting matched keywords in lowercase text.
    Returns the domain with the highest score, defaulting to 'Rural Access'.
    """
    text_lower = text.lower()
    scores: dict[str, int] = {domain: 0 for domain in DOMAIN_KEYWORDS}

    for domain, keywords in DOMAIN_KEYWORDS.items():
        for kw in keywords:
            if kw in text_lower:
                scores[domain] += 1

    best_domain = max(scores, key=lambda d: scores[d])
    # If no keyword matched at all, default to Rural Access
    if scores[best_domain] == 0:
        return "Rural Access"
    return best_domain


# ════════════════════════════════════════════════════════════
# SECTION B — DATABASE HELPERS
# ════════════════════════════════════════════════════════════

def fetch_solver_by_domain(domain: str) -> dict | None:
    """Return the first active solver matching the given domain."""
    try:
        res = (
            supabase.table("solvers")
            .select("*")
            .eq("domain", domain)
            .eq("status", "Active")
            .order("rating", desc=True)
            .limit(1)
            .execute()
        )
        if res.data:
            return res.data[0]
        return None
    except Exception as e:
        st.error(f"❌ Solver lookup failed: {e}")
        return None


def insert_query(citizen_name: str, raw_problem: str,
                 ai_category: str, solver_id: int) -> int | None:
    """Insert a new citizen query row and return its generated id."""
    try:
        res = (
            supabase.table("queries")
            .insert({
                "citizen_name":      citizen_name,
                "raw_problem":       raw_problem,
                "ai_category":       ai_category,
                "matched_solver_id": solver_id,
                "payment_status":    "Pending",
            })
            .execute()
        )
        if res.data:
            return res.data[0]["id"]
        return None
    except Exception as e:
        st.error(f"❌ Failed to save query: {e}")
        return None


def mark_query_paid(query_id: int) -> bool:
    """Update payment_status to 'Paid' for the given query id."""
    try:
        supabase.table("queries").update(
            {"payment_status": "Paid"}
        ).eq("id", query_id).execute()
        return True
    except Exception as e:
        st.error(f"❌ Payment update failed: {e}")
        return False


# ════════════════════════════════════════════════════════════
# SECTION C — QR CODE GENERATOR
# ════════════════════════════════════════════════════════════

def generate_upi_qr(fee: int) -> bytes | None:
    """
    Build a UPI deep-link and render it as a PNG QR code in memory.
    Returns raw PNG bytes, or None if qrcode library is unavailable.
    """
    if not QR_AVAILABLE:
        return None

    upi_link = (
        f"upi://pay?pa=jansetu@upi"
        f"&pn=JanSetu"
        f"&am={fee}"
        f"&cu=INR"
        f"&tn=JanSetu+Consultation+Fee"
    )

    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=8,
        border=3,
    )
    qr.add_data(upi_link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#000080", back_color="white")

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf.read()


# ════════════════════════════════════════════════════════════
# SECTION D — PAGE RENDER
# ════════════════════════════════════════════════════════════

# ── Page Header ─────────────────────────────────────────────
st.markdown(
    """
    <div style='margin-bottom:0.25rem;'>
        <span style='font-family:"Baloo 2",cursive; font-size:2rem;
                     font-weight:800; color:#FF6B00;'>🙋‍♂️ Citizen Portal</span>
    </div>
    <div style='font-size:0.92rem; color:#6B7280; margin-bottom:0.5rem;'>
        Describe your problem in <b>any language</b> — Hindi, English, or your local dialect.
        JanSetu's AI will instantly match you with a verified local specialist.
    </div>
    <div class='tricolor-bar'></div>
    """,
    unsafe_allow_html=True,
)

# ── How It Works strip ──────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
steps = [
    ("1️⃣", "Describe", "Type your problem"),
    ("2️⃣", "AI Match",  "We classify & match"),
    ("3️⃣", "Pay ₹",     "Scan UPI QR code"),
    ("4️⃣", "Connect",   "Get expert contact"),
]
for col, (icon, title, desc) in zip([c1, c2, c3, c4], steps):
    with col:
        st.markdown(
            f"""
            <div style='text-align:center; padding:0.6rem 0.2rem;
                        background:white; border-radius:10px;
                        border:1px solid #E8DDD0; margin-bottom:1rem;'>
                <div style='font-size:1.4rem;'>{icon}</div>
                <div style='font-weight:700; font-size:0.82rem;
                            color:#000080;'>{title}</div>
                <div style='font-size:0.72rem; color:#9CA3AF;'>{desc}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ════════════════════════════════════════════════════════════
# SECTION E — INPUT FORM
# ════════════════════════════════════════════════════════════

with st.form("citizen_form", clear_on_submit=False):
    st.markdown("### 📝 Submit Your Problem")

    col_name, col_lang = st.columns([2, 1])
    with col_name:
        citizen_name = st.text_input(
            "Your Name / आपका नाम",
            placeholder="e.g., Ramesh Kumar",
            help="Enter your full name",
        )
    with col_lang:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            "<div class='info-box'>✅ Hindi & English supported</div>",
            unsafe_allow_html=True,
        )

    raw_problem = st.text_area(
        "Describe your problem / अपनी समस्या बताएं",
        placeholder=(
            "e.g., 'Mere khet mein kal se patte pile pad rahe hain aur "
            "pest ka attack lag raha hai. Koi salah do.' \n\n"
            "or: 'My daughter needs affordable math tutoring for Class 10 boards.'"
        ),
        height=140,
        help="Write in Hindi, English, or mix both — our AI understands all.",
    )

    submitted = st.form_submit_button(
        "🔍 Find My Specialist  →",
        use_container_width=True,
        type="primary",
    )

# ════════════════════════════════════════════════════════════
# SECTION F — PROCESSING & RESULTS
# ════════════════════════════════════════════════════════════

if submitted:
    # ── Validation ──────────────────────────────────────────
    if not citizen_name.strip():
        st.warning("⚠️ Please enter your name.")
        st.stop()
    if len(raw_problem.strip()) < 10:
        st.warning("⚠️ Please describe your problem in at least 10 characters.")
        st.stop()

    # ── Step 1: Classify ────────────────────────────────────
    with st.spinner("🤖 JanSetu AI is analysing your problem…"):
        domain = classify_problem(raw_problem)

    color = DOMAIN_COLORS[domain]
    icon  = DOMAIN_ICONS[domain]

    st.markdown(
        f"""
        <div style='display:flex; align-items:center; gap:12px;
                    background:white; border-radius:12px; padding:1rem 1.25rem;
                    border:1px solid {color}33; border-left:5px solid {color};
                    margin:1rem 0;'>
            <div style='font-size:2rem;'>{icon}</div>
            <div>
                <div style='font-size:0.72rem; color:#9CA3AF;
                            text-transform:uppercase; letter-spacing:0.08em;'>
                    AI Classification
                </div>
                <div style='font-family:"Baloo 2",cursive; font-size:1.3rem;
                            font-weight:700; color:{color};'>
                    {domain}
                </div>
            </div>
            <div style='margin-left:auto; font-size:0.75rem; color:#6B7280;'>
                Confidence: High ✅
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Step 2: Fetch solver ─────────────────────────────────
    with st.spinner("🔎 Matching you with the best local expert…"):
        solver = fetch_solver_by_domain(domain)

    if not solver:
        st.error(
            f"😔 No active solver found for **{domain}** right now. "
            "Please try again shortly or contact support."
        )
        st.stop()

    # ── Step 3: Save query to DB ────────────────────────────
    query_id = insert_query(
        citizen_name=citizen_name.strip(),
        raw_problem=raw_problem.strip(),
        ai_category=domain,
        solver_id=solver["id"],
    )

    # Store in session state for payment confirmation
    st.session_state["current_query_id"] = query_id
    st.session_state["current_solver"]   = solver
    st.session_state["payment_done"]     = False

# ════════════════════════════════════════════════════════════
# SECTION G — SOLVER CARD + PAYMENT FLOW
# (Persists across reruns via session_state)
# ════════════════════════════════════════════════════════════

if st.session_state.get("current_solver"):
    solver   = st.session_state["current_solver"]
    query_id = st.session_state.get("current_query_id")
    paid     = st.session_state.get("payment_done", False)

    # ── Solver Profile Card ──────────────────────────────────
    stars = "⭐" * int(solver["rating"]) + (
        "✨" if solver["rating"] % 1 >= 0.5 else ""
    )
    domain_color = DOMAIN_COLORS.get(solver["domain"], "#FF6B00")

    st.markdown(
        f"""
        <div class='solver-card'>
            <div style='display:flex; justify-content:space-between;
                        align-items:flex-start; flex-wrap:wrap; gap:8px;'>
                <div>
                    <span class='solver-name'>👤 {solver["name"]}</span>
                    <span class='solver-domain-badge'
                          style='background:{domain_color};'>
                        {solver["domain"]}
                    </span>
                </div>
                <div style='font-size:0.82rem; color:#6B7280;
                            background:#F3F4F6; padding:4px 12px;
                            border-radius:20px;'>
                    Query #{query_id or "—"}
                </div>
            </div>

            <div style='display:grid; grid-template-columns:1fr 1fr 1fr;
                        gap:1rem; margin-top:1rem;'>
                <div>
                    <div style='font-size:0.7rem; color:#9CA3AF;
                                text-transform:uppercase; letter-spacing:0.06em;'>
                        Location
                    </div>
                    <div style='font-weight:600; font-size:0.95rem;
                                color:#1A1A2E; margin-top:2px;'>
                        📍 {solver["location"]}
                    </div>
                </div>
                <div>
                    <div style='font-size:0.7rem; color:#9CA3AF;
                                text-transform:uppercase; letter-spacing:0.06em;'>
                        Rating
                    </div>
                    <div style='font-weight:600; font-size:0.95rem;
                                color:#1A1A2E; margin-top:2px;'>
                        {stars} {solver["rating"]} / 5.0
                    </div>
                </div>
                <div>
                    <div style='font-size:0.7rem; color:#9CA3AF;
                                text-transform:uppercase; letter-spacing:0.06em;'>
                        Consultation Fee
                    </div>
                    <div style='font-weight:800; font-size:1.2rem;
                                color:#FF6B00; margin-top:2px;'>
                        ₹ {solver["fee"]}
                    </div>
                </div>
            </div>

            <div style='margin-top:0.75rem; padding:0.5rem 0.75rem;
                        background:#FFF8F0; border-radius:8px;
                        font-size:0.82rem; color:#6B7280;'>
                ✅ Verified Specialist &nbsp;|&nbsp;
                🔒 Escrow Protected &nbsp;|&nbsp;
                ⚡ Responds within 2 hours
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Payment Section ─────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)

    if not paid:
        st.markdown("### 💳 Secure Micro-Payment")
        st.markdown(
            f"""
            <div class='info-box'>
                Scan the UPI QR code below to pay <b>₹{solver["fee"]}</b>
                to JanSetu Escrow. Your payment is held safely until your
                consultation is complete.
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ── QR Code ─────────────────────────────────────────
        qr_bytes = generate_upi_qr(solver["fee"])

        col_qr, col_info = st.columns([1, 1.6], gap="large")

        with col_qr:
            st.markdown("<div class='qr-box'>", unsafe_allow_html=True)
            if qr_bytes:
                st.image(
                    qr_bytes,
                    caption=f"Scan to pay ₹{solver['fee']}",
                    width=220,
                )
            else:
                # Fallback: show UPI link text if qrcode not installed
                upi_link = (
                    f"upi://pay?pa=jansetu@upi&pn=JanSetu"
                    f"&am={solver['fee']}&cu=INR"
                )
                st.code(upi_link, language=None)
                st.caption("Install `qrcode[pil]` to show QR image.")
            st.markdown(
                f"""
                <div style='margin-top:0.5rem; font-size:0.78rem;
                            color:#6B7280; text-align:center;'>
                    Pay to: <b>jansetu@upi</b><br>
                    Amount: <b style='color:#FF6B00;'>₹{solver["fee"]}</b>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)

        with col_info:
            st.markdown(
                """
                <div style='padding:1rem 0;'>
                    <div style='font-weight:700; font-size:0.95rem;
                                color:#000080; margin-bottom:0.75rem;'>
                        📲 How to pay:
                    </div>
                    <div style='font-size:0.875rem; color:#374151;
                                line-height:1.8;'>
                        1. Open any UPI app<br>
                           <span style='color:#9CA3AF; font-size:0.78rem;'>
                           (PhonePe, GPay, Paytm, BHIM…)
                           </span><br>
                        2. Tap <b>Scan QR</b><br>
                        3. Point camera at the QR code<br>
                        4. Confirm ₹{} payment<br>
                        5. Click the green button below ✅
                    </div>
                </div>
                """.format(solver["fee"]),
                unsafe_allow_html=True,
            )

            # ── Payment Confirmation Button ──────────────────
            if st.button(
                f"👉 Click here after scanning to confirm payment  ✅",
                use_container_width=True,
                type="primary",
                key="confirm_payment_btn",
            ):
                if query_id:
                    success = mark_query_paid(query_id)
                    if success:
                        st.session_state["payment_done"] = True
                        st.rerun()
                    else:
                        st.error("Payment confirmation failed. Please retry.")
                else:
                    # Edge case: query wasn't saved, still mark locally
                    st.session_state["payment_done"] = True
                    st.rerun()

    else:
        # ── POST-PAYMENT SUCCESS SCREEN ─────────────────────
        st.markdown(
            f"""
            <div style='background:linear-gradient(135deg, #F0FDF4, #DCFCE7);
                        border:2px solid #22C55E; border-radius:16px;
                        padding:2rem; text-align:center; margin-top:1rem;'>
                <div style='font-size:3rem; margin-bottom:0.5rem;'>🎉</div>
                <div style='font-family:"Baloo 2",cursive; font-size:1.5rem;
                            font-weight:800; color:#15803D;'>
                    Payment Confirmed!
                </div>
                <div style='color:#166534; margin:0.5rem 0 1rem;
                            font-size:0.95rem;'>
                    Your consultation fee of <b>₹{solver["fee"]}</b>
                    is safely held in escrow.
                </div>

                <div style='background:white; border-radius:12px;
                            padding:1.25rem 2rem; display:inline-block;
                            border:1px solid #BBF7D0; margin-top:0.5rem;'>
                    <div style='font-size:0.75rem; color:#9CA3AF;
                                text-transform:uppercase; letter-spacing:0.08em;
                                margin-bottom:4px;'>
                        📞 Direct Contact Number
                    </div>
                    <div style='font-family:"Baloo 2",cursive; font-size:2rem;
                                font-weight:800; color:#000080;
                                letter-spacing:0.05em;'>
                        {solver["contact"]}
                    </div>
                    <div style='font-size:0.8rem; color:#6B7280; margin-top:4px;'>
                        {solver["name"]} · {solver["domain"]} Specialist
                    </div>
                </div>

                <div style='margin-top:1.25rem; font-size:0.82rem; color:#6B7280;'>
                    Call or WhatsApp the number above.<br>
                    Escrow is released after your session is complete.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ── New Query button ─────────────────────────────────
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button(
            "🔄 Submit a New Problem",
            use_container_width=True,
            key="new_query_btn",
        ):
            for key in ["current_query_id", "current_solver", "payment_done"]:
                st.session_state.pop(key, None)
            st.rerun()

# ── Footer nudge ────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown(
    """
    <div style='text-align:center; font-size:0.78rem; color:#9CA3AF;
                padding:1rem; border-top:1px solid #E8DDD0; margin-top:2rem;'>
        🔒 Your data is encrypted and never shared without consent. &nbsp;|&nbsp;
        JanSetu is a not-for-profit Digital Public Infrastructure initiative.
    </div>
    """,
    unsafe_allow_html=True,
)
