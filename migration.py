import os
import markdown
import requests
import time
import re
import json
from updated_auth import result


def migrate_to_onenote (filename, section, token, assets_path):
# ========================================================================================
# Reads a Markdown file, converts it to HTML (handling images), and uploads it to OneNote.
# ========================================================================================

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

# ------------ IMAGE HANDLING --------------- #
    #Using RegEx, extracts the embedded image filename.
    images = re.findall(r"!\[\[(.*?)\]\]", text)
    # Creates an empty dictionary
    image_map = {}

    # Creates the path to the specific image we need.
    for image_name in images:
        full_image_path = os.path.join(assets_path, image_name)
        # Check the path exists
        if os.path.exists(full_image_path) is False:
            print (f"ERROR: IMAGE NOT FOUND: {image_name}")
            continue
        else:
            image_map.update({image_name:full_image_path})

    # Replacing Obsidian embedded links with OneNote image tags
    for image_name in image_map:
        # Defining the old pattern to be removed.
        obsidian_link = f"![[{image_name}]]"
        # Defining the new tag for OneNote
        onenote_tag = f'<img src="name:{image_name}" alt="{image_name}" />'
        # Swaps all Obsidian links with our new OneNote tags
        text = text.replace(obsidian_link, onenote_tag)

# ----------------- IMAGE HANDLING END --------------------- #

    # Convert the file from Markdown to HTML
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
    "Authorization": "Bearer " + token
    }

    # Handles spaces in section names automatically
    parameters = {"sectionName": section}

    # Creates a dictionary with of the HTML.
    files = {
        "Presentation": (None, final_html, "text/html")
        }
    # Every time it finds an image, add it to the files dictionary.
    for name, path in image_map.items():
        files.update({name: (None, open(path, "rb"), "image/png") })

    response = requests.post(endpoint, headers=headers, params=parameters, files=files)

    print(f"Status Code: {response.status_code}")

    if response.status_code == 201:
        print ("SUCCESS")
        return True
    else:
        print (f"ERROR (Status Code: {response.status_code}): {response.text}")
        return False

def main():
    # Get the token and login.
    token = result['access_token']
    if not token:
        print ("ERROR: No token found!")
        exit ()
    else:
        print ("SUCCESS: Token acquired!")

    # Configuration
    vault_path = r"C:/Users/ryadl/OneDrive - St. George's University Of London/Documents/Obsidian Vault"
    assets_path = r"C:/Users/ryadl/OneDrive - St. George's University Of London/Documents/Obsidian Vault/Assets"
    count = 0
    STOP_AFTER = 150 # Safety brake

    # Initialises history.
    try:
        with open('modification_memory', 'r') as f:
            history = json.load(f)
    except:
        print ("File not found.")
        history = {}

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

                # Checks when it was last uploaded.
                currenttime = os.path.getmtime(full_path)

                # Checks if it has been recently modified against the known history.
                if filename in history and history[filename] == currenttime:
                    print ("Skipping, no changes since last upload.")
                    continue

                success = migrate_to_onenote(full_path, folder_name, token, assets_path)

                if success:
                    print(f"{filename} in Section: {folder_name} has been transferred!")
                    history.update({filename:currenttime})
                    with open ("modification_memory", "w") as f:
                        json.dump(history, f)
                    count += 1
                    if count >= STOP_AFTER:
                        print ("\n Paused, verify on OneNote.")
                        return

if __name__ == "__main__":
    main()
