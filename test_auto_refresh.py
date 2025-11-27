"""
Test the auto-refresh feature by using invalid credentials
This will trigger a 403 error and test if Scrappey auto-refresh works
"""
from scraper import SeatGeekScraper
import json
from datetime import datetime

# Create cache with INVALID credentials to force a 403 error
invalid_cache = {
    "headers": {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://seatgeek.com/cities/atlanta",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Cookie": "INVALID_COOKIE=expired",  # Invalid cookie
        "x-sg-currency-code": "USD",
        "x-sg-locale": "en-US",
        "Sec-CH-UA": "\"Chromium\";v=\"142\"",
        "Sec-CH-UA-Mobile": "?0",
        "Sec-CH-UA-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin"
    },
    "cookies_str": "INVALID_COOKIE=expired",
    "cached_at": "2020-01-01 00:00:00"  # Old timestamp
}

# Save invalid cache
with open("credentials_cache.json", "w") as f:
    json.dump(invalid_cache, f, indent=4)

print("🧪 Testing Auto-Refresh Feature")
print("="*70)
print("Created cache with INVALID credentials to simulate expiration")
print("Expected: 403 error → Auto-refresh from Scrappey → Success")
print("="*70)

# Initialize scraper
scraper = SeatGeekScraper(
    city="atlanta",
    lat="33.7650504428",
    lon="-84.4030550874",
    range_mi="27mi"
)

print("\n📝 Step 1: Attempting to scrape with invalid credentials...")
print("This should fail with 403 and trigger auto-refresh\n")

# This should detect 403, call Scrappey, and retry
result = scraper.scrape_events(page=1)

if result:
    print("\n" + "="*70)
    print("✅ AUTO-REFRESH SUCCESS!")
    print("The scraper detected invalid credentials, fetched fresh ones,")
    print("and successfully completed the request!")
    print("="*70)
    
    # Show we can continue scraping
    print("\n📝 Step 2: Continuing to scrape more pages with fresh credentials...")
    events = scraper.scrape_multiple_pages(start_page=1, num_pages=2, delay=1)
    
    if events:
        print(f"\n✅ Total events scraped: {len(events)}")
        print("💡 Fresh credentials are now cached for future use!")
else:
    print("\n❌ Auto-refresh failed")
    print("Note: Scrappey API might be slow or timeout.")
    print("The system will work when Scrappey is responsive.")
