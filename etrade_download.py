"""
E*TRADE confirmation download script

Usage:
    1. Go to E*TRADE and navigate to your stock plan page
    2. Open Developer Tools (F12) and go to Network tab
    3. Find the 'confirmations.json' request
    4. Right-click and select 'Copy as cURL'
    5. Save the cURL command to a file named 'request.txt'
    6. Run: python etrade_download.py < request.txt

Note: The cURL command contains your authentication information, so keep request.txt secure
"""

import json
import os
import shlex
import sys
from datetime import date, datetime

import requests


def parse_curl_command(curl_cmd: str) -> tuple[str, dict[str, str], str]:
    """Parse a cURL command to extract URL, headers, and data."""
    args = shlex.split(curl_cmd)
    url = None
    headers = {}
    data = None
    i = 0
    while i < len(args):
        if args[i] == "curl":
            i += 1
            url = args[i]
        elif args[i] == "-H":
            i += 1
            header = args[i]
            if ": " in header:
                key, value = header.split(": ", 1)
                headers[key] = value
        elif args[i] == "-b":
            i += 1
            cookie_str = args[i]
            if "Cookie" in headers:
                headers["Cookie"] += "; " + cookie_str
            else:
                headers["Cookie"] = cookie_str
        elif args[i] == "--data-raw":
            i += 1
            data = args[i]
        i += 1
    if not url or not data:
        raise ValueError("cURL command missing URL or data")
    return url, headers, data


# Read cURL command from stdin
print("Reading cURL command from stdin...")
try:
    curl_cmd = sys.stdin.read().strip()
    if not curl_cmd:
        raise ValueError("Empty cURL command")

    # Handle common copy-paste issues by replacing smart quotes
    curl_cmd = curl_cmd.replace('"', '"').replace('"', '"')

    # Remove any surrounding quotes if present
    if (curl_cmd.startswith('"') and curl_cmd.endswith('"')) or (curl_cmd.startswith("'") and curl_cmd.endswith("'")):
        curl_cmd = curl_cmd[1:-1]
except Exception as e:
    print(f"Error: Failed to read input: {e}")
    exit(1)

print("Successfully read cURL command")

# Parse the cURL command
try:
    url, headers, data_str = parse_curl_command(curl_cmd)
except ValueError as e:
    print(f"Error: {e}")
    exit(1)

# Parse JSON data and update parameters
try:
    data = json.loads(data_str)
    today = date.today().strftime("%m/%d/%Y")
    data["value"].update(
        {"taxYear": "", "startDate": "3/17/2018", "endDate": today, "planTypeCode": "All", "appType": "STOCKPLAN"}
    )
    data_str = json.dumps(data)
except json.JSONDecodeError:
    print("Error: Invalid JSON in --data-raw. Please check the cURL command.")
    exit(1)
except KeyError:
    print("Error: Missing 'value' key in data payload.")
    exit(1)

# Extract eId
try:
    eId = data["value"]["encryptedEmployeeId"]
except KeyError:
    print("Error: 'encryptedEmployeeId' not found in data payload.")
    exit(1)

# Fetch confirmations.json
print("Fetching confirmations.json...")
response = requests.post(url, headers=headers, data=data_str)
if response.status_code != 200:
    print(f"Error: Failed to fetch confirmations.json (Status: {response.status_code})")
    exit(1)

# Parse response
try:
    confirmations_data = response.json()
    confirmations = confirmations_data["data"]["confirmation"]["confirmations"]
except (json.JSONDecodeError, KeyError):
    print("Error: Unexpected response format from confirmations.json")
    exit(1)

# Filter relevant confirmations
relevant_types = ["Restricted Stock", "STOCK OPTIONS"]
relevant_confirmations = [conf for conf in confirmations if conf.get("planTypeCode") in relevant_types]

# Process confirmations
if not relevant_confirmations:
    print("No relevant confirmations found for 'Restricted Stock' or 'STOCK OPTIONS'.")
else:
    print(f"Found {len(relevant_confirmations)} relevant confirmations.")
    os.makedirs("docs", exist_ok=True)
    success_count = 0
    for i, conf in enumerate(relevant_confirmations, 1):
        # Format date
        date_str = conf.get("confirmationDate", "")
        try:
            date_obj = datetime.strptime(date_str, "%m/%d/%Y")
            formatted_date = date_obj.strftime("%Y-%m-%d")
        except ValueError:
            formatted_date = "unknown_date"
            print(f"Warning: Invalid date '{date_str}' for confirmation {conf.get('confirmationId')}")

        # Build filename and URL
        plan_type = conf["planTypeCode"].lower().replace(" ", "_")
        confirmationId = conf["confirmationId"]
        pdf_url = f"https://us.etrade.com/webapisp/stockplan/pdf/getReleaseConfirmation.pdf?eId={eId}&cId={confirmationId}"
        filename = f"docs/{formatted_date}_{plan_type}_{confirmationId}.pdf"

        # Download PDF
        print(f"Downloading PDF {i}/{len(relevant_confirmations)}: {filename}")
        try:
            pdf_response = requests.get(pdf_url, headers=headers)
            if pdf_response.status_code == 200:
                with open(filename, "wb") as f:
                    f.write(pdf_response.content)
                print(f"Downloaded {filename}")
                success_count += 1
            else:
                print(f"Failed to download {filename} (Status: {pdf_response.status_code})")
        except Exception as e:
            print(f"Error downloading {filename}: {e}")

    print(f"Successfully downloaded {success_count} out of {len(relevant_confirmations)} PDFs.")

print("Download process completed.")
