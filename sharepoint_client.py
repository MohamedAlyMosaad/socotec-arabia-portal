import streamlit as st
import pandas as pd
import io
from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext

SHAREPOINT_URL = "https://socotecgroup.sharepoint.com/sites/SOCOTECLIBAN"
ONEDRIVE_URL   = "https://socotecgroup-my.sharepoint.com/personal/mohamed_mossad_socotec_com"

@st.cache_resource(ttl=300)
def get_context(site_url: str):
    creds = UserCredential(
        st.secrets["SOCOTEC_EMAIL"],
        st.secrets["SOCOTEC_PASSWORD"]
    )
    return ClientContext(site_url).with_credentials(creds)

@st.cache_data(ttl=300, show_spinner=False)
def read_excel_from_sharepoint(file_path: str, sheet_name=0, site_url=SHAREPOINT_URL) -> pd.DataFrame:
    try:
        ctx = get_context(site_url)
        buf = io.BytesIO()
        ctx.web.get_file_by_server_relative_url(file_path).download(buf).execute_query()
        buf.seek(0)
        content = buf.read()
        if len(content) == 0:
            st.error(f"File downloaded but empty — likely auth failed silently: {file_path}")
            return pd.DataFrame()
        buf.seek(0)
        return pd.read_excel(buf, sheet_name=sheet_name)
    except Exception as e:
        err = str(e)
        if "401" in err or "Unauthorized" in err or "sign in" in err.lower():
            st.error(f"❌ Authentication failed — check SOCOTEC_EMAIL and SOCOTEC_PASSWORD in secrets")
        elif "404" in err or "not found" in err.lower():
            st.error(f"❌ File not found: {file_path} — check the path")
        elif "list index out of range" in err:
            st.error(f"❌ Auth failed silently (wrong password or MFA required): {file_path}")
        else:
            st.error(f"❌ {file_path}: {err}")
        return pd.DataFrame()

@st.cache_data(ttl=300, show_spinner=False)
def read_attendance_today() -> dict:
    import datetime
    today = datetime.date.today().strftime("%Y-%m-%d")
    all_sheets = read_excel_from_sharepoint(
        "/KSA Shared Documents/Socotec-Riyadh/Daily Attendance Log.xlsx",
        sheet_name=None
    )
    checked_in = exceptions = team_members = pd.DataFrame()
    if isinstance(all_sheets, dict):
        if "Daily_Attendance_Log" in all_sheets:
            df = all_sheets["Daily_Attendance_Log"]
            if "Date" in df.columns:
                df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.strftime("%Y-%m-%d")
                checked_in = df[df["Date"] == today]
        if "Daily_Exceptions" in all_sheets:
            df = all_sheets["Daily_Exceptions"]
            if "Date" in df.columns:
                df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.strftime("%Y-%m-%d")
                exceptions = df[df["Date"] == today]
        if "Team_Members" in all_sheets:
            team_members = all_sheets["Team_Members"]
    return {"checked_in": checked_in, "exceptions": exceptions,
            "team_members": team_members, "today": today}

@st.cache_data(ttl=600, show_spinner=False)
def read_rd6_data() -> pd.DataFrame:
    return read_excel_from_sharepoint(
        "/Documents/متطلبات الزيارة النهائية.xlsx",
        site_url=ONEDRIVE_URL
    )

@st.cache_data(ttl=300, show_spinner=False)
def read_claims_data() -> pd.DataFrame:
    return read_excel_from_sharepoint(
        "/KSA Shared Documents/Socotec-Riyadh/Socotec_Claims_2026.xlsx",
        sheet_name="ClaimsTable"
    )

def write_claim_to_sharepoint(claim: dict) -> bool:
    try:
        ctx = get_context(SHAREPOINT_URL)
        file_path = "/KSA Shared Documents/Socotec-Riyadh/Socotec_Claims_2026.xlsx"
        buf = io.BytesIO()
        ctx.web.get_file_by_server_relative_url(file_path).download(buf).execute_query()
        buf.seek(0)
        df = pd.read_excel(buf, sheet_name="ClaimsTable")
        df = pd.concat([df, pd.DataFrame([claim])], ignore_index=True)
        out = io.BytesIO()
        with pd.ExcelWriter(out, engine="openpyxl") as w:
            df.to_excel(w, sheet_name="ClaimsTable", index=False)
        out.seek(0)
        ctx.web.get_file_by_server_relative_url(file_path).save_binary_stream(out).execute_query()
        return True
    except Exception as e:
        st.error(f"Could not save claim: {e}")
        return False

@st.cache_data(ttl=600, show_spinner=False)
def read_saturday_ot() -> pd.DataFrame:
    return read_excel_from_sharepoint(
        "/KSA Shared Documents/نموذج زيارات يوم السبت (Over-Time Saturday Visits).xlsx"
    )
