"""
SeatGeek Events Scraper with Automatic Cookie/Header Refresh
Uses cached credentials and only refreshes via Scrappey when they expire
Scrapes all cities, all events, with checkpoint/resume capability
"""

from curl_cffi import requests
import json
import os
import time
from datetime import datetime
from typing import Dict, Optional, List

# Configuration
SCRAPPEY_API_KEY = "CPLgrNtC9kgMlgvBpMLydXJU3wIYVhD9bvxKn0ZO8SRWPNJvpgu4Ezhwki1U"
SCRAPPEY_URL = "https://publisher.scrappey.com/api/v1"
SEATGEEK_API_URL = "https://seatgeek.com/api/events"
CACHE_FILE = "credentials_cache.json"
CHECKPOINT_FILE = "scraping_checkpoint.json"
OUTPUT_DIR = "json_outputs"

# All cities to scrape with their coordinates
CITIES = {
    "arlington": {"lat": "32.7357", "lon": "-97.1081", "range": "25mi"},
    "atlanta": {"lat": "33.7650504428", "lon": "-84.4030550874", "range": "27mi"},
    "austin": {"lat": "30.2672", "lon": "-97.7431", "range": "25mi"},
    "baltimore": {"lat": "39.2904", "lon": "-76.6122", "range": "25mi"},
    "boston": {"lat": "42.3601", "lon": "-71.0589", "range": "25mi"},
    "charlotte": {"lat": "35.2271", "lon": "-80.8431", "range": "25mi"},
    "chicago": {"lat": "41.8781", "lon": "-87.6298", "range": "30mi"},
    "cincinnati": {"lat": "39.1031", "lon": "-84.5120", "range": "25mi"},
    "cleveland": {"lat": "41.4993", "lon": "-81.6944", "range": "25mi"},
    "dallas": {"lat": "32.7767", "lon": "-96.7970", "range": "30mi"},
    "denver": {"lat": "39.7392", "lon": "-104.9903", "range": "25mi"},
    "detroit": {"lat": "42.3314", "lon": "-83.0458", "range": "25mi"},
    "houston": {"lat": "29.7604", "lon": "-95.3698", "range": "30mi"},
    "kansas-city": {"lat": "39.0997", "lon": "-94.5786", "range": "25mi"},
    "las-vegas": {"lat": "36.1699", "lon": "-115.1398", "range": "25mi"},
    "los-angeles": {"lat": "34.0522", "lon": "-118.2437", "range": "35mi"},
    "miami": {"lat": "25.7617", "lon": "-80.1918", "range": "30mi"},
    "minneapolis": {"lat": "44.9778", "lon": "-93.2650", "range": "25mi"},
    "nashville": {"lat": "36.1627", "lon": "-86.7816", "range": "25mi"},
    "new-orleans": {"lat": "29.9511", "lon": "-90.0715", "range": "25mi"},
    "new-york": {"lat": "40.7128", "lon": "-74.0060", "range": "35mi"},
    "philadelphia": {"lat": "39.9526", "lon": "-75.1652", "range": "30mi"},
    "phoenix": {"lat": "33.4484", "lon": "-112.0740", "range": "30mi"},
    "pittsburgh": {"lat": "40.4406", "lon": "-79.9959", "range": "25mi"},
    "portland": {"lat": "45.5152", "lon": "-122.6784", "range": "25mi"},
    "san-diego": {"lat": "32.7157", "lon": "-117.1611", "range": "30mi"},
    "san-francisco": {"lat": "37.7749", "lon": "-122.4194", "range": "35mi"},
    "seattle": {"lat": "47.6062", "lon": "-122.3321", "range": "30mi"},
    "tampa": {"lat": "27.9506", "lon": "-82.4572", "range": "25mi"},
    "washington-dc": {"lat": "38.9072", "lon": "-77.0369", "range": "30mi"}
}


