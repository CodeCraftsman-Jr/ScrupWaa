"""
Universal Search - Search across all mobile phone scrapers
"""
import json
import os
from typing import List, Optional
from datetime import datetime

from scrapers.gsmarena import GSMArenaScraper
from scrapers.mobiles91 import Mobiles91Scraper
from scrapers.kimovil import KimovilScraper
from models.phone import Phone


class UniversalSearch:
    """Search across all available mobile phone scrapers."""
    
    def __init__(self):
        self.gsmarena = GSMArenaScraper()
        self.mobiles91 = Mobiles91Scraper()
        self.kimovil = KimovilScraper()
        
    def search_all(self, query: str, max_results_per_site: int = 10, sites: Optional[List[str]] = None, max_results: int = None) -> dict:
        """
        Search for phones across all scrapers.
        
        Args:
            query: Search query (e.g., "Samsung Galaxy S24", "iPhone 15", "OnePlus")
            max_results_per_site: Maximum results from each scraper (deprecated, use max_results)
            sites: List of sites to search (optional). Options: ['gsmarena', '91mobiles', 'kimovil']
            max_results: Maximum results to return (None for all)
            
        Returns:
            Dictionary with results from each scraper
        """
        # Use max_results if provided, otherwise fall back to max_results_per_site
        if max_results is not None:
            max_results_per_site = max_results
        
        if sites is None:
            sites = ['gsmarena', '91mobiles', 'kimovil']
        
        print(f"\n{'='*60}")
        print(f"UNIVERSAL SEARCH: '{query}'")
        print(f"Sites: {', '.join(sites)}")
        print(f"{'='*60}\n")
        
        results = {
            'query': query,
            'timestamp': datetime.now().isoformat(),
            'scrapers': {}
        }
        
        total_sites = len(sites)
        current_site = 0
        
        # GSMArena (most reliable)
        if 'gsmarena' in sites:
            current_site += 1
            print(f"[{current_site}/{total_sites}] Searching GSMArena...")
            try:
                # Use max_results_per_site (which now includes max_results if provided)
                gsm_phones = self.gsmarena.search_phones(query, max_results=max_results_per_site if max_results_per_site != 10 else None)
                results['scrapers']['gsmarena'] = {
                    'status': 'success',
                    'count': len(gsm_phones),
                    'phones': gsm_phones  # Keep as Phone objects for now
                }
                print(f"      [SUCCESS] Found {len(gsm_phones)} phones\n")
            except Exception as e:
                print(f"      [ERROR] {str(e)}\n")
                results['scrapers']['gsmarena'] = {
                    'status': 'error',
                    'error': str(e),
                    'count': 0,
                    'phones': []
                }
        
        # 91mobiles (Indian prices)
        if '91mobiles' in sites:
            current_site += 1
            print(f"[{current_site}/{total_sites}] Searching 91mobiles...")
            try:
                mob91_phones = self.mobiles91.search_phones(query, max_results=max_results_per_site)
                results['scrapers']['91mobiles'] = {
                    'status': 'success',
                    'count': len(mob91_phones),
                    'phones': [p.to_dict() for p in mob91_phones]
                }
                print(f"      [SUCCESS] Found {len(mob91_phones)} phones\n")
            except Exception as e:
                print(f"      [ERROR] {str(e)}\n")
                results['scrapers']['91mobiles'] = {
                    'status': 'error',
                    'error': str(e),
                    'count': 0,
                    'phones': []
                }
        
        # Kimovil (global prices - may be blocked)
        if 'kimovil' in sites:
            current_site += 1
            print(f"[{current_site}/{total_sites}] Searching Kimovil...")
            try:
                kim_phones = self.kimovil.search_phones(query, max_results=max_results_per_site)
                results['scrapers']['kimovil'] = {
                    'status': 'success',
                    'count': len(kim_phones),
                    'phones': [p.to_dict() for p in kim_phones]
                }
                print(f"      [SUCCESS] Found {len(kim_phones)} phones\n")
            except Exception as e:
                print(f"      [ERROR] {str(e)}\n")
                results['scrapers']['kimovil'] = {
                    'status': 'error',
                    'error': str(e),
                    'count': 0,
                    'phones': []
                }
        
        # Summary
        total = sum(s['count'] for s in results['scrapers'].values())
        results['total_found'] = total
        
        print(f"{'='*60}")
        print(f"SEARCH COMPLETE")
        print(f"{'='*60}")
        print(f"Total phones found: {total}")
        
        # Print counts for searched sites only
        for site in sites:
            if site in results['scrapers']:
                count = results['scrapers'][site]['count']
                print(f"  - {site}: {count}")
        
        print(f"{'='*60}\n")
        
        return results
    
    def search_and_save(self, query: str, max_results_per_site: int = 10, 
                       output_file: Optional[str] = None, detailed_format: bool = False) -> dict:
        """
        Search all scrapers and save results to JSON file.
        
        Args:
            query: Search query
            max_results_per_site: Max results per scraper
            output_file: Output JSON file path (auto-generated if None)
            detailed_format: If True, save in Flipkart-like detailed format
            
        Returns:
            Search results dictionary
        """
        results = self.search_all(query, max_results_per_site)
        
        # Generate filename if not provided
        if not output_file:
            safe_query = "".join(c if c.isalnum() else "_" for c in query)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            if detailed_format:
                output_file = f"data/detailed_{safe_query}_{timestamp}.json"
            else:
                output_file = f"data/search_{safe_query}_{timestamp}.json"
        
        # Ensure data directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Format results if detailed format requested
        if detailed_format:
            from format_results import format_detailed_results
            results_to_save = format_detailed_results(results)
        else:
            results_to_save = results
        
        # Save results
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results_to_save, f, indent=2, ensure_ascii=False)
        
        print(f"[SAVED] Results saved to: {output_file}\n")
        
        return results
    
    def display_results(self, results: dict, show_details: bool = True):
        """
        Display search results in a readable format.
        
        Args:
            results: Results dictionary from search_all()
            show_details: Whether to show detailed phone specs
        """
        print(f"\n{'='*80}")
        print(f"SEARCH RESULTS FOR: '{results['query']}'")
        print(f"{'='*80}\n")
        
        for scraper_name, data in results['scrapers'].items():
            print(f"[{scraper_name.upper()}] - {data['count']} phones found")
            print("-" * 80)
            
            if data['count'] == 0:
                print("  No results\n")
                continue
            
            for i, phone in enumerate(data['phones'], 1):
                print(f"\n  {i}. {phone['brand']} {phone['model']}")
                
                if show_details:
                    # Price
                    if phone.get('price'):
                        price_str = phone['price']
                        if phone.get('original_price'):
                            price_str += f" (was {phone['original_price']})"
                        print(f"     Price: {price_str}")
                    
                    # Rating
                    if phone.get('rating'):
                        stars = '[*]' * int(phone['rating'])
                        print(f"     Rating: {phone['rating']}/5 {stars}")
                    
                    # Key specs
                    if phone.get('specs'):
                        specs = phone['specs']
                        key_specs = []
                        
                        # Extract important specs
                        for key in ['Display', 'OS', 'Chipset', 'RAM', 'Storage', 
                                   'Camera', 'Battery', 'Screen']:
                            if key in specs:
                                key_specs.append(f"{key}: {specs[key]}")
                        
                        if key_specs:
                            print(f"     Specs: {' | '.join(key_specs[:3])}")
                    
                    # URL
                    if phone.get('url'):
                        print(f"     URL: {phone['url']}")
            
            print()
    
    def get_phone_details(self, url: str) -> Optional[Phone]:
        """
        Get detailed information for a specific phone URL.
        
        Args:
            url: Full URL to phone page
            
        Returns:
            Phone object with all details, or None if failed
        """
        print(f"\n[FETCHING] Getting details from: {url}\n")
        
        # Determine which scraper to use based on URL
        if 'gsmarena.com' in url:
            return self.gsmarena.scrape_phone(url)
        elif '91mobiles.com' in url:
            return self.mobiles91.scrape_phone(url)
        elif 'kimovil.com' in url:
            return self.kimovil.scrape_phone(url)
        else:
            print(f"[ERROR] Unknown website. Supported: GSMArena, 91mobiles, Kimovil")
            return None
    
    def compare_phones(self, phone_list: List[Phone]) -> dict:
        """
        Compare specifications across multiple phones.
        
        Args:
            phone_list: List of Phone objects to compare
            
        Returns:
            Comparison dictionary
        """
        if not phone_list:
            return {}
        
        comparison = {
            'phones': [],
            'specs_comparison': {}
        }
        
        # Collect all unique spec keys
        all_spec_keys = set()
        for phone in phone_list:
            if phone.specs:
                all_spec_keys.update(phone.specs.keys())
        
        # Build comparison
        for phone in phone_list:
            comparison['phones'].append({
                'name': f"{phone.brand} {phone.model}",
                'price': phone.price,
                'rating': phone.rating,
                'source': phone.source
            })
        
        # Compare each spec
        for spec_key in sorted(all_spec_keys):
            comparison['specs_comparison'][spec_key] = []
            for phone in phone_list:
                value = phone.specs.get(spec_key, 'N/A') if phone.specs else 'N/A'
                comparison['specs_comparison'][spec_key].append(value)
        
        return comparison


