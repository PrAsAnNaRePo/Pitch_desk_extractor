import requests
import json

url = "http://0.0.0.0:8000/v2/extract"

dynamic_key = [
    {
        "name": "companyName",
        "description": "Name of the insurance company",
        "type": "string"
    },
    {
        "name": "customerName",
        "description": "Full name of the insured customer",
        "type": "string"
    },
    {
        "name": "customerID",
        "description": "Unique identifier for the customer",
        "type": "string"
    },
    {
        "name": "policyNumber",
        "description": "Unique policy number assigned to the customer",
        "type": "string"
    },
    {
        "name": "premiumPayable",
        "description": "Total premium amount to be paid for the policy",
        "type": "number"
    },
    {
        "name": "carNumber",
        "description": "Vehicle registration number",
        "type": "string"
    },
    {
        "name": "model",
        "description": "Car model name",
        "type": "string"
    },
    {
        "name": "colour",
        "description": "Color of the insured vehicle",
        "type": "string"
    },
    {
        "name": "totalValue",
        "description": "Total insured value of the vehicle",
        "type": "number"
    },
    {
        "name": "chassisNumber",
        "description": "Chassis number of the insured vehicle",
        "type": "string"
    },
    {
        "name": "dateOfIssue",
        "description": "Date when the insurance policy was issued",
        "type": "date"
    },
    {
        "name": "timeOfIssue",
        "description": "Time when the insurance policy was issued",
        "type": "time"
    },
    {
        "name": "dateOfExpiry",
        "description": "Expiration date of the insurance policy",
        "type": "date"
    },
    {
        "name": "timeOfExpiry",
        "description": "Expiration time of the insurance policy",
        "type": "time"
    }
]

# Open the file in binary mode
with open("airbnb-original-deck-2008.pdf", "rb") as file:
    files = {"file": file}
    params = {"doc_type": "pitch desk", "dynamic_keys": json.dumps(dynamic_key)}  # Pass doc_type as a query parameter
    response = requests.get(url, files=files, params=params)

print(response.json())

# save the json response to a file
# Open the file in binary mode
with open("response.json", "w") as f:
    json.dump(response.json(), f, indent=4)