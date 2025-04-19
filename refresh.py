from google_auth_oauthlib.flow import InstalledAppFlow

# Replace with your scopes — YouTube example:
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

# Replace with path to your downloaded client_secret JSON
flow = InstalledAppFlow.from_client_secrets_file(
    "creds.json", SCOPES
)

creds = flow.run_local_server()

print("Access Token:", creds.token)
print("Refresh Token:", creds.refresh_token)
