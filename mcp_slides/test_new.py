from dotenv import load_dotenv
import os

load_dotenv()

from google_auth_oauthlib.flow import InstalledAppFlow

'''SCOPES = ["https://www.googleapis.com/auth/presentations"]

flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
creds = flow.run_local_server(port=0)

print("Access Token:", creds.token)
print("Refresh Token:", creds.refresh_token)
print("Client ID:", creds.client_id)
print("Client Secret:", creds.client_secret)'''

import os
from auth import get_slides_service  # Use the new token-based auth module

def create_presentation(service, title: str) -> str:
    """Create a new presentation with the given title."""
    presentation = service.presentations().create(body={"title": title}).execute()
    presentation_id = presentation.get("presentationId")
    print("✅ Presentation created successfully!")
    print("Presentation ID:", presentation_id)
    print("Shareable link:", f"https://docs.google.com/presentation/d/{presentation_id}/edit")
    return presentation_id

# --------- Run standalone test ---------
if __name__ == "__main__":
    try:
        slides_service = get_slides_service()  # Auth and refresh handled inside auth.py
        new_title = "New Presentation from auth.py"
        presentation_id = create_presentation(slides_service, new_title)

        # Verify by fetching the presentation title
        presentation = slides_service.presentations().get(presentationId=presentation_id).execute()
        print("Verified Title:", presentation.get("title"))

    except Exception as e:
        print(f"❌ Error: {e}")