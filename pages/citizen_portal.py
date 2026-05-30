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
]
,
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
    "Rural Access":"📡",
}

DOMAIN_DESC = {
    "Agriculture": "Agricultural Expert",
    "Education":   "Education Specialist",
    "Healthcare":  "Health Worker",
    "MSME":        "Business Advisor",
    "Rural Access":"Digital Access Specialist",
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

UPI_ID = "kr.ashish535.hd@okaxis"
UPI_NAME = "JanSetu"

def make_qr(fee: int):
    if not QR_AVAILABLE:
        return None
    upi = f"upi://pay?pa={UPI_ID}&pn={UPI_NAME}&am={fee}&cu=INR&tn=JanSetu+Consultation"
    qr = qrcode.QRCode(version=2, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=8, border=3)
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
# PAGE HEADER
# ════════════════════════════════════════════════════════════

st.markdown("## 🙋‍♂️ Citizen Portal")
st.caption("Describe your problem in any language — Hindi, English, or your local dialect. JanSetu will instantly match you with a verified local specialist.")
st.divider()

# ── How It Works ────────────────────────────────────────────
st.markdown("#### ✨ How It Works")
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.info("**① Describe**\nType your problem in any language")
with c2:
    st.info("**② AI Match**\nWe classify & find your expert")
with c3:
    st.info("**③ Pay ₹**\nScan the UPI QR code")
with c4:
    st.info("**④ Connect**\nGet direct contact instantly")

st.divider()


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

    st.divider()

    # ── AI Classification Result ─────────────────────────────
    st.success(f"**AI Classification Complete!**   {icon} Domain detected: **{domain}**   |   Confidence: High ✅")

    # ── Solver Profile Card (100% Native Streamlit) ──────────
    st.markdown(f"### 👤 Your Matched Expert  —  Query #{query_id or '—'}")

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

    st.caption("✅ Verified Specialist   |   🔒 Escrow Protected   |   ⚡ Responds within 2 hours")

    st.divider()

    # ════════════════════════════════════════════════════════
    # PAYMENT SECTION
    # ════════════════════════════════════════════════════════

    if not paid:
        st.markdown("### 💳 Secure UPI Micro-Payment")
        st.info(f"Scan the QR code below to Pay **₹{solver['fee']}** to JanSetu Escrow. Your payment is held safely until your consultation is complete.")

        qr_col, info_col = st.columns([1, 1], gap="large")

        with qr_col:
            st.markdown("**📱 Scan with any UPI App**")
            upi_deep_link = f"upi://pay?pa={UPI_ID}&pn={UPI_NAME}&am={solver['fee']}&cu=INR&tn=JanSetu+Consultation"
            qr_bytes = make_qr(solver["fee"])
            if qr_bytes:
                st.image(qr_bytes, width=240, caption=f"Pay ₹{solver['fee']} — JanSetu Escrow")
            else:
                st.code(upi_deep_link)
                st.caption("⚠️ Install `qrcode[pil]` in requirements.txt for QR image")

            st.caption(f"UPI ID: **{UPI_ID}**   |   Amount: **₹{solver['fee']}**")

            # Mobile deep link button — opens GPay/PhonePe/Paytm directly on phone
            st.markdown(
                f'<a href="{upi_deep_link}" '
                f'style="display:inline-block;margin-top:8px;padding:10px 18px;'
                f'background:#6C3CE1;color:white;border-radius:8px;'
                f'text-decoration:none;font-size:14px;font-weight:bold;">'
                f'📲 Open UPI App (Mobile)</a>',
                unsafe_allow_html=True,
            )
            st.caption("☝️ On mobile — tap above to open GPay / PhonePe / Paytm directly")

        with info_col:
            st.markdown("**📲 Steps to Pay:**")
            st.markdown("""
1. Open **PhonePe / GPay / Paytm / BHIM**
2. Tap **Scan QR Code**
3. Point your camera at the QR
4. Confirm the payment of ₹{}
5. Come back here and click the button below ✅
            """.format(solver["fee"]))

            st.markdown("---")

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

        st.success("## 🎉 Payment Confirmed!")
        st.markdown(f"Your consultation fee of **₹{solver['fee']}** is safely held in JanSetu escrow.")

        st.divider()

        st.markdown("### 📞 Your Expert's Direct Contact")

        contact_col, detail_col = st.columns(2)

        with contact_col:
            st.metric(
                label="📱 Phone Number",
                value=solver["contact"],
            )
            st.success("Tap & call this number directly!")

        with detail_col:
            st.metric(
                label="👤 Expert Name",
                value=solver["name"],
            )
            st.metric(
                label=f"{icon} Domain",
                value=f"{domain} Specialist",
            )

        st.info("📲 Call or WhatsApp the number above.  Escrow is released after your session is complete.")

        st.divider()

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
st.divider()
st.caption("🔒 Your data is never shared without consent. JanSetu is a DPI - Digital Public Infrastructure initiative for Bharat.")
