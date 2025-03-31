import requests
import json
from datetime import datetime, timedelta
import time

def debug_invitation_api():
    """Debug the invitation API by making test requests with different parameters."""
    print("=== Invitation API Debugging Tool ===")
    
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
    
    # Initial test - check API health
    print("\n[Test 1] Checking API health with default request...")
    
    payload = {
        "username": "brolyz",
        "limit": 1,
        "endDate": end_date
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        status_code = response.status_code
        
        print(f"Status code: {status_code}")
        print("Response headers:")
        for key, value in response.headers.items():
            print(f"  {key}: {value}")
        
        try:
            response_json = response.json()
            print("\nResponse body:")
            print(json.dumps(response_json, indent=2))
            
            if 200 <= status_code < 300:
                print("\n✅ API request successful!")
                invitation_link = response_json.get('data', {}).get('invitationLink')
                if invitation_link:
                    print(f"Invitation link: {invitation_link}")
                else:
                    print("❌ No invitation link found in the response data")
            else:
                print("\n❌ API request failed with error status")
                
        except ValueError:
            print("\nNon-JSON response received:")
            print(response.text[:500]) # Print first 500 chars of response
            
    except Exception as e:
        print(f"❌ Exception occurred during request: {e}")
    
    # Test 2 - different date format
    print("\n\n[Test 2] Trying with different date format...")
    alt_end_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
    
    payload = {
        "username": "brolyz",
        "limit": 1,
        "endDate": alt_end_date
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"Status code: {response.status_code}")
        try:
            print(json.dumps(response.json(), indent=2))
        except:
            print(response.text[:500])
    except Exception as e:
        print(f"Exception: {e}")
    
    # Test 3 - Check if token is expired/invalid
    print("\n\n[Test 3] Checking token validity...")
    
    # Test with a basic GET request to the API
    test_url = "https://api.backoffice.brolyz.com/v1/health"
    try:
        response = requests.get(test_url, headers=headers)
        print(f"Health check status code: {response.status_code}")
        try:
            print(json.dumps(response.json(), indent=2))
        except:
            print(response.text[:500])
            
        if 401 <= response.status_code <= 403:
            print("\n❌ Token appears to be expired or invalid")
            print("Solution: You need to update the token in the script")
        elif response.status_code >= 400:
            print("\n❌ API may be unreachable or down")
        else:
            print("\n✅ Token appears to be valid")
            
    except Exception as e:
        print(f"Exception: {e}")
    
    # Recommendations
    print("\n=== Debugging Summary ===")
    print("Based on the test results, possible issues could be:")
    print("1. The authentication token may be expired (common issue)")
    print("2. The API endpoint may have changed or be unavailable")
    print("3. The required request format may have changed")
    print("\nRecommendations:")
    print("- Update the authentication token in the script")
    print("- Check the API documentation for any changes")
    print("- If using a VPN, try disabling it")
    print("- Try running the script from a different network")

if __name__ == "__main__":
    debug_invitation_api() 