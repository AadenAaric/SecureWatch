from google.oauth2 import service_account
import google.auth.transport.requests
from django.http import JsonResponse
import os
SCOPES = ["https://www.googleapis.com/auth/firebase.messaging"]

# Load the service account key JSON file
SERVICE_ACCOUNT_FILE = os.path.join(
    os.path.dirname(__file__),
    "watch-3e30d-firebase-adminsdk-6g1su-ff5cdf359b.json"
)   

def get_access_token():
    try:
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        
        request = google.auth.transport.requests.Request()
        credentials.refresh(request)
        
        return credentials.token
    except Exception as e:
        print(f"Error getting access token: {e}")
        return None

