"""
Scrape phones by category from GSMArena and save to MongoDB
Categories: Smartphones, Tablets, Smart Watches, Feature Phones, etc.
"""

import os
import sys
import time
import random
from datetime import datetime
from typing import List
from bs4 import BeautifulSoup

# Add function directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(current_dir, 'function'))

from utils.browser_client import HeadlessBrowserClient
from utils.mongodb_client import MongoDBClient
from scrapers.gsmarena import GSMArenaScraper


# GSMArena categories
CATEGORIES = {
    "Smartphones": "https://www.gsmarena.com/results.php3?sQuickSearch=yes&mode=allphones",
    "Tablets": "https://www.gsmarena.com/results.php3?nTabletYes=1",
    "Smart Watches": "https://www.gsmarena.com/results.php3?nSmartWatchesYes=1",
    "Feature Phones": "https://www.gsmarena.com/results.php3?nFeaturePhoneYes=1"
}


class CategoryScraper:
    """Scrape phones by category from GSMArena."""
    
    def __init__(self):
        self.browser = HeadlessBrowserClient()
        self.scraper = GSMArenaScraper(client=self.browser)
        self.mongo_client = MongoDBClient()
        # Use different collection for category-based scraping
        self.mongo_client.collection = self.mongo_client.db["phone_category_data"]
        print(f"[MONGODB] Using collection: phone_category_data")
    
    def get_phones_from_category(self, category_url: str, max_results: int = 0) -> List[str]:
        """
        Get list of phone URLs from a category page.
        
        Args:
            category_url: URL of the category page
            max_results: Maximum number of phones to scrape (0 = all)
            
        Returns:
            List of phone URLs
        """
        print(f"🔍 Fetching phones from category page...")
        
        phone_urls = []
        page_num = 1
        
        while True:
            # Construct page URL
            if page_num == 1:
                page_url = category_url
            else:
                # GSMArena pagination: add &iPage=2, &iPage=3, etc.
                separator = "&" if "?" in category_url else "?"
                page_url = f"{category_url}{separator}iPage={page_num}"
            
            print(f"📄 Loading page {page_num}...")
            
            response = self.browser.get(page_url)
            if not response:
                print(f"⚠️  Failed to load page {page_num}")
                break
            
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Find all phone links
            phone_links = soup.select('div.makers a')
            
            if not phone_links:
                print(f"✅ No more phones found on page {page_num}")
                break
            
            for link in phone_links:
                href = link.get('href')
                if href and href.endswith('.php'):
                    full_url = f"https://www.gsmarena.com/{href}"
                    phone_urls.append(full_url)
                    
                    # Check if we've reached the limit
                    if max_results > 0 and len(phone_urls) >= max_results:
                        print(f"✅ Reached maximum of {max_results} phones")
                        return phone_urls
            
            print(f"   Found {len(phone_links)} phones on page {page_num}")
            
            # Check if there's a next page
            next_page = soup.select_one('a.pages-next')
            if not next_page:
                print(f"✅ No more pages")
                break
            
            page_num += 1
            
            # Delay between pages
            time.sleep(random.uniform(2, 4))
        
        return phone_urls
    
    def scrape_category(self, category_name: str, category_url: str, max_results: int = 0):
        """
        Scrape all phones from a category.
        
        Args:
            category_name: Name of the category
            category_url: URL of the category page
            max_results: Maximum results to scrape (0 = all)
            
        Returns:
            Number of phones saved
        """
        print("\n" + "=" * 70)
        print(f"SCRAPING CATEGORY: {category_name}")
        print("=" * 70)
        
        try:
            # Get all phone URLs in this category
            phone_urls = self.get_phones_from_category(category_url, max_results)
            
            if not phone_urls:
                print(f"⚠️  No phones found in category: {category_name}")
                return 0
            
            print(f"\n📊 Found {len(phone_urls)} phones in {category_name}")
            print(f"🚀 Starting scraping...\n")
            
            saved_count = 0
            failed_count = 0
            
            for idx, url in enumerate(phone_urls, 1):
                print(f"[{idx}/{len(phone_urls)}] Scraping: {url}")
                
                try:
                    # Scrape phone
                    phone = self.scraper.scrape_phone(url)
                    
                    if phone:
                        # Convert to dict and add category + source
                        phone_dict = phone.to_dict() if hasattr(phone, 'to_dict') else phone
                        
                        phone_data = {
                            'category': category_name,
                            'source': 'GSMArena',
                            **phone_dict
                        }
                        
                        # Save to MongoDB
                        doc_id = self.mongo_client.save_phone(
                            query=category_name,
                            phone_data=phone_data,
                            method='headless_browser'
                        )
                        
                        if doc_id:
                            saved_count += 1
                            print(f"✅ Saved to MongoDB")
                        else:
                            failed_count += 1
                            print(f"⚠️  Failed to save to MongoDB")
                    else:
                        failed_count += 1
                        print(f"⚠️  Failed to scrape phone")
                    
                except Exception as e:
                    failed_count += 1
                    print(f"❌ Error scraping phone: {e}")
                
                # Delay between phones
                if idx < len(phone_urls):
                    delay = random.uniform(3, 6)
                    print(f"⏳ Waiting {delay:.1f}s before next request...")
                    time.sleep(delay)
            
            print(f"\n✅ {category_name} Complete:")
            print(f"   - Scraped: {saved_count}/{len(phone_urls)}")
            print(f"   - Failed: {failed_count}/{len(phone_urls)}")
            
            return saved_count
            
        except Exception as e:
            print(f"❌ Error scraping category {category_name}: {e}")
            import traceback
            traceback.print_exc()
            return 0


