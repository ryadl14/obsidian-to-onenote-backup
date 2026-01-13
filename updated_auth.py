import msal

# Importing client secret isn't neccessary since the security comes from logging in via the browser.
from config import CLIENT_ID

# Sets the scope, allowing us to create and read notes as well as allowing persist long-term access.
SCOPES = ["Notes.Create", "Notes.Read", "User.Read"]
AUTHORITY_URL = "https://login.microsoftonline.com/common"

# Create our app.
app = msal.PublicClientApplication(CLIENT_ID, authority = AUTHORITY_URL)

# Initialise result variable.
result = None

result = app.acquire_token_interactive (scopes=SCOPES, port=80)
if "access_token" in result:
    print(result["access_token"])
else:
    print (result.get("error"))
    print (result.get("error_description"))
