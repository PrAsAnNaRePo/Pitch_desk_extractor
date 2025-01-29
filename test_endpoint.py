import requests
import json

url = "http://localhost:8000/extract"

# Open the file in binary mode
with open("airbnb-original-deck-2008.pdf", "rb") as file:
    files = {"file": file}
    params = {"doc_type": "pdf"}  # Pass doc_type as a query parameter
    response = requests.get(url, files=files, params=params)

print(response.json())

# save the json response to a file

with open("response.json", "w") as f:
    json.dump(response.json(), f, indent=4)