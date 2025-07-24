# auth.py
import os
import csv
import logging
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Define scopes
SCOPES_SLIDES = ["https://www.googleapis.com/auth/presentations"]
SCOPES_DRIVE = ["https://www.googleapis.com/auth/drive"]
ALL_SCOPES = SCOPES_SLIDES + SCOPES_DRIVE

# Token CSV location
TOKEN_CSV_PATH = "tokens.csv"

def save_tokens_to_csv(creds: Credentials, path: str = TOKEN_CSV_PATH):
    """Save credentials to a CSV file."""
    with open(path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=[
            "access_token", "refresh_token", "client_id", "client_secret", "scopes"
        ])
        writer.writeheader()
        writer.writerow({
            "access_token": creds.token,
            "refresh_token": creds.refresh_token,
            "client_id": creds.client_id,
            "client_secret": creds.client_secret,
            "scopes": ",".join(creds.scopes or [])
        })

def load_tokens_from_csv(path: str = TOKEN_CSV_PATH):
    """Load credentials from CSV file."""
    if not os.path.exists(path):
        return None
    with open(path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            return row
    return None

def _build_creds(scopes: list) -> Credentials:
    token_data = load_tokens_from_csv()

    if token_data is None:
        print("🔐 No token found. Starting OAuth flow...")
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", scopes)
        creds = flow.run_local_server(port=0)
        save_tokens_to_csv(creds)
        return creds

    creds = Credentials(
        token=token_data["access_token"],
        refresh_token=token_data["refresh_token"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=token_data["client_id"],
        client_secret=token_data["client_secret"],
        scopes=scopes,
    )

    # If expired or scope mismatch, refresh or redo OAuth
    if creds.refresh_token and (not creds.token or creds.expired):
        creds.refresh(Request())

    # If scope mismatch, redo OAuth
    if not set(scopes).issubset(set(creds.scopes or [])):
        print("🔁 Token scopes insufficient. Re-authenticating...")
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", scopes)
        creds = flow.run_local_server(port=0)
        save_tokens_to_csv(creds)

    return creds

def get_slides_service():
    return build("slides", "v1", credentials=_build_creds(ALL_SCOPES))

def get_drive_service():
    return build("drive", "v3", credentials=_build_creds(ALL_SCOPES))