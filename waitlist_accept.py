import json
import requests
import time
import sys

def accept_waitlist_user(email, invitation_link):
    """Call the waitlist accept endpoint for a user."""
    url = "http://localhost:8080/v1/waitlist/accept"
    
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    payload = {
        "email": email,
        "invitationLink": invitation_link
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
        
        return {
            "email": email,
            "status": "success",
            "response": response_content
        }
    except requests.exceptions.RequestException as e:
        error_message = f"Error accepting waitlist user {email}: {e}"
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
            "status": "failed",
            "error": str(e),
            "response": response_content
        }

def main():
    # Load invitation links from JSON file
    try:
        with open("invitation_links.json", "r") as f:
            invitation_data = json.load(f)
    except Exception as e:
        print(f"Error loading invitation_links.json: {e}")
        sys.exit(1)
    
    if not invitation_data:
        print("No invitation links found in the file.")
        sys.exit(1)
    
    # Filter out entries with no link
    valid_entries = [entry for entry in invitation_data if entry.get("link")]
    
    if not valid_entries:
        print("No valid invitation links found in the file.")
        print("Please run the invitation link generator first and make sure it creates valid links.")
        sys.exit(1)
    
    print(f"Found {len(valid_entries)} valid invitation links to process.")
    
    # Process each invitation and accept waitlist users
    results = []
    for i, entry in enumerate(valid_entries, 1):
        email = entry["email"]
        invitation_link = entry["link"]
        
        print(f"[{i}/{len(valid_entries)}] Accepting waitlist user: {email}")
        print(f"Invitation link: {invitation_link}")
        result = accept_waitlist_user(email, invitation_link)
        results.append(result)
        
        # Add a small delay to avoid overwhelming the API
        if i < len(valid_entries):  # Don't sleep after the last email
            time.sleep(0.5)
    
    # Print summary
    success_count = sum(1 for r in results if r["status"] == "success")
    print(f"\nResults: {success_count} successful, {len(valid_entries) - success_count} failed")
    
    for result in results:
        status = "SUCCESS" if result["status"] == "success" else "FAILED"
        print(f"{status}: {result['email']}")
        if result["status"] != "success":
            print(f"  Error: {result.get('error', 'Unknown error')}")
        print("-" * 50)
    
    # Save results to a file
    output_file = "waitlist_accept_results.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    main() 