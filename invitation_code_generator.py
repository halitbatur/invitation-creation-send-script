import requests
import json
from datetime import datetime, timedelta
import time

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
        "authorization": "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6ImE5ZGRjYTc2YzEyMzMyNmI5ZTJlODJkOGFjNDg0MWU1MzMyMmI3NmEiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiSGFsaXQgRnVhdCBCYXR1ciIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQ2c4b2NMcGZ0aGpmNXg1WW10cDhHZFB3VUNGOWJmNVhkWWpnODVVcGJuaGVqR3Vfajd6NUE9czk2LWMiLCJ0d29GYWN0b3JWZXJpZmllZCI6dHJ1ZSwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL2Jyb2x5ei1iYWNrb2ZmaWNlIiwiYXVkIjoiYnJvbHl6LWJhY2tvZmZpY2UiLCJhdXRoX3RpbWUiOjE3NDM0MDcwOTEsInVzZXJfaWQiOiJZU3BEZUJseXc3Y210Q1lQYlRNZjdqdEQ3aDMyIiwic3ViIjoiWVNwRGVCbHl3N2NtdENZUGJUTWY3anREN2gzMiIsImlhdCI6MTc0MzQ1MzMyMCwiZXhwIjoxNzQzNDU2OTIwLCJlbWFpbCI6ImhhbGl0LmJhdHVyQGNtbGV0ZWFtLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7Imdvb2dsZS5jb20iOlsiMTA3ODU0NTc1NjY0MzY0NTA1MjE2Il0sImVtYWlsIjpbImhhbGl0LmJhdHVyQGNtbGV0ZWFtLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6Imdvb2dsZS5jb20ifX0.KfeHqYEFJh3xZ4aDo84gXENNPIfOy9t4NEZID7il5OVeQRtrXtKzdMgfJ_ThK2CIpkgsnfAlM1rgGDGU_z2ESICWR9isB4ft1karhMTn3Piu6S7YQsuRVTF3bDtkUlv_2cSSphPL0BS5Sn6d1jLPdyC_EP65wsS0s3RX_D9zOrwle5-9-XWe1QH79v9pWwnWnCxC3AHVE0-D0rr2z_nLO30qzLr5WpLLFKKNSMSYPKYnryEKMoWG44jlMcVNbfNPSFzY3SaM459IF4YwfxxxxNQ_3EuawiMO_s6uSu00xhQtvV9ml_Z3aWwVdxhs3jnL_MPGmSP8XqFczgozSoyBOQ",
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
        
        # Try to get the response content regardless of status code
        response_content = {}
        try:
            response_content = response.json()
        except:
            response_content = {"text": response.text}
            
        # Now check for success status
        response.raise_for_status()
        
        # Extract the invitation link from the response
        invitation_link = response_content.get('url')
        
        if not invitation_link:
            print(f"Warning: No invitation link found in response for {email}")
            print(f"Response content: {json.dumps(response_content, indent=2)}")
            
        return {
            "email": email,
            "link": invitation_link,
            "response": response_content
        }
    except requests.exceptions.RequestException as e:
        error_message = f"Error generating invitation link for {email}: {e}"
        print(error_message)
        
        # Try to get the response content for more details
        response_content = {}
        try:
            if 'response' in locals():
                try:
                    response_content = response.json()
                except:
                    response_content = {"status_code": response.status_code, "text": response.text}
        except:
            pass
            
        print(f"Error details for {email}:")
        print(f"Status code: {getattr(response, 'status_code', 'N/A')}")
        print(f"Response content: {json.dumps(response_content, indent=2)}")
        
        return {
            "email": email,
            "link": None,
            "error": str(e),
            "response": response_content
        }

def main():
    # List of emails to generate invitation links for
    # You can replace this with your actual email list or read from a file
    emails = [
        "pizimeka@polkaroad.net",
        "halit.batur@cmleteam.com",
        "ebubekir.karanfil@cmleteam.com",
        "hasan.kilic@cmleteam.com"
    ]
    
    # Generate invitation links for each email
    results = []
    for i, email in enumerate(emails, 1):
        print(f"[{i}/{len(emails)}] Generating invitation link for {email}...")
        result = generate_invitation_link(email)
        results.append(result)
        # Add a small delay to avoid overwhelming the API
        if i < len(emails):  # Don't sleep after the last email
            time.sleep(1)
    
    # Print results
    success_count = sum(1 for r in results if r.get("link"))
    print(f"\nResults: {success_count} successful, {len(emails) - success_count} failed")
    
    for result in results:
        if result.get("link"):
            print(f"SUCCESS: {result['email']}")
            print(f"Link: {result['link']}")
        else:
            print(f"FAILED: {result['email']}")
            print(f"Error: {result.get('error', 'Unknown error')}")
        print("-" * 50)
    
    # Save results to a file with full details
    with open("invitation_links_full.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"Full results saved to invitation_links_full.json")
    
    # Save a simplified version with just email and link
    simplified_results = [{"email": r["email"], "link": r["link"]} for r in results]
    with open("invitation_links.json", "w") as f:
        json.dump(simplified_results, f, indent=2)
    print(f"Simplified results saved to invitation_links.json")

if __name__ == "__main__":
    main()
