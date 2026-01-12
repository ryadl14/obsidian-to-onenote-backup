import requests
import markdown
import os
from auth import get_token

# Get the token
token = get_token()
if not token:
	print ("ERROR: No token found!")
	exit ()
else:
	print ("SUCCESS: Token acquired!")

# Convert the file from Markdown to HTML
# r = raw string
path = r"C:\Users\ryadl\OneDrive - St. George's University Of London\Documents\Obsidian Vault\sample.md"
with open(path, "r") as file:
	text = (file.read())

html_body = markdown.markdown(text)

# Extract the filename for the title
basename = os.path.basename(path)
print (basename)

#rsplit splits from the right, splitting from the 1st ., and selecting the fir>title = (basename.rsplit(".",1)[0])
print ("Title is :", title)

current_dir_name = 

# Wrap in full HTML with a title
final_html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
</head>
<body>
    {html_body}
</body>
</html>
"""

# Send to OneNote
endpoint = "https://graph.microsoft.com/v1.0/me/onenote/pages?sectionName=Practice"
headers = {
	"Authorization": "Bearer " + token,
	"Content-Type": "text/html"
}

response = requests.post(endpoint, headers=headers, data=html_content)

print(f"Status Code: {response.status_code}")
print(response.text)
