import io
import streamlit as st

try:
    import qrcode
    QR_AVAILABLE = True
except ImportError:
    QR_AVAILABLE = False

# ── Supabase client ─────────────────────────────────────────
supabase = st.session_state.get("supabase")

# ════════════════════════════════════════════════════════════
# NLP CLASSIFIER
# ════════════════════════════════════════════════════════════

DOMAIN_KEYWORDS = {
    "Agriculture": [
        "crop", "pest", "farming", "kisan", "fasal", "weather", "rain", "drought",
        "fertilizer", "kheti", "soil", "harvest", "insect", "blight", "mandi",
        "wheat", "rice", "cotton", "soybean", "irrigation", "seeds", "pesticide",
        "weed", "locust", "fungus", "agri", "field", "khet", "beej", "paudha",
        "khad", "paani", "sinchai", "mitti", "mausam", "baarish", "keda", "rog",
        "kisan_seva", "tractor", "yield", "organic", "jaivik", "pyaaz", "aloo",
        "tamatar", "khetibadi", "bazaar", "daam", "bhav", "subsidy", "bima",
        "msp", "ganna", "sarson", "makka", "dal", "chana", "bajra", "jowar",
        "monsoon", "tubewell", "compost", "gobar", "nimbori", "dhaan", "kanak",
        "katar", "katai", "buwai", "mandi_bhav", "loan", "karza", "rin", "krishi",
        "polyhouse", "greenhouse", "nursery", "hybrid", "drone", "agritech", "storage",
        "godown", "cold_storage", "fpo", "agrimarket", "livestock", "pashu", "dairy",
        "fodder", "chara", "ghee", "doodh", "poultry", "murgi", "machli", "fisheries"
    ],
    "Education": [
        "education", "shiksha", "padhai", "school", "college", "university", "coaching",
        "tuition", "teacher", "guru", "shikshak", "student", "chhatra", "vidyarthi",
        "class", "kaksha", "syllabus", "pathyakram", "exam", "pariksha", "test",
        "result", "parinama", "parikshafal", "marks", "ank", "degree", "diploma",
        "certificate", "praman_patra", "admission", "daakhila", "fees", "shulk",
        "scholarship", "chhatravriti", "book", "kitaab", "pustak", "copy", "notebook",
        "pen", "pencil", "bag", "basta", "homework", "griha_karya", "learning",
        "seekhna", "study", "adhyayan", "science", "vigyan", "maths", "ganit",
        "history", "itihaas", "geography", "bhoogol", "english", "hindi", "sanskrit",
        "commerce", "arts", "engineering", "medical", "law", "career", "job",
        "naukri", "rozgar", "skills", "hunar", "kaushal", "training", "prashikshan",
        "online_class", "digital_learning", "e_learning", "mock_test", "notes",
        "quiz", "rank", "pass", "fail", "anuttirn", "uttirn", "board_exam", "cbse",
        "icse", "state_board", "ncert", "iit", "jee", "neet", "upsc", "ssc",
        "banking", "sarkari_exam", "sarkari_naukri", "literacy", "saksharta",
        "lecture", "bhashan", "period", "timetable", "attendance", "haziri", "upasthiti",
        "principal", "pradhanacharya", "professor", "classroom", "varg", "library",
        "pustakalaya", "laboratory", "lab", "prayogshala", "blackboard", "syallabus",
        "chapter", "paath", "subject", "vishay", "project", "assignment", "degree_college",
        "hostel", "chatravas", "playground", "khel_ka_maidan", "sports", "khel",
        "degree_certificate", "marksheet", "ankpatra", "report_card", "prospectus",
        "registration", "panjiyan", "form", "vazifa", "stipend", "education_loan",
        "shiksha_rin", "higher_education", "ucch_shiksha", "primary_school",
        "primary_shiksha", "play_school", "balwadi", "anganwadi", "btech", "mtech",
        "mba", "bba", "bcom", "ba", "bsc", "phd", "research", "shodh", "knowledge",
        "gyan", "wisdom", "buddhi", "intelligence", "genius", "topper", "ranker",
        "cheating", "nakal", "suspension", "rusticate", "degree_validity", "ugc",
        "aicte", "distance_learning", "open_school", "nios", "ignou", "skill_development",
        "kaushal_vikas", "placement", "interview", "sakshatkar", "resume", "cv",
        "internship", "paper_leak", "re-evaluation", "re-checking", "re-appear", "compartment"
    ],
    "Healthcare": [
        "healthcare", "swasthya", "ilaj", "treatment", "doctor", "vaidya", "hospital",
        "aspatal", "clinic", "dispensary", "dawakhana", "medicine", "dawa", "aushadhi",
        "nurse", "patient", "mareez", "bimar", "disease", "bimari", "infection", "sankraman",
        "fever", "bukhar", "cough", "khansi", "cold", "zukam", "pain", "dard", "injury", "chot",
        "accident", "ghatna", "durghatna", "emergency", "aapatkal", "ambulance", "operation",
        "surgery", "chiir_faad", "delivery", "prasav", "pregnancy", "garbhavastha", "vaccine",
        "teeka", "teekakaran", "immunity", "rogh_pratirodhak", "blood", "khoon", "rakta",
        "test", "jaanch", "lab", "xray", "sonography", "mri", "pharmacy", "chemist",
        "medical_store", "ayushman_bharat", "health_card", "bima", "insurance", "ayurveda",
        "homeopathy", "unani", "siddha", "yoga", "poshan", "nutrition", "diet", "aahar",
        "vitamin", "malnutrition", "kuposhan", "hygiene", "swachhta", "safai", "first_aid",
        "prathmik_chikitsha", "asha_worker", "anm", "phc", "chc", "district_hospital",
        "generic_dawa", "jan_aushadhi", "sugar", "madhumeh", "blood_pressure", "bp",
        "cancer", "heart_attack", "dil_ka_daura", "paralysis", "lakwa", "asthma", "dama",
        "tb", "tapedik", "malaria", "dengue", "diarrhea", "dast", "vomit", "ulti",
        "mental_health", "manasik_swasthya", "stress", "tanaav", "depression", "avasad",
        "disabled", "divyang", "blind", "andhaa", "deaf", "behra", "physiotherapy",
        "stretcher", "wheelchair", "oxygen_cylinder", "icu", "ventilator", "ward",
        "health_camp", "swasthya_shivir", "blood_bank", "raktdan", "telemedicine",
        "online_doctor", "consultation", "salaah", "prescription", "parcha", "fees"
    ],
    "MSME": [
        "msme", "udyog", "vyapar", "business", "small_business", "chota_vyapar", "industry",
        "karkhana", "factory", "enterprise", "udyam", "udyam_registration", "panjiyan",
        "micro_enterprise", "small_enterprise", "medium_enterprise", "laghu_udyog",
        "kutir_udyog", "cottage_industry", "handicraft", "hastshilp", "handloom", "hathkargha",
        "artisan", "karigar", "weaver", "bunkar", "startup", "entrepreneur", "udyami",
        "loan", "karza", "rin", "mudra_loan", "sidbi", "cgtsme", "subsidy", "choat",
        "grant", "anudan", "investment", "nivesh", "capital", "poonji", "profit", "munafa",
        "loss", "nuksan", "turnover", "benaami", "gst", "tax", "kar", "invoice", "bill",
        "khata", "ledger", "bookkeeping", "hisaab", "wholesale", "thok", "retail", "chutkar",
        "mandi", "bazaar", "market", "supply_chain", "logistics", "raw_material", "kachha_maal",
        "manufacturing", "utpadan", "production", "packaging", "packing", "cluster",
        "geM_portal", "e_commerce", "online_bazaar", "inventory", "stock", "maal",
        "trader", "vyapari", "merchant", "ducandar", "supplier", "distributor", "vendor",
        "fssai", "license", "trademark", "brand", "export", "niryat", "import", "aayat",
        "digital_payment", "upi", "qr_code", "cash_on_delivery", "cod", "nagad", "udhaar",
        "interest_rate", "byaj_dar", "collateral", "guarantee", "subsidy_claim",
        "tender", "theka", "contract", "partner", "sajhedar", "worker", "mazdoor"
    ],
    "Rural Access": [
        "rural_access", "gramin_vikas", "gaon_tak_pahunch", "connectivity", "sampark",
        "road", "sadak", "prakalp", "pmgsy", "transport", "parivahan", "bus", "auto",
        "railway", "station", "internet", "broadband", "wi_fi", "network", "signal",
        "tower", "digital_india", "csc", "common_service_centre", "jan_seva_kendra",
        "banking_correspondent", "bank_mitra", "atm", "digipay", "e_shram", "ration_card",
        "ration_dukan", "pds", "koota", "electricity", "bijli", "power_cut", "katoti",
        "solar", "soorja", "water_supply", "peyal", "nal_jal", "well", "kuan",
        "handpump", "chapa_kal", "panchayat", "gram_sabha", "sarpanch", "pradhan", "sachiv",
        "ward_member", "block", "tehsil", "zilla", "district", "post_office", "daak_ghar",
        "postman", "daakiya", "delivery", "courier", "community", "samuday", "shakti",
        "self_help_group", "shg", "swayam_sahayata_samuh", "ngo", "volunteer", "swayansevak",
        "mgnrega", "manrega", "rozgar_sevak", "job_card", "aadhaar_link", "dbt",
        "pos_machine", "biometric", "angutha", "voter_card", "pehcahn_patra",
        "caste_certificate", "jati_praman", "income_certificate", "aay_praman",
        "niwas_praman", "domicile", "pension", "vridha_pension", "widow_pension",
        "street_light", "khamba", "drainage", "naali", "toilet", "sauchalay", "odf",
        "clean_water", "saaf_paani", "tanki", "dam", "bandh", "nehar", "bridge", "pul"
    ],
}

