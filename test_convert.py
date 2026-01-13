# This script was to test how to convert the files using the markdown package.

import markdown

text = open(r"C:\Users\ryadl\OneDrive - St. George's University Of London\Documents\Obsidian Vault\sample.md")
text_content = (text.read())
print (text_content)

text_content = markdown.markdown(text_content)
print ("\n")
print ("This is the converted text:\n", text_content)

text.close()
