import xml.etree.ElementTree as ET
import requests

file_name = "YOUR XLIFF FILE"
# Open XLIFF file and parse its contents
tree = ET.parse(file_name)
root = tree.getroot()

# Remove any namespace prefix from all tags
for elem in root.iter():
    elem.tag = elem.tag.split('}', 1)[-1]

# Set the API endpoint URL
url = "https://api.mymemory.translated.net/get"

# Find all <target> tags with state = "needs-translation"
for target in root.iter("target"):
    print(target.attrib.get("state"))
    if target.attrib.get("state") == "needs-translation":
        # Get the text to be translated
        text = target.text
        print(text)
        # Set the parameters for the API request
        params = {"q": text, "langpair": "en|vi"}
        # Make the API request
        response = requests.get(url, params=params)
        # Parse the JSON response
        data = response.json()
        # Get the translated text from the response
        translated_text = data["responseData"]["translatedText"]
        # Replace the text within the <target> tag with the translated text
        target.text = translated_text
        print(target.text)
        # Update the state to "translated"
        target.attrib["state"] = "translated"

# Write the updated XLIFF file contents to disk
tree.write(file_name, encoding="utf-8", xml_declaration=True)
