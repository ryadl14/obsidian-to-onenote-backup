import os
import markdown
import requests
import time
from auth import get_token


def migrate_to_onenote (filename, section, token):
    # Get the title
    basename = os.path.basename(filename)
    # rsplit splits from the right, splitting from the 1st ., and selecting the first (0) item, in this case the title and not the file extension
    title = basename.rsplit(".",1)[0]

    print(f"Reading: {title}")

    # Read the file
    try:
	    with open(filename, "r", encoding = "utf-8") as file:
		    text = (file.read())
    except Exception as e:
	    print(f"Error reading file: {e}")
	    return False

    # Convert the file from Markdown to HTML
    # r = raw string
    html_body = markdown.markdown(text)

    # Wrap in full HTML with a title
    final_html = f"""
    <!DOCTYPE html>
    <html>
    <head><title>{title}</title></head>
    <body>{html_body}</body>
    </html>
    """

    # Send to OneNote
    endpoint = "https://graph.microsoft.com/v1.0/me/onenote/pages"
    headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "text/html"
    }

    # Handles spaces in section names automatically
    parameters = {"sectionName": section}

    response = requests.post(endpoint, headers=headers, params=parameters, data=final_html.encode('utf-8'))

    print(f"Status Code: {response.status_code}")

    if response.status_code == 201:
        print ("SUCCESS")
        return True
    else:
        print (f"ERROR (Status Code: {response.status_code}): {response.text}")
        return False

# Checks that the file hasn't already been uploaded.
def duplicate_check(title, token):
    endpoint = "https://graph.microsoft.com/v1.0/me/onenote/pages"
    headers = {"Authorization": "Bearer " + token}
    params = {"$filter":f"title eq '{title}'"}
    response = requests.get(endpoint, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        # Return True if "value" list has items, False if it's empty.
        return len(data['value']) > 0

    return False

def main():
    # Get the token and login.
    token = get_token()
    if not token:
        print ("ERROR: No token found!")
        exit ()
    else:
        print ("SUCCESS: Token acquired!")

    # Configuration
    vault_path = r"C:/Users/ryadl/OneDrive - St. George's University Of London/Documents/Obsidian Vault" 
    count = 0
    STOP_AFTER = 150 # Safety brake

    # Walking the folder with the .md files.
    for (root,dirs,files) in os.walk(vault_path):
        if ".trash" in root:
            continue

        folder_name = os.path.basename(root)

        for filename in files:
            if filename.endswith(".md"):
                # Gets the full path for filename
                full_path = os.path.join(root, filename)

                # Gets the title again.
                basename = os.path.basename(filename)
                title = basename.rsplit(".",1)[0]

                # Checks if the file has already been uploaded.
                if duplicate_check (title, token):
                    print (f"Skipping {title}. Already uploaded!")
                    continue

                success = migrate_to_onenote(full_path, folder_name, token)

                if success:
                    print(f"{filename} in Section: {folder_name} has been transferred!") 
                    count += 1
                    if count >= STOP_AFTER:
                        print ("\n Paused, verify on OneNote.")
                        return

if __name__ == "__main__":
    main()