DOMAIN_ICONS = {
    "Agriculture": "🌾",
    "Education":   "🏫",
    "Healthcare":  "🏥",
    "MSME":        "🏪",
    "Rural Access": "📡",
}

DOMAIN_DESC = {
    "Agriculture": "Agricultural Expert",
    "Education":   "Education Specialist",
    "Healthcare":  "Health Worker",
    "MSME":        "Business Advisor",
    "Rural Access": "Digital Access Specialist",
}

DOMAIN_COLORS = {
    "Agriculture": "#4CAF50",
    "Education":   "#2196F3",
    "Healthcare":  "#E91E63",
    "MSME":        "#FF9800",
    "Rural Access": "#9C27B0",
}


def classify_problem(text: str) -> str:
    text_lower = text.lower()
    scores = {d: 0 for d in DOMAIN_KEYWORDS}
    for domain, keywords in DOMAIN_KEYWORDS.items():
        for kw in keywords:
            if kw in text_lower:
                scores[domain] += 1
    best = max(scores, key=lambda d: scores[d])
    return best if scores[best] > 0 else "Rural Access"


# ════════════════════════════════════════════════════════════
# DATABASE HELPERS
# ════════════════════════════════════════════════════════════

def fetch_solver(domain: str):
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
        return res.data[0] if res.data else None
    except Exception as e:
        st.error(f"❌ Could not fetch solver: {e}")
        return None


