# Obsidian to OneNote Migration Tool

A Python-based tool which allows you to synchronize an Obsidian Vault with Microsoft OneNote. Converts Markdown files to HTML, manages embedded images, and uses last modified metadata to only upload new or updated files.

## Features

* **Folder Structure:** Recursively walks through the Vault, creating OneNote sections based on the folder names.
* **Markdown to HTML:** Converts Obsidian-flavored Markdown into OneNote-compatible HTML.
* **Smart Sync:** Maintains a local JSON history (`modification_memory`) to track file modification times. It automatically skips files that haven't changed since the last successful upload.
* **Image Support:** Detects local image embeds (e.g., `![[image.png]]`), finds them in your Assets folder, and embeds them directly into the OneNote page using multipart requests.
* **Autosave:** Updates the history file immediately after every successful upload to prevent data loss.

## Prerequisites

* **Python 3.x**
* **Microsoft Azure App Registration** (Client ID required)
* **Obsidian Vault** (although any Markdown software would work!)

### Required Python Libraries
Install the dependencies using pip:
```bash
pip install requests markdown msal
```

## How to Run:

* Ensure you have a config.py file containing your CLIENT_ID from the Microsoft Azure Portal.
```py
# In this general format
CLIENT_ID = "XXXXX-XXXX-XXXXX-XXXXX-XXXXXXXXX"
```
* Open migration.py and update the following variables in the main() function to match your local file system:
```python
# Path to your Obsidian Vault root
vault_path = r"C:/Users/ryadl/OneDrive.../Obsidian Vault"

# Path to your Assets/Attachments folder
assets_path = r"C:/Users/ryadl/OneDrive.../Obsidian Vault/Assets"
```
N.B. The way my Obsidian is set up, all images are stored in the Assets folder, and within the .md files, there are image links to the folder. Your set up may be different.
2. Run the migration script
```py
python migration.py
```
* A browser popup will open where you will be prompted to sign into your Microsoft Account.

## How it's Made:
You always hear computer scientists say the best way to learn is to start building something that makes your life easier. For me, this was it. I love using Obsidian for university notes primarily due to the aesthetic and the easy image embedding. However, after my laptop made a noise that **terrified** me, I realised that if my laptop broke, I would lose all of my notes. Obsidian does offer a paid subscription for syncing, but learning how to do it myself would help me develop my skills and save money.

* My first step was using the Markdown package to convert from Markdown to HTML, which is OneNote's language of choice.
* Then I registered an app on Microsoft Azure to allow communicating with the Microsoft Graph API, using the Notes.Create, Notes.Read, and User.Read scopes.
. I also implemented my `updated_auth.py` script which used Microsoft Authentication Library (MSAL) for easy OAuth2 authentication. 
* Next was images. I used Regex to find the embedded image tags, and bundled them into a multipart HTTP request so they appear exactly in line with the text.
* Finally I created a modification memory system using JSON. By comparing the "Date modified" of the files against a dictionary, the script will skip all files that did not change since the last upload, saving time and resources.

## Lessons Learned:
In this independent project, I learned how to:
* Further develop my Python and Bash skills.
* Take my first steps into using JSON, Azure, MSAL, and API requests.
* Use `os.walk` to navigate and traverse across directories.
* Familiarise myself with HTML and Regex.
