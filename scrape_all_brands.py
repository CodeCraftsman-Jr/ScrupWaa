"""
Scrape all major phone brands and save to MongoDB
"""

import os
import sys
import time
from datetime import datetime

# Add function directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(current_dir, 'function'))

from universal_search import UniversalSearch
from utils.mongodb_client import MongoDBClient


# All major phone brands to scrape
BRANDS = [
    "Samsung",
    "Apple", 
    "Nokia",
    "Sony",
    "LG",
    "HTC",
    "Motorola",
    "Lenovo",
    "Xiaomi",
    "Google",
    "Oppo",
    "Realme",
    "OnePlus",
    "Nothing",
    "vivo",
    "Asus",
    "Infinix",
    "Tecno"
]


def scrape_brand(brand: str, searcher: UniversalSearch, mongo_client: MongoDBClient, max_results: int = 0):
    """
    Scrape all phones for a specific brand.
    
    Args:
        brand: Brand name to search
        searcher: UniversalSearch instance
        mongo_client: MongoDBClient instance
        max_results: Maximum results per brand (0 = all)
    """
    print("\n" + "=" * 70)
    print(f"SCRAPING BRAND: {brand}")
    print("=" * 70)
    
    try:
        # Search for brand
        results = searcher.search_all(
            query=brand,
            sites=['gsmarena'],
            max_results=max_results if max_results > 0 else None
        )
        
        # Get phones from results
        gsmarena_data = results.get('scrapers', {}).get('gsmarena', {})
        phones = gsmarena_data.get('phones', [])
        
        if not phones:
            print(f"⚠️  No phones found for {brand}")
            return 0
        
        # Convert to dict and add source
        results_dict = []
        for phone in phones:
            phone_dict = phone.to_dict() if hasattr(phone, 'to_dict') else phone
            
            organized_phone = {
                'source': 'GSMArena',
                **phone_dict
            }
            
            results_dict.append(organized_phone)
        
        # Save each phone to MongoDB
        saved_count = 0
        for phone in results_dict:
            try:
                doc_id = mongo_client.save_phone(
                    query=brand,
                    phone_data=phone,
                    method='headless_browser'
                )
                if doc_id:
                    saved_count += 1
            except Exception as e:
                print(f"⚠️  Failed to save phone: {e}")
        
        print(f"✅ {brand}: Scraped {len(results_dict)} phones, Saved {saved_count} to MongoDB")
        return saved_count
        
    except Exception as e:
        print(f"❌ Error scraping {brand}: {e}")
        import traceback
        traceback.print_exc()
        return 0


def main():
    print("=" * 70)
    print("MULTI-BRAND PHONE SCRAPER")
    print("Scraping all major phone brands")
    print("=" * 70)
    
    # Get configuration
    max_results_per_brand = int(os.environ.get('MAX_RESULTS_PER_BRAND', 0))
    delay_between_brands = int(os.environ.get('DELAY_BETWEEN_BRANDS', 10))
    
    print(f"\n[CONFIG] Brands to scrape: {len(BRANDS)}")
    print(f"[CONFIG] Max results per brand: {max_results_per_brand if max_results_per_brand > 0 else 'All'}")
    print(f"[CONFIG] Delay between brands: {delay_between_brands}s")
    print(f"[CONFIG] Brands: {', '.join(BRANDS)}\n")
    
    # Initialize
    searcher = UniversalSearch()
    
    try:
        mongo_client = MongoDBClient()
        print("[MONGODB] ✅ MongoDB initialized\n")
    except Exception as e:
        print(f"[MONGODB] ❌ MongoDB initialization failed: {e}")
        return 1
    
    # Scrape all brands
    total_saved = 0
    successful_brands = []
    failed_brands = []
    
    start_time = datetime.now()
    
    for idx, brand in enumerate(BRANDS, 1):
        print(f"\n[{idx}/{len(BRANDS)}] Processing: {brand}")
        
        saved = scrape_brand(brand, searcher, mongo_client, max_results_per_brand)
        
        if saved > 0:
            total_saved += saved
            successful_brands.append((brand, saved))
        else:
            failed_brands.append(brand)
        
        # Delay between brands (except after last one)
        if idx < len(BRANDS):
            print(f"⏳ Waiting {delay_between_brands}s before next brand...")
            time.sleep(delay_between_brands)
    
    # Summary
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print("\n" + "=" * 70)
    print("SCRAPING COMPLETE")
    print("=" * 70)
    print(f"⏱️  Duration: {duration:.0f}s ({duration/60:.1f} minutes)")
    print(f"✅ Total phones saved: {total_saved}")
    print(f"✅ Successful brands: {len(successful_brands)}/{len(BRANDS)}")
    
    if successful_brands:
        print(f"\n📊 Breakdown:")
        for brand, count in successful_brands:
            print(f"   - {brand}: {count} phones")
    
    if failed_brands:
        print(f"\n⚠️  Failed brands ({len(failed_brands)}):")
        for brand in failed_brands:
            print(f"   - {brand}")
    
    # Get MongoDB stats
    try:
        stats = mongo_client.get_collection_stats()
        print(f"\n[MONGODB] Database Stats:")
        print(f"  - Total documents: {stats.get('total_documents', 0)}")
        print(f"  - Total phones: {stats.get('total_documents', 0)}")
    except Exception as e:
        print(f"[MONGODB] ⚠️  Could not fetch stats: {e}")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