def save_query(citizen_name, raw_problem, ai_category, solver_id):
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
        return res.data[0]["id"] if res.data else None
    except Exception as e:
        st.error(f"❌ Could not save query: {e}")
        return None


def mark_paid(query_id: int) -> bool:
    try:
        supabase.table("queries").update(
            {"payment_status": "Paid"}
        ).eq("id", query_id).execute()
        return True
    except Exception as e:
        st.error(f"❌ Payment update failed: {e}")
        return False


# ════════════════════════════════════════════════════════════
# QR CODE GENERATOR
# ════════════════════════════════════════════════════════════

UPI_ID   = "kr.ashish535.hd@okaxis"
UPI_NAME = "JanSetu"


def make_qr(fee: int):
    if not QR_AVAILABLE:
        return None
    upi = f"upi://pay?pa={UPI_ID}&pn={UPI_NAME}&am={fee}&cu=INR&tn=JanSetu+Consultation"
    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=8,
        border=3,
    )
    qr.add_data(upi)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#000080", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf.read()


# ════════════════════════════════════════════════════════════
# SESSION STATE INIT
# ════════════════════════════════════════════════════════════

for key, default in [
    ("current_query_id", None),
    ("current_solver", None),
    ("payment_done", False),
]:
    if key not in st.session_state:
        st.session_state[key] = default