def interactive_search():
    """Interactive command-line search interface."""
    searcher = UniversalSearch()
    
    print("""
╔════════════════════════════════════════════════════════════════╗
║                 UNIVERSAL MOBILE PHONE SEARCH                  ║
║                                                                ║
║  Search across GSMArena, 91mobiles, and Kimovil              ║
║  Get specs, prices, and ratings for any mobile phone          ║
╚════════════════════════════════════════════════════════════════╝
    """)
    
    while True:
        print("\nOptions:")
        print("  1. Search for phones")
        print("  2. Get details from URL")
        print("  3. Exit")
        
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == '1':
            query = input("\nEnter search query (e.g., 'Samsung S24', 'iPhone 15'): ").strip()
            if not query:
                print("[ERROR] Query cannot be empty")
                continue
            
            max_results = input("Max results per site (default 5): ").strip()
            max_results = int(max_results) if max_results.isdigit() else 5
            
            save = input("Save results to file? (y/n, default y): ").strip().lower()
            save = save != 'n'
            
            # Perform search
            if save:
                results = searcher.search_and_save(query, max_results)
            else:
                results = searcher.search_all(query, max_results)
            
            # Display results
            show_details = input("\nShow detailed specs? (y/n, default y): ").strip().lower()
            show_details = show_details != 'n'
            searcher.display_results(results, show_details)
            
        elif choice == '2':
            url = input("\nEnter phone URL: ").strip()
            if not url:
                print("[ERROR] URL cannot be empty")
                continue
            
            phone = searcher.get_phone_details(url)
            if phone:
                print(f"\n[SUCCESS] Retrieved: {phone.brand} {phone.model}")
                print(f"Price: {phone.price or 'N/A'}")
                print(f"Rating: {phone.rating or 'N/A'}")
                print(f"\nFull details:")
                print(json.dumps(phone.to_dict(), indent=2))
        
        elif choice == '3':
            print("\nGoodbye!")
            break
        
        else:
            print("[ERROR] Invalid choice")


if __name__ == "__main__":
    # Example usage
    searcher = UniversalSearch()
    
    # Quick search example
    results = searcher.search_and_save("Samsung Galaxy S24", max_results_per_site=3)
    searcher.display_results(results)
