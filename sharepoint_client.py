"""
SharePoint connector using Office365-REST-Python-Client.
Authenticates with SOCOTEC credentials — no Azure AD app needed.
Credentials stored in Streamlit secrets, never in code.
"""
import streamlit as st
import pandas as pd
import io
from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext

SHAREPOINT_URL = "https://socotecgroup.sharepoint.com/sites/SOCOTECLIBAN"
ONEDRIVE_URL   = "https://socotecgroup-my.sharepoint.com/personal/mohamed_mossad_socotec_com"

@st.cache_resource(ttl=300)  # reconnect every 5 minutes
def get_context(site_url: str):
    """Get authenticated SharePoint context."""
    creds = UserCredential(
        st.secrets["SOCOTEC_EMAIL"],
        st.secrets["SOCOTEC_PASSWORD"]
    )
    ctx = ClientContext(site_url).with_credentials(creds)
    return ctx

@st.cache_data(ttl=300, show_spinner=False)  # cache 5 min
def read_excel_from_sharepoint(file_path: str, sheet_name=0, site_url=SHAREPOINT_URL) -> pd.DataFrame:
    """
    Read an Excel file from SharePoint into a DataFrame.
    file_path: relative path e.g. '/KSA Shared Documents/Socotec-Riyadh/Daily Attendance Log.xlsx'
    """
    try:
        ctx = get_context(site_url)
        response = ctx.web.get_file_by_server_relative_url(file_path).download().execute_query()
        df = pd.read_excel(io.BytesIO(response.content), sheet_name=sheet_name)
        return df
    except Exception as e:
        st.error(f"Could not read {file_path}: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=300, show_spinner=False)
def read_attendance_today() -> dict:
    """
    Read today's attendance from Daily_Attendance_Log + Daily_Exceptions.
    Returns {'checked_in': df, 'exceptions': df}
    """
    import datetime
    today = datetime.date.today().strftime("%Y-%m-%d")

    # Read all sheets
    all_sheets = read_excel_from_sharepoint(
        "/KSA Shared Documents/Socotec-Riyadh/Daily Attendance Log.xlsx",
        sheet_name=None
    )

    checked_in  = pd.DataFrame()
    exceptions  = pd.DataFrame()
    team_members = pd.DataFrame()

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

    return {
        "checked_in":   checked_in,
        "exceptions":   exceptions,
        "team_members": team_members,
        "today":        today
    }

@st.cache_data(ttl=600, show_spinner=False)
def read_rd6_data() -> pd.DataFrame:
    """Read RD6 final visit requirements from personal OneDrive."""
    return read_excel_from_sharepoint(
        "/personal/mohamed_mossad_socotec_com/Documents/متطلبات الزيارة النهائية.xlsx",
        site_url=ONEDRIVE_URL
    )

@st.cache_data(ttl=300, show_spinner=False)
def read_claims_data() -> pd.DataFrame:
    """Read claims tracker Excel."""
    return read_excel_from_sharepoint(
        "/KSA Shared Documents/Socotec-Riyadh/Socotec_Claims_2026.xlsx",
        sheet_name="ClaimsTable"
    )

def write_claim_to_sharepoint(claim: dict) -> bool:
    """Append a new claim row to the Claims Excel."""
    try:
        ctx = get_context(SHAREPOINT_URL)
        file_path = "/KSA Shared Documents/Socotec-Riyadh/Socotec_Claims_2026.xlsx"

        # Download current file
        response = ctx.web.get_file_by_server_relative_url(file_path).download().execute_query()
        df = pd.read_excel(io.BytesIO(response.content), sheet_name="ClaimsTable")

        # Append new row
        new_row = pd.DataFrame([claim])
        df = pd.concat([df, new_row], ignore_index=True)

        # Upload back
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name="ClaimsTable", index=False)
        output.seek(0)

        ctx.web.get_file_by_server_relative_url(file_path).save_binary_stream(output).execute_query()
        return True
    except Exception as e:
        st.error(f"Could not save claim: {e}")
        return False

@st.cache_data(ttl=600, show_spinner=False)
def read_saturday_ot() -> pd.DataFrame:
    """Read Saturday OT submissions."""
    return read_excel_from_sharepoint(
        "/KSA Shared Documents/نموذج زيارات يوم السبت (Over-Time Saturday Visits).xlsx"
    )
