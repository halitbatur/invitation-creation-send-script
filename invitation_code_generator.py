import requests
import json
from datetime import datetime, timedelta
import time
import csv

def read_emails_from_csv():
    """Read emails from waitlist.csv file."""
    emails = []
    try:
        with open('waitlist.csv', 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                if row['email']:  # Only add non-empty emails
                    emails.append(row['email'])
        return emails
    except Exception as e:
        print(f"Error reading waitlist.csv: {e}")
        return []

def read_failed_emails():
    """Read emails from invitation_links.json that have null links."""
    try:
        with open('invitation_links.json', 'r') as file:
            data = json.load(file)
            # Filter for entries where link is None
            failed_entries = [entry for entry in data if entry.get("link") is None]
            return failed_entries
    except Exception as e:
        print(f"Error reading invitation_links.json: {e}")
        return []

# Function to generate invitation link for an email
def generate_invitation_link(email):
    # Calculate end date (1 month from now)
    end_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    
    # API endpoint
    url = "https://api.backoffice.brolyz.com/v1/invitation"
    
    # Headers
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "authorization": "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6ImE5ZGRjYTc2YzEyMzMyNmI5ZTJlODJkOGFjNDg0MWU1MzMyMmI3NmEiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiSGFsaXQgRnVhdCBCYXR1ciIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQ2c4b2NMcGZ0aGpmNXg1WW10cDhHZFB3VUNGOWJmNVhkWWpnODVVcGJuaGVqR3Vfajd6NUE9czk2LWMiLCJ0d29GYWN0b3JWZXJpZmllZCI6dHJ1ZSwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL2Jyb2x5ei1iYWNrb2ZmaWNlIiwiYXVkIjoiYnJvbHl6LWJhY2tvZmZpY2UiLCJhdXRoX3RpbWUiOjE3NDM0MDcwOTEsInVzZXJfaWQiOiJZU3BEZUJseXc3Y210Q1lQYlRNZjdqdEQ3aDMyIiwic3ViIjoiWVNwRGVCbHl3N2NtdENZUGJUTWY3anREN2gzMiIsImlhdCI6MTc0MzUxMDc3MywiZXhwIjoxNzQzNTE0MzczLCJlbWFpbCI6ImhhbGl0LmJhdHVyQGNtbGV0ZWFtLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7Imdvb2dsZS5jb20iOlsiMTA3ODU0NTc1NjY0MzY0NTA1MjE2Il0sImVtYWlsIjpbImhhbGl0LmJhdHVyQGNtbGV0ZWFtLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6Imdvb2dsZS5jb20ifX0.APYXzdCCdVqNC1orFCGCN9F5eKXJdwS0HMjjJlTmQaYeCgT0PK0hJaPZCF8cxXmRrF0d6WjtaNamfupyIeSkuXBJ0H1KPGRdpLBdhvnd1p3jBbe7B6oOLwUBNkDuZXZGuu884DgbuP43o4C29Cwu0gyOYUF2C_7-RfAfNsMPvLTUuGLXurCfheodD0CxyKyhxvkuvMJIFvXNsjfq7Tx0Y5QeUndZ_uOHWPM6bVG9ly2Rs7YysPhsKNqUjXkNbwVFO2O_AWJu5TtgOfaI_LN3cnB27CFwmPSo_zKV5qgS0wkH577F5S5iuTQiDJZmYVSVZsV8DVl820ZZYKdejI7-XQ",
        "content-type": "application/json",
        "priority": "u=1, i",
        "sec-ch-ua": "\"Not:A-Brand\";v=\"24\", \"Chromium\";v=\"134\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "x-languagecode": "en-US"
    }
    
    # Request body
    payload = {
        "username": "brolyz",
        "limit": 1,
        "endDate": end_date
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        
        try:
            response_data = response.json()
        except:
            print(f"Error: Could not parse JSON response for {email}")
            return {"email": email, "link": None}
            
        # Check for success status
        response.raise_for_status()
        
        # Extract the invitation link from the response
        invitation_link = response_data.get('url')
        
        if not invitation_link:
            print(f"Warning: No invitation link found in response for {email}")
            
        return {
            "email": email,
            "link": invitation_link
        }
    except requests.exceptions.RequestException as e:
        print(f"Error generating invitation link for {email}: {e}")
        
        # Print status code if available
        if 'response' in locals():
            print(f"Status code: {response.status_code}")
        
        return {
            "email": email,
            "link": None
        }

def main():
    # Read failed emails from invitation_links.json
    print("Reading failed emails from invitation_links.json...")
    failed_entries = read_failed_emails()
    
    if not failed_entries:
        print("No failed emails found in invitation_links.json. All emails have valid links.")
        return
    
    print(f"Found {len(failed_entries)} emails with failed link generation.")
    
    # Load existing results
    try:
        with open('invitation_links.json', 'r') as file:
            existing_results = json.load(file)
    except Exception as e:
        print(f"Error reading existing invitation_links.json: {e}")
        existing_results = []
    
    # Create a dictionary of existing results for easy lookup
    existing_dict = {entry["email"]: entry for entry in existing_results}
    
    # Generate invitation links for failed emails
    for i, entry in enumerate(failed_entries, 1):
        email = entry["email"]
        print(f"[{i}/{len(failed_entries)}] Retrying invitation link generation for {email}...")
        result = generate_invitation_link(email)
        
        # Update the existing result
        if email in existing_dict:
            existing_dict[email] = result
    
    # Convert back to list and save
    updated_results = list(existing_dict.values())
    with open("invitation_links.json", "w") as f:
        json.dump(updated_results, f, indent=2)
    
    # Print summary of retries
    success_count = sum(1 for r in updated_results if r.get("link") and r["email"] in [e["email"] for e in failed_entries])
    print(f"\nRetry Results: {success_count} successful, {len(failed_entries) - success_count} failed")
    
    # Print only the retried emails
    for entry in failed_entries:
        email = entry["email"]
        result = existing_dict.get(email, {"email": email, "link": None})
        if result.get("link"):
            print(f"SUCCESS: {email}")
            print(f"Link: {result['link']}")
        else:
            print(f"FAILED: {email}")
        print("-" * 50)
    
    print(f"Updated results saved to invitation_links.json")

if __name__ == "__main__":
    main()