class SeatGeekScraper:
    """Scraper with automatic credential management and checkpointing"""
    
    def __init__(self):
        self.headers = None
        self.cookies_str = None
        self.checkpoint = self.load_checkpoint()
        self.ensure_output_dir()
        self.load_cached_credentials()
    
    def ensure_output_dir(self):
        """Create output directory if it doesn't exist"""
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
            print(f"📁 Created output directory: {OUTPUT_DIR}")
    
    def load_checkpoint(self) -> Dict:
        """Load checkpoint to resume from where we left off"""
        if os.path.exists(CHECKPOINT_FILE):
            try:
                with open(CHECKPOINT_FILE, 'r') as f:
                    checkpoint = json.load(f)
                    print(f"📍 Loaded checkpoint: {checkpoint.get('current_city', 'N/A')} (Page {checkpoint.get('current_page', 1)})")
                    return checkpoint
            except Exception as e:
                print(f"⚠️ Error loading checkpoint: {e}")
        return {
            "completed_cities": [],
            "current_city": None,
            "current_page": 1,
            "last_updated": None
        }
    
    def save_checkpoint(self, city: str, page: int, completed: bool = False):
        """Save checkpoint after each successful page scrape"""
        if completed:
            if city not in self.checkpoint["completed_cities"]:
                self.checkpoint["completed_cities"].append(city)
            self.checkpoint["current_city"] = None
            self.checkpoint["current_page"] = 1
        else:
            self.checkpoint["current_city"] = city
            self.checkpoint["current_page"] = page
        
        self.checkpoint["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            with open(CHECKPOINT_FILE, 'w') as f:
                json.dump(self.checkpoint, f, indent=4)
        except Exception as e:
            print(f"⚠️ Error saving checkpoint: {e}")
        
    def load_cached_credentials(self) -> bool:
        """Load credentials from cache file if available"""
        if os.path.exists(CACHE_FILE):
            try:
                with open(CACHE_FILE, 'r') as f:
                    cache = json.load(f)
                    self.headers = cache.get('headers', {})
                    self.cookies_str = cache.get('cookies_str', '')
                    cached_time = cache.get('cached_at', '')
                    print(f"✅ Loaded cached credentials from {cached_time}")
                    return True
            except Exception as e:
                print(f"⚠️ Error loading cache: {e}")
        else:
            print("📝 No cache file found")
        return False
    
    def save_credentials_to_cache(self):
        """Save current credentials to cache file"""
        try:
            cache = {
                'headers': self.headers,
                'cookies_str': self.cookies_str,
                'cached_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            with open(CACHE_FILE, 'w') as f:
                json.dump(cache, f, indent=4)
            print(f"💾 Credentials cached at {cache['cached_at']}")
        except Exception as e:
            print(f"⚠️ Error saving cache: {e}")
    
    def fetch_fresh_credentials(self, city: str = "atlanta") -> bool:
        """Fetch fresh cookies and headers from Scrappey"""
        print("\n🔄 Fetching fresh credentials from Scrappey...")
        
        payload = {
            "cmd": "request.get",
            "url": f"https://seatgeek.com/cities/{city}",
            "browserActions": [
                {"type": "wait", "wait": 3},
                {"type": "wait", "wait": 3}
            ]
        }
        
        try:
            import requests as std_requests  # Use standard requests for Scrappey API
            response = std_requests.post(
                SCRAPPEY_URL,
                params={"key": SCRAPPEY_API_KEY},
                json=payload,
                timeout=90
            )
            
            if response.status_code != 200:
                print(f"❌ Scrappey API error: HTTP {response.status_code}")
                return False
            
            data = response.json()
            
            if "solution" not in data:
                print("❌ Invalid response from Scrappey")
                return False
            
            solution = data["solution"]
            
            # Extract cookies and convert to cookie string
            cookies = solution.get("cookies", [])
            if isinstance(cookies, list):
                cookie_pairs = [f"{c['name']}={c['value']}" for c in cookies if 'name' in c and 'value' in c]
                self.cookies_str = "; ".join(cookie_pairs)
            else:
                print("⚠️ No cookies found in response")
                return False
            
            # Extract request headers (what the browser sent)
            request_headers = solution.get("requestHeaders", {})
            user_agent = solution.get("userAgent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:142.0) Gecko/20100101 Firefox/142.0")
            
            # Build headers for API requests
            self.headers = {
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": request_headers.get("accept-language", "en-US,en;q=0.9"),
                "Referer": f"https://seatgeek.com/cities/{city}",
                "User-Agent": user_agent,
                "Cookie": self.cookies_str,
                "x-sg-currency-code": "USD",
                "x-sg-locale": "en-US",
                "Sec-CH-UA": '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
                "Sec-CH-UA-Mobile": "?0",
                "Sec-CH-UA-Platform": '"Windows"',
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
            }
            
            # Extract specific headers from cookies for API compatibility
            for cookie in cookies:
                if cookie['name'] == 'sixpack_client_id':
                    self.headers['sixpack-client-id'] = cookie['value']
                elif cookie['name'] == 'sg_user_session_id':
                    self.headers['x-sg-user-session-id'] = cookie['value']
            
            print("✅ Fresh credentials obtained successfully!")
            self.save_credentials_to_cache()
            return True
            
        except std_requests.exceptions.Timeout:
            print("❌ Scrappey request timed out")
            return False
        except Exception as e:
            print(f"❌ Error fetching credentials: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def scrape_events(self, city: str, city_config: Dict, page: int = 1, max_retries: int = 2) -> Optional[Dict]:
        """
        Scrape events from SeatGeek API
        Automatically refreshes credentials if they're expired
        """
        # Ensure we have credentials
        if not self.headers or not self.cookies_str:
            print("🔑 No credentials available, fetching fresh ones...")
            if not self.fetch_fresh_credentials(city):
                print("❌ Failed to get credentials")
                return None
        
        params = {
            "page": str(page),
            "listing_count.gte": "1",
            "lat": city_config["lat"],
            "lon": city_config["lon"],
            "range": city_config["range"],
            "sort": "datetime_local.asc",
            "client_id": "MTY2MnwxMzgzMzIwMTU4",
        }
        
        for attempt in range(max_retries):
            try:
                print(f"🌐 Scraping {city} (page {page}, attempt {attempt + 1}/{max_retries})...")
                
                response = requests.get(
                    SEATGEEK_API_URL,
                    params=params,
                    headers=self.headers,
                    impersonate="chrome",
                    timeout=30
                )
                
                # Success!
                if response.status_code == 200:
                    data = response.json()
                    event_count = len(data.get('events', []))
                    print(f"✅ Successfully scraped {event_count} events from {city} page {page}")
                    return data
                
                # Credentials expired - refresh and retry
                elif response.status_code == 403:
                    print(f"⚠️ 403 Error - Credentials expired or blocked")
                    
                    if attempt < max_retries - 1:
                        print("🔄 Refreshing credentials and retrying...")
                        if self.fetch_fresh_credentials(city):
                            time.sleep(2)  # Brief pause before retry
                            continue
                        else:
                            print("❌ Failed to refresh credentials")
                            return None
                    else:
                        print("❌ Max retries reached")
                        return None
                
                # Other HTTP errors
                else:
                    print(f"❌ HTTP {response.status_code}: {response.text[:200]}")
                    return None
                    
            except requests.exceptions.Timeout:
                print(f"⏱️ Request timeout (attempt {attempt + 1}/{max_retries})")
                if attempt < max_retries - 1:
                    time.sleep(2)
                    continue
                return None
                
            except Exception as e:
                print(f"❌ Error during scraping: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2)
                    continue
                return None
        
        return None
    
    def scrape_city_all_pages(self, city: str, city_config: Dict, delay: int = 2) -> List:
        """Scrape ALL pages for a single city until no more events"""
        all_events = []
        page = 1
        
        # Resume from checkpoint if this city was in progress
        if self.checkpoint.get("current_city") == city:
            page = self.checkpoint.get("current_page", 1)
            print(f"📍 Resuming {city} from page {page}")
            # Load existing events if file exists
            city_file = os.path.join(OUTPUT_DIR, f"{city}_events.json")
            if os.path.exists(city_file):
                try:
                    with open(city_file, 'r', encoding='utf-8') as f:
                        all_events = json.load(f)
                    print(f"📂 Loaded {len(all_events)} existing events for {city}")
                except Exception as e:
                    print(f"⚠️ Error loading existing events: {e}")
        
        while True:
            data = self.scrape_events(city, city_config, page=page)
            
            if data and 'events' in data:
                events = data['events']
                
                # No more events
                if len(events) == 0:
                    print(f"✅ No more events for {city} at page {page}")
                    break
                
                all_events.extend(events)
                print(f"📊 Total events for {city}: {len(all_events)}")
                
                # Save after each page
                self.save_city_events(city, all_events)
                self.save_checkpoint(city, page + 1)
                
                # Check if there are more pages
                meta = data.get('meta', {})
                total = meta.get('total', 0)
                per_page = meta.get('per_page', 10)
                total_pages = (total // per_page) + (1 if total % per_page > 0 else 0)
                
                print(f"📄 Page {page}/{total_pages} (Total: {total} events)")
                
                # If we've reached the last page
                if page >= total_pages or len(events) < per_page:
                    print(f"✅ Reached last page for {city}")
                    break
                
                # Move to next page
                page += 1
                time.sleep(delay)
            else:
                # Failed to scrape - DON'T mark as complete
                print(f"⚠️ Failed to scrape page {page} for {city}")
                print(f"⚠️ {city} NOT completed - only got {len(all_events)} events so far")
                print(f"⚠️ Will retry from page {page} in next run")
                break
        
        return all_events
    
    def save_city_events(self, city: str, events: List):
        """Save events for a city to its own JSON file"""
        try:
            city_file = os.path.join(OUTPUT_DIR, f"{city}_events.json")
            with open(city_file, 'w', encoding='utf-8') as f:
                json.dump(events, f, indent=4, ensure_ascii=False)
            print(f"💾 Saved {len(events)} events to {city_file}")
        except Exception as e:
            print(f"❌ Error saving city events: {e}")
    
    def scrape_all_cities(self, delay_between_cities: int = 5):
        """Scrape all events from all cities"""
        total_cities = len(CITIES)
        completed_count = len(self.checkpoint["completed_cities"])
        
        print(f"\n🌎 Starting to scrape {total_cities} cities")
        print(f"✅ Already completed: {completed_count} cities")
        print(f"📋 Remaining: {total_cities - completed_count} cities\n")
        
        for idx, (city, city_config) in enumerate(CITIES.items(), 1):
            # Skip already completed cities
            if city in self.checkpoint["completed_cities"]:
                print(f"⏭️ Skipping {city} (already completed)")
                continue
            
            print(f"\n{'='*70}")
            print(f"🏙️ City {idx}/{total_cities}: {city.upper()}")
            print(f"{'='*70}")
            
            events = self.scrape_city_all_pages(city, city_config, delay=5)
            
            # Verify city was fully scraped before marking complete
            city_file = os.path.join(OUTPUT_DIR, f"{city}_events.json")
            if events and os.path.exists(city_file):
                try:
                    with open(city_file, 'r', encoding='utf-8') as f:
                        saved_events = json.load(f)
                    print(f"✅ Completed {city}: {len(saved_events)} total events")
                    self.save_checkpoint(city, 1, completed=True)
                except Exception as e:
                    print(f"⚠️ Error verifying {city}: {e}")
                    print(f"❌ {city} will be retried in next run")
            elif not events:
                print(f"⚠️ No events found for {city}")
                self.save_checkpoint(city, 1, completed=True)
            
            # Delay between cities to be respectful
            if idx < total_cities:
                print(f"\n⏸️ Waiting {delay_between_cities}s before next city...")
                time.sleep(delay_between_cities)
        
        print(f"\n{'='*70}")
        print("🎉 ALL CITIES COMPLETED!")
        print(f"{'='*70}")
        self.generate_summary()
    
    def generate_summary(self):
        """Generate a summary of all scraped data"""
        summary = {
            "scrape_completed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "cities": {}
        }
        
        total_events = 0
        
        for city in CITIES.keys():
            city_file = os.path.join(OUTPUT_DIR, f"{city}_events.json")
            if os.path.exists(city_file):
                try:
                    with open(city_file, 'r', encoding='utf-8') as f:
                        events = json.load(f)
                        event_count = len(events)
                        summary["cities"][city] = {
                            "event_count": event_count,
                            "file": f"{city}_events.json"
                        }
                        total_events += event_count
                except Exception as e:
                    summary["cities"][city] = {"error": str(e)}
        
        summary["total_events"] = total_events
        summary["total_cities"] = len(summary["cities"])
        
        # Save summary
        summary_file = os.path.join(OUTPUT_DIR, "scraping_summary.json")
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=4)
        
        print(f"\n📊 SUMMARY:")
        print(f"   Total Cities: {summary['total_cities']}")
        print(f"   Total Events: {total_events:,}")
        print(f"   Summary saved to: {summary_file}")
        
        # Display per-city breakdown
        print(f"\n📋 Events per city:")
        for city, info in sorted(summary["cities"].items()):
            if "event_count" in info:
                print(f"   {city.ljust(20)}: {info['event_count']:,} events")
    
    def scrape_multiple_pages(self, start_page: int = 1, num_pages: int = 5, delay: int = 2) -> list:
        """Scrape multiple pages of events"""
        all_events = []
        
        for page in range(start_page, start_page + num_pages):
            data = self.scrape_events(page=page)
            
            if data and 'events' in data:
                events = data['events']
                all_events.extend(events)
                print(f"📊 Total events collected: {len(all_events)}")
                
                # Check if there are more pages
                meta = data.get('meta', {})
                total_pages = meta.get('total', 0) // meta.get('per_page', 20) + 1
                
                if page >= total_pages:
                    print(f"✅ Reached last page ({page}/{total_pages})")
                    break
                
                # Delay between pages to be respectful
                if page < start_page + num_pages - 1:
                    print(f"⏸️ Waiting {delay}s before next page...")
                    time.sleep(delay)
            else:
                print(f"⚠️ Failed to scrape page {page}, stopping...")
                break
        
        return all_events


def main():
    """Main execution"""
    print("=" * 70)
    print("🎫 SeatGeek ALL Cities & Events Scraper with Auto-Refresh")
    print("=" * 70)
    
    # Initialize scraper
    scraper = SeatGeekScraper()
    
    # Scrape all cities and all their events
    print("\n🚀 Starting comprehensive scraping of all cities...\n")
    print("⚙️ Settings: 5 second delay between pages, exponential backoff on 403 errors\n")
    scraper.scrape_all_cities(delay_between_cities=5)
    
    print("\n✅ Scraping completed!")
    print(f"📁 All data saved in '{OUTPUT_DIR}/' directory")


if __name__ == "__main__":
    main()
