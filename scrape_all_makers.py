"""
Scrape ALL phone brands from GSMArena makers page and their phones
Dynamically discovers all brands from https://www.gsmarena.com/makers.php3
"""

import os
import sys
import time
from datetime import datetime
from bs4 import BeautifulSoup

# Add function directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(current_dir, 'function'))

from utils.browser_client import HeadlessBrowserClient
from utils.mongodb_client import MongoDBClient
from scrapers.gsmarena import GSMArenaScraper


class AllBrandsScraper:
    """Scrape all brands dynamically from GSMArena."""
    
    MAKERS_URL = "https://www.gsmarena.com/makers.php3"
    
    def __init__(self):
        self.browser = HeadlessBrowserClient()
        # Pass the browser client to GSMArenaScraper to reuse it
        self.scraper = GSMArenaScraper(client=self.browser)
        self.mongo_client = MongoDBClient()
        # Use different collection for all makers scraping
        self.mongo_client.collection = self.mongo_client.db["phone_all_makers"]
        print(f"[MONGODB] Using collection: phone_all_makers")
    
    def get_all_brands(self):
        """
        Get all phone brands from makers page.
        
        Returns:
            List of tuples: [(brand_name, brand_url, device_count), ...]
        """
        print(f"🔍 Fetching all brands from: {self.MAKERS_URL}")
        
        response = self.browser.get(self.MAKERS_URL)
        if not response:
            print("❌ Failed to load makers page")
            return []
        
        soup = BeautifulSoup(response.text, 'lxml')
        
        # Find all brand links in the makers table
        brands = []
        brand_cells = soup.select('table td a')
        
        for link in brand_cells:
            brand_name = link.get_text(strip=True)
            brand_url = link.get('href')
            
            if brand_url and brand_name:
                # Extract device count from the text (e.g., "Samsung 1274 devices")
                parent_text = link.parent.get_text(strip=True)
                device_count = 0
                
                # Try to extract number from text like "Samsung 1274 devices"
                import re
                match = re.search(r'(\d+)\s+devices?', parent_text)
                if match:
                    device_count = int(match.group(1))
                
                full_url = f"https://www.gsmarena.com/{brand_url}"
                brands.append((brand_name, full_url, device_count))
        
        print(f"✅ Found {len(brands)} brands")
        return brands
    
    def get_phones_from_brand(self, brand_url: str, max_results: int = 0):
        """
        Get all phone URLs from a brand page.
        
        Args:
            brand_url: URL of the brand page
            max_results: Maximum number of phones (0 = all)
            
        Returns:
            List of phone URLs
        """
        phone_urls = []
        page_num = 1
        
        while True:
            # Construct page URL
            if page_num == 1:
                page_url = brand_url
            else:
                # GSMArena uses &sName=brandname.php3 format, need to add iPage
                page_url = f"{brand_url}&iPage={page_num}"
            
            print(f"   📄 Page {page_num}: {page_url}")
            
            response = self.browser.get(page_url)
            if not response:
                print(f"   ❌ Failed to load page {page_num}")
                break
            
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Find all phone links
            phone_links = soup.select('div.makers a')
            
            if not phone_links:
                print(f"   ✅ No more phones on page {page_num}")
                break
            
            print(f"   ✅ Found {len(phone_links)} phones on page {page_num}")
            
            for link in phone_links:
                href = link.get('href')
                if href and href.endswith('.php'):
                    full_url = f"https://www.gsmarena.com/{href}"
                    phone_urls.append(full_url)
                    
                    if max_results > 0 and len(phone_urls) >= max_results:
                        print(f"   🎯 Reached max_results limit: {max_results}")
                        return phone_urls
            
            # Check for next page link
            next_page = soup.select_one('a.pages-next')
            if not next_page:
                print(f"   ✅ No next page button found, ending pagination")
                break
            
            page_num += 1
            time.sleep(2)
        
        print(f"   📊 Total phones collected: {len(phone_urls)}")
        return phone_urls
    
    def scrape_brand(self, brand_name: str, brand_url: str, device_count: int, max_results: int = 0):
        """
        Scrape all phones from a brand.
        
        Args:
            brand_name: Name of the brand
            brand_url: URL of the brand page
            device_count: Total devices for this brand
            max_results: Maximum results to scrape (0 = all)
            
        Returns:
            Number of phones saved
        """
        print("\n" + "=" * 70)
        print(f"BRAND: {brand_name} ({device_count} devices)")
        print("=" * 70)
        
        try:
            # Get all phone URLs
            print(f"📱 Fetching phone list...")
            phone_urls = self.get_phones_from_brand(brand_url, max_results)
            
            if not phone_urls:
                print(f"⚠️  No phones found (likely rate limited)")
                print(f"⏰ Cooling down for 120 seconds...")
                time.sleep(120)  # Long cooldown after rate limit
                return 0
            
            print(f"📊 Found {len(phone_urls)} phones to scrape")
            
            saved_count = 0
            
            for idx, url in enumerate(phone_urls, 1):
                print(f"\n[{idx}/{len(phone_urls)}] {url}")
                
                try:
                    phone = self.scraper.scrape_phone(url)
                    
                    if phone:
                        phone_dict = phone.to_dict() if hasattr(phone, 'to_dict') else phone
                        
                        phone_data = {
                            'source': 'GSMArena',
                            **phone_dict
                        }
                        
                        doc_id = self.mongo_client.save_phone(
                            query=brand_name,
                            phone_data=phone_data,
                            method='headless_browser'
                        )
                        
                        if doc_id:
                            saved_count += 1
                    
                except Exception as e:
                    print(f"❌ Error: {e}")
                
                # Delay between phones
                if idx < len(phone_urls):
                    import random
                    time.sleep(random.uniform(3, 6))
            
            print(f"\n✅ {brand_name}: Saved {saved_count}/{len(phone_urls)} phones")
            return saved_count
            
        except Exception as e:
            print(f"❌ Error scraping {brand_name}: {e}")
            return 0


