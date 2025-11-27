"""
Quick test using cached credentials from our successful test.py
"""
from scraper import SeatGeekScraper
import json
from datetime import datetime

# Create initial cache with working credentials
initial_cache = {
    "headers": {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://seatgeek.com/cities/atlanta",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
        "Cookie": "sg_l=en-US; sg_c=USD; sixpack_client_id=51731516-3b7c-4b94-9eb6-8f94b6f1a31f; SeatGeekEntrance=category=entrance%3Bdt=%3Bap=%3BadId=; sg_user_session_id=01d3e679-28d6-4283-8af8-34eb29eec99b; lastRskxRun=1764258299714; rskxRunCookie=0; rCookie=ezgy28169ppc61bfy1cincmihlu8g3; _ketch_consent_v1_=eyJhbmFseXRpY3MiOnsic3RhdHVzIjoiZ3JhbnRlZCIsImNhbm9uaWNhbFB1cnBvc2VzIjpbImFuYWx5dGljcyJdfSwiZXNzZW50aWFsX3B1cnBvc2VzIjp7InN0YXR1cyI6ImdyYW50ZWQiLCJjYW5vbmljYWxQdXJwb3NlcyI6WyJlc3NlbnRpYWxfc2VydmljZXMiXX0sInBlcnNvbmFsaXNhdGlvbiI6eyJzdGF0dXMiOiJncmFudGVkIiwiY2Fub25pY2FsUHVycG9zZXMiOlsicGVyc29uYWxpemF0aW9uIiwiYmVoYXZpb3JhbF9hZHZlcnRpc2luZyJdfSwicHJvZHVjdF9lbmhhbmNlbWVudCI6eyJzdGF0dXMiOiJncmFudGVkIiwiY2Fub25pY2FsUHVycG9zZXMiOlsicHJvZF9lbmhhbmNlbWVudCJdfX0%3D; _gcl_au=1.1.471349969.1764258301; _swb_consent_=eyJjb2xsZWN0ZWRBdCI6MTc2NDI1ODMwMCwiY29udGV4dCI6eyJjb25maWd1cmF0aW9uSWQiOiJjMlZoZEdkbFpXc3ZjMlZoZEdkbFpXdGZZMjl0TDNCeWIyUjFZM1RwYjI0dlpHVm1ZWFZzZEM5bGJpOHhOall6TWpjeU9UWTIiLCJzb3VyY2UiOiJsZWdhbEJhc2lzRGVmYXVsdCJ9LCJlbnZpcm9ubWVudENvZGUiOiJwcm9kdWN0aW9uIiwiaWRlbnRpdGllcyI6eyJzZWF0Z2Vla19zaXhwYWNrX2lkX2Jhc2VkX2lkZW50aXR5IjoiNTE3MzE1MTYtM2I3Yy00Yjk0LTllYjYtOGY5NGI2ZjFhMzFmIn0sImp1cmlzZGljdGlvbkNvZGUiOiJkZWZhdWx0IiwicHJvcGVydHlDb2RlIjoic2VhdGdlZWtfY29tIiwicHVycG9zZXMiOnsiYW5hbHl0aWNzIjp7ImFsbG93ZWQiOiJ0cnVlIiwibGVnYWxCYXNpc0NvZGUiOiJkaXNjbG9zdXJlIn0sImVzc2VudGlhbF9wdXJwb3NlcyI6eyJhbGxvd2VkIjoidHJ1ZSIsImxlZ2FsQmFzaXNDb2RlIjoiZGlzY2xvc3VyZSJ9LCJwZXJzb25hbGlzYXRpb24iOnsiYWxsb3dlZCI6InRydWUiLCJsZWdhbEJhc2lzQ29kZSI6ImRpc2Nsb3N1cmUifSwicHJvZHVjdF9lbmhhbmNlbWVudCI6eyJhbGxvd2VkIjoidHJ1ZSIsImxlZ2FsQmFzaXNDb2RlIjoiZGlzY2xvc3VyZSJ9fX0%3D; IR_gbd=seatgeek.com; IR_20501=1764258303726%7C4523102%7C1764258303726%7C%7C; IR_PI=09b0a0ec-cba8-11f0-9754-89749fe80ca8%7C1764258303726; _fbp=fb.1.1764258304099.68919474269862590; _uetsid=0a9990f0cba811f0ab92171e472a1ee4; _uetvid=0a9986d0cba811f0a10ab73f272c79e0; forterToken=f5e3a9f4d71741089882cf36e88a78ea_1764258295119__UDF43-m4_23ck_; sg-exit-intent-modal=true; _ga=GA1.1.607221899.1764258304; _ga_MYEXKXLE1H=GS2.1.s1764258374$o1$g1$t1764258469$j59$l0$h619088937; _ga_44M3TK17XS=GS2.1.s1764258303$o1$g1$t1764258469$j59$l0$h202159575; FPID=FPID2.2.NXGPCDKRGBpA3b9L7V7JPKZ5K9MU2RqtE69ALNq%2FbpI%3D.1764258304; FPAU=1.1.471349969.1764258301; _tt_enable_cookie=1; _ttp=01KB2ZZNNMDAM9NEF3WYBZ927H_.tt.1; datadome=oNIPQMqQ6Bkmuw_E4rUxLFcQjOr6IK5TEEryAVZBDO77z3_Ckh3NYt0j0zaZl0jG7EfiRAs7KTMKm~eIl4noqMETrNEmWud9Tmc9QR8zl_tXmlPl6pICissjxuB3SIWm; FPLC=R1zl5pVcmBISYTze53AvyNDT53y5zw1uoNS3Poj8Ug5Cdvf24Y8NR1XBRib919Kv9xVFnOuZFSmnm9i%2BHAiFqmD2Typs%2F%2B4ED2Vazcbrmk4BMXZhS61bv%2BrYZF2AVw%3D%3D; _gtmeec=e30%3D; FPGSID=1.1764258468.1764258468.G-44M3TK17XS.GFLDn0sz5Kot-52AL2W6UQ; ttcsid=1764258469564::LMQvFv-WViUFxYZ2gxu6.1.1764258474210.0; ttcsid_C4TLGV5G6B59DEMSOHN0=1764258469563::AjERyc8CX3CjgegUijyG.1.1764258474210.0; _dd_s=rum=0&expire=1764259399854",
        "x-sg-currency-code": "USD",
        "x-sg-locale": "en-US",
        "Sec-CH-UA": "\"Chromium\";v=\"142\", \"Google Chrome\";v=\"142\", \"Not_A Brand\";v=\"99\"",
        "Sec-CH-UA-Mobile": "?0",
        "Sec-CH-UA-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin"
    },
    "cookies_str": "sg_l=en-US; sg_c=USD; sixpack_client_id=51731516-3b7c-4b94-9eb6-8f94b6f1a31f",
    "cached_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

# Save initial cache
with open("credentials_cache.json", "w") as f:
    json.dump(initial_cache, f, indent=4)

print("✅ Created initial credentials cache")

# Now run the scraper
print("\n" + "="*70)
scraper = SeatGeekScraper(
    city="atlanta",
    lat="33.7650504428",
    lon="-84.4030550874",
    range_mi="27mi"
)

# Test with a single page first
print("\n🧪 Testing with cached credentials...\n")
result = scraper.scrape_events(page=1)

if result:
    print("\n✅ Scraping works! Now getting more pages...")
    events = scraper.scrape_multiple_pages(start_page=1, num_pages=3, delay=2)
    
    if events:
        output_file = f"seatgeek_events_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(events, f, indent=4, ensure_ascii=False)
        
        print(f"\n✅ SUCCESS! Scraped {len(events)} total events")
        print(f"💾 Saved to: {output_file}")
else:
    print("\n⚠️ Cached credentials didn't work, Scrappey will be called on next attempt")
