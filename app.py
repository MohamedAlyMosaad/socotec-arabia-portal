import streamlit as st
import pandas as pd
from datetime import datetime, date
import json, requests, base64, calendar

st.set_page_config(page_title="SOCOTEC Arabia Portal", page_icon="🏢",
                   layout="wide", initial_sidebar_state="collapsed")

ADMIN_TL     = "Mohamed Mossad"

# ── GITHUB CONSTANTS (defined early — used by PIN and claims functions) ──
GITHUB_REPO  = "MohamedAlyMosaad/socotec-arabia-portal"
CLAIMS_PATH  = "data/claims.json"
PINS_PATH    = "data/pins.json"
GITHUB_RAW   = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/{CLAIMS_PATH}"
PINS_RAW_URL = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/{PINS_PATH}"
LOGO_B64  = "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"

# ── ALL ENGINEERS (for Nizar full-access view) ────────────────────
_ALL_ENGINEERS = [
    "Jubran Alshahrani","Khaled Alshehri","Abdulamajeed Fahad","Abdulaziz QSEM",
    "Abdulwahab Alsharari","Ehsan Awad","Khalid Daghriri","Saeed Alqahtani",
    "Waleed Khalid","Younis YOUSEF","Bader ORAINI","Ayman ASHRAF","Omar Abdulkareem",
    "Raed Huwaizi","Abdulkarim Ghurmullah","Mohammad Alsaleh","Abdulrhman Jaafari",
    "Hamad Khudaysh","Sultan Almalki","Adel EID","Abdulelah DAFER","Tahar BAHAR",
    "Mohamed RAJA","Wahid Ali","Mahmoud Ibrahim",
    "Abdullah Qarni","Abdullah Qurashi","Hatim Mansour","Abdulaziz Otaibi","Nawaf Afifi",
    "Meshari Alsharari","Khalid Khalaf","Yazeed Adilah","Tariq Alsharari",
    "Mansour Sultan","Meshari DHAHER","Abdullah ALHABIB",
    "Abdullah Mahdi","Abdulmohsen Bakari","Wesam Thabet","Thamer AZMI","Ali KAMAL",
    "Abdulkarim Dhumran","Nawaf Sanad","Salim Khalid","Mohya Otaibi","Ali GFAELY",
    "Ahmed Khalid","Osama Hassan","Amr Saif",
    "Mohamed Mossad","Ibrahim ABDELMASSIH","Noaman Rashed",
]

# ── TEAMS ─────────────────────────────────────────────────────────
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
     "engineers": _ALL_ENGINEERS,
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

# ── PIN AUTH (self-service, stored in GitHub data/pins.json) ──────
@st.cache_data(ttl=30)
def _load_pins_from_github() -> dict:
    """Load PIN file from GitHub. Returns {} if not found."""
    try:
        r = requests.get(PINS_RAW_URL, timeout=8)
        if r.status_code == 200:
            return r.json()
        return {}
    except Exception:
        return {}

def _save_pin_to_github(tl: str, hashed_pin: str):
    """Write/update a TL PIN in data/pins.json on GitHub."""
    token = _github_token()
    if not token:
        st.error("❌ GITHUB_TOKEN not set — cannot save PIN.")
        return False
    hdrs    = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
    api_url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{PINS_PATH}"
    gr      = requests.get(api_url, headers=hdrs, timeout=8)
    if gr.status_code == 200:
        fi  = gr.json()
        sha = fi["sha"]
        try:    existing = json.loads(base64.b64decode(fi["content"]).decode())
        except: existing = {}
    elif gr.status_code == 404:
        sha, existing = None, {}
    else:
        st.error(f"❌ GitHub GET {gr.status_code}")
        return False
    existing[tl] = hashed_pin
    new_b64 = base64.b64encode(
        json.dumps(existing, ensure_ascii=False, indent=2).encode()
    ).decode()
    body = {"message": f"Set PIN for {tl}", "content": new_b64}
    if sha: body["sha"] = sha
    pr = requests.put(api_url, headers=hdrs, json=body, timeout=10)
    if pr.status_code in (200, 201):
        st.cache_data.clear()
        return True
    st.error(f"❌ GitHub PUT {pr.status_code}")
    return False

def _hash_pin(pin: str) -> str:
    """Simple hash so raw PINs are never stored."""
    import hashlib
    return hashlib.sha256(("socotec_salt_" + pin.strip()).encode()).hexdigest()

def _master_pin() -> str:
    """Admin master override PIN from Streamlit secrets."""
    try:    return str(st.secrets.get("MASTER_PIN", ""))
    except: return ""

