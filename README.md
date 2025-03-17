# Skatteguru Stock Plan Confirmation Document Download Script for E\*TRADE

This Python script automates the process of downloading confirmation PDFs from E\*TRADE for "Restricted Stock" and "STOCK OPTIONS" plan types.

## What Is the Purpose?

### Why We Created This Script and the Problem It Solves

E\*TRADE users, particularly those managing stock plans like Restricted Stock or Stock Options, often face the daunting task of downloading numerous confirmation PDFs for tax filing purposes. These documents are essential for accurately reporting income, gains, or losses to tax authorities. However, the manual process of retrieving these files from E\*TRADE's web interface presents significant challenges.

#### The Problem
- **Time-Consuming Manual Downloads**: E\*TRADE requires users to download each confirmation PDF individually. For users with dozens, hundreds, or even more transactions, this requires repetitive clicking and waiting—especially since some may have up to 100+ PDFs to retrieve.
- **Risk of Missing Documents**: With such a high volume of files, it's easy to accidentally overlook a single confirmation. Missing even one document could lead to incomplete or incorrect tax filings, potentially triggering penalties, audits, or financial discrepancies.
- **Error-Prone Process**: The repetitive nature of navigating the website, locating each file, and downloading it increases the chance of human error—whether it's downloading the wrong file, losing track of progress, or skipping a step.

#### The Solution
We created this script to automate the entire process, offering a simple yet powerful fix:
- **Bulk Downloading**: The script retrieves and downloads all relevant PDFs in one streamlined operation, slashing the time and effort required from hours to mere minutes.
- **Improved Accuracy**: By systematically capturing every confirmation for "Restricted Stock" and "Stock Options," it eliminates the risk of missing critical documents, ensuring tax filings are complete and correct.
- **Scalability**: Designed to handle large numbers of PDFs effortlessly, the script is perfect for users with extensive transaction histories—whether it's 10 files or 100+.
- **Ease of Use**: Users can simply copy a cURL command from their browser and run the script.

