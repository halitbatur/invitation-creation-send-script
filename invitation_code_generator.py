import requests
import json
from datetime import datetime, timedelta
import time
import pandas as pd
import os

def read_emails_from_xlsx():
    """Read emails from XLSX file."""
    try:
        # Read the XLSX file without using the first row as header
        df = pd.read_excel('waitlist.xlsx', header=None)
        
        # Get the first column (index 0) and convert to list
        emails = df[0].dropna().tolist()  # dropna() removes any null values
        
        print(f"Successfully read {len(emails)} emails from XLSX file")
        return emails
    except Exception as e:
        print(f"Error reading waitlist.xlsx: {e}")
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

def load_existing_results():
    """Load existing results from invitation_links.json if it exists."""
    try:
        if os.path.exists('invitation_links.json'):
            with open('invitation_links.json', 'r') as file:
                data = json.load(file)
                print(f"Loaded {len(data)} existing entries from invitation_links.json")
                return data
        return []
    except Exception as e:
        print(f"Error loading invitation_links.json: {e}")
        return []

def save_result(results):
    """Save results to invitation_links.json."""
    try:
        with open("invitation_links.json", "w") as f:
            json.dump(results, f, indent=2)
        print("Results saved to invitation_links.json")
    except Exception as e:
        print(f"Error saving results: {e}")

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
        "authorization": "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjcxMTE1MjM1YTZjNjE0NTRlZmRlZGM0NWE3N2U0MzUxMzY3ZWViZTAiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiSGFsaXQgRnVhdCBCYXR1ciIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQ2c4b2NMcGZ0aGpmNXg1WW10cDhHZFB3VUNGOWJmNVhkWWpnODVVcGJuaGVqR3Vfajd6NUE9czk2LWMiLCJ0d29GYWN0b3JWZXJpZmllZCI6dHJ1ZSwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL2Jyb2x5ei1iYWNrb2ZmaWNlIiwiYXVkIjoiYnJvbHl6LWJhY2tvZmZpY2UiLCJhdXRoX3RpbWUiOjE3NDM0MDcwOTEsInVzZXJfaWQiOiJZU3BEZUJseXc3Y210Q1lQYlRNZjdqdEQ3aDMyIiwic3ViIjoiWVNwRGVCbHl3N2NtdENZUGJUTWY3anREN2gzMiIsImlhdCI6MTc0NDIyMDQ3MCwiZXhwIjoxNzQ0MjI0MDcwLCJlbWFpbCI6ImhhbGl0LmJhdHVyQGNtbGV0ZWFtLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7Imdvb2dsZS5jb20iOlsiMTA3ODU0NTc1NjY0MzY0NTA1MjE2Il0sImVtYWlsIjpbImhhbGl0LmJhdHVyQGNtbGV0ZWFtLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6Imdvb2dsZS5jb20ifX0.PcYhdrF8i8O2GgBhVJ5_EpA4rBQ8rvrOlLN2TeAfISDMOA5XokzJkmohK5OjEm4_CmSJY14uCY5yAVKzeDzohFphohofumYB-ahcZa5-Cw3hbnOfC8QzeYh3osRu83ZM3ojI9S6tOn3A-KwBhOoHAkizxsCAnejGD5K12N0C9fN-Q7jl8U4QzT_dO97PwXYTaY1bwiUleDS-ZJljO66s-EIm6kxYlx3sst8qiOIp35KQE-ehEBO49TatXImbTys8I4odDs19JKWihbyUYrvUZE-KVgQdDA2649fVXYRkZLyDP6r1ARpBOabHjCMU66WPJcOp97qQLyoADLfihctWFw",
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
    # Read emails from XLSX file
    print("Reading emails from waitlist.xlsx...")
    all_emails = read_emails_from_xlsx()
    
    if not all_emails:
        print("No emails found in waitlist.xlsx. Please check the file exists and contains valid email addresses.")
        return
    
    # Load existing results if any
    existing_results = load_existing_results()
    
    # Create a dictionary of existing results for easy lookup
    processed_emails = {entry["email"] for entry in existing_results}
    
    # Filter out already processed emails
    emails_to_process = [email for email in all_emails if email not in processed_emails]
    
    if not emails_to_process:
        print("All emails have already been processed!")
        return
    
    print(f"Found {len(all_emails)} total emails. {len(processed_emails)} already processed. {len(emails_to_process)} left to process.")
    
    # Generate invitation links for each email
    for i, email in enumerate(emails_to_process, 1):
        print(f"[{i}/{len(emails_to_process)}] Generating invitation link for {email}...")
        result = generate_invitation_link(email)
        
        # Add to existing results
        existing_results.append(result)
        
        # Save after each successful generation
        save_result(existing_results)
        
        # Show status
        if result.get("link"):
            print(f"SUCCESS: {result['email']}")
            print(f"Link: {result['link']}")
        else:
            print(f"FAILED: {result['email']}")
        print("-" * 50)
        
        # Add a small delay to avoid overwhelming the API
        if i < len(emails_to_process):  # Don't sleep after the last email
            time.sleep(1)
    
    # Print final summary
    success_count = sum(1 for r in existing_results if r.get("link"))
    print(f"\nFinal Results: {success_count} successful, {len(all_emails) - success_count} failed")
    print(f"All results saved to invitation_links.json")

if __name__ == "__main__":
    main()
