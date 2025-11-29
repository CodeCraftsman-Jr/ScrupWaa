"""
GitHub Actions scraper with Appwrite proxy support
Fetches proxies from Appwrite database and uses them to bypass rate limiting
"""

import os
import sys
import json
import random
from datetime import datetime
from appwrite.client import Client
from appwrite.services.databases import Databases

# Add function directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(current_dir, 'function'))

from universal_search import UniversalSearch


def fetch_proxies_from_appwrite():
    """Fetch proxy list from Appwrite database"""
    print("[APPWRITE] Fetching proxies from database...")
    
    try:
        # Initialize Appwrite client
        client = Client()
        client.set_endpoint(os.environ['APPWRITE_ENDPOINT'])
        client.set_project(os.environ['APPWRITE_PROJECT_ID'])
        client.set_key(os.environ['APPWRITE_API_KEY'])
        
        # Get database service
        databases = Databases(client)
        
        # Fetch proxy documents
        result = databases.list_documents(
            database_id=os.environ['APPWRITE_DATABASE_ID'],
            collection_id=os.environ['APPWRITE_COLLECTION_ID']
        )
        
        proxies = []
        for doc in result['documents']:
            # Documents have fields: proxy, type, response_time, tested_at, status
            if doc.get('status') != 'failed':  # Only use working proxies
                proxy_url = doc.get('proxy')  # Field name is 'proxy'
                
                if proxy_url:
                    # Format: ip:port or http://ip:port
                    if not proxy_url.startswith('http'):
                        proxy_url = f"http://{proxy_url}"
                    
                    proxy_data = {
                        'http': proxy_url,
                        'https': proxy_url,
                    }
                    
                    proxies.append(proxy_data)
        
        print(f"[APPWRITE] ✅ Fetched {len(proxies)} working proxies")
        return proxies
    
    except Exception as e:
        print(f"[APPWRITE] ❌ Error fetching proxies: {e}")
        print("[APPWRITE] Continuing without proxies...")
        return []


def setup_proxy_rotation(proxies):
    """Set up proxy rotation for HTTP client with failure tracking"""
    if not proxies:
        return None
    
    # Track failed proxies
    failed_proxies = set()
    current_proxy_index = [0]  # Use list to maintain reference
    
    def get_next_proxy():
        """Get next working proxy from the list, rotating on failures"""
        if not proxies or len(failed_proxies) >= len(proxies):
            return None
        
        # Try up to len(proxies) times to find a working proxy
        for _ in range(len(proxies)):
            proxy = proxies[current_proxy_index[0] % len(proxies)]
            current_proxy_index[0] += 1
            
            # Skip failed proxies
            proxy_key = proxy.get('http', '')
            if proxy_key not in failed_proxies:
                return proxy
        
        return None
    
    def mark_proxy_failed(proxy):
        """Mark a proxy as failed"""
        if proxy:
            proxy_key = proxy.get('http', '')
            failed_proxies.add(proxy_key)
            print(f"[PROXY] ❌ Marked proxy as failed: {proxy_key[:50]}... ({len(failed_proxies)}/{len(proxies)} failed)")
    
    return get_next_proxy, mark_proxy_failed


def main():
    print("=" * 60)
    print("GitHub Actions Phone Scraper")
    print("=" * 60)
    
    # Get configuration from environment
    search_query = os.environ.get('SEARCH_QUERY', 'Samsung')
    max_results = int(os.environ.get('MAX_RESULTS', 20))
    
    # Fetch proxies from Appwrite
    proxies = fetch_proxies_from_appwrite()
    proxy_getter = setup_proxy_rotation(proxies)
    
    print(f"\n[CONFIG] Search query: {search_query}")
    print(f"[CONFIG] Max results: {max_results if max_results > 0 else 'All'}")
    print(f"[CONFIG] Proxies available: {len(proxies)}")
    print()
    
    # Initialize searcher
    searcher = UniversalSearch()
    
    # Inject proxy getter into HTTP client if available
    if proxy_getter and hasattr(searcher.gsmarena, 'client'):
        get_next_proxy, mark_proxy_failed = proxy_getter
        original_get = searcher.gsmarena.client.get
        
        current_proxy = [None]  # Track current proxy
        
        def get_with_proxy(url, **kwargs):
            """Wrapper to add proxy to requests with rotation on failure"""
            max_proxy_retries = 5  # Try up to 5 different proxies
            
            for proxy_attempt in range(max_proxy_retries):
                # Get a new proxy for each attempt
                proxy = get_next_proxy()
                current_proxy[0] = proxy
                
                if proxy:
                    kwargs['proxies'] = proxy
                    proxy_display = proxy.get('http', 'Unknown')
                    # Mask IP in log (show last part only)
                    if '//' in proxy_display:
                        proxy_display = proxy_display.split('//')[1]
                    print(f"🔒 Using proxy [{proxy_attempt + 1}/{max_proxy_retries}]: {proxy_display[:30]}...")
                else:
                    # No more proxies available, try without proxy
                    print(f"⚠️  No proxies available, trying direct connection...")
                    kwargs.pop('proxies', None)
                
                try:
                    # Try the request with current proxy
                    result = original_get(url, max_retries=2, **kwargs)  # Reduce retries per proxy
                    if result:
                        return result
                    # If result is None, mark proxy as failed and try next one
                    if proxy:
                        mark_proxy_failed(proxy)
                except Exception as e:
                    print(f"❌ Proxy failed: {str(e)[:100]}")
                    if proxy:
                        mark_proxy_failed(proxy)
                    continue
            
            # All proxies failed, try one last time without proxy
            print(f"⚠️  All proxies failed, attempting direct connection...")
            kwargs.pop('proxies', None)
            return original_get(url, **kwargs)
        
        searcher.gsmarena.client.get = get_with_proxy
        print("[PROXY] ✅ Proxy rotation with failover enabled")
    else:
        print("[PROXY] ⚠️  No proxy rotation (running without proxies)")
    
    # Run search
    try:
        print("\n" + "=" * 60)
        print(f"SEARCHING: '{search_query}'")
        print("=" * 60 + "\n")
        
        results = searcher.search_all(
            query=search_query,
            sites=['gsmarena'],
            max_results=max_results if max_results > 0 else None
        )
        
        # Convert to dict for JSON serialization
        results_dict = []
        for phone in results.get('gsmarena', []):
            if hasattr(phone, 'to_dict'):
                results_dict.append(phone.to_dict())
            else:
                results_dict.append(phone)
        
        # Save results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"data/github_scrape_{search_query.replace(' ', '_')}_{timestamp}.json"
        
        # Ensure data directory exists
        os.makedirs('data', exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                'query': search_query,
                'timestamp': datetime.now().isoformat(),
                'total_results': len(results_dict),
                'proxies_used': len(proxies),
                'results': results_dict
            }, f, indent=2, ensure_ascii=False)
        
        print("\n" + "=" * 60)
        print("SCRAPING COMPLETE")
        print("=" * 60)
        print(f"✅ Scraped {len(results_dict)} phones")
        print(f"✅ Saved to: {filename}")
        print(f"✅ Proxies used: {len(proxies)}")
        
        # Also save as latest.json for easy access
        with open('data/latest_scrape.json', 'w', encoding='utf-8') as f:
            json.dump({
                'query': search_query,
                'timestamp': datetime.now().isoformat(),
                'total_results': len(results_dict),
                'proxies_used': len(proxies),
                'results': results_dict
            }, f, indent=2, ensure_ascii=False)
        
        return 0
    
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