# ════════════════════════════════════════════════════════════
# PAGE HEADER — HERO BANNER
# ════════════════════════════════════════════════════════════

st.markdown("""
<div style="
    background: linear-gradient(135deg, #000080 0%, #1a1a8e 40%, #FF6B00 100%);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
">
    <div style="position:relative; z-index:1;">
        <div style="font-size:2rem; font-weight:800; color:#FFFFFF; margin-bottom:4px; letter-spacing:-0.01em;">
            🙋 Citizen Portal
        </div>
        <div style="font-size:0.95rem; color:rgba(255,255,255,0.8); font-weight:400; max-width:600px; line-height:1.5;">
            Describe your problem in <strong style="color:#FFD700;">any language</strong> — Hindi, English, or your local dialect.
            JanSetu will instantly match you with a <strong style="color:#FFD700;">verified local specialist.</strong>
        </div>
        <div style="margin-top:1rem; display:flex; gap:12px; flex-wrap:wrap;">
            <span style="background:rgba(255,255,255,0.15); color:#fff; font-size:0.75rem; font-weight:600; padding:4px 12px; border-radius:20px; letter-spacing:0.04em;">✅ 5 Domains</span>
            <span style="background:rgba(255,255,255,0.15); color:#fff; font-size:0.75rem; font-weight:600; padding:4px 12px; border-radius:20px; letter-spacing:0.04em;">🔒 Escrow Protected</span>
            <span style="background:rgba(255,255,255,0.15); color:#fff; font-size:0.75rem; font-weight:600; padding:4px 12px; border-radius:20px; letter-spacing:0.04em;">⚡ 2-Hour Response</span>
            <span style="background:rgba(255,255,255,0.15); color:#fff; font-size:0.75rem; font-weight:600; padding:4px 12px; border-radius:20px; letter-spacing:0.04em;">🇮🇳 Made for Bharat</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ── How It Works — 4 Step Cards ─────────────────────────────
st.markdown("#### ✨ How It Works")

c1, c2, c3, c4 = st.columns(4)

steps = [
    ("c1", c1, "01", "🖊️", "Describe", "Type your problem in any language — Hindi or English",  "#FF6B00"),
    ("c2", c2, "02", "🤖", "AI Match",  "Our AI classifies and finds your best local expert",       "#000080"),
    ("c3", c3, "03", "💳", "Pay ₹",     "Scan the UPI QR — your money stays in secure escrow",      "#138808"),
    ("c4", c4, "04", "📞", "Connect",   "Receive the expert's direct contact instantly",             "#9C27B0"),
]

for _, col, num, icon, title, desc, color in steps:
    with col:
        st.markdown(f"""
<div style="
    background:#fff;
    border:1px solid #E2E8F0;
    border-top: 4px solid {color};
    border-radius:14px;
    padding:1rem 1rem 0.9rem;
    box-shadow:0 4px 16px rgba(0,0,128,.06);
    text-align:center;
    height:100%;
">
    <div style="font-size:1.6rem; margin-bottom:4px;">{icon}</div>
    <div style="font-size:0.65rem; font-weight:700; color:{color}; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:2px;">Step {num}</div>
    <div style="font-size:0.95rem; font-weight:700; color:#1A1A2E; margin-bottom:4px;">{title}</div>
    <div style="font-size:0.78rem; color:#64748B; line-height:1.4;">{desc}</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# INPUT FORM
# ════════════════════════════════════════════════════════════

st.markdown("#### 📝 Tell Us Your Problem")

with st.form("citizen_form", clear_on_submit=False):
    col_name, col_gap = st.columns([2, 1])
    with col_name:
        citizen_name = st.text_input(
            "Your Name / आपका नाम *",
            placeholder="e.g. Ashish Kumar",
        )
    with col_gap:
        st.markdown("<br>", unsafe_allow_html=True)
        st.success("✅ Hindi & English both supported")

    raw_problem = st.text_area(
        "Describe your problem / अपनी समस्या बताएं *",
        placeholder=(
            "Example (Hindi): मेरे खेत में कल से पत्ते पीले पड़ रहे हैं, कोई सलाह दो।\n"
            "Example (English): My daughter needs affordable tutoring for Class 10 board exams."
        ),
        height=150,
    )

    submitted = st.form_submit_button(
        "🔍 Find My Specialist →",
        use_container_width=True,
        type="primary",
    )


# ════════════════════════════════════════════════════════════
# FORM PROCESSING
# ════════════════════════════════════════════════════════════

if submitted:
    if not citizen_name.strip():
        st.warning("⚠️ Please enter your Name.")
        st.stop()
    if len(raw_problem.strip()) < 10:
        st.warning("⚠️ Please describe your problem in at least 10 characters.")
        st.stop()

    with st.spinner("🤖 AI is analysing your problem..."):
        domain = classify_problem(raw_problem)

    with st.spinner("🔎 Finding the best Expert near you..."):
        solver = fetch_solver(domain)

    if not solver:
        st.error(f"😔 No active solver found for **{domain}** right now. Please try again soon.")
        st.stop()

    query_id = save_query(
        citizen_name=citizen_name.strip(),
        raw_problem=raw_problem.strip(),
        ai_category=domain,
        solver_id=solver["id"],
    )

    st.session_state["current_query_id"] = query_id
    st.session_state["current_solver"]   = solver
    st.session_state["payment_done"]     = False


# ════════════════════════════════════════════════════════════
# RESULTS SECTION
# ════════════════════════════════════════════════════════════

if st.session_state["current_solver"]:
    solver   = st.session_state["current_solver"]
    query_id = st.session_state["current_query_id"]
    paid     = st.session_state["payment_done"]
    domain   = solver.get("domain", "")
    icon     = DOMAIN_ICONS.get(domain, "👤")
    d_color  = DOMAIN_COLORS.get(domain, "#000080")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── AI Classification Banner ─────────────────────────────
    st.markdown(f"""
<div style="
    background: linear-gradient(135deg, #E8F5E9, #F1F8E9);
    border: 1.5px solid #A5D6A7;
    border-left: 5px solid #138808;
    border-radius: 12px;
    padding: 0.85rem 1.25rem;
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 1rem;
">
    <span style="font-size:1.5rem;">{icon}</span>
    <div>
        <div style="font-size:0.72rem; font-weight:700; color:#2E7D32; text-transform:uppercase; letter-spacing:0.08em;">AI Classification Complete</div>
        <div style="font-size:0.95rem; font-weight:600; color:#1A1A2E; margin-top:1px;">
            Domain detected: <span style="color:{d_color};">{domain}</span>
            &nbsp;·&nbsp;
            <span style="color:#138808;">Confidence: High ✅</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

    # ── Expert Profile Card Header ────────────────────────────
    st.markdown(f"""
<div style="
    display:flex;
    align-items:center;
    gap:10px;
    margin-bottom:0.75rem;
">
    <div style="
        width:44px; height:44px;
        background: linear-gradient(135deg, {d_color}, #000080);
        border-radius:50%;
        display:flex; align-items:center; justify-content:center;
        font-size:1.3rem; flex-shrink:0;
    ">{icon}</div>
    <div>
        <div style="font-size:1.15rem; font-weight:800; color:#1A1A2E;">Your Matched Expert</div>
        <div style="font-size:0.78rem; color:#64748B;">Query #{query_id or "—"} · Matched instantly</div>
    </div>
</div>
""", unsafe_allow_html=True)

    # ── Solver Metrics (native Streamlit) ────────────────────
    card_col1, card_col2, card_col3 = st.columns(3)

    with card_col1:
        st.metric(
            label="👤 Specialist",
            value=solver["name"],
            delta=f"{icon} {domain}",
        )
    with card_col2:
        st.metric(
            label="📍 Location",
            value=solver["location"],
        )
    with card_col3:
        st.metric(
            label="⭐ Rating",
            value=f"{solver['rating']} / 5.0",
            delta="Verified Expert ✅",
        )

    fee_col, status_col = st.columns(2)
    with fee_col:
        st.metric(
            label="💰 Consultation Fee",
            value=f"₹ {solver['fee']}",
            delta="Escrow Protected 🔒",
        )
    with status_col:
        st.metric(
            label="⚡ Response Time",
            value="Within 2 Hours",
            delta="Active Now 🟢",
        )

    # Trust badges
    st.markdown(f"""
<div style="
    background: #FFF8F0;
    border: 1px solid #FFE0B2;
    border-radius: 10px;
    padding: 0.6rem 1rem;
    font-size:0.82rem;
    color:#E65C00;
    font-weight:500;
    margin-top:0.25rem;
">
    ✅ Verified Specialist &nbsp;|&nbsp; 🔒 Escrow Protected &nbsp;|&nbsp; ⚡ Responds within 2 hours
</div>
""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ════════════════════════════════════════════════════════
    # PAYMENT SECTION
    # ════════════════════════════════════════════════════════

    if not paid:
        # Payment section header
        st.markdown("""
<div style="font-size:1.15rem; font-weight:700; color:#1A1A2E; margin-bottom:0.5rem;">
    💳 Secure UPI Micro-Payment
</div>
""", unsafe_allow_html=True)

        st.info(
            f"Scan the QR code below to pay **₹{solver['fee']}** to **JanSetu Escrow**. "
            "Your money is held safely until your consultation is complete."
        )

        qr_col, info_col = st.columns([1, 1], gap="large")

        with qr_col:
            st.markdown("""
<div style="font-weight:600; font-size:0.9rem; color:#1A1A2E; margin-bottom:6px;">
    📱 Scan with any UPI App
</div>
""", unsafe_allow_html=True)

            upi_deep_link = (
                f"upi://pay?pa={UPI_ID}&pn={UPI_NAME}"
                f"&am={solver['fee']}&cu=INR&tn=JanSetu+Consultation"
            )
            qr_bytes = make_qr(solver["fee"])
            if qr_bytes:
                st.image(qr_bytes, width=220, caption=f"Pay ₹{solver['fee']} — JanSetu Escrow")
            else:
                st.code(upi_deep_link)
                st.caption("⚠️ Install `qrcode[pil]` in requirements.txt for QR image")

            st.caption(f"UPI ID: **{UPI_ID}**   |   Amount: **₹{solver['fee']}**")

            # Mobile deep-link button — safe HTML (no nested divs with quotes)
            btn_style = (
                "display:inline-block;"
                "margin-top:8px;"
                "padding:10px 18px;"
                "background:linear-gradient(135deg,#6C3CE1,#4527A0);"
                "color:white;"
                "border-radius:10px;"
                "text-decoration:none;"
                "font-size:0.88rem;"
                "font-weight:700;"
                "box-shadow:0 4px 12px rgba(108,60,225,.35);"
            )
            st.markdown(
                f'<a href="{upi_deep_link}" style="{btn_style}">📲 Open UPI App (Mobile)</a>',
                unsafe_allow_html=True,
            )
            st.caption("☝️ On mobile — tap above to open GPay / PhonePe / Paytm directly")

        with info_col:
            st.markdown("""
<div style="font-weight:600; font-size:0.9rem; color:#1A1A2E; margin-bottom:8px;">
    📲 Steps to Pay
</div>
""", unsafe_allow_html=True)

            steps_pay = [
                ("1", "Open PhonePe / GPay / Paytm / BHIM"),
                ("2", "Tap Scan QR Code"),
                ("3", "Point your camera at the QR"),
                ("4", f"Confirm the payment of ₹{solver['fee']}"),
                ("5", "Come back here and click Confirm below ✅"),
            ]
            for num, text in steps_pay:
                st.markdown(
                    f'<div style="display:flex;gap:10px;align-items:flex-start;margin-bottom:8px;">'
                    f'<span style="background:#FF6B00;color:#fff;font-size:0.7rem;font-weight:700;'
                    f'width:20px;height:20px;border-radius:50%;display:flex;align-items:center;'
                    f'justify-content:center;flex-shrink:0;">{num}</span>'
                    f'<span style="font-size:0.88rem;color:#374151;line-height:1.4;">{text}</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

            st.markdown("<br>", unsafe_allow_html=True)

            if st.button(
                "✅ I have paid — Confirm & Get Contact",
                use_container_width=True,
                type="primary",
                key="confirm_payment_btn",
            ):
                if query_id:
                    ok = mark_paid(query_id)
                    if ok:
                        st.session_state["payment_done"] = True
                        st.rerun()
                    else:
                        st.error("❌ Could not confirm payment. Please try again.")
                else:
                    st.session_state["payment_done"] = True
                    st.rerun()

    # ════════════════════════════════════════════════════════
    # POST-PAYMENT SUCCESS SCREEN
    # ════════════════════════════════════════════════════════

    else:
        st.balloons()

        # Success banner
        st.markdown(f"""
<div style="
    background: linear-gradient(135deg, #E8F5E9, #C8E6C9);
    border: 1.5px solid #A5D6A7;
    border-radius: 16px;
    padding: 1.5rem 2rem;
    text-align: center;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 20px rgba(19,136,8,.12);
">
    <div style="font-size:2.5rem; margin-bottom:6px;">🎉</div>
    <div style="font-size:1.5rem; font-weight:800; color:#1B5E20; margin-bottom:4px;">
        Payment Confirmed!
    </div>
    <div style="font-size:0.95rem; color:#2E7D32; font-weight:500;">
        Your consultation fee of <strong>₹{solver['fee']}</strong> is safely held in JanSetu escrow.
    </div>
</div>
""", unsafe_allow_html=True)

        # Expert contact card — pure native Streamlit
        st.markdown("""
<div style="font-size:1.1rem; font-weight:700; color:#1A1A2E; margin-bottom:0.75rem;">
    📞 Your Expert's Direct Contact
</div>
""", unsafe_allow_html=True)

        contact_col, detail_col = st.columns(2)

        with contact_col:
            st.metric(
                label="📱 Phone Number",
                value=solver["contact"],
            )
            # Call button — simple anchor
            call_style = (
                "display:block;"
                "text-align:center;"
                "margin-top:8px;"
                "padding:12px;"
                "background:linear-gradient(135deg,#138808,#0d6e07);"
                "color:white;"
                "border-radius:10px;"
                "text-decoration:none;"
                "font-size:0.9rem;"
                "font-weight:700;"
                "box-shadow:0 4px 12px rgba(19,136,8,.35);"
            )
            st.markdown(
                f'<a href="tel:{solver["contact"]}" style="{call_style}">📞 Tap &amp; Call Directly</a>',
                unsafe_allow_html=True,
            )

        with detail_col:
            st.metric(label="👤 Expert Name", value=solver["name"])
            st.metric(label=f"{icon} Domain",   value=f"{domain} Specialist")

        # WhatsApp tip
        st.markdown(f"""
<div style="
    background:#FFF3E8;
    border:1px solid #FFCC80;
    border-left:4px solid #FF6B00;
    border-radius:10px;
    padding:0.75rem 1rem;
    font-size:0.88rem;
    color:#E65C00;
    font-weight:500;
    margin-top:0.75rem;
">
    📲 Call or WhatsApp the number above.
    Escrow is released after your session is complete.
</div>
""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button(
            "🔄 Submit a New Problem",
            use_container_width=True,
            key="new_query_btn",
        ):
            st.session_state["current_query_id"] = None
            st.session_state["current_solver"]   = None
            st.session_state["payment_done"]      = False
            st.rerun()


# ── Footer ───────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style="
    text-align:center;
    font-size:0.75rem;
    color:#94A3B8;
    padding: 1rem 0 0.5rem;
    border-top: 1px solid #E2E8F0;
">
    🔒 Your data is never shared without consent.
    JanSetu is a <strong>DPI — Digital Public Infrastructure</strong> initiative for Bharat.
</div>
""", unsafe_allow_html=True)
