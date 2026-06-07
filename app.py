import streamlit as st
import pandas as pd
from datetime import datetime, date
import json
import requests
import base64
import calendar

st.set_page_config(
    page_title="SOCOTEC Arabia Portal",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── ADMIN ─────────────────────────────────────────────────────────
ADMIN_TL = "Mohamed Mossad"

# ── TEAM DATA (updated from Daily_Attendance_Log June 2026) ───────
ALL_TEAMS = [
    {"tl":"Mohamed Mossad",      "region":"Riyadh",
     "engineers":["Jubran Alshahrani","Khaled Alshehri","Abdulamajeed Fahad",
                  "Abdulaziz QSEM","Abdulwahab Alsharari","Ehsan Awad",
                  "Khalid Daghriri","Saeed Alqahtani","Waleed Khalid",
                  "Younis YOUSEF","Bader ORAINI","Ayman ASHRAF","Omar Abdulkareem"],
     "rd6":["Ehsan Awad","Younis YOUSEF","Khaled Alshehri","Jubran Alshahrani"]},
    {"tl":"Ibrahim ABDELMASSIH", "region":"Western / Southern",
     "engineers":["Raed Huwaizi","Abdulkarim Ghurmullah","Mohammad Alsaleh",
                  "Abdulrhman Jaafari","Hamad Khudaysh","Sultan Almalki",
                  "Adel EID","Abdulelah DAFER","Tahar BAHAR","Mohamed RAJA",
                  "Wahid Ali","Mahmoud Ibrahim"],
     "rd6":["Abdulkarim Ghurmullah","Hamad Khudaysh","Sultan Almalki"]},
    {"tl":"Mahmoud IBRAHIM",     "region":"Jeddah / Mecca / Taef",
     "engineers":["Abdullah Qarni","Abdullah Qurashi","Hatim Mansour",
                  "Abdulaziz Otaibi","Nawaf Afifi"],
     "rd6":["Hatim Mansour","Nawaf Afifi"]},
    {"tl":"Noaman Rashed",       "region":"Al-Qassim / Northern",
     "engineers":["Meshari Alsharari","Khalid Khalaf","Yazeed Adilah",
                  "Tariq Alsharari","Mansour Sultan","Meshari DHAHER","Abdullah ALHABIB"],
     "rd6":["Khalid Khalaf","Yazeed Adilah"]},
    {"tl":"Osama HASSAN",        "region":"Dammam / Khobar / Jubail",
     "engineers":["Abdullah Mahdi","Abdulmohsen Bakari","Wesam Thabet",
                  "Thamer AZMI","Ali KAMAL"],
     "rd6":["Osama Hassan"]},
    {"tl":"Wahid Ali",           "region":"Madinah / Hail / Tabuk",
     "engineers":["Abdulkarim Dhumran","Nawaf Sanad","Salim Khalid",
                  "Mohya Otaibi","Ali GFAELY"],
     "rd6":["Mohya Otaibi","Abdulkarim Dhumran","Salim Khalid"]},
    {"tl":"Amr Saif",            "region":"Al-Ahsa / Eastern",
     "engineers":["Ahmed Khalid"],
     "rd6":["Amr Saif"]},
    {"tl":"Mohamed Ismail",      "region":"Eastern Region",
     "engineers":["Osama Hassan","Amr Saif"],
     "rd6":["Osama Hassan"]},
    {"tl":"Nizar Lazreq",        "region":"All Regions (Manager)",
     "engineers":["Mohamed Mossad","Ibrahim ABDELMASSIH","Noaman Rashed"],
     "rd6":[]},
]
TL_NAMES = [t["tl"] for t in ALL_TEAMS]

KNOWN_EMAILS = {
    "abdulaziz.qsem@socotec.com":         "Abdulaziz QSEM",
    "khalid.daghriri@socotec.com":        "Khalid Daghriri",
    "abdulwahab.alsharari@socotec.com":   "Abdulwahab Alsharari",
    "waleed.khalid@socotec.com":          "Waleed Khalid",
    "saeed.alqahtani@socotec.com":        "Saeed Alqahtani",
    "abdulamajeed.fahad@socotec.com":     "Abdulamajeed Fahad",
    "mohamed.mossad@socotec.com":         "Mohamed Mossad",
    "yousef.younis@socotec.com":          "Younis YOUSEF",
    "jubran.alshahrani@socotec.com":      "Jubran Alshahrani",
    "bader.oraini@socotec.com":           "Bader ORAINI",
    "khaled.alshehri@socotec.com":        "Khaled Alshehri",
    "ehsan.awad@socotec.com":             "Ehsan Awad",
    "ayman.ashraf@socotec.com":           "Ayman ASHRAF",
    "omar.abdulkareem@socotec.com":       "Omar Abdulkareem",
    "mohamed.soliman@socotec.com":        "Mohamed Soliman",
    "Ibrahim.ABDELMASSIH@socotec.com":    "Ibrahim ABDELMASSIH",
    "raed.huwaizi@socotec.com":           "Raed Huwaizi",
    "abdulkarim.ghurmullah@socotec.com":  "Abdulkarim Ghurmullah",
    "mohammad.alsaleh@socotec.com":       "Mohammad Alsaleh",
    "abdulrhman.jaafari@socotec.com":     "Abdulrhman Jaafari",
    "hamad.khudaysh@socotec.com":         "Hamad Khudaysh",
    "sultan.farhan@socotec.com":          "Sultan Almalki",
    "adel.eid@socotec.com":               "Adel EID",
    "abdelelah.dafer@socotec.com":        "Abdulelah DAFER",
    "tahar.bahr@socotec.com":             "Tahar BAHAR",
    "mohammed.raja@socotec.com":          "Mohamed RAJA",
    "mahmoud.ibrahim@socotec.com":        "Mahmoud Ibrahim",
    "wahid.ali@socotec.com":              "Wahid Ali",
    "abdullah.qarni@socotec.com":         "Abdullah Qarni",
    "abdullah.qurashi@socotec.com":       "Abdullah Qurashi",
    "hatim.mansour@socotec.com":          "Hatim Mansour",
    "abdulaziz.otaibi@socotec.com":       "Abdulaziz Otaibi",
    "nawaf.afifi@socotec.com":            "Nawaf Afifi",
    "noaman.rashed@socotec.com":          "Noaman Rashed",
    "meshari.alsharari@socotec.com":      "Meshari Alsharari",
    "khalid.khalaf@socotec.com":          "Khalid Khalaf",
    "yazeed.adilah@socotec.com":          "Yazeed Adilah",
    "tariq.alsharari@socotec.com":        "Tariq Alsharari",
    "mansour.sultan@socotec.com":         "Mansour Sultan",
    "meshari.dhaher@socotec.com":         "Meshari DHAHER",
    "abdullah.habib@socotec.com":         "Abdullah ALHABIB",
    "osama.hassan@socotec.com":           "Osama Hassan",
    "abdullah.mahdi@socotec.com":         "Abdullah Mahdi",
    "abdulmohsen.bakari@socotec.com":     "Abdulmohsen Bakari",
    "wesam.thabet@socotec.com":           "Wesam Thabet",
    "thamer.azmi@socotec.com":            "Thamer AZMI",
    "ali.kamal@socotec.com":              "Ali KAMAL",
    "abdulkarim.dhumran@socotec.com":     "Abdulkarim Dhumran",
    "nawaf.sanad@socotec.com":            "Nawaf Sanad",
    "salim.khalid@socotec.com":           "Salim Khalid",
    "mohya.otaibi@socotec.com":           "Mohya Otaibi",
    "ali.ghfaely@socotec.com":            "Ali GFAELY",
    "amr.saif@socotec.com":               "Amr Saif",
    "ahmed.khalid@socotec.com":           "Ahmed Khalid",
    "Nizar.LAZREG@socotec.com":           "Nizar Lazreq",
}

# ── PIN AUTHENTICATION ────────────────────────────────────────────
def get_pins() -> dict:
    """
    Load TL PINs from Streamlit secrets.
    Add to secrets.toml:
      TL_PINS = '{"Mohamed Mossad":"0000","Ibrahim ABDELMASSIH":"1234",...}'
    Mohamed Mossad's PIN also acts as admin master override.
    TLs with no PIN configured get auto-access (no gate shown).
    """
    try:
        raw = st.secrets.get("TL_PINS", "{}")
        return json.loads(raw)
    except Exception:
        return {}

def check_pin(tl_name: str, entered: str) -> bool:
    pins = get_pins()
    correct = pins.get(tl_name, "")
    if not correct:
        return True  # no PIN configured = open
    # Admin PIN also unlocks any account
    admin_pin = pins.get(ADMIN_TL, "")
    return entered.strip() == correct.strip() or (admin_pin and entered.strip() == admin_pin)

def is_authenticated(tl_name: str) -> bool:
    return st.session_state.get(f"auth_{tl_name}", False)

def show_pin_gate(tl_name: str):
    pins = get_pins()
    if tl_name not in pins:
        st.session_state[f"auth_{tl_name}"] = True
        st.rerun()
        return

    st.markdown("""
    <div style="height:40px;"></div>
    <div style="display:flex;justify-content:center;">
      <div style="background:#1C1C2E;border-radius:20px;padding:40px 50px;
                  box-shadow:0 8px 32px rgba(0,0,0,0.4);max-width:360px;width:100%;text-align:center;">
        <div style="font-size:48px;margin-bottom:16px;">🔒</div>
        <div style="font-size:20px;font-weight:700;color:white;margin-bottom:6px;">""" +
        tl_name +
        """</div>
        <div style="font-size:13px;color:#90CAF9;margin-bottom:8px;">
          Enter your 4-digit PIN to access your portal
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    col = st.columns([1, 2, 1])[1]
    with col:
        st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
        pin_input = st.text_input(
            "PIN", type="password", max_chars=4,
            placeholder="● ● ● ●",
            label_visibility="collapsed",
            key=f"pin_input_{tl_name}"
        )
        if st.button("Unlock →", type="primary", use_container_width=True,
                     key=f"pin_btn_{tl_name}"):
            if check_pin(tl_name, pin_input):
                st.session_state[f"auth_{tl_name}"] = True
                st.rerun()
            else:
                st.error("❌ Incorrect PIN. Please try again.")


# ── STYLING ───────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stHeader"]    { display: none !important; }
[data-testid="stToolbar"]   { display: none !important; }
[data-testid="stDecoration"]{ display: none !important; }
.stDeployButton             { display: none !important; }
.stApp > header             { display: none !important; }
div[data-testid="stStatusWidget"] { display: none !important; }
.block-container { padding-top: 0 !important; padding-bottom: 2rem; max-width: 1200px; }
section[data-testid="stSidebar"] { display: none; }
.portal-header {
    background: linear-gradient(135deg, #0072BB 0%, #005A96 100%);
    margin: -1rem -1rem 0; padding: 14px 28px;
    display: flex; align-items: center; justify-content: space-between;
}
.portal-logo { display: flex; align-items: center; gap: 12px; }
.portal-logo-text { color: white; }
.portal-logo-title { font-size: 15px; font-weight: 700; letter-spacing: -0.01em; line-height: 1.2; }
.portal-logo-sub { font-size: 10px; opacity: 0.7; letter-spacing: 0.03em; }
.portal-header-right { display: flex; align-items: center; gap: 10px; }
.date-chip { background: rgba(255,255,255,0.15); color: white; font-size: 11px; padding: 5px 12px; border-radius: 20px; font-family: 'DM Mono', monospace; }
.user-chip { width: 32px; height: 32px; border-radius: 50%; background: rgba(255,255,255,0.2); color: white; font-size: 12px; font-weight: 600; display: flex; align-items: center; justify-content: center; }
.welcome-banner { background: linear-gradient(135deg, #0072BB, #005A96); border-radius: 14px; padding: 24px 28px; color: white; margin-bottom: 18px; position: relative; overflow: hidden; }
.welcome-banner::before { content: ''; position: absolute; right: -30px; top: -30px; width: 200px; height: 200px; border-radius: 50%; background: rgba(255,255,255,0.05); }
.welcome-greeting { font-size: 13px; opacity: 0.75; margin-bottom: 4px; }
.welcome-name { font-size: 22px; font-weight: 600; margin-bottom: 3px; }
.welcome-role { font-size: 12px; opacity: 0.7; margin-bottom: 18px; }
.welcome-stats { display: flex; gap: 28px; padding-top: 16px; border-top: 1px solid rgba(255,255,255,0.15); }
.ws-num { font-size: 24px; font-weight: 600; font-family: 'DM Mono', monospace; }
.ws-label { font-size: 10px; opacity: 0.7; margin-top: 2px; }
.stat-grid { display: grid; grid-template-columns: repeat(4,1fr); gap: 12px; margin-bottom: 20px; }
.stat-card { background: white; border-radius: 12px; padding: 16px; border-top: 3px solid var(--accent, #0072BB); box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 4px 12px rgba(0,0,0,0.04); }
.stat-label { font-size: 11px; color: #6B7280; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 6px; }
.stat-val { font-size: 26px; font-weight: 700; color: var(--accent, #0072BB); font-family: 'DM Mono', monospace; line-height: 1; }
.stat-sub { font-size: 11px; color: #9CA3AF; margin-top: 4px; }
.tool-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px,1fr)); gap: 12px; margin-bottom: 24px; }
.tool-card { background: white; border-radius: 14px; padding: 20px 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 4px 12px rgba(0,0,0,0.04); cursor: pointer; border-bottom: 3px solid var(--tc, #0072BB); transition: transform 0.15s, box-shadow 0.15s; }
.tool-card:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(0,0,0,0.1); }
.tool-icon { width: 44px; height: 44px; border-radius: 12px; background: var(--tb, #E6F3FB); display: flex; align-items: center; justify-content: center; font-size: 20px; margin-bottom: 10px; }
.tool-name { font-size: 13px; font-weight: 600; margin-bottom: 4px; }
.tool-desc { font-size: 11px; color: #9CA3AF; line-height: 1.4; margin-bottom: 8px; }
.tool-tag { display: inline-block; font-size: 10px; font-weight: 500; padding: 2px 8px; border-radius: 20px; background: var(--tb, #E6F3FB); color: var(--tc, #0072BB); }
.sec-title { font-size: 11px; font-weight: 600; color: #9CA3AF; text-transform: uppercase; letter-spacing: 0.07em; margin-bottom: 12px; }
.att-row { border-radius: 10px; padding: 12px 16px; margin-bottom: 8px; display: flex; align-items: center; gap: 12px; border-left: 4px solid #ccc; }
.att-row.att-in  { background: #F0FBF5; border-left-color: #00A94F; }
.att-row.att-out { background: #FFF5F5; border-left-color: #EF4444; }
.att-av-in  { width: 36px; height: 36px; border-radius: 50%; background: #E6F7EE; color: #007A38; font-size: 12px; font-weight: 700; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.att-av-out { width: 36px; height: 36px; border-radius: 50%; background: #FEE2E2; color: #991B1B; font-size: 12px; font-weight: 700; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.att-name   { font-size: 13px; font-weight: 500; flex: 1; color: #111; }
.att-detail { font-size: 11px; color: #6B7280; }
.pill-in  { background: #DCFCE7; color: #166534; padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: 600; }
.pill-out { background: #FEE2E2; color: #991B1B; padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: 600; }
.time-tag { background: #E0F2FE; color: #0369A1; font-size: 11px; font-family: 'DM Mono', monospace; padding: 3px 8px; border-radius: 6px; }
.section-card { background: white; border-radius: 14px; padding: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 4px 12px rgba(0,0,0,0.04); margin-bottom: 14px; }
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ─────────────────────────────────────────────────
if "page"      not in st.session_state: st.session_state.page      = "Home"
if "active_tl" not in st.session_state: st.session_state.active_tl = "Mohamed Mossad"

# ── DATA CONNECTIONS ──────────────────────────────────────────────
try:
    from sharepoint_client import read_attendance_today, read_claims_data
    DATA_CONNECTED = True
except Exception:
    DATA_CONNECTED = False

def safe_load(fn, fallback=None):
    try: return fn()
    except Exception: return fallback if fallback is not None else pd.DataFrame()

# ── CLAIMS: GitHub JSON ───────────────────────────────────────────
GITHUB_REPO = "MohamedAlyMosaad/socotec-arabia-portal"
CLAIMS_PATH = "data/claims.json"
GITHUB_RAW  = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/{CLAIMS_PATH}"

def _github_token():
    try: return st.secrets["GITHUB_TOKEN"]
    except Exception: return None

@st.cache_data(ttl=60)
def load_claims() -> list:
    try:
        r = requests.get(GITHUB_RAW, timeout=10)
        if r.status_code == 200:
            data = r.json()
            raw = data if isinstance(data, list) else data.get("claims", []) if isinstance(data, dict) else []
            return [_normalize_claim(c) for c in raw if isinstance(c, dict)]
        return []
    except Exception:
        return []

def _normalize_claim(c: dict) -> dict:
    return {
        "id":              c.get("id",              c.get("Id",          "")),
        "team_leader":     c.get("team_leader",      c.get("TeamLeader",  ADMIN_TL)),
        "engineer":        c.get("engineer",         c.get("Engineer",    "")),
        "type":            c.get("type",             c.get("ClaimType",   c.get("claim_type", ""))),
        "category":        c.get("category",         c.get("Category",    "")),
        "date":            c.get("date",             c.get("Date",        "")),
        "description":     c.get("description",      c.get("Description", "")),
        "attachment":      c.get("attachment",       ""),
        "attachment_name": c.get("attachment_name",  ""),
        "logged_at":       c.get("logged_at",        c.get("LoggedAt",    "")),
        "auto_generated":  str(c.get("AutoGenerated", c.get("auto_generated", "No"))),
        "month":           c.get("month",            c.get("Month",       "")),
    }

def save_claim(new_claim: dict):
    token = _github_token()
    if not token:
        st.error("❌ GITHUB_TOKEN not set in Streamlit secrets.")
        return
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
    api_url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{CLAIMS_PATH}"
    get_resp = requests.get(api_url, headers=headers, timeout=10)
    if get_resp.status_code == 200:
        file_info = get_resp.json()
        sha = file_info["sha"]
        existing_raw = base64.b64decode(file_info["content"]).decode("utf-8")
        try:
            existing = json.loads(existing_raw)
            if isinstance(existing, dict) and "claims" in existing:
                existing = existing["claims"]
            if not isinstance(existing, list): existing = []
        except Exception:
            existing = []
    elif get_resp.status_code == 404:
        sha, existing = None, []
    else:
        st.error(f"❌ GitHub GET failed: {get_resp.status_code}")
        return
    existing_normalized = [_normalize_claim(c) for c in existing if isinstance(c, dict)]
    existing_normalized.append(new_claim)
    new_content = base64.b64encode(
        json.dumps(existing_normalized, ensure_ascii=False, indent=2).encode("utf-8")
    ).decode("utf-8")
    put_body = {
        "message": f"Add claim: {new_claim.get('engineer','?')} — {new_claim.get('type','?')}",
        "content": new_content,
    }
    if sha: put_body["sha"] = sha
    put_resp = requests.put(api_url, headers=headers, json=put_body, timeout=15)
    if put_resp.status_code in (200, 201):
        st.cache_data.clear()
    else:
        st.error(f"❌ GitHub PUT failed: {put_resp.status_code} — {put_resp.text[:300]}")

def filter_claims_for_tl(claims: list, viewer_tl: str) -> list:
    if viewer_tl == ADMIN_TL:
        return claims
    return [c for c in claims if c.get("team_leader", "") == viewer_tl]

# ── HEADER ────────────────────────────────────────────────────────
active_tl = st.session_state.active_tl
my_team   = next((t for t in ALL_TEAMS if t["tl"] == active_tl), ALL_TEAMS[0])
initials  = "".join(w[0] for w in active_tl.split()[:2]).upper()
today     = date.today()
day_name  = calendar.day_name[today.weekday()]
MONTHS    = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

# Read logo from file at runtime to avoid hardcoding large string
import os
_logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo_b64.txt")
_LOGO_B64 = ""
try:
    with open(_logo_path) as _f:
        _LOGO_B64 = _f.read().strip()
except Exception:
    pass

st.markdown(f"""
<div class="portal-header">
  <div class="portal-logo">
    <div style="width:40px;height:40px;background:white;border-radius:10px;display:flex;
                align-items:center;justify-content:center;margin-right:10px;flex-shrink:0;padding:3px;">
      {"<img src='data:image/png;base64," + _LOGO_B64 + "' style='width:100%;height:100%;object-fit:contain;'>" if _LOGO_B64 else "🏢"}
    </div>
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
PAGES = ["Home", "Attendance", "Claims", "RD6", "Saturday OT", "Links"]
st.markdown("""<style>
div[data-testid="stHorizontalBlock"]:has(button[kind="secondary"]) {
    background: #005A96; margin: 0 -1rem; padding: 0 8px; gap: 0 !important;
}
div[data-testid="stHorizontalBlock"]:has(button[kind="secondary"]) button {
    background: transparent !important; border: none !important;
    border-bottom: 2px solid transparent !important; border-radius: 0 !important;
    color: rgba(255,255,255,0.6) !important; padding: 8px 14px !important;
    font-size: 13px !important; font-weight: 500 !important;
}
div[data-testid="stHorizontalBlock"]:has(button[kind="primary"]) button[kind="primary"] {
    background: transparent !important; border: none !important;
    border-bottom: 2px solid white !important; border-radius: 0 !important;
    color: white !important; padding: 8px 14px !important;
    font-size: 13px !important; font-weight: 600 !important;
}
div[data-testid="stSelectbox"] label { display: none !important; }
div[data-testid="stSelectbox"] > div {
    background: rgba(255,255,255,0.08) !important;
    border-color: rgba(255,255,255,0.15) !important; color: white !important;
}
</style>""", unsafe_allow_html=True)

nav_cols = st.columns(len(PAGES) + 1)
for col, page in zip(nav_cols[:-1], PAGES):
    with col:
        btn_type = "primary" if st.session_state.page == page else "secondary"
        if st.button(page, key=f"nav_{page}", use_container_width=True, type=btn_type):
            st.session_state.page = page
            st.rerun()
with nav_cols[-1]:
    if st.button("🔄", key="nav_refresh", help="Refresh data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# TL selector
new_tl = st.selectbox("Team", TL_NAMES, index=TL_NAMES.index(active_tl), label_visibility="collapsed")
if new_tl != active_tl:
    st.session_state.active_tl = new_tl
    st.rerun()

active_tl = st.session_state.active_tl
my_team   = next((t for t in ALL_TEAMS if t["tl"] == active_tl), ALL_TEAMS[0])

# ── PIN GATE ──────────────────────────────────────────────────────
if not is_authenticated(active_tl):
    show_pin_gate(active_tl)
    st.stop()

# ── ATTENDANCE DATA ───────────────────────────────────────────────
att_data = safe_load(
    read_attendance_today,
    {"checked_in": pd.DataFrame(), "exceptions": pd.DataFrame(),
     "team_members": pd.DataFrame(), "today": str(today)}
) if DATA_CONNECTED else {
    "checked_in": pd.DataFrame(), "exceptions": pd.DataFrame(),
    "team_members": pd.DataFrame(), "today": str(today)
}

checked_in_df = att_data.get("checked_in",  pd.DataFrame())
exceptions_df = att_data.get("exceptions",  pd.DataFrame())
my_engineers  = my_team["engineers"]
today_str     = str(today)

no_response_emails = set()
no_response_names  = set()
if not exceptions_df.empty and "EngineerEmail" in exceptions_df.columns:
    for _, r in exceptions_df.iterrows():
        email = str(r.get("EngineerEmail", "")).strip().lower()
        no_response_emails.add(email)
        eng_name = str(r.get("EngineerName", "")).strip()
        if eng_name:
            no_response_names.add(eng_name.lower())

checkin_details = {}
if not checked_in_df.empty and "EngineerEmail" in checked_in_df.columns:
    for _, r in checked_in_df.iterrows():
        if str(r.get("Date", "")).strip() != today_str: continue
        if "نعم" not in str(r.get("Status", "")): continue
        email  = str(r.get("EngineerEmail", "")).strip().lower()
        visits = str(r.get("No_x002e__of_visits ", r.get("No_of_visits", "0"))).strip()
        checkin_details[email] = {
            "time":     str(r.get("CheckInTime", ""))[:5] if r.get("CheckInTime") else "—",
            "location": str(r.get("WorkLocation", "")) or "—",
            "visits":   visits or "0",
        }

att_rows = []
for eng in my_engineers:
    eng_email = next((e for e, n in KNOWN_EMAILS.items() if n == eng), None)
    if eng_email is None:
        eng_email = eng.lower().replace(" ", ".") + "@socotec.com"
    is_no = (
        eng_email in no_response_emails or
        eng.lower() in no_response_names or
        any(eng.lower() in n for n in no_response_names)
    )
    if is_no:
        att_rows.append({"Engineer": eng, "Status": "out", "Check-in": "—", "Location": "—", "Visits": "—"})
    else:
        d = checkin_details.get(eng_email, {})
        att_rows.append({
            "Engineer": eng, "Status": "in",
            "Check-in": d.get("time", "—"),
            "Location": d.get("location", "—"),
            "Visits":   d.get("visits", "0"),
        })

in_count  = sum(1 for r in att_rows if r["Status"] == "in")
out_count = sum(1 for r in att_rows if r["Status"] == "out")
claims_df = safe_load(read_claims_data) if DATA_CONNECTED else pd.DataFrame()
m_str     = today.strftime("%Y-%m")
claims_month = len(claims_df[claims_df.get("Month", pd.Series()) == m_str]) \
    if not claims_df.empty and "Month" in claims_df.columns else 0

# ══════════════════════════════════════════════════════════════════
# PAGE: HOME
# ══════════════════════════════════════════════════════════════════
if st.session_state.page == "Home":
    hour     = datetime.now().hour
    greeting = "Good morning" if hour < 12 else "Good afternoon" if hour < 17 else "Good evening"
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
      <div class="stat-card" style="--accent:#0072BB;"><div class="stat-label">Team size</div>
        <div class="stat-val">{len(my_engineers)}</div><div class="stat-sub">{my_team['region']}</div></div>
      <div class="stat-card" style="--accent:#00A94F;"><div class="stat-label">Checked in today</div>
        <div class="stat-val">{in_count}</div><div class="stat-sub">as of now</div></div>
      <div class="stat-card" style="--accent:#F59E0B;"><div class="stat-label">No response</div>
        <div class="stat-val">{out_count}</div><div class="stat-sub">Today</div></div>
      <div class="stat-card" style="--accent:#EF4444;"><div class="stat-label">Claims (month)</div>
        <div class="stat-val">{claims_month}</div><div class="stat-sub">{MONTHS[today.month-1]} {today.year}</div></div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="sec-title">Quick access</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="tool-grid">
      <a href="https://rd6-socotec.streamlit.app/" target="_blank" style="text-decoration:none;">
        <div class="tool-card" style="--tc:#3B82F6;--tb:#EFF6FF;">
          <div class="tool-icon">📄</div><div class="tool-name">RD6 Generator</div>
          <div class="tool-desc">Completion of works reports</div><span class="tool-tag">Streamlit</span>
        </div></a>
      <a href="https://socotec-zones.streamlit.app/" target="_blank" style="text-decoration:none;">
        <div class="tool-card" style="--tc:#8B5CF6;--tb:#F5F3FF;">
          <div class="tool-icon">🗺️</div><div class="tool-name">Zone Manager</div>
          <div class="tool-desc">Engineer zone assignments</div><span class="tool-tag">Streamlit</span>
        </div></a>
      <div class="tool-card" style="--tc:#00A94F;--tb:#E6F7EE;">
        <div class="tool-icon">✅</div><div class="tool-name">Attendance</div>
        <div class="tool-desc">Daily check-in status</div><span class="tool-tag">Live</span></div>
      <div class="tool-card" style="--tc:#EF4444;--tb:#FEE2E2;">
        <div class="tool-icon">📋</div><div class="tool-name">Claims Tracker</div>
        <div class="tool-desc">Log & track engineer claims</div><span class="tool-tag">Built-in</span></div>
      <div class="tool-card" style="--tc:#F59E0B;--tb:#FFFBEB;">
        <div class="tool-icon">📅</div><div class="tool-name">Saturday OT</div>
        <div class="tool-desc">Overtime visit submissions</div><span class="tool-tag">Form + Log</span></div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# PAGE: ATTENDANCE
# ══════════════════════════════════════════════════════════════════
elif st.session_state.page == "Attendance":
    st.markdown(
        f'<div class="welcome-banner">'
        f'<div class="welcome-greeting">Daily attendance</div>'
        f'<div class="welcome-name">✅ {active_tl}\'s team</div>'
        f'<div class="welcome-role">{day_name}, {today.day} {MONTHS[today.month-1]} {today.year}</div>'
        f'</div>',
        unsafe_allow_html=True
    )
    c1, c2, c3 = st.columns(3)
    c1.metric("Checked in", in_count)
    c2.metric("No response", out_count)
    c3.metric("Total team", len(my_engineers))
    filt = st.radio("Filter", ["All", "Checked in", "No response"], horizontal=True)
    rows_show = [
        r for r in att_rows
        if filt == "All"
        or (filt == "Checked in"  and r["Status"] == "in")
        or (filt == "No response" and r["Status"] == "out")
    ]
    for r in rows_show:
        ini   = "".join(w[0] for w in r["Engineer"].split()[:2]).upper()
        pill  = '<span class="pill-in">✅ Checked in</span>'  if r["Status"] == "in" else '<span class="pill-out">❌ No response</span>'
        ttag  = f'<span class="time-tag">{r["Check-in"]}</span>' if r["Check-in"] != "—" else ""
        det   = (f'{r["Location"]} · {r["Visits"]} visits'
                 if r["Location"] not in ("—", "", None)
                 else ("✓ Present" if r["Status"] == "in" else "No check-in recorded"))
        rcls  = "att-row att-in"  if r["Status"] == "in" else "att-row att-out"
        avcls = "att-av-in"       if r["Status"] == "in" else "att-av-out"
        st.markdown(f"""
        <div class="{rcls}">
          <div class="{avcls}">{ini}</div>
          <div style="flex:1">
            <div class="att-name">{r['Engineer']}</div>
            <div class="att-detail">{det}</div>
          </div>
          {ttag}{pill}
        </div>""", unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    st.link_button(
        "📊 Open full attendance log →",
        "https://socotecgroup.sharepoint.com/:x:/r/sites/SOCOTECLIBAN/_layouts/15/Doc.aspx?sourcedoc=%7B7A35EE01-7D25-4E50-A5E1-CB583F76E818%7D"
    )

# ══════════════════════════════════════════════════════════════════
# PAGE: CLAIMS
# ══════════════════════════════════════════════════════════════════
elif st.session_state.page == "Claims":
    is_admin = (active_tl == ADMIN_TL)

    st.markdown("""
    <div style="background:linear-gradient(135deg,#1565C0,#1976D2);
                border-radius:12px;padding:20px 24px;margin-bottom:20px;">
      <div style="font-size:11px;color:#90CAF9;text-transform:uppercase;
                  letter-spacing:1px;margin-bottom:4px;">Claims tracker</div>
      <div style="font-size:22px;font-weight:700;color:#fff;">
        🗂️ Log &amp; track engineer claims
      </div>
      <div style="font-size:13px;color:#BBDEFB;margin-top:4px;">
        All claims saved to shared GitHub
      </div>
    </div>
    """, unsafe_allow_html=True)

    if not is_admin:
        st.info(f"🔒 **Private view** — showing only claims for team: **{active_tl}**")

    raw_claims     = load_claims()
    visible_claims = filter_claims_for_tl(raw_claims, active_tl)

    tab_log, tab_summary, tab_history = st.tabs(
        ["📝 Log a claim", "📊 Team summary", "📜 History"]
    )

    # ── Log a claim ───────────────────────────────────────────────
    with tab_log:
        with st.container(border=True):
            col_left, col_right = st.columns(2)
            with col_left:
                engineer   = st.selectbox("Engineer", my_team["engineers"])
                claim_type = st.selectbox(
                    "Claim type",
                    ["Visit delay", "Missed check-in", "Late submission",
                     "Equipment issue", "Travel expense", "Other"]
                )
            with col_right:
                claim_date = st.date_input("Date", value=date.today())
                category_map = {
                    "Visit delay":      "VISIT",
                    "Missed check-in":  "ATTENDANCE",
                    "Late submission":  "SUBMISSION",
                    "Equipment issue":  "EQUIPMENT",
                    "Travel expense":   "TRAVEL",
                    "Other":            "OTHER",
                }
                category = category_map.get(claim_type, "OTHER")
                st.text_input("Category", value=category, disabled=True)

        description = st.text_area("Description (optional)", height=80)

        # Attachment upload (image or PDF, max 2 MB)
        uploaded_file = st.file_uploader(
            "📎 Attach a file (optional — image or PDF, max 2 MB)",
            type=["jpg", "jpeg", "png", "pdf"],
            key="claim_attachment"
        )
        attachment_b64  = ""
        attachment_name = ""
        if uploaded_file is not None:
            if uploaded_file.size > 2 * 1024 * 1024:
                st.warning("⚠️ File exceeds 2 MB — please attach a smaller file.")
            else:
                attachment_b64  = base64.b64encode(uploaded_file.read()).decode("utf-8")
                attachment_name = uploaded_file.name
                st.success(f"📎 Attached: {attachment_name}")

        if st.button("➕ Submit claim", type="primary", use_container_width=True):
            if not engineer:
                st.error("Please select an engineer.")
            else:
                new_claim = {
                    "id":              str(int(datetime.now().timestamp())),
                    "team_leader":     active_tl,
                    "engineer":        engineer,
                    "type":            claim_type,
                    "category":        category,
                    "date":            str(claim_date),
                    "description":     description,
                    "attachment":      attachment_b64,
                    "attachment_name": attachment_name,
                    "logged_at":       datetime.now().isoformat(),
                }
                save_claim(new_claim)
                st.success(f"✅ Claim logged for **{engineer}**.")
                st.rerun()

    # ── Team summary ──────────────────────────────────────────────
    with tab_summary:
        if not visible_claims:
            st.info("No claims recorded yet for your team.")
        else:
            df = pd.DataFrame(visible_claims)
            if is_admin and "team_leader" in df.columns:
                all_tls  = sorted(df["team_leader"].dropna().unique().tolist())
                sel_tls  = st.multiselect("Filter by team leader", all_tls, default=all_tls)
                df = df[df["team_leader"].isin(sel_tls)]
            c1, c2, c3 = st.columns(3)
            c1.metric("Total claims", len(df))
            c2.metric("Engineers affected",
                      df["engineer"].nunique() if "engineer" in df.columns else 0)
            this_m = today.strftime("%Y-%m")
            c3.metric("This month",
                      len(df[df["date"].astype(str).str.startswith(this_m)])
                      if "date" in df.columns else 0)
            if "type" in df.columns:
                st.bar_chart(df["type"].value_counts())

    # ── History ───────────────────────────────────────────────────
    with tab_history:
        if not visible_claims:
            st.info("No claims history for your team yet.")
        else:
            df_hist = pd.DataFrame(visible_claims)
            display_cols = ["date", "engineer", "type", "category", "description"]
            if is_admin:
                display_cols = ["date", "team_leader", "engineer",
                                "type", "category", "description"]
            df_hist = df_hist[[c for c in display_cols if c in df_hist.columns]]
            if "date" in df_hist.columns:
                df_hist = df_hist.sort_values("date", ascending=False)
            st.dataframe(df_hist, use_container_width=True, hide_index=True)

            # Attachment viewer
            claims_with_att = [c for c in visible_claims if c.get("attachment")]
            if claims_with_att:
                st.markdown("---")
                st.markdown("**📎 Attachments**")
                for c in claims_with_att:
                    att_b64  = c.get("attachment", "")
                    att_name = c.get("attachment_name",
                                     f"{c.get('engineer','')} — {c.get('date','')}")
                    if not att_b64:
                        continue
                    label = f"📎 {c.get('engineer','')} — {c.get('date','')} — {c.get('type','')}"
                    with st.expander(label):
                        try:
                            img_data = base64.b64decode(att_b64)
                            if att_name.lower().endswith((".jpg", ".jpeg", ".png")):
                                st.image(img_data, caption=att_name)
                            else:
                                st.markdown(
                                    f'<a href="data:application/pdf;base64,{att_b64}" '
                                    f'download="{att_name}">⬇️ Download {att_name}</a>',
                                    unsafe_allow_html=True
                                )
                        except Exception:
                            st.warning("Could not display attachment.")

# ══════════════════════════════════════════════════════════════════
# PAGE: RD6
# ══════════════════════════════════════════════════════════════════
elif st.session_state.page == "RD6":
    st.markdown(
        '<div class="welcome-banner">'
        '<div class="welcome-greeting">RD6 Dashboard</div>'
        '<div class="welcome-name">📊 Final visit requirements</div>'
        '<div class="welcome-role">Live data in SharePoint Excel</div>'
        '</div>',
        unsafe_allow_html=True
    )
    c1, c2 = st.columns(2)
    with c1:
        st.link_button(
            "📊 Open RD6 Excel on SharePoint →",
            "https://socotecgroup-my.sharepoint.com/:x:/r/personal/mohamed_mossad_socotec_com/_layouts/15/doc2.aspx?sourcedoc=%7B1E8B3450-766D-4717-80AF-A496EC21E39E%7D",
            use_container_width=True
        )
    with c2:
        st.link_button("📄 Open RD6 Generator App →", "https://rd6-socotec.streamlit.app/",
                       use_container_width=True)
    st.info("The RD6 Excel is always live on SharePoint. Use the filters to view by engineer, status, or region.")
    st.markdown('<div class="sec-title">RD6 engineers by team</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    for i, team in enumerate(ALL_TEAMS):
        if not team["rd6"]:
            continue
        with cols[i % 3]:
            is_me = team["tl"] == active_tl
            color = "#00A94F" if is_me else "#0072BB"
            st.markdown(f"""
            <div class="section-card" style="border-left:4px solid {color}">
              <div style="font-size:12px;font-weight:600;color:{color};margin-bottom:4px;">{team['tl']}</div>
              <div style="font-size:10px;color:#9CA3AF;margin-bottom:6px;">{team['region']}</div>
              <div style="font-size:11px;color:#374151;">{', '.join(team['rd6'])}</div>
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# PAGE: SATURDAY OT
# ══════════════════════════════════════════════════════════════════
elif st.session_state.page == "Saturday OT":
    st.markdown(
        '<div class="welcome-banner">'
        '<div class="welcome-greeting">Saturday overtime</div>'
        '<div class="welcome-name">📅 Saturday OT Visit Submissions</div>'
        '<div class="welcome-role">Submit requests and view the log</div>'
        '</div>',
        unsafe_allow_html=True
    )
    c1, c2 = st.columns(2)
    with c1:
        st.link_button("📝 Submit Saturday Visit Form",
                       "https://forms.cloud.microsoft/e/shfQ9UjNEV",
                       use_container_width=True)
    with c2:
        st.link_button(
            "📊 View Submissions Log",
            "https://socotecgroup.sharepoint.com/:x:/r/sites/SOCOTECLIBAN/_layouts/15/Doc.aspx?sourcedoc=%7BBEC26706-1B1D-41B4-A9ED-75B47B9CB108%7D",
            use_container_width=True
        )

# ══════════════════════════════════════════════════════════════════
# PAGE: LINKS
# ══════════════════════════════════════════════════════════════════
elif st.session_state.page == "Links":
    st.markdown(
        '<div class="welcome-banner">'
        '<div class="welcome-greeting">Resources</div>'
        '<div class="welcome-name">🔗 Links & Resources</div>'
        '<div class="welcome-role">All SOCOTEC Arabia tools and documents</div>'
        '</div>',
        unsafe_allow_html=True
    )
    links = [
        ("📊", "Daily Attendance Log", "Full attendance Excel",
         "https://socotecgroup.sharepoint.com/:x:/r/sites/SOCOTECLIBAN/_layouts/15/Doc.aspx?sourcedoc=%7B7A35EE01-7D25-4E50-A5E1-CB583F76E818%7D"),
        ("📝", "Saturday OT Form", "نموذج زيارات يوم السبت",
         "https://forms.cloud.microsoft/e/shfQ9UjNEV"),
        ("📋", "Saturday OT Log", "Submissions Excel",
         "https://socotecgroup.sharepoint.com/:x:/r/sites/SOCOTECLIBAN/_layouts/15/Doc.aspx?sourcedoc=%7BBEC26706-1B1D-41B4-A9ED-75B47B9CB108%7D"),
        ("📊", "RD6 Dashboard Excel", "Final visit requirements",
         "https://socotecgroup-my.sharepoint.com/:x:/r/personal/mohamed_mossad_socotec_com/_layouts/15/doc2.aspx?sourcedoc=%7B1E8B3450-766D-4717-80AF-A496EC21E39E%7D"),
        ("🔒", "RD6 Insulation Certificates", "Attachments folder",
         "https://socotecgroup.sharepoint.com/sites/SOCOTECLIBAN/KSA%20Shared%20Documents/Forms/AllItems.aspx?id=%2Fsites%2FSOCOTECLIBAN%2FKSA%20Shared%20Documents%2FTeam%20Leaders%20RD6%20follow%2DUp%2FRD6%20Attachments"),
        ("📄", "RD6 Generator", "Streamlit app", "https://rd6-socotec.streamlit.app/"),
        ("🗺️", "Zone Manager", "Streamlit app", "https://socotec-zones.streamlit.app/"),
    ]
    cols = st.columns(2)
    for i, (icon, name, desc, url) in enumerate(links):
        with cols[i % 2]:
            st.link_button(f"{icon} {name} — {desc}", url, use_container_width=True)
