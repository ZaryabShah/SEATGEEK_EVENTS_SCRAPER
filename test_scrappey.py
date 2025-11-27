import requests
import json

# Scrappey API configuration
SCRAPPEY_API_KEY = "CPLgrNtC9kgMlgvBpMLydXJU3wIYVhD9bvxKn0ZO8SRWPNJvpgu4Ezhwki1U"
SCRAPPEY_URL = "https://publisher.scrappey.com/api/v1"

def get_fresh_headers_and_cookies():
    """
    Use Scrappey to load SeatGeek and extract headers and cookies
    """
    print("🔄 Fetching fresh headers and cookies from Scrappey...")
    
    payload = {
        "cmd": "request.get",
        "url": "https://seatgeek.com/cities/atlanta",
        "browserActions": [
            {
                "type": "wait",
                "wait": 3
            },
            {
                "type": "wait",
                "wait": 3
            }
        ]
    }
    
    try:
        response = requests.post(
            SCRAPPEY_URL,
            params={"key": SCRAPPEY_API_KEY},
            json=payload,
            timeout=60
        )
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            # Save full response for inspection
            with open("scrappey_response.json", "w") as f:
                json.dump(data, f, indent=4)
            print("✅ Full response saved to scrappey_response.json")
            
            # Extract and display relevant information
            if "solution" in data:
                solution = data["solution"]
                
                print("\n" + "="*60)
                print("📋 RESPONSE HEADERS:")
                print("="*60)
                if "responseHeaders" in solution:
                    for key, value in solution["responseHeaders"].items():
                        print(f"{key}: {value}")
                
                print("\n" + "="*60)
                print("🍪 COOKIES:")
                print("="*60)
                if "cookies" in solution:
                    cookies = solution["cookies"]
                    if isinstance(cookies, list):
                        for cookie in cookies:
                            print(f"{cookie.get('name', 'N/A')}: {cookie.get('value', 'N/A')}")
                    elif isinstance(cookies, dict):
                        for key, value in cookies.items():
                            print(f"{key}: {value}")
                    else:
                        print(f"Cookies: {cookies}")
                
                print("\n" + "="*60)
                print("🌐 REQUEST HEADERS (sent by browser):")
                print("="*60)
                if "requestHeaders" in solution:
                    for key, value in solution["requestHeaders"].items():
                        print(f"{key}: {value}")
                
                # Check if we have the data we need
                has_cookies = "cookies" in solution and solution["cookies"]
                has_headers = "requestHeaders" in solution or "responseHeaders" in solution
                
                if has_cookies and has_headers:
                    print("\n" + "="*60)
                    print("✅ SUCCESS: We have both cookies and headers!")
                    print("="*60)
                    return True
                else:
                    print("\n" + "="*60)
                    print("⚠️ WARNING: Missing some data")
                    print(f"Has cookies: {has_cookies}")
                    print(f"Has headers: {has_headers}")
                    print("="*60)
                    return False
            else:
                print("\n❌ No 'solution' key in response")
                print(f"Response keys: {list(data.keys())}")
                return False
        else:
            print(f"❌ Error: HTTP {response.status_code}")
            print(f"Response: {response.text[:500]}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out after 60 seconds")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Testing Scrappey API for SeatGeek headers and cookies extraction\n")
    success = get_fresh_headers_and_cookies()
    
    if success:
        print("\n✅ Test PASSED - We can proceed with the automated scraper!")
    else:
        print("\n❌ Test FAILED - Need to investigate the API response")
