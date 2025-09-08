from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle, os

# YouTube API scope (read-only)
SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]

def get_authenticated_service():
    creds = None
    
    # Check if token already exists
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    # If no valid creds, log in again
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
            creds = flow.run_local_server(port=0)  # login via browser
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build("youtube", "v3", credentials=creds)

if __name__ == "__main__":
    youtube = get_authenticated_service()
    request = youtube.channels().list(part="statistics", mine=True)
    response = request.execute()
    print(response)