def main():
    print("=" * 70)
    print("ALL BRANDS SCRAPER (Dynamic Discovery)")
    print("Scraping ALL brands from GSMArena makers page")
    print("=" * 70)
    
    # Configuration
    max_results_per_brand = int(os.environ.get('MAX_RESULTS_PER_BRAND', 0))
    delay_between_brands = int(os.environ.get('DELAY_BETWEEN_BRANDS', 10))
    min_devices = int(os.environ.get('MIN_DEVICES', 0))  # Minimum devices to scrape brand
    
    print(f"\n[CONFIG] Max results per brand: {max_results_per_brand if max_results_per_brand > 0 else 'All'}")
    print(f"[CONFIG] Delay between brands: {delay_between_brands}s")
    print(f"[CONFIG] Minimum devices filter: {min_devices if min_devices > 0 else 'None'}\n")
    
    # Initialize
    scraper = AllBrandsScraper()
    
    # Get all brands
    brands = scraper.get_all_brands()
    
    if not brands:
        print("❌ No brands found")
        return 1
    
    # Filter by minimum devices if specified
    if min_devices > 0:
        brands = [(name, url, count) for name, url, count in brands if count >= min_devices]
        print(f"📊 Filtered to {len(brands)} brands with {min_devices}+ devices\n")
    
    # Display brands
    print(f"📋 Brands to scrape:")
    for name, url, count in brands:
        print(f"   - {name}: {count} devices")
    
    # Scrape all brands
    total_saved = 0
    results = []
    
    start_time = datetime.now()
    
    for idx, (brand_name, brand_url, device_count) in enumerate(brands, 1):
        print(f"\n{'='*70}")
        print(f"[{idx}/{len(brands)}] Processing: {brand_name}")
        print(f"{'='*70}")
        
        saved = scraper.scrape_brand(brand_name, brand_url, device_count, max_results_per_brand)
        
        total_saved += saved
        results.append((brand_name, saved, device_count))
        
        # Delay between brands
        if idx < len(brands):
            print(f"\n⏳ Waiting {delay_between_brands}s before next brand...")
            time.sleep(delay_between_brands)
    
    # Summary
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print("\n" + "=" * 70)
    print("SCRAPING COMPLETE")
    print("=" * 70)
    print(f"⏱️  Duration: {duration:.0f}s ({duration/60:.1f} minutes)")
    print(f"✅ Total phones saved: {total_saved}")
    print(f"✅ Brands processed: {len(brands)}")
    
    print(f"\n📊 Top Brands by Phones Saved:")
    sorted_results = sorted(results, key=lambda x: x[1], reverse=True)[:10]
    for brand, saved, total in sorted_results:
        print(f"   - {brand}: {saved} phones (out of {total})")
    
    # MongoDB stats
    try:
        stats = scraper.mongo_client.get_collection_stats()
        print(f"\n[MONGODB] Database Stats:")
        print(f"  - Total documents: {stats.get('total_documents', 0)}")
    except Exception as e:
        print(f"\n[MONGODB] ⚠️  Could not fetch stats: {e}")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
