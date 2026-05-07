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
    [data-testid="stHeader"] { display: none !important; }
    [data-testid="stToolbar"] { display: none !important; }
    [data-testid="stDecoration"] { display: none !important; }
    .stDeployButton { display: none !important; }
    /* Hide the Streamlit top nav completely */
    .stApp > header { display: none !important; }
    div[data-testid="stStatusWidget"] { display: none !important; }
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

/* TL selector integration */
    div[data-testid="stSelectbox"] > div { border-color: transparent !important; background: #1a1a2e !important; }
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
    border-radius: 10px; padding: 12px 16px;
    margin-bottom: 8px; display: flex; align-items: center; gap: 12px;
    border-left: 4px solid #ccc;
}
.att-row.att-in  { background: #F0FBF5; border-left-color: #00A94F; }
.att-row.att-out { background: #FFF5F5; border-left-color: #EF4444; }
.att-av-in  { width: 36px; height: 36px; border-radius: 50%; background: #E6F7EE; color: #007A38; font-size: 12px; font-weight: 700; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.att-av-out { width: 36px; height: 36px; border-radius: 50%; background: #FEE2E2; color: #991B1B; font-size: 12px; font-weight: 700; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.att-av { width: 36px; height: 36px; border-radius: 50%; background: #E6F3FB; color: #0072BB; font-size: 12px; font-weight: 700; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.att-name { font-size: 13px; font-weight: 500; flex: 1; color: #111; }
.att-detail { font-size: 11px; color: #6B7280; }
.pill-in  { background: #DCFCE7; color: #166534; padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: 600; }
.pill-out { background: #FEE2E2; color: #991B1B; padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: 600; }
.time-tag { background: #E0F2FE; color: #0369A1; font-size: 11px; font-family: 'DM Mono', monospace; padding: 3px 8px; border-radius: 6px; }

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
import calendar
today     = date.today()
day_name  = calendar.day_name[today.weekday()]
MONTHS    = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
date_str  = f"{day_name[:3]} {today.day} {MONTHS[today.month-1]}"


st.markdown(f"""
<div class="portal-header">
  <div class="portal-logo">
    <div style="width:40px;height:40px;background:white;border-radius:10px;display:flex;align-items:center;justify-content:center;margin-right:10px;flex-shrink:0;padding:3px;"><img src="data:image/jpeg;base64,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" style="width:100%;height:100%;object-fit:contain;"></div>
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

# ── NAV + TL SELECTOR ────────────────────────────────────────────
PAGES = ["Home","Attendance","Claims","RD6","Saturday OT","Links"]

# Inject CSS to make nav buttons look like nav tabs
st.markdown("""
<style>
/* Style nav row */
div[data-testid="stHorizontalBlock"]:has(button[kind="secondary"]) {
    background: #005A96;
    margin: 0 -1rem;
    padding: 0 8px;
    gap: 0 !important;
}
/* Nav buttons */
div[data-testid="stHorizontalBlock"]:has(button[kind="secondary"]) button {
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    border-radius: 0 !important;
    color: rgba(255,255,255,0.6) !important;
    padding: 8px 14px !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    white-space: nowrap !important;
}
div[data-testid="stHorizontalBlock"]:has(button[kind="secondary"]) button:hover {
    color: white !important;
    background: rgba(255,255,255,0.05) !important;
}
/* Active nav button - using primary type */
div[data-testid="stHorizontalBlock"]:has(button[kind="primary"]) button[kind="primary"] {
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid white !important;
    border-radius: 0 !important;
    color: white !important;
    padding: 8px 14px !important;
    font-size: 13px !important;
    font-weight: 600 !important;
}
/* TL selector row */
div[data-testid="stHorizontalBlock"]:has(div[data-testid="stSelectbox"]) {
    background: #1C1C2E;
    margin: 0 -1rem;
    padding: 4px 16px;
    align-items: center;
}
div[data-testid="stSelectbox"] label { display: none !important; }
div[data-testid="stSelectbox"] > div {
    background: rgba(255,255,255,0.08) !important;
    border-color: rgba(255,255,255,0.15) !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# Render nav as buttons
nav_cols = st.columns(len(PAGES) + 1)
for i, (col, page) in enumerate(zip(nav_cols[:-1], PAGES)):
    with col:
        btn_type = "primary" if st.session_state.page == page else "secondary"
        if st.button(page, key=f"nav_{page}", use_container_width=True, type=btn_type):
            st.session_state.page = page
            st.rerun()

# TL selector + refresh in last col & sidebar area
with nav_cols[-1]:
    if st.button("🔄", key="nav_refresh", help="Refresh data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# TL selector below nav
new_tl = st.selectbox("Team", TL_NAMES, index=TL_NAMES.index(active_tl), label_visibility="collapsed")
if new_tl != active_tl:
    st.session_state.active_tl = new_tl
    st.rerun()

active_tl = st.session_state.active_tl
my_team   = next(t for t in ALL_TEAMS if t["tl"] == active_tl)


# ── LOAD DATA ─────────────────────────────────────────────────────
att_data   = safe_load(read_attendance_today, {"checked_in":pd.DataFrame(),"exceptions":pd.DataFrame(),"team_members":pd.DataFrame(),"today":str(today)}) if DATA_CONNECTED else {"checked_in":pd.DataFrame(),"exceptions":pd.DataFrame(),"team_members":pd.DataFrame(),"today":str(today)}
claims_df  = safe_load(read_claims_data) if DATA_CONNECTED else pd.DataFrame()

checked_in_df = att_data.get("checked_in", pd.DataFrame())
exceptions_df = att_data.get("exceptions", pd.DataFrame())
my_engineers  = my_team["engineers"]

# Build attendance view
checked_names = set()
att_rows = []

# CORRECT LOGIC:
# 1. Get today's NO-RESPONSE from checkedIn array (Status = "No Response" + Date = today)
# 2. Everyone NOT in no-response list = checked in
# This works because the Non-Response Alert flow writes "No Response" rows with real names + today's date

today_str = str(today)  # "2026-05-07"

# Build no-response set from today's "No Response" rows
no_response_emails = set()
no_response_names  = set()

if not checked_in_df.empty and "EngineerEmail" in checked_in_df.columns:
    for _, r in checked_in_df.iterrows():
        row_date = str(r.get("Date","")).strip()
        status   = str(r.get("Status","")).strip()
        email    = str(r.get("EngineerEmail","")).strip().lower()
        if row_date != today_str: continue
        if "No Response" in status or status == "No Response":
            no_response_emails.add(email)
            eng_name = str(r.get("EngineerName","")).strip()
            if eng_name:
                no_response_names.add(eng_name.lower())

# Build attendance rows: checked-in = my team minus no-response
KNOWN_EMAILS = {
    "abdulaziz.qsem@socotec.com":       "Abdulaziz QSEM",
    "khalid.daghriri@socotec.com":      "Khalid Daghriri",
    "abdulwahab.alsharari@socotec.com": "Abdulwahab Alsharari",
    "waleed.khalid@socotec.com":        "Waleed Khalid",
    "saeed.alqahtani@socotec.com":      "Saeed Alqahtani",
    "abdulamajeed.fahad@socotec.com":   "Abdulamajeed Fahad",
    "mohamed.mossad@socotec.com":       "Mohamed Mossad",
    "yousef.younis@socotec.com":        "Younis YOUSEF",
    "jubran.alshahrani@socotec.com":    "Jubran Alshahrani",
    "bader.oraini@socotec.com":         "Bader ORAINI",
    "khaled.alshehri@socotec.com":      "Khaled Alshehri",
    "ehsan.awad@socotec.com":           "Ehsan Awad",
    "ayman.ashraf@socotec.com":         "Ayman ASHRAF",
}

# Get check-in details for engineers who DID check in
checkin_details = {}
if not checked_in_df.empty and "EngineerEmail" in checked_in_df.columns:
    for _, r in checked_in_df.iterrows():
        row_date = str(r.get("Date","")).strip()
        status   = str(r.get("Status","")).strip()
        email    = str(r.get("EngineerEmail","")).strip().lower()
        if row_date != today_str: continue
        if "نعم" in status:  # genuine check-in (Arabic yes)
            visits = str(r.get("No_x002e__of_visits ", r.get("No_of_visits","0"))).strip()
            checkin_details[email] = {
                "time":     str(r.get("CheckInTime",""))[:5] if r.get("CheckInTime") else "—",
                "location": str(r.get("WorkLocation","")) or "—",
                "visits":   visits or "0",
            }

for eng in my_engineers:
    # Find email for this engineer
    eng_email = next((e for e,n in KNOWN_EMAILS.items() if n == eng), None)
    if eng_email is None:
        eng_email = eng.lower().replace(" ",".") + "@socotec.com"
    
    is_no_response = (
        eng_email in no_response_emails or
        eng.lower() in no_response_names or
        any(eng.lower() in n for n in no_response_names)
    )
    
    if is_no_response:
        att_rows.append({
            "Engineer": eng, "Status": "out",
            "Check-in": "—", "Location": "—", "Visits": "—",
        })
    else:
        details = checkin_details.get(eng_email, {})
        checked_names.add(eng)
        att_rows.append({
            "Engineer": eng,
            "Status":   "in",
            "Check-in": details.get("time", "—"),
            "Location": details.get("location", "—"),
            "Visits":   details.get("visits", "0"),
        })

# Add exceptions (no response)
exc_names = set()
if not exceptions_df.empty and "EngineerName" in exceptions_df.columns:
    exc_names = set(exceptions_df["EngineerName"].astype(str).str.strip().tolist())

# no-response handled above

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
    
    # DEBUG - remove after testing
    with st.expander("🔍 Debug info (remove after Sunday test)"):
        st.write(f"today_str: **{today_str}**")
        st.write(f"checked_in_df shape: {checked_in_df.shape}")
        st.write(f"checked_in_df columns: {list(checked_in_df.columns) if not checked_in_df.empty else 'EMPTY'}")
        if not checked_in_df.empty:
            st.write(f"Total rows: {len(checked_in_df)}")
            if 'Date' in checked_in_df.columns:
                unique_dates = checked_in_df['Date'].unique().tolist()
                st.write(f"Unique dates in data: {unique_dates[-5:]}")
                today_rows = checked_in_df[checked_in_df['Date'].astype(str) == today_str]
                st.write(f"Rows for today ({today_str}): {len(today_rows)}")
                if len(today_rows) > 0:
                    st.write(today_rows[['EngineerName','EngineerEmail','Date','Status']].head(10))
            else:
                st.write("NO Date column found!")
                st.write(f"Sample row: {checked_in_df.iloc[0].to_dict() if len(checked_in_df) > 0 else 'none'}")
        st.write(f"no_response_emails found: {no_response_emails}")

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
        detail = f'{r["Location"]} · {r["Visits"]} visits' if r["Location"] not in ("—", "", None) else ("✓ Present" if r["Status"] == "in" else "No check-in recorded")
        row_class = "att-row att-in" if r["Status"] == "in" else "att-row att-out"
        av_class  = "att-av-in"  if r["Status"] == "in" else "att-av-out"
        st.markdown(f"""
        <div class="{row_class}">
          <div class="{av_class}">{ini}</div>
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
    c1, c2 = st.columns(2)
    with c1:
        st.link_button("📊 Open RD6 Excel on SharePoint →","https://socotecgroup-my.sharepoint.com/:x:/r/personal/mohamed_mossad_socotec_com/_layouts/15/doc2.aspx?sourcedoc=%7B1E8B3450-766D-4717-80AF-A496EC21E39E%7D",use_container_width=True)
    with c2:
        st.link_button("📄 Open RD6 Generator App →","https://rd6-socotec.streamlit.app/",use_container_width=True)
    st.info("The RD6 Excel is always live on SharePoint. Use the filters to view by engineer, status, or region. Use the Generator to create new RD6 reports.")

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