#### Why It Matters
Accurate tax reporting is non-negotiable, and missing a single confirmation can throw off calculations, leading to costly mistakes. This script, and the help at [https://www.skatteguru.se/help-center/etrade-documents](https://www.skatteguru.se/help-center/etrade-documents), empowers E\*TRADE users to save time, reduce stress, and file their taxes with confidence—knowing they have every necessary document in hand.

### Prior Art & Credits
We originally wrote a [JavaScript snippet](https://gist.github.com/isakb/f9652fd4d89e283aafd0c301d7ac3f07) that enabled downloading all PDFs as a .zip file, but after an update to the E\*TRADE website, this stopped working. [@tomasaschan](https://github.com/tomasaschan) shared an approach similar to this script, and we let Grok 3.0 write this python script based on his approach, with a few tweaks.

## Dependencies

To use this script, you'll need the following installed on your system:

- **Python 3.x**: The script requires Python 3. You can download it from [python.org](https://www.python.org) if you don't already have it installed.
- **requests library**: This Python library is used to make HTTP requests. Install it via pip by running:
  ```bash
  pip install requests
  ```

Ensure you have these dependencies set up before proceeding.

## Usage Instructions

Follow these steps to use the script effectively:

### Step 1: Prepare the cURL Command

1. **Log in to E\*TRADE**: Access your E\*TRADE account and navigate to your [Stock Plan Confirmations](https://us.etrade.com/etx/sp/stockplan/#/myAccount/stockPlanConfirmations).
2. **Open Developer Tools**:
   - Press `F12` on your keyboard, or right-click anywhere on the page and select "Inspect" to open the developer tools in your browser.
   - Switch to the "Network" tab to monitor network requests.
3. **Locate the `confirmations.json` Request**:
   - Look for a request named `confirmations.json` in the list of network activity.
   - If it doesn't appear, refresh the page (press `F5`) to trigger the request.
4. **Copy the cURL Command**:
   - Right-click the `confirmations.json` request in the Network tab.
   - Select "Copy" > "Copy as cURL" (or "Copy as cURL (bash)" depending on your browser - we have only tested this in Google Chrome).

### Step 2: Run the Script

1. **Save the Script**:
   - Copy the provided script code into a file named `etrade_download.py` and save it in a convenient location on your computer.
2. **Provide the cURL Command**:
   - Paste the copied cURL command into a text file and save it as `request.txt` in the same directory as `etrade_download.py`.
   - Open a terminal or command prompt, navigate to the script's directory, and run:
     ```bash
     python etrade_download.py < request.txt && rm request.txt
     ```

## How It Works

Here's what the script does behind the scenes:

- **Reads the cURL Command**: It extracts the URL, headers (including authentication cookies), and request data from the cURL command you provide.
- **Updates the Request**: The script modifies the request payload to fetch all confirmations from March 17, 2018, to the current date, covering all plan types initially.
- **Fetches Confirmation Data**: It sends a POST request to E\*TRADE's API to retrieve the `confirmations.json` data.
- **Filters Confirmations**: The script narrows down the results to only include "Restricted Stock" and "STOCK OPTIONS" plan types.
- **Downloads PDFs**: For each relevant confirmation:
  - It constructs a PDF URL using the `encryptedEmployeeId` (eId) and `confirmationId`.
  - Downloads the PDF to a `docs` folder in your script's directory, naming files in the format `YYYY-MM-DD_plan_type_confirmationId.pdf` (e.g., `2023-01-15_restricted_stock_12345678.pdf`).

The script provides feedback throughout the process, letting you know how many confirmations were found and the status of each download.

## Notes

- **Security**: The cURL command contains sensitive authentication details. Remove the `request.txt` file from your computer as soon as you have finished downloading the PDF files (if you use the command `python etrade_download.py < request.txt && rm request.txt`, it will be removed for you).
- **Date Range**: By default, the script fetches confirmations from March 17, 2018, to today. To change this range, edit the `startDate` and `endDate` values in the script (look for the line `data["value"].update(...)`).
- **Output Directory**: PDFs are saved to a `docs` folder, which the script creates automatically if it doesn't exist.

## Troubleshooting

If you encounter issues, here are some common problems and solutions:

- **"Error: Failed to read input"**: Ensure you've provided the cURL command correctly in the file.
- **"Error: Invalid JSON in --data-raw"**: Check that the cURL command was copied accurately. Avoid modifying it manually, and watch out for smart quotes (`"` or `"`) that some text editors might introduce—replace them with standard quotes (`"`).
- **"Failed to fetch confirmations.json (Status: 403)"**: This indicates an authentication issue. Your session may have expired. Log back into E\*TRADE, copy a fresh cURL command, and try again.
- **"Failed to download ... (Status: 404)"**: The PDF URL format might have changed, or the confirmation data is incomplete. Double-check the `confirmations.json` response structure. It is also possible that E\*Trade has updated their website, rendering this script useless.

For additional help, review the script's output messages or refer to the inline comments in the code.

### Disclaimer

**Use at Your Own Risk**: This script is provided "as is" without any warranties or guarantees of any kind. We strive to ensure it works as intended, but we cannot be held responsible for any issues, errors, or consequences that may arise from its use. This includes inaccuracies in downloaded documents, failed downloads, or any impact on your E\*TRADE account.

**E\*TRADE Website Changes**: E\*TRADE may update or modify their website, API, or document retrieval processes at any time without notice. Such changes could affect the script's functionality, and it may stop working or require updates to remain compatible. We are not responsible for maintaining or updating the script in response to these changes.

**No Affiliation**: This script is an independent tool created to assist E\*TRADE users. It is not affiliated with, endorsed by, or supported by E\*TRADE Financial Corporation or any of its affiliates.

**Data Security**: The script may include sensitive information, such as authentication cookies used in commands like cURL. You must handle this data carefully and avoid sharing it with others. We are not liable for any security breaches or unauthorized access that may result from misuse of this information.

**Tax Filing Responsibility**: While this script aims to simplify downloading confirmation PDFs, it is your responsibility to ensure all necessary documents are correctly obtained and used for tax filing. We are not responsible for missing or incorrect documents that could lead to errors in your tax reporting.

By using this script, you acknowledge these terms and agree to use it at your own risk.
