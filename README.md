# Invitation Link Creator

This repository contains Python scripts to generate invitation links for a list of email addresses by calling the Brolyz invitation API.

## Requirements

- Python 3.6 or higher
- `requests` library

Install required packages:

```bash
pip install requests
```

## Usage

### Step 1: Generate Invitation Links

#### Method 1: Hardcoded Emails

Edit the `emails` list in `invitation_code_generator.py` to include your desired email addresses, then run:

```bash
python invitation_code_generator.py
```

#### Method 2: Emails from File

Create a text file with one email address per line, then run:

```bash
python invitation_code_generator_from_file.py emails.txt
```

If you run without specifying a file, an example `emails.txt` file will be created for you.

### Step 2: Accept Users from Waitlist

After generating invitation links (which creates `invitation_links.json`), you can send acceptance emails by running:

```bash
python waitlist_accept.py
```

This script:
1. Reads the `invitation_links.json` file
2. Makes API calls to the waitlist accept endpoint for each valid entry
3. Saves results to `waitlist_accept_results.json`

**Note**: The waitlist accept endpoint should be running on `http://localhost:8080`. If it's on a different host or port, edit the URL in `waitlist_accept.py`.

## Troubleshooting

If you encounter problems with the API calls, you can run the debugging tool:

```bash
python debug_invitation.py
```

This script:
1. Performs diagnostic tests on the invitation API
2. Shows detailed information about API responses
3. Checks for token validity and common issues
4. Provides recommendations for fixing problems

Common issues:
- The authentication token may be expired (you'll need to update it in the scripts)
- The API endpoint may be down or unreachable
- The API request format may have changed

## Output

The scripts will:

1. Generate invitation links for each email address
2. Print progress during execution
3. Display a summary of results
4. Save results to JSON files

## Notes

- The scripts use small delays between API calls to avoid rate limiting
- Invitation links are valid for 30 days from creation
- The auth token used for API calls might expire over time and need to be updated 