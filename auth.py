import msal # Needed to speak to Microsoft Auth
import sys

# Import keys from config.py
from config import CLIENT_ID, CLIENT_SECRET

# SCOPES = permissions we are asking for
# Notes.Create = write pages, Notes.Read = check if they exist.
SCOPES = ["Notes.Create", "Notes.Read", "User.Read"]

# 'common' means both work and personal accounts are accepted
AUTHORITY_URL = "https://login.microsoftonline.com/common"

def get_token():
    # Setup
    # ConfidentialClientApplication represents the app holding its ID and Secret ID
    app = msal.ConfidentialClientApplication(
        CLIENT_ID, authority=AUTHORITY_URL, client_credential=CLIENT_SECRET
    )

    # Generate Login URL
    # Builds a special link, showing Microsoft the App ID and Permissions (Scopes)
    auth_url = app.get_authorization_request_url(SCOPES)

    print(f"----------------------------------------------------------------")
    print(f"Please click this URL to login:\n{auth_url}")
    print(f"----------------------------------------------------------------")
    print("\nAfter logging in, you will be redirected to a blank page.")
    # The redirect is where Microsoft sends the 'access code'.
    print("Look at the URL bar. It will look like: http://localhost:8000/callback?code=M.R3...")

    # 3. Get the Code
    # Manually copy-paste the code Microsoft gave us from the browser back to here. 
    auth_code = input("Paste the full 'code' part from the URL here: ")

    # Clean the code if the user pasted the full URL
    if "code=" in auth_code:
        auth_code = auth_code.split("code=")[1].split("&")[0]

    # Exchange Code for Token
    result = app.acquire_token_by_authorization_code(auth_code, scopes=SCOPES)

    if "access_token" in result:
        print("\n SUCCESS! We have a token.")
	# Print a snippet to prove we got it
        print(f"Token: {result['access_token'][:20]}...")
        return result["access_token"]
    else:
        print(f"\n ERROR: {result.get('error_description')}")
        return None

if __name__ == "__main__":
    get_token()
