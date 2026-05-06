import streamlit as st
import pandas as pd
from datetime import datetime, date
import time

st.set_page_config(
    page_title="SOCOTEC Arabia Portal",
    page_icon="assets/logo.png" if False else "🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── TEAM DATA ─────────────────────────────────────────────────────
ALL_TEAMS = [
    {"tl":"Amr Saif",             "region":"Al-Ahsa / Eastern",        "engineers":["Ahmed Khalid","Amr Saif"],                                                                                                                                    "rd6":["Amr Saif"],                                              "rd7":["Omar Abdulkareem"]},
    {"tl":"Ibrahim ABDEL MASSIH", "region":"Asir / Jazan / Najran",    "engineers":["Abdulelah AL QAHTANI","Abdulkareem GHURMULLAH","Hamad ALKHUDAYSH","Raed HUWAIZI","Sultan ALMALKI"],                                                           "rd6":["Abdulkareem GHURMULLAH","Hamad ALKHUDAYSH","Sultan ALMALKI"],"rd7":["Adel Eid"]},
    {"tl":"Mahmoud IBRAHIM",      "region":"Jeddah / Mecca / Taef",    "engineers":["Abdulaziz ALOTEIBI","Abdullah AL QARNI","Abdullah AL QURASHI","Hatim MANSOUR","Nawaf AFIFI"],                                                                 "rd6":["Hatim MANSOUR","Nawaf AFIFI"],                           "rd7":["Adel Eid"]},
    {"tl":"Noaman Rashed",        "region":"Al-Qassim / Northern",     "engineers":["Abdullah HABIB","Khalid KHALAF","Mansour SULTAN","Meshari ALSHARARI","Meshari DHAHER","Tariq ALSHARARI","Yazeed ADILAH"],                                     "rd6":["Khalid KHALAF","Yazeed ADILAH"],                         "rd7":["Omar Abdulkareem"]},
    {"tl":"Osama HASSAN",         "region":"Dammam / Khobar / Jubail", "engineers":["Abdullah ALANAZI","Abdulmohsen BAKARI","Ali KAMAL","Thamer AZMI","Wessam Thabet"],                                                                            "rd6":["Osama HASSAN"],                                          "rd7":["Omar Abdulkareem"]},
    {"tl":"Wahid Ali",            "region":"Madinah / Hail / Tabuk",   "engineers":["Ali Ghfaely","Mishari Al Harbi","Mohamed Al Qarni","Mohya el otibi","abdulkarim dhumran","nwaf sanad","salim khaled"],                                        "rd6":["Mohya el otibi","abdulkarim dhumran","salim khaled"],    "rd7":["Omar Abdulkareem"]},
    {"tl":"Mohamed Mossad",       "region":"Riyadh",                   "engineers":["Jubran Alshahrani","Waleed Khalid","Bader ORAINI","Ehsan Awad","Abdulaziz QSEM","Ayman ASHRAF","Khaled Alshehri","Khalid Daghriri","Saeed Alqahtani","Abdulamajeed Fahad","Abdulwahab Alsharari"],"rd6":["Ehsan Awad","Younis YOUSEF","Khaled Alshehri","Jubran Alshahrani"],"rd7":["Omar Abdulkareem"]},
]
TL_NAMES = [t["tl"] for t in ALL_TEAMS]

# ── STYLING ───────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0 !important; padding-bottom: 2rem; max-width: 1200px; }
section[data-testid="stSidebar"] { display: none; }

/* Header */
.portal-header {
    background: linear-gradient(135deg, #0072BB 0%, #005A96 100%);
    margin: -1rem -1rem 0; padding: 14px 28px;
    display: flex; align-items: center; justify-content: space-between;
}
.portal-logo { display: flex; align-items: center; gap: 12px; }
.portal-logo-box {
    width: 38px; height: 38px; background: rgba(255,255,255,0.2);
    border-radius: 10px; display: flex; align-items: center;
    justify-content: center; font-size: 20px;
}
.portal-logo-text { color: white; }
.portal-logo-title { font-size: 15px; font-weight: 700; letter-spacing: -0.01em; line-height: 1.2; }
.portal-logo-sub { font-size: 10px; opacity: 0.7; letter-spacing: 0.03em; }
.portal-header-right { display: flex; align-items: center; gap: 10px; }
.date-chip { background: rgba(255,255,255,0.15); color: white; font-size: 11px; padding: 5px 12px; border-radius: 20px; font-family: 'DM Mono', monospace; }
.user-chip { width: 32px; height: 32px; border-radius: 50%; background: rgba(255,255,255,0.2); color: white; font-size: 12px; font-weight: 600; display: flex; align-items: center; justify-content: center; }

/* Nav */
.portal-nav {
    background: #005A96; display: flex; gap: 0;
    margin: 0 -1rem; padding: 0 16px;
    overflow-x: auto; scrollbar-width: none;
}
.portal-nav::-webkit-scrollbar { display: none; }
.nav-item {
    padding: 10px 18px; font-size: 13px; font-weight: 500;
    color: rgba(255,255,255,0.6); cursor: pointer;
    border-bottom: 2px solid transparent; white-space: nowrap;
    transition: all 0.15s;
}
.nav-item:hover { color: rgba(255,255,255,0.9); }
.nav-item.active { color: white; border-bottom-color: white; }

/* Welcome banner */
.welcome-banner {
    background: linear-gradient(135deg, #0072BB, #005A96);
    border-radius: 14px; padding: 24px 28px; color: white;
    margin-bottom: 18px; position: relative; overflow: hidden;
}
.welcome-banner::before {
    content: ''; position: absolute; right: -30px; top: -30px;
    width: 200px; height: 200px; border-radius: 50%;
    background: rgba(255,255,255,0.05);
}
.welcome-greeting { font-size: 13px; opacity: 0.75; margin-bottom: 4px; }
.welcome-name { font-size: 22px; font-weight: 600; margin-bottom: 3px; }
.welcome-role { font-size: 12px; opacity: 0.7; margin-bottom: 18px; }
.welcome-stats { display: flex; gap: 28px; padding-top: 16px; border-top: 1px solid rgba(255,255,255,0.15); }
.ws-num { font-size: 24px; font-weight: 600; font-family: 'DM Mono', monospace; }
.ws-label { font-size: 10px; opacity: 0.7; margin-top: 2px; }

/* Stat cards */
.stat-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 12px; margin-bottom: 20px; }
.stat-card {
    background: white; border-radius: 12px; padding: 16px;
    border-top: 3px solid var(--accent, #0072BB);
    box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 4px 12px rgba(0,0,0,0.04);
}
.stat-label { font-size: 11px; color: #6B7280; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 6px; }
.stat-val { font-size: 26px; font-weight: 700; color: var(--accent, #0072BB); font-family: 'DM Mono', monospace; line-height: 1; }
.stat-sub { font-size: 11px; color: #9CA3AF; margin-top: 4px; }

/* Tool cards */
.tool-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px,1fr)); gap: 12px; margin-bottom: 24px; }
.tool-card {
    background: white; border-radius: 14px; padding: 20px 16px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 4px 12px rgba(0,0,0,0.04);
    cursor: pointer; border-bottom: 3px solid var(--tc, #0072BB);
    transition: transform 0.15s, box-shadow 0.15s;
}
.tool-card:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(0,0,0,0.1); }
.tool-icon { width: 44px; height: 44px; border-radius: 12px; background: var(--tb, #E6F3FB); display: flex; align-items: center; justify-content: center; font-size: 20px; margin-bottom: 10px; }
.tool-name { font-size: 13px; font-weight: 600; margin-bottom: 4px; }
.tool-desc { font-size: 11px; color: #9CA3AF; line-height: 1.4; margin-bottom: 8px; }
.tool-tag { display: inline-block; font-size: 10px; font-weight: 500; padding: 2px 8px; border-radius: 20px; background: var(--tb, #E6F3FB); color: var(--tc, #0072BB); }

/* Section title */
.sec-title { font-size: 11px; font-weight: 600; color: #9CA3AF; text-transform: uppercase; letter-spacing: 0.07em; margin-bottom: 12px; }

/* Attendance row */
.att-row {
    background: white; border-radius: 10px; padding: 12px 16px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05); margin-bottom: 8px;
    display: flex; align-items: center; gap: 12px;
}
.att-av {
    width: 36px; height: 36px; border-radius: 50%;
    background: #E6F3FB; color: #0072BB;
    font-size: 12px; font-weight: 700;
    display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}
.att-name { font-size: 13px; font-weight: 500; flex: 1; }
.att-detail { font-size: 11px; color: #9CA3AF; }
.pill-in  { background: #E6F7EE; color: #007A38; padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: 500; }
.pill-out { background: #FEE2E2; color: #991B1B; padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: 500; }
.time-tag { background: #F3F4F6; color: #374151; font-size: 11px; font-family: 'DM Mono', monospace; padding: 3px 8px; border-radius: 6px; }

/* Summary card */
.section-card { background: white; border-radius: 14px; padding: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 4px 12px rgba(0,0,0,0.04); margin-bottom: 14px; }
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ─────────────────────────────────────────────────
if "page" not in st.session_state: st.session_state.page = "Home"
if "active_tl" not in st.session_state: st.session_state.active_tl = "Mohamed Mossad"

# ── DATA ──────────────────────────────────────────────────────────
try:
    from sharepoint_client import read_attendance_today, read_claims_data, write_claim_to_sharepoint
    DATA_CONNECTED = True
except Exception:
    DATA_CONNECTED = False

def safe_load(fn, fallback=None):
    try: return fn()
    except Exception: return fallback if fallback is not None else pd.DataFrame()

# ── HEADER ────────────────────────────────────────────────────────
active_tl = st.session_state.active_tl
my_team   = next(t for t in ALL_TEAMS if t["tl"] == active_tl)
initials  = "".join(w[0] for w in active_tl.split()[:2]).upper()
today     = date.today()
import calendar
day_name = calendar.day_name[today.weekday()]
DAYS      = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
MONTHS    = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
date_str  = f"{day_name[:3]} {today.day} {MONTHS[today.month-1]}"

# Fix day of week
import calendar
day_name = calendar.day_name[today.weekday()]

st.markdown(f"""
<div class="portal-header">
  <div class="portal-logo">
    <div class="portal-logo-box">🏢</div>
    <div class="portal-logo-text">
      <div class="portal-logo-title">Socotec Arabia</div>
      <div class="portal-logo-sub">Management Portal</div>
    </div>
  </div>
  <div class="portal-header-right">
    <div class="date-chip">{day_name[:3]} {today.day} {MONTHS[today.month-1]}</div>
    <div class="user-chip">{initials}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── NAV ───────────────────────────────────────────────────────────
PAGES = ["Home","Attendance","Claims","RD6","Saturday OT","Links"]
nav_html = '<div class="portal-nav">'
for p in PAGES:
    active_cls = "active" if st.session_state.page == p else ""
    nav_html += f'<div class="nav-item {active_cls}" onclick="window.location.href=\'?page={p}\'">{p}</div>'
nav_html += '</div>'
st.markdown(nav_html, unsafe_allow_html=True)

# Handle URL-based navigation
params = st.query_params
if "page" in params and params["page"] in PAGES:
    st.session_state.page = params["page"]

# ── TL SELECTOR ───────────────────────────────────────────────────
col_tl, col_refresh = st.columns([3,1])
with col_tl:
    new_tl = st.selectbox("Team", TL_NAMES, index=TL_NAMES.index(active_tl), label_visibility="collapsed")
    if new_tl != active_tl:
        st.session_state.active_tl = new_tl
        st.rerun()
with col_refresh:
    if st.button("🔄 Refresh", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

active_tl = st.session_state.active_tl
my_team   = next(t for t in ALL_TEAMS if t["tl"] == active_tl)

# ── NAV BUTTONS (hidden but functional) ──────────────────────────
nav_cols = st.columns(len(PAGES))
for i, (col, page) in enumerate(zip(nav_cols, PAGES)):
    with col:
        if st.button(page, key=f"nav_{page}", use_container_width=True,
                     type="primary" if st.session_state.page == page else "secondary"):
            st.session_state.page = page
            st.rerun()

st.markdown("---")

# ── LOAD DATA ─────────────────────────────────────────────────────
att_data   = safe_load(read_attendance_today, {"checked_in":pd.DataFrame(),"exceptions":pd.DataFrame(),"team_members":pd.DataFrame(),"today":str(today)}) if DATA_CONNECTED else {"checked_in":pd.DataFrame(),"exceptions":pd.DataFrame(),"team_members":pd.DataFrame(),"today":str(today)}
claims_df  = safe_load(read_claims_data) if DATA_CONNECTED else pd.DataFrame()

checked_in_df = att_data.get("checked_in", pd.DataFrame())
exceptions_df = att_data.get("exceptions", pd.DataFrame())
my_engineers  = my_team["engineers"]

# Build attendance view
checked_names = set()
att_rows = []

if not checked_in_df.empty and "EngineerName" in checked_in_df.columns:
    for _, r in checked_in_df.iterrows():
        name = str(r.get("EngineerName","")).strip()
        if name in my_engineers:
            checked_names.add(name)
            att_rows.append({
                "Engineer": name,
                "Status": "in",
                "Check-in": str(r.get("CheckInTime",""))[:5] if r.get("CheckInTime") else "—",
                "Location": str(r.get("WorkLocation","")) or "—",
                "Visits": str(r.get("No_of_visits","0")) or "0",
            })

# Add exceptions (no response)
exc_names = set()
if not exceptions_df.empty and "EngineerName" in exceptions_df.columns:
    exc_names = set(exceptions_df["EngineerName"].astype(str).str.strip().tolist())

for eng in my_engineers:
    if eng not in checked_names:
        att_rows.append({"Engineer":eng,"Status":"out","Check-in":"—","Location":"—","Visits":"—"})

in_count  = sum(1 for r in att_rows if r["Status"] == "in")
out_count = sum(1 for r in att_rows if r["Status"] == "out")

m = today.strftime("%Y-%m")
claims_month = len(claims_df[claims_df.get("Month", pd.Series()) == m]) if not claims_df.empty and "Month" in claims_df.columns else 0

# ── HOME ──────────────────────────────────────────────────────────
if st.session_state.page == "Home":
    hour = today.hour if hasattr(today, 'hour') else datetime.now().hour
    greeting = "Good morning" if datetime.now().hour < 12 else "Good afternoon" if datetime.now().hour < 17 else "Good evening"

    st.markdown(f"""
    <div class="welcome-banner">
      <div class="welcome-greeting">{greeting},</div>
      <div class="welcome-name">{active_tl}</div>
      <div class="welcome-role">Team Leader · {my_team['region']} · SOCOTEC Arabia</div>
      <div class="welcome-stats">
        <div><div class="ws-num">{in_count}</div><div class="ws-label">Checked in today</div></div>
        <div><div class="ws-num">{out_count}</div><div class="ws-label">No response</div></div>
        <div><div class="ws-num">{claims_month}</div><div class="ws-label">Claims this month</div></div>
        <div><div class="ws-num">{len(my_engineers)}</div><div class="ws-label">Team size</div></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="stat-grid">
      <div class="stat-card" style="--accent:#0072BB;">
        <div class="stat-label">Team size</div>
        <div class="stat-val">{len(my_engineers)}</div>
        <div class="stat-sub">{my_team['region']}</div>
      </div>
      <div class="stat-card" style="--accent:#00A94F;">
        <div class="stat-label">Checked in today</div>
        <div class="stat-val">{in_count}</div>
        <div class="stat-sub">as of 10:30 AM</div>
      </div>
      <div class="stat-card" style="--accent:#F59E0B;">
        <div class="stat-label">No response</div>
        <div class="stat-val">{out_count}</div>
        <div class="stat-sub">Today</div>
      </div>
      <div class="stat-card" style="--accent:#EF4444;">
        <div class="stat-label">Claims (month)</div>
        <div class="stat-val">{claims_month}</div>
        <div class="stat-sub">{MONTHS[today.month-1]} {today.year}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-title">Quick access</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="tool-grid">
      <a href="https://rd6-socotec.streamlit.app/" target="_blank" style="text-decoration:none;">
        <div class="tool-card" style="--tc:#3B82F6;--tb:#EFF6FF;">
          <div class="tool-icon">📄</div>
          <div class="tool-name">RD6 Generator</div>
          <div class="tool-desc">Completion of works reports</div>
          <span class="tool-tag">Streamlit</span>
        </div>
      </a>
      <a href="https://socotec-zones.streamlit.app/" target="_blank" style="text-decoration:none;">
        <div class="tool-card" style="--tc:#8B5CF6;--tb:#F5F3FF;">
          <div class="tool-icon">🗺️</div>
          <div class="tool-name">Zone Manager</div>
          <div class="tool-desc">Engineer zone assignments</div>
          <span class="tool-tag">Streamlit</span>
        </div>
      </a>
      <div class="tool-card" style="--tc:#00A94F;--tb:#E6F7EE;" onclick="">
        <div class="tool-icon">✅</div>
        <div class="tool-name">Attendance</div>
        <div class="tool-desc">Daily check-in status</div>
        <span class="tool-tag">Live</span>
      </div>
      <div class="tool-card" style="--tc:#EF4444;--tb:#FEE2E2;" onclick="">
        <div class="tool-icon">📋</div>
        <div class="tool-name">Claims Tracker</div>
        <div class="tool-desc">Log & track engineer claims</div>
        <span class="tool-tag">Built-in</span>
      </div>
      <div class="tool-card" style="--tc:#F59E0B;--tb:#FFFBEB;" onclick="">
        <div class="tool-icon">📅</div>
        <div class="tool-name">Saturday OT</div>
        <div class="tool-desc">Overtime visit submissions</div>
        <span class="tool-tag">Form + Log</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── ATTENDANCE ────────────────────────────────────────────────────
elif st.session_state.page == "Attendance":
    st.markdown(f'<div class="welcome-banner"><div class="welcome-greeting">Daily attendance</div><div class="welcome-name">✅ {active_tl}\'s team</div><div class="welcome-role">{day_name}, {today.day} {MONTHS[today.month-1]} {today.year}</div></div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("Checked in", in_count)
    c2.metric("No response", out_count)
    c3.metric("Total team", len(my_engineers))

    filt = st.radio("Filter", ["All","Checked in","No response"], horizontal=True)
    rows_show = [r for r in att_rows if filt == "All" or (filt == "Checked in" and r["Status"] == "in") or (filt == "No response" and r["Status"] == "out")]

    for r in rows_show:
        ini = "".join(w[0] for w in r["Engineer"].split()[:2]).upper()
        pill = '<span class="pill-in">✅ Checked in</span>' if r["Status"] == "in" else '<span class="pill-out">❌ No response</span>'
        time_tag = f'<span class="time-tag">{r["Check-in"]}</span>' if r["Check-in"] != "—" else ""
        detail = f'{r["Location"]} · {r["Visits"]} visits' if r["Location"] != "—" else "No check-in recorded"
        st.markdown(f"""
        <div class="att-row">
          <div class="att-av">{ini}</div>
          <div style="flex:1"><div class="att-name">{r['Engineer']}</div><div class="att-detail">{detail}</div></div>
          {time_tag}{pill}
        </div>""", unsafe_allow_html=True)

    st.markdown('<br>', unsafe_allow_html=True)
    st.link_button("📊 Open full attendance log →", "https://socotecgroup.sharepoint.com/:x:/r/sites/SOCOTECLIBAN/_layouts/15/Doc.aspx?sourcedoc=%7B7A35EE01-7D25-4E50-A5E1-CB583F76E818%7D")

# ── CLAIMS ────────────────────────────────────────────────────────
elif st.session_state.page == "Claims":
    st.markdown('<div class="welcome-banner"><div class="welcome-greeting">Claims tracker</div><div class="welcome-name">📋 Log & track engineer claims</div><div class="welcome-role">All claims saved to shared GitHub — visible to all team leaders</div></div>', unsafe_allow_html=True)

    CLAIM_TYPES = {
        "visit":   ["Visit delay","Missed visit","Ignore client contact","Unprofessional attitude"],
        "rd6":     ["Late report submission","Incomplete report","Visit submission with photo missing","Wrong project data entered"],
        "attend":  ["Missed check-in"],
        "safety":  ["Safety violation on-site","Near-miss not reported"],
        "conduct": ["Falsified record","Conflict of interest","Data breach"],
    }
    ALL_CLAIM_TYPES = {v:k for k,vals in CLAIM_TYPES.items() for v in vals}

    tab_log, tab_summary, tab_history = st.tabs(["📝 Log a claim","📊 Team summary","📜 History"])

    with tab_log:
        with st.form("claim_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                eng = st.selectbox("Engineer", my_team["engineers"])
                claim_type = st.selectbox("Claim type", list(ALL_CLAIM_TYPES.keys()))
            with c2:
                claim_date = st.date_input("Date", value=today)
                cat = ALL_CLAIM_TYPES.get(claim_type,"visit")
                st.text_input("Category", value=cat.upper(), disabled=True)
            desc = st.text_area("Description (optional)", height=80)
            evidence = st.file_uploader("Evidence (image or PDF)", type=["jpg","jpeg","png","pdf"], accept_multiple_files=True)
            submitted = st.form_submit_button("Log claim ✓", type="primary", use_container_width=True)
            if submitted:
                claim = {"Engineer":eng,"Date":str(claim_date),"ClaimType":claim_type,"Category":cat,"Description":desc,"AutoGenerated":"No","Month":str(claim_date)[:7]}
                if DATA_CONNECTED:
                    with st.spinner("Saving..."):
                        ok = write_claim_to_sharepoint(claim)
                    if ok:
                        st.success(f"✅ Claim logged for {eng}")
                        st.cache_data.clear()
                else:
                    st.warning("Not connected — claim not saved")

    with tab_summary:
        if claims_df.empty:
            st.info("No claims data yet.")
        else:
            for eng in my_team["engineers"]:
                ec = claims_df[claims_df.get("Engineer",pd.Series())==eng] if "Engineer" in claims_df.columns else pd.DataFrame()
                v = len(ec[ec.get("Category","")=="visit"]) if not ec.empty else 0
                r2= len(ec[ec.get("Category","")=="rd6"]) if not ec.empty else 0
                a = len(ec[ec.get("Category","")=="attend"]) if not ec.empty else 0
                cols = st.columns([3,1,1,1])
                cols[0].write(f"**{eng}**")
                cols[1].metric("V",f"{v}/6")
                cols[2].metric("R",f"{r2}/6")
                cols[3].metric("A",a)

    with tab_history:
        if claims_df.empty:
            st.info("No claims logged yet.")
        else:
            ef = st.selectbox("Engineer",["All"]+my_team["engineers"],key="h_eng")
            cf = st.selectbox("Category",["All","visit","rd6","attend","safety","conduct"],key="h_cat")
            df_show = claims_df.copy()
            if ef!="All" and "Engineer" in df_show.columns: df_show=df_show[df_show["Engineer"]==ef]
            if cf!="All" and "Category" in df_show.columns: df_show=df_show[df_show["Category"]==cf]
            st.dataframe(df_show,use_container_width=True,hide_index=True)

# ── RD6 ──────────────────────────────────────────────────────────
elif st.session_state.page == "RD6":
    st.markdown('<div class="welcome-banner"><div class="welcome-greeting">RD6 Dashboard</div><div class="welcome-name">📊 Final visit requirements</div><div class="welcome-role">Live data in SharePoint Excel</div></div>', unsafe_allow_html=True)
    st.link_button("📊 Open RD6 Excel on SharePoint →","https://socotecgroup-my.sharepoint.com/:x:/r/personal/mohamed_mossad_socotec_com/_layouts/15/doc2.aspx?sourcedoc=%7B1E8B3450-766D-4717-80AF-A496EC21E39E%7D",use_container_width=False)
    st.info("The RD6 Excel is always live on SharePoint. Use the filters in Excel to view by engineer, status, or region.")

    st.markdown('<div class="sec-title">RD6 engineers by team</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    for i, team in enumerate(ALL_TEAMS):
        with cols[i % 3]:
            is_me = team["tl"] == active_tl
            color = "#00A94F" if is_me else "#0072BB"
            st.markdown(f"""
            <div class="section-card" style="border-left:4px solid {color}">
              <div style="font-size:12px;font-weight:600;color:{color};margin-bottom:4px;">{team['tl']}</div>
              <div style="font-size:10px;color:#9CA3AF;margin-bottom:6px;">{team['region']}</div>
              <div style="font-size:11px;color:#374151;">{', '.join(team['rd6'])}</div>
            </div>""", unsafe_allow_html=True)

# ── SATURDAY OT ───────────────────────────────────────────────────
elif st.session_state.page == "Saturday OT":
    st.markdown('<div class="welcome-banner"><div class="welcome-greeting">Saturday overtime</div><div class="welcome-name">📅 Saturday OT Visit Submissions</div><div class="welcome-role">Submit requests and view the log</div></div>', unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1: st.link_button("📝 Submit Saturday Visit Form","https://forms.cloud.microsoft/e/shfQ9UjNEV",use_container_width=True)
    with c2: st.link_button("📊 View Submissions Log","https://socotecgroup.sharepoint.com/:x:/r/sites/SOCOTECLIBAN/_layouts/15/Doc.aspx?sourcedoc=%7BBEC26706-1B1D-41B4-A9ED-75B47B9CB108%7D",use_container_width=True)

# ── LINKS ─────────────────────────────────────────────────────────
elif st.session_state.page == "Links":
    st.markdown('<div class="welcome-banner"><div class="welcome-greeting">Resources</div><div class="welcome-name">🔗 Links & Resources</div><div class="welcome-role">All SOCOTEC Arabia tools and documents</div></div>', unsafe_allow_html=True)
    links = [
        ("📊","Daily Attendance Log","Full attendance Excel","https://socotecgroup.sharepoint.com/:x:/r/sites/SOCOTECLIBAN/_layouts/15/Doc.aspx?sourcedoc=%7B7A35EE01-7D25-4E50-A5E1-CB583F76E818%7D"),
        ("📝","Saturday OT Form","نموذج زيارات يوم السبت","https://forms.cloud.microsoft/e/shfQ9UjNEV"),
        ("📋","Saturday OT Log","Submissions Excel","https://socotecgroup.sharepoint.com/:x:/r/sites/SOCOTECLIBAN/_layouts/15/Doc.aspx?sourcedoc=%7BBEC26706-1B1D-41B4-A9ED-75B47B9CB108%7D"),
        ("📊","RD6 Dashboard Excel","Final visit requirements","https://socotecgroup-my.sharepoint.com/:x:/r/personal/mohamed_mossad_socotec_com/_layouts/15/doc2.aspx?sourcedoc=%7B1E8B3450-766D-4717-80AF-A496EC21E39E%7D"),
        ("🔒","RD6 Insulation Certificates","Attachments folder","https://socotecgroup.sharepoint.com/sites/SOCOTECLIBAN/KSA%20Shared%20Documents/Forms/AllItems.aspx?id=%2Fsites%2FSOCOTECLIBAN%2FKSA%20Shared%20Documents%2FTeam%20Leaders%20RD6%20follow%2DUp%2FRD6%20Attachments"),
        ("📄","RD6 Generator","Streamlit app","https://rd6-socotec.streamlit.app/"),
        ("🗺️","Zone Manager","Streamlit app","https://socotec-zones.streamlit.app/"),
    ]
    cols = st.columns(2)
    for i,(icon,name,desc,url) in enumerate(links):
        with cols[i%2]:
            st.link_button(f"{icon} {name} — {desc}",url,use_container_width=True)