def _check_pin(tl: str, entered: str) -> bool:
    """Return True if entered PIN matches stored hash OR master override."""
    # Master override always works
    mp = _master_pin()
    if mp and entered.strip() == mp:
        return True
    pins    = _load_pins_from_github()
    stored  = pins.get(tl, "")
    if not stored:
        return False   # no PIN set yet — should go through setup flow
    return _hash_pin(entered) == stored

def _has_pin_set(tl: str) -> bool:
    return bool(_load_pins_from_github().get(tl, ""))

def _is_auth(tl: str) -> bool:
    key = "pin_ok_" + tl.replace(" ", "_").replace(".", "_")
    return st.session_state.get(key, False)

def _set_auth(tl: str):
    key = "pin_ok_" + tl.replace(" ", "_").replace(".", "_")
    st.session_state[key] = True

# ── STYLING ───────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');
html,body,[class*="css"]{font-family:'DM Sans',sans-serif;}
#MainMenu,footer,header{visibility:hidden;}
[data-testid="stHeader"],[data-testid="stToolbar"],[data-testid="stDecoration"]{display:none!important;}
.stDeployButton,.stApp>header,div[data-testid="stStatusWidget"]{display:none!important;}
.block-container{padding-top:0!important;padding-bottom:2rem;max-width:1200px;}
section[data-testid="stSidebar"]{display:none;}
.portal-header{background:linear-gradient(135deg,#0072BB 0%,#005A96 100%);margin:-1rem -1rem 0;padding:14px 28px;display:flex;align-items:center;justify-content:space-between;}
.portal-logo{display:flex;align-items:center;gap:12px;}
.portal-logo-title{font-size:15px;font-weight:700;color:white;letter-spacing:-0.01em;line-height:1.2;}
.portal-logo-sub{font-size:10px;color:rgba(255,255,255,0.7);}
.date-chip{background:rgba(255,255,255,0.15);color:white;font-size:11px;padding:5px 12px;border-radius:20px;font-family:'DM Mono',monospace;}
.user-chip{width:32px;height:32px;border-radius:50%;background:rgba(255,255,255,0.2);color:white;font-size:12px;font-weight:600;display:flex;align-items:center;justify-content:center;}
.welcome-banner{background:linear-gradient(135deg,#0072BB,#005A96);border-radius:14px;padding:24px 28px;color:white;margin-bottom:18px;position:relative;overflow:hidden;}
.welcome-banner::before{content:'';position:absolute;right:-30px;top:-30px;width:200px;height:200px;border-radius:50%;background:rgba(255,255,255,0.05);}
.welcome-greeting{font-size:13px;opacity:.75;margin-bottom:4px;}
.welcome-name{font-size:22px;font-weight:600;margin-bottom:3px;}
.welcome-role{font-size:12px;opacity:.7;margin-bottom:18px;}
.welcome-stats{display:flex;gap:28px;padding-top:16px;border-top:1px solid rgba(255,255,255,0.15);}
.ws-num{font-size:24px;font-weight:600;font-family:'DM Mono',monospace;}
.ws-label{font-size:10px;opacity:.7;margin-top:2px;}
.stat-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:20px;}
.stat-card{background:white;border-radius:12px;padding:16px;border-top:3px solid var(--accent,#0072BB);box-shadow:0 1px 3px rgba(0,0,0,.06),0 4px 12px rgba(0,0,0,.04);}
.stat-label{font-size:11px;color:#6B7280;text-transform:uppercase;letter-spacing:.06em;margin-bottom:6px;}
.stat-val{font-size:26px;font-weight:700;color:var(--accent,#0072BB);font-family:'DM Mono',monospace;line-height:1;}
.stat-sub{font-size:11px;color:#9CA3AF;margin-top:4px;}
.tool-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:12px;margin-bottom:24px;}
.tool-card{background:white;border-radius:14px;padding:20px 16px;box-shadow:0 1px 3px rgba(0,0,0,.06),0 4px 12px rgba(0,0,0,.04);cursor:pointer;border-bottom:3px solid var(--tc,#0072BB);transition:transform .15s,box-shadow .15s;}
.tool-card:hover{transform:translateY(-2px);box-shadow:0 8px 24px rgba(0,0,0,.1);}
.tool-icon{width:44px;height:44px;border-radius:12px;background:var(--tb,#E6F3FB);display:flex;align-items:center;justify-content:center;font-size:20px;margin-bottom:10px;}
.tool-name{font-size:13px;font-weight:600;margin-bottom:4px;}
.tool-desc{font-size:11px;color:#9CA3AF;line-height:1.4;margin-bottom:8px;}
.tool-tag{display:inline-block;font-size:10px;font-weight:500;padding:2px 8px;border-radius:20px;background:var(--tb,#E6F3FB);color:var(--tc,#0072BB);}
.sec-title{font-size:11px;font-weight:600;color:#9CA3AF;text-transform:uppercase;letter-spacing:.07em;margin-bottom:12px;}
.att-row{border-radius:10px;padding:12px 16px;margin-bottom:8px;display:flex;align-items:center;gap:12px;border-left:4px solid #ccc;}
.att-row.att-in{background:#F0FBF5;border-left-color:#00A94F;}
.att-row.att-out{background:#FFF5F5;border-left-color:#EF4444;}
.att-av-in{width:36px;height:36px;border-radius:50%;background:#E6F7EE;color:#007A38;font-size:12px;font-weight:700;display:flex;align-items:center;justify-content:center;flex-shrink:0;}
.att-av-out{width:36px;height:36px;border-radius:50%;background:#FEE2E2;color:#991B1B;font-size:12px;font-weight:700;display:flex;align-items:center;justify-content:center;flex-shrink:0;}
.att-name{font-size:13px;font-weight:500;flex:1;color:#111;}
.att-detail{font-size:11px;color:#6B7280;}
.pill-in{background:#DCFCE7;color:#166534;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:600;}
.pill-out{background:#FEE2E2;color:#991B1B;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:600;}
.time-tag{background:#E0F2FE;color:#0369A1;font-size:11px;font-family:'DM Mono',monospace;padding:3px 8px;border-radius:6px;}
.section-card{background:white;border-radius:14px;padding:20px;box-shadow:0 1px 3px rgba(0,0,0,.06),0 4px 12px rgba(0,0,0,.04);margin-bottom:14px;}
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ─────────────────────────────────────────────────
if "page"      not in st.session_state: st.session_state.page      = "Home"
if "active_tl" not in st.session_state: st.session_state.active_tl = "Mohamed Mossad"

# ── SHAREPOINT ────────────────────────────────────────────────────
try:
    from sharepoint_client import read_attendance_today, read_claims_data
    DATA_CONNECTED = True
except Exception:
    DATA_CONNECTED = False

def safe_load(fn, fallback=None):
    try:    return fn()
    except: return fallback if fallback is not None else pd.DataFrame()

# ── CLAIMS: GitHub JSON ───────────────────────────────────────────

def _github_token():
    try:    return st.secrets["GITHUB_TOKEN"]
    except: return None

@st.cache_data(ttl=60)
def load_claims() -> list:
    try:
        r = requests.get(GITHUB_RAW, timeout=10)
        if r.status_code == 200:
            data = r.json()
            raw = data if isinstance(data, list) else data.get("claims", []) if isinstance(data, dict) else []
            return [_norm(c) for c in raw if isinstance(c, dict)]
        return []
    except: return []

def _norm(c):
    return {
        "id":              c.get("id",              c.get("Id",          "")),
        "team_leader":     c.get("team_leader",      c.get("TeamLeader",  ADMIN_TL)),
        "engineer":        c.get("engineer",         c.get("Engineer",    "")),
        "type":            c.get("type",             c.get("ClaimType",   c.get("claim_type",""))),
        "category":        c.get("category",         c.get("Category",    "")),
        "date":            c.get("date",             c.get("Date",        "")),
        "description":     c.get("description",      c.get("Description", "")),
        "attachment":      c.get("attachment",       ""),
        "attachment_name": c.get("attachment_name",  ""),
        "logged_at":       c.get("logged_at",        c.get("LoggedAt",    "")),
        "auto_generated":  str(c.get("AutoGenerated", c.get("auto_generated","No"))),
        "month":           c.get("month",            c.get("Month",       "")),
    }

def save_claim(claim):
    token = _github_token()
    if not token:
        st.error("❌ GITHUB_TOKEN not set in Streamlit secrets.")
        return
    hdrs = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
    url  = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{CLAIMS_PATH}"
    gr   = requests.get(url, headers=hdrs, timeout=10)
    if gr.status_code == 200:
        fi  = gr.json()
        sha = fi["sha"]
        try:
            ex = json.loads(base64.b64decode(fi["content"]).decode("utf-8"))
            if isinstance(ex, dict): ex = ex.get("claims", [])
            if not isinstance(ex, list): ex = []
        except: ex = []
    elif gr.status_code == 404: sha, ex = None, []
    else: st.error(f"❌ GitHub GET {gr.status_code}"); return
    ex = [_norm(c) for c in ex if isinstance(c, dict)]
    ex.append(claim)
    new_b64 = base64.b64encode(json.dumps(ex, ensure_ascii=False, indent=2).encode()).decode()
    body = {"message": f"Add claim: {claim.get('engineer','?')} — {claim.get('type','?')}", "content": new_b64}
    if sha: body["sha"] = sha
    pr = requests.put(url, headers=hdrs, json=body, timeout=15)
    if pr.status_code in (200, 201): st.cache_data.clear()
    else: st.error(f"❌ GitHub PUT {pr.status_code} — {pr.text[:300]}")

def _filter_claims(claims, viewer):
    if viewer in (ADMIN_TL, "Nizar Lazreq"): return claims
    return [c for c in claims if c.get("team_leader","") == viewer]

# ── HEADER ────────────────────────────────────────────────────────
active_tl = st.session_state.active_tl
my_team   = next((t for t in ALL_TEAMS if t["tl"] == active_tl), ALL_TEAMS[0])
initials  = "".join(w[0] for w in active_tl.split()[:2]).upper()
today     = date.today()
day_name  = calendar.day_name[today.weekday()]
MONTHS    = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

st.markdown(f"""
<div class="portal-header">
  <div class="portal-logo">
    <div style="width:40px;height:40px;background:white;border-radius:10px;display:flex;align-items:center;justify-content:center;margin-right:10px;flex-shrink:0;padding:3px;">
      <img src="data:image/png;base64,{LOGO_B64}" style="width:100%;height:100%;object-fit:contain;">
    </div>
    <div>
      <div class="portal-logo-title">Socotec Arabia</div>
      <div class="portal-logo-sub">Management Portal</div>
    </div>
  </div>
  <div style="display:flex;align-items:center;gap:10px;">
    <div class="date-chip">{day_name[:3]} {today.day} {MONTHS[today.month-1]}</div>
    <div class="user-chip">{initials}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── NAV ───────────────────────────────────────────────────────────
PAGES = ["Home","Attendance","Claims","RD6","Zone Manager","Saturday OT","Links"]
st.markdown("""<style>
div[data-testid="stHorizontalBlock"]:has(button[kind="secondary"]){
  background:#005A96;margin:0 -1rem;padding:0 8px;gap:0!important;}
div[data-testid="stHorizontalBlock"]:has(button[kind="secondary"]) button{
  background:transparent!important;border:none!important;
  border-bottom:2px solid transparent!important;border-radius:0!important;
  color:rgba(255,255,255,.6)!important;padding:8px 14px!important;
  font-size:13px!important;font-weight:500!important;}
div[data-testid="stHorizontalBlock"]:has(button[kind="primary"]) button[kind="primary"]{
  background:transparent!important;border:none!important;
  border-bottom:2px solid white!important;border-radius:0!important;
  color:white!important;padding:8px 14px!important;
  font-size:13px!important;font-weight:600!important;}
div[data-testid="stSelectbox"] label{display:none!important;}
div[data-testid="stSelectbox"]>div{
  background:rgba(255,255,255,.08)!important;
  border-color:rgba(255,255,255,.15)!important;color:white!important;}
</style>""", unsafe_allow_html=True)

nav_cols = st.columns(len(PAGES)+1)
for col, page in zip(nav_cols[:-1], PAGES):
    with col:
        t = "primary" if st.session_state.page == page else "secondary"
        if st.button(page, key=f"nav_{page}", use_container_width=True, type=t):
            st.session_state.page = page; st.rerun()
with nav_cols[-1]:
    if st.button("🔄", key="nav_refresh", use_container_width=True):
        st.cache_data.clear(); st.rerun()

new_tl = st.selectbox("Team", TL_NAMES, index=TL_NAMES.index(active_tl),
                       label_visibility="collapsed")
if new_tl != active_tl:
    st.session_state.active_tl = new_tl; st.rerun()

active_tl = st.session_state.active_tl
my_team   = next((t for t in ALL_TEAMS if t["tl"] == active_tl), ALL_TEAMS[0])

# (PIN gate is inside Claims tab only)

# ── ATTENDANCE DATA ───────────────────────────────────────────────
_att_fallback = {"checked_in":pd.DataFrame(),"exceptions":pd.DataFrame(),
                 "team_members":pd.DataFrame(),"today":str(today)}
att_data      = safe_load(read_attendance_today, _att_fallback) if DATA_CONNECTED else _att_fallback
checked_in_df = att_data.get("checked_in",  pd.DataFrame())
exceptions_df = att_data.get("exceptions",  pd.DataFrame())
my_engineers  = my_team["engineers"]
today_str     = str(today)

no_resp_emails = set()
no_resp_names  = set()
if not exceptions_df.empty and "EngineerEmail" in exceptions_df.columns:
    for _, r in exceptions_df.iterrows():
        no_resp_emails.add(str(r.get("EngineerEmail","")).strip().lower())
        n = str(r.get("EngineerName","")).strip()
        if n: no_resp_names.add(n.lower())

checkin_det = {}
if not checked_in_df.empty and "EngineerEmail" in checked_in_df.columns:
    for _, r in checked_in_df.iterrows():
        if str(r.get("Date","")).strip() != today_str: continue
        if "نعم" not in str(r.get("Status","")): continue
        em = str(r.get("EngineerEmail","")).strip().lower()
        v  = str(r.get("No_x002e__of_visits ", r.get("No_of_visits","0"))).strip()
        checkin_det[em] = {
            "time":     str(r.get("CheckInTime",""))[:5] if r.get("CheckInTime") else "—",
            "location": str(r.get("WorkLocation","")) or "—",
            "visits":   v or "0",
        }

att_rows = []
for eng in my_engineers:
    em = next((e for e,n in KNOWN_EMAILS.items() if n==eng), None)
    if em is None: em = eng.lower().replace(" ",".")+"@socotec.com"
    no = (em in no_resp_emails or eng.lower() in no_resp_names or
          any(eng.lower() in n for n in no_resp_names))
    if no: att_rows.append({"Engineer":eng,"Status":"out","Check-in":"—","Location":"—","Visits":"—"})
    else:
        d = checkin_det.get(em,{})
        att_rows.append({"Engineer":eng,"Status":"in","Check-in":d.get("time","—"),
                         "Location":d.get("location","—"),"Visits":d.get("visits","0")})

in_c  = sum(1 for r in att_rows if r["Status"]=="in")
out_c = sum(1 for r in att_rows if r["Status"]=="out")
claims_df  = safe_load(read_claims_data) if DATA_CONNECTED else pd.DataFrame()
m_str      = today.strftime("%Y-%m")
claims_mon = len(claims_df[claims_df.get("Month",pd.Series())==m_str])              if not claims_df.empty and "Month" in claims_df.columns else 0

# ══════════════════════════════════════════════════════════════════
# HOME
# ══════════════════════════════════════════════════════════════════
if st.session_state.page == "Home":
    h  = datetime.now().hour
    gr = "Good morning" if h<12 else "Good afternoon" if h<17 else "Good evening"
    st.markdown(f"""
    <div class="welcome-banner">
      <div class="welcome-greeting">{gr},</div>
      <div class="welcome-name">{active_tl}</div>
      <div class="welcome-role">Team Leader · {my_team['region']} · SOCOTEC Arabia</div>
      <div class="welcome-stats">
        <div><div class="ws-num">{in_c}</div><div class="ws-label">Checked in today</div></div>
        <div><div class="ws-num">{out_c}</div><div class="ws-label">No response</div></div>
        <div><div class="ws-num">{claims_mon}</div><div class="ws-label">Claims this month</div></div>
        <div><div class="ws-num">{len(my_engineers)}</div><div class="ws-label">Team size</div></div>
      </div>
    </div>""", unsafe_allow_html=True)
    st.markdown(f"""<div class="stat-grid">
      <div class="stat-card" style="--accent:#0072BB;"><div class="stat-label">Team size</div>
        <div class="stat-val">{len(my_engineers)}</div><div class="stat-sub">{my_team['region']}</div></div>
      <div class="stat-card" style="--accent:#00A94F;"><div class="stat-label">Checked in today</div>
        <div class="stat-val">{in_c}</div><div class="stat-sub">as of now</div></div>
      <div class="stat-card" style="--accent:#F59E0B;"><div class="stat-label">No response</div>
        <div class="stat-val">{out_c}</div><div class="stat-sub">Today</div></div>
      <div class="stat-card" style="--accent:#EF4444;"><div class="stat-label">Claims (month)</div>
        <div class="stat-val">{claims_mon}</div>
        <div class="stat-sub">{MONTHS[today.month-1]} {today.year}</div></div>
    </div>""", unsafe_allow_html=True)
    st.markdown('<div class="sec-title">Quick access</div>', unsafe_allow_html=True)
    st.markdown("""<div class="tool-grid">
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
        <div class="tool-desc">Overtime visit submissions</div><span class="tool-tag">Form</span></div>
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# ATTENDANCE
# ══════════════════════════════════════════════════════════════════
elif st.session_state.page == "Attendance":
    st.markdown(
        f'<div class="welcome-banner"><div class="welcome-greeting">Daily attendance</div>' +
        f'<div class="welcome-name">✅ {active_tl}\'s team</div>' +
        f'<div class="welcome-role">{day_name}, {today.day} {MONTHS[today.month-1]} {today.year}</div></div>',
        unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    c1.metric("Checked in", in_c); c2.metric("No response", out_c); c3.metric("Total", len(my_engineers))
    filt = st.radio("Filter",["All","Checked in","No response"], horizontal=True)
    for r in att_rows:
        if filt=="Checked in" and r["Status"]!="in": continue
        if filt=="No response" and r["Status"]!="out": continue
        ini   = "".join(w[0] for w in r["Engineer"].split()[:2]).upper()
        pill  = '<span class="pill-in">✅ Checked in</span>' if r["Status"]=="in" else '<span class="pill-out">❌ No response</span>'
        ttag  = f'<span class="time-tag">{r["Check-in"]}</span>' if r["Check-in"]!="—" else ""
        det   = (f'{r["Location"]} · {r["Visits"]} visits' if r["Location"] not in ("—","",None)
                 else ("✓ Present" if r["Status"]=="in" else "No check-in recorded"))
        rc    = "att-row att-in" if r["Status"]=="in" else "att-row att-out"
        av    = "att-av-in"     if r["Status"]=="in" else "att-av-out"
        st.markdown(f'''<div class="{rc}"><div class="{av}">{ini}</div>
          <div style="flex:1"><div class="att-name">{r["Engineer"]}</div>
          <div class="att-detail">{det}</div></div>{ttag}{pill}</div>''', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    st.link_button("📊 Open full attendance log →",
        "https://socotecgroup.sharepoint.com/:x:/r/sites/SOCOTECLIBAN/_layouts/15/Doc.aspx?sourcedoc=%7B7A35EE01-7D25-4E50-A5E1-CB583F76E818%7D")

# ══════════════════════════════════════════════════════════════════
# CLAIMS
# ══════════════════════════════════════════════════════════════════
elif st.session_state.page == "Claims":
    is_admin = active_tl in (ADMIN_TL, "Nizar Lazreq")

    # ── PIN gate — protects Claims tab only ───────────────────────
    if not _is_auth(active_tl):
        has_pin = _has_pin_set(active_tl)
        st.markdown("""
        <div style="height:20px;"></div>
        <div style="display:flex;justify-content:center;">
          <div style="background:#1C1C2E;border-radius:20px;padding:36px 48px;
                      max-width:340px;width:100%;text-align:center;
                      box-shadow:0 8px 32px rgba(0,0,0,.5);">
            <div style="font-size:40px;margin-bottom:12px;">""" +
            ("🔒" if has_pin else "🔑") + """</div>
            <div style="font-size:17px;font-weight:700;color:white;margin-bottom:5px;">"""
            + active_tl + """</div>
            <div style="font-size:13px;color:#90CAF9;">"""
            + ("Enter PIN to access Claims" if has_pin else "Create your PIN to access Claims") +
            """</div>
          </div>
        </div>""", unsafe_allow_html=True)
        col = st.columns([1,2,1])[1]
        with col:
            st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
            if has_pin:
                pin_val = st.text_input("PIN", type="password", max_chars=4,
                                        placeholder="● ● ● ●", label_visibility="collapsed",
                                        key="claims_pin_enter")
                if st.button("Unlock →", type="primary", use_container_width=True,
                             key="claims_pin_btn"):
                    if _check_pin(active_tl, pin_val):
                        _set_auth(active_tl); st.rerun()
                    else:
                        st.error("❌ Incorrect PIN")
            else:
                st.markdown("<div style='font-size:12px;color:#90CAF9;text-align:center;margin-bottom:6px;'>Choose a 4-digit PIN you will remember</div>", unsafe_allow_html=True)
                p1 = st.text_input("New PIN", type="password", max_chars=4,
                                    placeholder="● ● ● ●", label_visibility="collapsed",
                                    key="claims_pin_new")
                p2 = st.text_input("Confirm PIN", type="password", max_chars=4,
                                    placeholder="● ● ● ●", label_visibility="collapsed",
                                    key="claims_pin_confirm")
                if st.button("Set PIN & Enter →", type="primary", use_container_width=True,
                             key="claims_pin_set"):
                    if len(p1) != 4 or not p1.isdigit():
                        st.error("❌ Must be exactly 4 digits")
                    elif p1 != p2:
                        st.error("❌ PINs do not match")
                    else:
                        with st.spinner("Saving PIN..."):
                            ok = _save_pin_to_github(active_tl, _hash_pin(p1))
                        if ok:
                            _set_auth(active_tl); st.success("✅ PIN set!"); st.rerun()
        st.stop()

    st.markdown("""<div style="background:linear-gradient(135deg,#1565C0,#1976D2);
      border-radius:12px;padding:20px 24px;margin-bottom:20px;">
      <div style="font-size:11px;color:#90CAF9;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px;">
        Claims tracker</div>
      <div style="font-size:22px;font-weight:700;color:#fff;">🗂️ Log &amp; track engineer claims</div>
      <div style="font-size:13px;color:#BBDEFB;margin-top:4px;">All claims saved to shared GitHub</div>
    </div>""", unsafe_allow_html=True)
    if not is_admin:
        st.info(f"🔒 **Private view** — showing only claims for: **{active_tl}**")

    raw      = load_claims()
    visible  = _filter_claims(raw, active_tl)
    tl, ts, th = st.tabs(["📝 Log a claim","📊 Team summary","📜 History"])

    with tl:
        with st.container(border=True):
            cl, cr = st.columns(2)
            with cl:
                eng  = st.selectbox("Engineer", my_team["engineers"])
                ctyp = st.selectbox("Claim type",["Visit delay","Missed check-in",
                       "Late submission","Equipment issue","Travel expense","Other"])
            with cr:
                cdt  = st.date_input("Date", value=date.today())
                cmap = {"Visit delay":"VISIT","Missed check-in":"ATTENDANCE",
                        "Late submission":"SUBMISSION","Equipment issue":"EQUIPMENT",
                        "Travel expense":"TRAVEL","Other":"OTHER"}
                cat  = cmap.get(ctyp,"OTHER")
                st.text_input("Category", value=cat, disabled=True)
        desc = st.text_area("Description (optional)", height=80)
        uf   = st.file_uploader("📎 Attach file (image/PDF, max 2 MB)",
                                 type=["jpg","jpeg","png","pdf"], key="att_up")
        ab64, aname = "", ""
        if uf:
            if uf.size > 2*1024*1024: st.warning("⚠️ File too large (>2 MB)")
            else:
                ab64  = base64.b64encode(uf.read()).decode()
                aname = uf.name
                st.success(f"📎 {aname}")
        if st.button("➕ Submit claim", type="primary", use_container_width=True):
            save_claim({"id":str(int(datetime.now().timestamp())),"team_leader":active_tl,
                        "engineer":eng,"type":ctyp,"category":cat,"date":str(cdt),
                        "description":desc,"attachment":ab64,"attachment_name":aname,
                        "logged_at":datetime.now().isoformat()})
            st.success(f"✅ Claim logged for **{eng}**.")
            st.rerun()

    with ts:
        if not visible: st.info("No claims yet.")
        else:
            df = pd.DataFrame(visible)
            if is_admin and "team_leader" in df.columns:
                tls = sorted(df["team_leader"].dropna().unique().tolist())
                sel = st.multiselect("Filter by TL", tls, default=tls)
                df  = df[df["team_leader"].isin(sel)]
            c1,c2,c3 = st.columns(3)
            c1.metric("Total", len(df))
            c2.metric("Engineers", df["engineer"].nunique() if "engineer" in df.columns else 0)
            c3.metric("This month", len(df[df["date"].astype(str).str.startswith(today.strftime("%Y-%m"))]) if "date" in df.columns else 0)
            if "type" in df.columns: st.bar_chart(df["type"].value_counts())

    with th:
        if not visible: st.info("No history yet.")
        else:
            dh = pd.DataFrame(visible)
            cols = ["date","team_leader","engineer","type","category","description"] if is_admin else ["date","engineer","type","category","description"]
            dh   = dh[[c for c in cols if c in dh.columns]]
            if "date" in dh.columns: dh = dh.sort_values("date",ascending=False)
            st.dataframe(dh, use_container_width=True, hide_index=True)
            atts = [c for c in visible if c.get("attachment")]
            if atts:
                st.markdown("---")
                st.markdown("**📎 Attachments**")
                for c in atts:
                    ab64 = c.get("attachment",""); an = c.get("attachment_name",f"{c.get('engineer','')}_{c.get('date','')}")
                    if not ab64: continue
                    with st.expander(f"📎 {c.get('engineer','')} — {c.get('date','')} — {c.get('type','')}"):
                        try:
                            bd = base64.b64decode(ab64)
                            if an.lower().endswith((".jpg",".jpeg",".png")): st.image(bd, caption=an)
                            else: st.markdown(f'<a href="data:application/pdf;base64,{ab64}" download="{an}">⬇️ Download {an}</a>',unsafe_allow_html=True)
                        except: st.warning("Could not display.")

# ══════════════════════════════════════════════════════════════════
# RD6
# ══════════════════════════════════════════════════════════════════
elif st.session_state.page == "RD6":
    st.markdown('<div class="welcome-banner"><div class="welcome-greeting">RD6 Dashboard</div><div class="welcome-name">📊 Final visit requirements</div><div class="welcome-role">Live data in SharePoint Excel</div></div>',unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1: st.link_button("📊 Open RD6 Excel →","https://socotecgroup-my.sharepoint.com/:x:/r/personal/mohamed_mossad_socotec_com/_layouts/15/doc2.aspx?sourcedoc=%7B1E8B3450-766D-4717-80AF-A496EC21E39E%7D",use_container_width=True)
    with c2: st.link_button("📄 Open RD6 Generator →","https://rd6-socotec.streamlit.app/",use_container_width=True)
    st.info("RD6 Excel is always live on SharePoint. Use the filters to view by engineer, status, or region.")
    st.markdown('<div class="sec-title">RD6 engineers by team</div>',unsafe_allow_html=True)
    cols = st.columns(3)
    for i,team in enumerate(ALL_TEAMS):
        if not team["rd6"]: continue
        with cols[i%3]:
            col = "#00A94F" if team["tl"]==active_tl else "#0072BB"
            st.markdown(f'<div class="section-card" style="border-left:4px solid {col}"><div style="font-size:12px;font-weight:600;color:{col};margin-bottom:4px;">{team["tl"]}</div><div style="font-size:10px;color:#9CA3AF;margin-bottom:6px;">{team["region"]}</div><div style="font-size:11px;color:#374151;">{", ".join(team["rd6"])}</div></div>',unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# ZONE MANAGER
# ══════════════════════════════════════════════════════════════════
elif st.session_state.page == "Zone Manager":
    st.markdown('<div class="welcome-banner"><div class="welcome-greeting">Zone assignments</div><div class="welcome-name">🗺️ Zone Manager</div><div class="welcome-role">Engineer zone & project assignments — opens in a new tab</div></div>',unsafe_allow_html=True)
    st.info("The Zone Manager is a separate Streamlit app. Click the button below to open it.")
    st.link_button("🗺️ Open Zone Manager App →","https://socotec-zones.streamlit.app/",use_container_width=True)
    st.markdown("""
    <div class="section-card" style="margin-top:16px;">
      <div style="font-size:13px;font-weight:600;color:#0072BB;margin-bottom:8px;">About Zone Manager</div>
      <div style="font-size:13px;color:#374151;line-height:1.6;">
        The Zone Manager handles engineer-to-zone assignments across all regions.
        Use it to view which engineers are assigned to which project zones,
        update assignments, and track coverage across the IDI Division.
      </div>
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# SATURDAY OT
# ══════════════════════════════════════════════════════════════════
elif st.session_state.page == "Saturday OT":
    st.markdown('<div class="welcome-banner"><div class="welcome-greeting">Saturday overtime</div><div class="welcome-name">📅 Saturday OT Visit Submissions</div><div class="welcome-role">Submit requests and view the log</div></div>',unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1: st.link_button("📝 Submit Saturday Visit Form","https://forms.cloud.microsoft/e/shfQ9UjNEV",use_container_width=True)
    with c2: st.link_button("📊 View Submissions Log","https://socotecgroup.sharepoint.com/:x:/r/sites/SOCOTECLIBAN/_layouts/15/Doc.aspx?sourcedoc=%7BBEC26706-1B1D-41B4-A9ED-75B47B9CB108%7D",use_container_width=True)

# ══════════════════════════════════════════════════════════════════
# LINKS
# ══════════════════════════════════════════════════════════════════
elif st.session_state.page == "Links":
    st.markdown('<div class="welcome-banner"><div class="welcome-greeting">Resources</div><div class="welcome-name">🔗 Links & Resources</div><div class="welcome-role">All SOCOTEC Arabia tools and documents</div></div>',unsafe_allow_html=True)
    for i,(icon,name,desc,url) in enumerate([
        ("📊","Daily Attendance Log","Full attendance Excel","https://socotecgroup.sharepoint.com/:x:/r/sites/SOCOTECLIBAN/_layouts/15/Doc.aspx?sourcedoc=%7B7A35EE01-7D25-4E50-A5E1-CB583F76E818%7D"),
        ("📝","Saturday OT Form","نموذج زيارات يوم السبت","https://forms.cloud.microsoft/e/shfQ9UjNEV"),
        ("📋","Saturday OT Log","Submissions Excel","https://socotecgroup.sharepoint.com/:x:/r/sites/SOCOTECLIBAN/_layouts/15/Doc.aspx?sourcedoc=%7BBEC26706-1B1D-41B4-A9ED-75B47B9CB108%7D"),
        ("📊","RD6 Dashboard Excel","Final visit requirements","https://socotecgroup-my.sharepoint.com/:x:/r/personal/mohamed_mossad_socotec_com/_layouts/15/doc2.aspx?sourcedoc=%7B1E8B3450-766D-4717-80AF-A496EC21E39E%7D"),
        ("🔒","RD6 Certificates","Attachments folder","https://socotecgroup.sharepoint.com/sites/SOCOTECLIBAN/KSA%20Shared%20Documents/Forms/AllItems.aspx?id=%2Fsites%2FSOCOTECLIBAN%2FKSA%20Shared%20Documents%2FTeam%20Leaders%20RD6%20follow%2DUp%2FRD6%20Attachments"),
        ("📄","RD6 Generator","Streamlit app","https://rd6-socotec.streamlit.app/"),
        ("🗺️","Zone Manager","Streamlit app","https://socotec-zones.streamlit.app/"),
    ]):
        with st.columns(2)[i%2]:
            st.link_button(f"{icon} {name} — {desc}", url, use_container_width=True)
