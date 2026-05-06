import streamlit as st
import pandas as pd
import requests
import json
import io

GITHUB_RAW = "https://raw.githubusercontent.com/MohamedAlyMosaad/socotec-arabia-portal/main/data"

def read_attendance_today() -> dict:
    """Read attendance from GitHub JSON file written by Power Automate."""
    try:
        url = f"{GITHUB_RAW}/attendance.json"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()

        # Parse checkedIn rows
        checked_in_rows = data.get("checkedIn", [])
        exceptions_rows = data.get("exceptions", [])

        checked_in = pd.DataFrame(checked_in_rows) if checked_in_rows else pd.DataFrame()
        exceptions  = pd.DataFrame(exceptions_rows) if exceptions_rows else pd.DataFrame()

        # Normalize column names
        if not checked_in.empty:
            checked_in.columns = [c.strip() for c in checked_in.columns]
        if not exceptions.empty:
            exceptions.columns = [c.strip() for c in exceptions.columns]

        return {
            "checked_in":   checked_in,
            "exceptions":   exceptions,
            "team_members": pd.DataFrame(),
            "today":        data.get("date", "")
        }
    except Exception as e:
        st.warning(f"Could not load attendance data: {e}")
        return {"checked_in": pd.DataFrame(), "exceptions": pd.DataFrame(),
                "team_members": pd.DataFrame(), "today": ""}

def read_claims_data() -> pd.DataFrame:
    """Read claims from GitHub JSON file."""
    try:
        url = f"{GITHUB_RAW}/claims.json"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return pd.DataFrame(r.json())
    except Exception:
        return pd.DataFrame()

def write_claim_to_sharepoint(claim: dict) -> bool:
    """Write claim to GitHub via API."""
    try:
        token = st.secrets.get("GITHUB_TOKEN", "")
        repo  = st.secrets.get("GITHUB_REPO", "MohamedAlyMosaad/socotec-arabia-portal")
        if not token:
            st.error("GITHUB_TOKEN not set in secrets")
            return False

        # Get current claims
        raw_url = f"https://raw.githubusercontent.com/{repo}/main/data/claims.json"
        r = requests.get(raw_url, timeout=10)
        claims = r.json() if r.status_code == 200 else []
        claims.append(claim)

        # Get SHA of existing file
        api_url = f"https://api.github.com/repos/{repo}/contents/data/claims.json"
        headers = {"Authorization": f"token {token}", "Content-Type": "application/json"}
        sha_r = requests.get(api_url, headers=headers)
        sha = sha_r.json().get("sha", "") if sha_r.status_code == 200 else ""

        import base64
        content = base64.b64encode(json.dumps(claims, ensure_ascii=False, indent=2).encode()).decode()
        payload = {"message": "Add claim", "content": content}
        if sha:
            payload["sha"] = sha

        resp = requests.put(api_url, headers=headers, json=payload)
        return resp.status_code in [200, 201]
    except Exception as e:
        st.error(f"Could not save claim: {e}")
        return False

def read_rd6_data() -> pd.DataFrame:
    return pd.DataFrame()

def read_saturday_ot() -> pd.DataFrame:
    return pd.DataFrame()
