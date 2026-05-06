"""
SOCOTEC Arabia Management Portal
Multi-page Streamlit app — reads live from SharePoint
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import time

# ── PAGE CONFIG ───────────────────────────────────────────────────
st.set_page_config(
    page_title="SOCOTEC Arabia Portal",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── TEAM DATA ─────────────────────────────────────────────────────
ALL_TEAMS = [
    {"tl": "Amr Saif",             "region": "Al-Ahsa / Eastern",        "engineers": ["Ahmed Khalid", "Amr Saif"], "rd6": ["Amr Saif"], "rd7": ["Omar Abdulkareem"]},
    {"tl": "Ibrahim ABDEL MASSIH", "region": "Asir / Jazan / Najran",    "engineers": ["Abdulelah AL QAHTANI","Abdulkareem GHURMULLAH","Hamad ALKHUDAYSH","Raed HUWAIZI","Sultan ALMALKI"], "rd6": ["Abdulkareem GHURMULLAH","Hamad ALKHUDAYSH","Sultan ALMALKI"], "rd7": ["Adel Eid"]},
    {"tl": "Mahmoud IBRAHIM",      "region": "Jeddah / Mecca / Taef",    "engineers": ["Abdulaziz ALOTEIBI","Abdullah AL QARNI","Abdullah AL QURASHI","Hatim MANSOUR","Nawaf AFIFI"], "rd6": ["Hatim MANSOUR","Nawaf AFIFI"], "rd7": ["Adel Eid"]},
    {"tl": "Noaman Rashed",        "region": "Al-Qassim / Northern",     "engineers": ["Abdullah HABIB","Khalid KHALAF","Mansour SULTAN","Meshari ALSHARARI","Meshari DHAHER","Tariq ALSHARARI","Yazeed ADILAH"], "rd6": ["Khalid KHALAF","Yazeed ADILAH"], "rd7": ["Omar Abdulkareem"]},
    {"tl": "Osama HASSAN",         "region": "Dammam / Khobar / Jubail", "engineers": ["Abdullah ALANAZI","Abdulmohsen BAKARI","Ali KAMAL","Thamer AZMI","Wessam Thabet"], "rd6": ["Osama HASSAN"], "rd7": ["Omar Abdulkareem"]},
    {"tl": "Wahid Ali",            "region": "Madinah / Hail / Tabuk",   "engineers": ["Ali Ghfaely","Mishari Al Harbi","Mohamed Al Qarni","Mohya el otibi","abdulkarim dhumran","nwaf sanad","salim khaled"], "rd6": ["Mohya el otibi","abdulkarim dhumran","salim khaled"], "rd7": ["Omar Abdulkareem"]},
    {"tl": "Mohamed Mossad",       "region": "Riyadh",                   "engineers": ["Jubran Alshahrani","Waleed Khalid","Bader ORAINI","Ehsan Awad","Abdulaziz QSEM","Ayman ASHRAF","Khaled Alshehri","Khalid Daghriri","Saeed Alqahtani","Abdulamajeed Fahad","Abdulwahab Alsharari"], "rd6": ["Ehsan Awad","Younis YOUSEF","Khaled Alshehri","Jubran Alshahrani"], "rd7": ["Omar Abdulkareem"]},
]

TL_NAMES = [t["tl"] for t in ALL_TEAMS]

# ── CUSTOM CSS ────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main theme */
    .main-header {
        background: linear-gradient(135deg, #0072BB, #005A96);
        padding: 1rem 1.5rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 1.5rem;
    }
    .main-header h1 { color: white; margin: 0; font-size: 1.6rem; }
    .main-header p  { color: rgba(255,255,255,0.8); margin: 0; font-size: 0.9rem; }

    /* Metric cards */
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        border-left: 4px solid #0072BB;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        margin-bottom: 0.5rem;
    }
    .metric-card.green  { border-left-color: #00A94F; }
    .metric-card.amber  { border-left-color: #F59E0B; }
    .metric-card.red    { border-left-color: #EF4444; }
    .metric-card.purple { border-left-color: #8B5CF6; }
    .metric-label { font-size: 0.75rem; color: #6B7280; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px; }
    .metric-value { font-size: 1.8rem; font-weight: 700; color: #0072BB; line-height: 1; }
    .metric-card.green  .metric-value { color: #00A94F; }
    .metric-card.amber  .metric-value { color: #F59E0B; }
    .metric-card.red    .metric-value { color: #EF4444; }
    .metric-card.purple .metric-value { color: #8B5CF6; }
    .metric-sub { font-size: 0.75rem; color: #9CA3AF; margin-top: 2px; }

    /* Status pills */
    .pill-in     { background: #E6F7EE; color: #007A38; padding: 3px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 500; }
    .pill-out    { background: #FEE2E2; color: #991B1B; padding: 3px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 500; }
    .pill-closed { background: #E6F7EE; color: #007A38; padding: 3px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 500; }
    .pill-pending{ background: #FEF3C7; color: #92400E; padding: 3px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 500; }
    .pill-open   { background: #F3F4F6; color: #374151; padding: 3px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 500; }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Sidebar */
    .css-1d391kg { background: #F7F8FA; }
    section[data-testid="stSidebar"] > div { background: #F7F8FA; }
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ─────────────────────────────────────────────────
if "active_tl" not in st.session_state:
    st.session_state.active_tl = "Mohamed Mossad"
if "page" not in st.session_state:
    st.session_state.page = "Home"

# ── SIDEBAR ───────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/SOCOTEC_logo.svg/200px-SOCOTEC_logo.svg.png", width=140)
    st.markdown("**Arabia Management Portal**")
    st.caption(f"Today: {date.today().strftime('%A, %d %b %Y')}")
    st.divider()

    # TL selector
    st.markdown("**Team view**")
    active_tl = st.selectbox(
        "Team Leader",
        TL_NAMES,
        index=TL_NAMES.index(st.session_state.active_tl),
        label_visibility="collapsed"
    )
    st.session_state.active_tl = active_tl
    my_team = next(t for t in ALL_TEAMS if t["tl"] == active_tl)
    st.caption(f"📍 {my_team['region']} · {len(my_team['engineers'])} engineers")

    st.divider()

    # Navigation
    pages = {
        "🏠 Home":        "Home",
        "✅ Attendance":  "Attendance",
        "📋 Claims":      "Claims",
        "📊 RD6":         "RD6",
        "📅 Saturday OT": "Saturday",
        "🔗 Links":       "Links",
    }
    for label, page_id in pages.items():
        if st.button(label, use_container_width=True,
                     type="primary" if st.session_state.page == page_id else "secondary"):
            st.session_state.page = page_id
            st.rerun()

    st.divider()
    if st.button("🔄 Refresh data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    st.caption("Data auto-refreshes every 5 min")

# ── IMPORT DATA MODULE ────────────────────────────────────────────
try:
    from sharepoint_client import (
        read_attendance_today, read_rd6_data,
        read_claims_data, write_claim_to_sharepoint,
        read_saturday_ot
    )
    DATA_CONNECTED = True
except Exception:
    DATA_CONNECTED = False

def safe_load(fn, fallback=None):
    try:
        return fn()
    except Exception:
        return fallback if fallback is not None else pd.DataFrame()

# ── PAGE: HOME ────────────────────────────────────────────────────
if st.session_state.page == "Home":
    st.markdown(f"""
    <div class="main-header">
        <h1>🏢 SOCOTEC Arabia Management Portal</h1>
        <p>Welcome, {active_tl} · {my_team['region']} Team</p>
    </div>
    """, unsafe_allow_html=True)

    if not DATA_CONNECTED:
        st.warning("⚠️ SharePoint connection not configured. Add SOCOTEC_EMAIL and SOCOTEC_PASSWORD to Streamlit secrets.")

    # Live stats
    with st.spinner("Loading today's data..."):
        att_data = safe_load(read_attendance_today, {"checked_in": pd.DataFrame(), "exceptions": pd.DataFrame(), "team_members": pd.DataFrame(), "today": str(date.today())}) if DATA_CONNECTED else {"checked_in": pd.DataFrame(), "exceptions": pd.DataFrame(), "team_members": pd.DataFrame(), "today": str(date.today())}
        claims_df = safe_load(read_claims_data) if DATA_CONNECTED else pd.DataFrame()

    my_engineers = my_team["engineers"]
    checked_in_df = att_data.get("checked_in", pd.DataFrame())
    exceptions_df = att_data.get("exceptions", pd.DataFrame())

    if not checked_in_df.empty and "EngineerEmail" in checked_in_df.columns:
        my_checked = checked_in_df[checked_in_df["EngineerName"].isin(my_engineers)]
        checked_count = len(my_checked)
    else:
        checked_count = 0

    if not exceptions_df.empty and "EngineerName" in exceptions_df.columns:
        my_exceptions = exceptions_df[exceptions_df["EngineerName"].isin(my_engineers)]
        exception_count = len(my_exceptions)
    else:
        exception_count = len(my_engineers) - checked_count

    m = date.today().strftime("%Y-%m")
    if not claims_df.empty and "Month" in claims_df.columns:
        claims_month = len(claims_df[claims_df["Month"] == m])
    else:
        claims_month = 0

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Team size</div><div class="metric-value">{len(my_engineers)}</div><div class="metric-sub">{my_team["region"]}</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card green"><div class="metric-label">Checked in today</div><div class="metric-value">{checked_count}</div><div class="metric-sub">as of 10:30 AM</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card amber"><div class="metric-label">No response</div><div class="metric-value">{exception_count}</div><div class="metric-sub">Today</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-card red"><div class="metric-label">Claims this month</div><div class="metric-value">{claims_month}</div><div class="metric-sub">{date.today().strftime("%B %Y")}</div></div>', unsafe_allow_html=True)

    st.divider()

    # Quick links
    st.subheader("Quick access")
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.link_button("📄 RD6 Generator", "https://rd6-socotec.streamlit.app/", use_container_width=True)
    with c2:
        st.link_button("🗺️ Zone Manager", "https://socotec-zones.streamlit.app/", use_container_width=True)
    with c3:
        if st.button("✅ Attendance", use_container_width=True):
            st.session_state.page = "Attendance"; st.rerun()
    with c4:
        if st.button("📋 Claims", use_container_width=True):
            st.session_state.page = "Claims"; st.rerun()
    with c5:
        if st.button("📊 RD6 Dashboard", use_container_width=True):
            st.session_state.page = "RD6"; st.rerun()

# ── PAGE: ATTENDANCE ──────────────────────────────────────────────
elif st.session_state.page == "Attendance":
    st.markdown(f'<div class="main-header"><h1>✅ Daily Attendance</h1><p>{active_tl}\'s team · {date.today().strftime("%A, %d %b %Y")}</p></div>', unsafe_allow_html=True)

    col_date, col_filt, _ = st.columns([2, 2, 4])
    with col_date:
        selected_date = st.date_input("Date", value=date.today(), label_visibility="collapsed")

    with st.spinner("Loading attendance..."):
        att_data = safe_load(read_attendance_today) if DATA_CONNECTED else {"checked_in": pd.DataFrame(), "exceptions": pd.DataFrame(), "team_members": pd.DataFrame(), "today": str(date.today())}

    checked_in_df = att_data.get("checked_in", pd.DataFrame())
    exceptions_df = att_data.get("exceptions", pd.DataFrame())
    my_engineers  = my_team["engineers"]

    # Build unified attendance view
    rows = []
    checked_names = set()
    if not checked_in_df.empty and "EngineerName" in checked_in_df.columns:
        today_str = str(selected_date)
        day_df = checked_in_df[pd.to_datetime(checked_in_df["Date"], errors="coerce").dt.strftime("%Y-%m-%d") == today_str] if "Date" in checked_in_df.columns else checked_in_df
        for _, r in day_df.iterrows():
            if r.get("EngineerName", "") in my_engineers:
                checked_names.add(r.get("EngineerName", ""))
                rows.append({
                    "Engineer":    r.get("EngineerName", ""),
                    "Status":      "✅ Checked in",
                    "Check-in":    str(r.get("CheckInTime", ""))[:5] if r.get("CheckInTime") else "—",
                    "Location":    str(r.get("WorkLocation", "")),
                    "Visits":      str(r.get("No_of_visits", "0")),
                })

    for eng in my_engineers:
        if eng not in checked_names:
            rows.append({
                "Engineer": eng,
                "Status":   "❌ No response",
                "Check-in": "—",
                "Location": "—",
                "Visits":   "—",
            })

    df_view = pd.DataFrame(rows)
    in_count  = len([r for r in rows if "Checked" in r["Status"]])
    out_count = len([r for r in rows if "No response" in r["Status"]])

    c1, c2, c3 = st.columns(3)
    c1.metric("Checked in",  in_count)
    c2.metric("No response", out_count)
    c3.metric("Total team",  len(my_engineers))

    with col_filt:
        filt = st.selectbox("Filter", ["All", "Checked in", "No response"], label_visibility="collapsed")

    if filt == "Checked in":
        df_view = df_view[df_view["Status"].str.contains("Checked")]
    elif filt == "No response":
        df_view = df_view[df_view["Status"].str.contains("No response")]

    if df_view.empty:
        st.info("No records found. Check-in data loads after 10:30 AM.")
    else:
        st.dataframe(df_view, use_container_width=True, hide_index=True,
                     column_config={"Status": st.column_config.TextColumn(width="medium")})

    st.link_button("📊 Open full attendance log", "https://socotecgroup.sharepoint.com/:x:/r/sites/SOCOTECLIBAN/_layouts/15/Doc.aspx?sourcedoc=%7B7A35EE01-7D25-4E50-A5E1-CB583F76E818%7D")

# ── PAGE: CLAIMS ──────────────────────────────────────────────────
elif st.session_state.page == "Claims":
    st.markdown('<div class="main-header"><h1>📋 Claims Tracker</h1><p>Log and track engineer claims — live from SharePoint</p></div>', unsafe_allow_html=True)

    tab_log, tab_summary, tab_history = st.tabs(["Log a claim", "Team summary", "History"])

    with st.spinner("Loading claims..."):
        claims_df = safe_load(read_claims_data) if DATA_CONNECTED else pd.DataFrame()

    CLAIM_TYPES = {
        "visit":   ["Visit delay", "Missed visit", "Ignore client contact", "Unprofessional attitude"],
        "rd6":     ["Late report submission", "Incomplete report", "Visit submission with photo missing", "Wrong project data entered"],
        "attend":  ["Missed check-in"],
        "safety":  ["Safety violation on-site", "Near-miss not reported"],
        "conduct": ["Falsified record", "Conflict of interest", "Data breach"],
    }
    ALL_CLAIM_TYPES = {v: k for k, vals in CLAIM_TYPES.items() for v in vals}

    with tab_log:
        with st.form("claim_form"):
            c1, c2 = st.columns(2)
            with c1:
                eng = st.selectbox("Engineer", my_team["engineers"])
                claim_type = st.selectbox("Claim type", list(ALL_CLAIM_TYPES.keys()))
            with c2:
                claim_date = st.date_input("Date", value=date.today())
                category = ALL_CLAIM_TYPES.get(claim_type, "visit")
                st.text_input("Category (auto)", value=category.upper(), disabled=True)
            description = st.text_area("Description (optional)", height=80)
            evidence = st.file_uploader("Evidence (image or PDF)", type=["jpg","jpeg","png","pdf"], accept_multiple_files=True)
            submitted = st.form_submit_button("Log claim", type="primary", use_container_width=True)

            if submitted:
                claim = {
                    "Engineer":      eng,
                    "Date":          str(claim_date),
                    "ClaimType":     claim_type,
                    "Category":      category,
                    "Description":   description,
                    "AutoGenerated": "No",
                    "Month":         str(claim_date)[:7],
                }
                if DATA_CONNECTED:
                    with st.spinner("Saving claim..."):
                        ok = write_claim_to_sharepoint(claim)
                    if ok:
                        st.success(f"✅ Claim logged for {eng}")
                        st.cache_data.clear()
                    else:
                        st.error("Could not save. Check connection.")
                else:
                    st.warning("Not connected to SharePoint — claim not saved.")

    with tab_summary:
        if claims_df.empty:
            st.info("No claims data available.")
        else:
            m = date.today().strftime("%Y-%m")
            month_claims = claims_df[claims_df.get("Month", pd.Series()) == m] if "Month" in claims_df.columns else claims_df
            for eng in my_team["engineers"]:
                eng_claims = month_claims[month_claims.get("Engineer", pd.Series()) == eng] if "Engineer" in month_claims.columns else pd.DataFrame()
                v = len(eng_claims[eng_claims.get("Category","") == "visit"]) if not eng_claims.empty else 0
                r = len(eng_claims[eng_claims.get("Category","") == "rd6"])   if not eng_claims.empty else 0
                a = len(eng_claims[eng_claims.get("Category","") == "attend"]) if not eng_claims.empty else 0
                total = v + r + a
                col_n, col_v, col_r, col_a, col_t = st.columns([3,1,1,1,1])
                col_n.write(f"**{eng}**")
                col_v.metric("Visits",     f"{v}/6")
                col_r.metric("RD6",        f"{r}/6")
                col_a.metric("Attendance", a)
                col_t.metric("Total",      total)

    with tab_history:
        if claims_df.empty:
            st.info("No claims data available.")
        else:
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                eng_filter = st.selectbox("Engineer", ["All"] + my_team["engineers"])
            with col_f2:
                cat_filter = st.selectbox("Category", ["All", "visit", "rd6", "attend", "safety", "conduct"])

            df_show = claims_df.copy()
            if eng_filter != "All" and "Engineer" in df_show.columns:
                df_show = df_show[df_show["Engineer"] == eng_filter]
            if cat_filter != "All" and "Category" in df_show.columns:
                df_show = df_show[df_show["Category"] == cat_filter]

            st.dataframe(df_show, use_container_width=True, hide_index=True)

# ── PAGE: RD6 ─────────────────────────────────────────────────────
elif st.session_state.page == "RD6":
    st.markdown('<div class="main-header"><h1>📊 RD6 Dashboard</h1><p>Final visit requirements — live from SharePoint</p></div>', unsafe_allow_html=True)

    st.link_button("📊 Open full Excel on SharePoint →",
        "https://socotecgroup-my.sharepoint.com/:x:/r/personal/mohamed_mossad_socotec_com/_layouts/15/doc2.aspx?sourcedoc=%7B1E8B3450-766D-4717-80AF-A496EC21E39E%7D",
        use_container_width=False)

    if DATA_CONNECTED:
        with st.spinner("Loading RD6 data..."):
            rd6_df = safe_load(read_rd6_data)
    else:
        rd6_df = pd.DataFrame()
        st.warning("SharePoint not connected — showing link to Excel only.")

    if not rd6_df.empty:
        # Stats
        total   = len(rd6_df)
        status_col = next((c for c in rd6_df.columns if "status" in c.lower()), None)
        if status_col:
            closed  = len(rd6_df[rd6_df[status_col].astype(str).str.contains("Closed", case=False, na=False)])
            pending = total - closed
        else:
            closed = pending = 0

        c1, c2, c3 = st.columns(3)
        c1.metric("Total",   total)
        c2.metric("Closed",  closed)
        c3.metric("Pending", pending)

        # Filters
        col_s, col_e, col_st = st.columns(3)
        with col_s:
            search = st.text_input("Search name or project", placeholder="Type to filter...")
        with col_e:
            eng_col = next((c for c in rd6_df.columns if "engineer" in c.lower() or "inspector" in c.lower()), None)
            if eng_col:
                engs = ["All"] + sorted(rd6_df[eng_col].dropna().unique().tolist())
                eng_f = st.selectbox("Engineer", engs)
            else:
                eng_f = "All"
        with col_st:
            if status_col:
                statuses = ["All"] + sorted(rd6_df[status_col].dropna().unique().tolist())
                st_f = st.selectbox("Status", statuses)
            else:
                st_f = "All"

        df_show = rd6_df.copy()
        if search:
            mask = df_show.astype(str).apply(lambda col: col.str.contains(search, case=False, na=False)).any(axis=1)
            df_show = df_show[mask]
        if eng_f != "All" and eng_col:
            df_show = df_show[df_show[eng_col] == eng_f]
        if st_f != "All" and status_col:
            df_show = df_show[df_show[status_col] == st_f]

        st.caption(f"Showing {len(df_show)} of {total} records")
        st.dataframe(df_show, use_container_width=True, hide_index=True, height=500)

# ── PAGE: SATURDAY OT ─────────────────────────────────────────────
elif st.session_state.page == "Saturday":
    st.markdown('<div class="main-header"><h1>📅 Saturday Overtime Visits</h1><p>Submit and track overtime visit requests</p></div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.link_button("📝 Submit Saturday Visit Form",
            "https://forms.cloud.microsoft/e/shfQ9UjNEV",
            use_container_width=True)
    with c2:
        st.link_button("📊 Open Submissions Excel",
            "https://socotecgroup.sharepoint.com/:x:/r/sites/SOCOTECLIBAN/_layouts/15/Doc.aspx?sourcedoc=%7BBEC26706-1B1D-41B4-A9ED-75B47B9CB108%7D",
            use_container_width=True)

    if DATA_CONNECTED:
        with st.spinner("Loading Saturday submissions..."):
            sat_df = safe_load(read_saturday_ot)
        if not sat_df.empty:
            st.subheader("Recent submissions")
            st.dataframe(sat_df, use_container_width=True, hide_index=True, height=400)
    else:
        st.info("Use the links above to access the form and submission log directly.")

# ── PAGE: LINKS ───────────────────────────────────────────────────
elif st.session_state.page == "Links":
    st.markdown('<div class="main-header"><h1>🔗 Resources & Links</h1><p>All SOCOTEC Arabia resources in one place</p></div>', unsafe_allow_html=True)

    links = [
        ("📊", "Daily Attendance Log",       "Full attendance Excel",        "https://socotecgroup.sharepoint.com/:x:/r/sites/SOCOTECLIBAN/_layouts/15/Doc.aspx?sourcedoc=%7B7A35EE01-7D25-4E50-A5E1-CB583F76E818%7D"),
        ("📝", "Saturday OT Form",           "نموذج زيارات يوم السبت",       "https://forms.cloud.microsoft/e/shfQ9UjNEV"),
        ("📋", "Saturday OT Log",            "Submissions Excel",             "https://socotecgroup.sharepoint.com/:x:/r/sites/SOCOTECLIBAN/_layouts/15/Doc.aspx?sourcedoc=%7BBEC26706-1B1D-41B4-A9ED-75B47B9CB108%7D"),
        ("📊", "RD6 Dashboard Excel",        "Final visit requirements",      "https://socotecgroup-my.sharepoint.com/:x:/r/personal/mohamed_mossad_socotec_com/_layouts/15/doc2.aspx?sourcedoc=%7B1E8B3450-766D-4717-80AF-A496EC21E39E%7D"),
        ("🔒", "RD6 Insulation Certificates","Attachments folder",            "https://socotecgroup.sharepoint.com/sites/SOCOTECLIBAN/KSA%20Shared%20Documents/Forms/AllItems.aspx?id=%2Fsites%2FSOCOTECLIBAN%2FKSA%20Shared%20Documents%2FTeam%20Leaders%20RD6%20follow%2DUp%2FRD6%20Attachments"),
        ("📄", "RD6 Generator",              "Streamlit app",                 "https://rd6-socotec.streamlit.app/"),
        ("🗺️", "Zone Manager",              "Streamlit app",                 "https://socotec-zones.streamlit.app/"),
    ]

    cols = st.columns(2)
    for i, (icon, name, desc, url) in enumerate(links):
        with cols[i % 2]:
            st.link_button(f"{icon} {name} — {desc}", url, use_container_width=True)