def main():
    print("=" * 70)
    print("CATEGORY-BASED PHONE SCRAPER")
    print("Scraping phones organized by category")
    print("=" * 70)
    
    # Get configuration
    max_results_per_category = int(os.environ.get('MAX_RESULTS_PER_CATEGORY', 0))
    delay_between_categories = int(os.environ.get('DELAY_BETWEEN_CATEGORIES', 15))
    
    print(f"\n[CONFIG] Categories to scrape: {len(CATEGORIES)}")
    print(f"[CONFIG] Max results per category: {max_results_per_category if max_results_per_category > 0 else 'All'}")
    print(f"[CONFIG] Delay between categories: {delay_between_categories}s")
    print(f"[CONFIG] Categories: {', '.join(CATEGORIES.keys())}\n")
    
    # Initialize scraper
    try:
        scraper = CategoryScraper()
    except Exception as e:
        print(f"❌ Failed to initialize scraper: {e}")
        return 1
    
    # Scrape all categories
    total_saved = 0
    category_results = {}
    
    start_time = datetime.now()
    
    for idx, (category_name, category_url) in enumerate(CATEGORIES.items(), 1):
        print(f"\n[{idx}/{len(CATEGORIES)}] Processing category: {category_name}")
        
        saved = scraper.scrape_category(category_name, category_url, max_results_per_category)
        
        total_saved += saved
        category_results[category_name] = saved
        
        # Delay between categories (except after last one)
        if idx < len(CATEGORIES):
            print(f"\n⏳ Waiting {delay_between_categories}s before next category...")
            time.sleep(delay_between_categories)
    
    # Summary
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print("\n" + "=" * 70)
    print("SCRAPING COMPLETE")
    print("=" * 70)
    print(f"⏱️  Duration: {duration:.0f}s ({duration/60:.1f} minutes)")
    print(f"✅ Total phones saved: {total_saved}")
    print(f"✅ Categories processed: {len(CATEGORIES)}")
    
    print(f"\n📊 Breakdown by Category:")
    for category, count in category_results.items():
        print(f"   - {category}: {count} phones")
    
    # Get MongoDB stats
    try:
        stats = scraper.mongo_client.get_collection_stats()
        print(f"\n[MONGODB] Collection: phone_category_data")
        print(f"  - Total documents: {stats.get('total_documents', 0)}")
    except Exception as e:
        print(f"\n[MONGODB] ⚠️  Could not fetch stats: {e}")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
