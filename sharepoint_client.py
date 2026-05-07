import streamlit as st
import pandas as pd
import requests
import json
import base64
from datetime import date

GITHUB_RAW = "https://raw.githubusercontent.com/MohamedAlyMosaad/socotec-arabia-portal/main/data"
GITHUB_API = "https://api.github.com/repos/MohamedAlyMosaad/socotec-arabia-portal/contents/data"

def _today():
    return date.today().strftime("%Y-%m-%d")

def read_attendance_today() -> dict:
    """Read attendance JSON from GitHub. Returns ALL rows unfiltered — app.py handles date filtering."""
    try:
        r = requests.get(f"{GITHUB_RAW}/attendance.json", timeout=10)
        r.raise_for_status()

        # Power Automate stores file as base64-encoded JSON string
        # Try parsing as direct JSON first (in case format changed)
        raw = None
        try:
            raw = r.json()
            # If it's a string (base64), decode it
            if isinstance(raw, str):
                raw = json.loads(base64.b64decode(raw).decode('utf-8'))
        except Exception:
            # Try base64 decode of raw text
            try:
                raw = json.loads(base64.b64decode(r.text.strip()).decode('utf-8'))
            except Exception:
                raw = json.loads(r.text)

        if not raw or not isinstance(raw, dict):
            st.warning("attendance.json format unexpected")
            return _empty_att()

        checked_in_raw = raw.get("checkedIn", raw.get("value", []))
        exceptions_raw = raw.get("exceptions", [])

        # Build DataFrames — NO date filtering here, let app.py handle it
        df_in  = pd.DataFrame(checked_in_raw)  if checked_in_raw  else pd.DataFrame()
        df_exc = pd.DataFrame(exceptions_raw)  if exceptions_raw  else pd.DataFrame()

        # Normalize column names
        df_in  = _norm_cols(df_in)
        df_exc = _norm_cols(df_exc)

        return {
            "checked_in":   df_in,
            "exceptions":   df_exc,
            "team_members": pd.DataFrame(),
            "today":        raw.get("date", _today()),
        }
    except Exception as e:
        st.warning(f"Could not load attendance: {e}")
        return _empty_att()

def _empty_att():
    return {"checked_in": pd.DataFrame(), "exceptions": pd.DataFrame(),
            "team_members": pd.DataFrame(), "today": _today()}

def _norm_cols(df):
    """Normalize DataFrame column names from Power Automate output."""
    if df.empty: return df
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]
    rename = {}
    for c in df.columns:
        cl = c.lower().replace(' ','').replace('_','').replace('.','').replace('x002e','')
        if cl == 'engineername':  rename[c] = 'EngineerName'
        if cl == 'engineeremail': rename[c] = 'EngineerEmail'
        if cl == 'checkintime':   rename[c] = 'CheckInTime'
        if cl == 'worklocation':  rename[c] = 'WorkLocation'
        if 'ofvisit' in cl:       rename[c] = 'Visits'
        if cl == 'date':          rename[c] = 'Date'
        if cl == 'status':        rename[c] = 'Status'
        if cl == 'team':          rename[c] = 'Team'
    df = df.rename(columns=rename)
    # Ensure Date is string in yyyy-mm-dd format
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.strftime('%Y-%m-%d')
    return df

def read_claims_data() -> pd.DataFrame:
    try:
        r = requests.get(f"{GITHUB_RAW}/claims.json", timeout=10)
        if r.status_code == 404: return pd.DataFrame()
        r.raise_for_status()
        data = r.json()
        return pd.DataFrame(data) if data else pd.DataFrame()
    except Exception:
        return pd.DataFrame()

def write_claim_to_sharepoint(claim: dict) -> bool:
    try:
        token = st.secrets.get("GITHUB_TOKEN", "")
        repo  = "MohamedAlyMosaad/socotec-arabia-portal"
        if not token:
            st.error("GITHUB_TOKEN not set in secrets")
            return False

        headers = {"Authorization": f"token {token}", "Content-Type": "application/json"}
        raw_url = f"https://raw.githubusercontent.com/{repo}/main/data/claims.json"
        r = requests.get(raw_url, timeout=10)
        claims = r.json() if r.status_code == 200 else []
        if not isinstance(claims, list): claims = []
        claims.append(claim)

        api_url = f"https://api.github.com/repos/{repo}/contents/data/claims.json"
        sha_r = requests.get(api_url, headers=headers, timeout=10)
        sha = sha_r.json().get("sha","") if sha_r.status_code == 200 else ""

        content_b64 = base64.b64encode(
            json.dumps(claims, ensure_ascii=False, indent=2).encode('utf-8')
        ).decode('utf-8')

        payload = {"message": f"Add claim: {claim.get('Engineer','')}", "content": content_b64}
        if sha: payload["sha"] = sha

        resp = requests.put(api_url, headers=headers, json=payload, timeout=15)
        return resp.status_code in [200, 201]
    except Exception as e:
        st.error(f"Could not save claim: {e}")
        return False

def read_rd6_data() -> pd.DataFrame:
    return pd.DataFrame()

def read_saturday_ot() -> pd.DataFrame:
    return pd.DataFrame()
