import streamlit as st
import pandas as pd
import requests
import json
import base64
from datetime import date

GITHUB_RAW  = "https://raw.githubusercontent.com/MohamedAlyMosaad/socotec-arabia-portal/main/data"
GITHUB_API  = "https://api.github.com/repos/MohamedAlyMosaad/socotec-arabia-portal/contents/data"

def _today():
    return date.today().strftime("%Y-%m-%d")

def read_attendance_today() -> dict:
    try:
        r = requests.get(f"{GITHUB_RAW}/attendance.json", timeout=10)
        r.raise_for_status()

        # The file content is double-encoded — Power Automate base64'd the JSON
        # Try direct JSON first, then base64 decode
        try:
            raw = r.json()
        except Exception:
            # Content might be base64 string
            raw = json.loads(base64.b64decode(r.text.strip()).decode('utf-8'))

        today = _today()

        # Handle both formats Power Automate might send
        checked_in_raw = raw.get("checkedIn", raw.get("value", []))
        exceptions_raw = raw.get("exceptions", [])

        # Convert to DataFrames
        df_in  = pd.DataFrame(checked_in_raw)  if checked_in_raw  else pd.DataFrame()
        df_exc = pd.DataFrame(exceptions_raw)  if exceptions_raw  else pd.DataFrame()

        # Normalize column names — Power Automate uses various casings
        def norm_cols(df):
            if df.empty: return df
            df.columns = [c.strip() for c in df.columns]
            rename = {}
            for c in df.columns:
                cl = c.lower().replace(' ','').replace('_','')
                if cl == 'engineername':   rename[c] = 'EngineerName'
                if cl == 'engineeremail':  rename[c] = 'EngineerEmail'
                if cl == 'checkintime':    rename[c] = 'CheckInTime'
                if cl == 'worklocation':   rename[c] = 'WorkLocation'
                if cl == 'no_ofvisits' or cl == 'noofvisits' or cl == 'no_of_visits': rename[c] = 'No_of_visits'
                if cl == 'date':           rename[c] = 'Date'
                if cl == 'status':         rename[c] = 'Status'
                if cl == 'team':           rename[c] = 'Team'
            return df.rename(columns=rename)

        df_in  = norm_cols(df_in)
        df_exc = norm_cols(df_exc)

        # Filter by today's date if Date column exists
        if not df_in.empty and 'Date' in df_in.columns:
            df_in['Date'] = pd.to_datetime(df_in['Date'], errors='coerce').dt.strftime('%Y-%m-%d')
            df_in = df_in[df_in['Date'] == today]

        if not df_exc.empty and 'Date' in df_exc.columns:
            df_exc['Date'] = pd.to_datetime(df_exc['Date'], errors='coerce').dt.strftime('%Y-%m-%d')
            df_exc = df_exc[df_exc['Date'] == today]

        # checked_in = those in attendance log (they responded)
        # exceptions  = those who did NOT respond
        return {
            "checked_in":   df_in,
            "exceptions":   df_exc,
            "team_members": pd.DataFrame(),
            "today":        raw.get("date", today),
            "raw_date":     raw.get("date", today)
        }
    except Exception as e:
        st.warning(f"Could not load attendance: {e}")
        return {"checked_in": pd.DataFrame(), "exceptions": pd.DataFrame(),
                "team_members": pd.DataFrame(), "today": _today(), "raw_date": _today()}

def read_claims_data() -> pd.DataFrame:
    try:
        r = requests.get(f"{GITHUB_RAW}/claims.json", timeout=10)
        if r.status_code == 404:
            return pd.DataFrame()
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
            st.error("GITHUB_TOKEN not set in Streamlit secrets")
            return False

        headers = {
            "Authorization": f"token {token}",
            "Content-Type": "application/json"
        }

        # Get existing claims
        raw_url = f"https://raw.githubusercontent.com/{repo}/main/data/claims.json"
        r = requests.get(raw_url, timeout=10)
        claims = r.json() if r.status_code == 200 else []
        if not isinstance(claims, list):
            claims = []
        claims.append(claim)

        # Get SHA for update
        api_url = f"https://api.github.com/repos/{repo}/contents/data/claims.json"
        sha_r = requests.get(api_url, headers=headers, timeout=10)
        sha = sha_r.json().get("sha", "") if sha_r.status_code == 200 else ""

        content = base64.b64encode(
            json.dumps(claims, ensure_ascii=False, indent=2).encode('utf-8')
        ).decode('utf-8')

        payload = {"message": f"Add claim: {claim.get('Engineer','')}", "content": content}
        if sha:
            payload["sha"] = sha

        resp = requests.put(api_url, headers=headers, json=payload, timeout=15)
        return resp.status_code in [200, 201]
    except Exception as e:
        st.error(f"Could not save claim: {e}")
        return False

def read_rd6_data() -> pd.DataFrame:
    return pd.DataFrame()

def read_saturday_ot() -> pd.DataFrame:
    return pd.DataFrame()
