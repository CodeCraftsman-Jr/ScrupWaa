"""
Format search results in detailed Flipkart-like format
"""
import json
from typing import List, Dict
from models.phone import Phone


def format_detailed_results(results: dict) -> dict:
    """
    Format search results in Flipkart-style detailed format.
    
    Args:
        results: Results from UniversalSearch.search_all()
        
    Returns:
        Detailed formatted results dictionary
    """
    formatted = {
        "total_result": results['total_found'],
        "query": results['query'],
        "query_params": results.get('query_params', {
            "page_number": None,
            "sort": None,
            "min_price": None,
            "max_price": None,
            "others": None
        }),
        "timestamp": results['timestamp'],
        "result": []
    }
    
    # Process results from each scraper
    for scraper_name, scraper_data in results['scrapers'].items():
        if scraper_data['count'] == 0:
            continue
        
        for phone_data in scraper_data['phones']:
            # Create detailed phone entry
            detailed_entry = {
                "name": f"{phone_data['brand']} {phone_data['model']}",
                "link": phone_data['url'],
                "current_price": phone_data.get('price'),
                "original_price": phone_data.get('original_price'),
                "discounted": phone_data.get('discounted', False),
                "thumbnail": phone_data.get('thumbnail'),
                "query_url": phone_data['url'],
                "rating": phone_data.get('rating'),
                "in_stock": phone_data.get('in_stock', True),
                "f_assured": phone_data.get('f_assured', False),
                "source": phone_data.get('source', scraper_name),
                
                # Seller info
                "seller": {
                    "seller_name": phone_data.get('seller_name') or scraper_name,
                    "seller_rating": phone_data.get('seller_rating')
                },
                
                # Highlights
                "highlights": phone_data.get('highlights', []),
                
                # Offers
                "offers": phone_data.get('offers', []),
                
                # Detailed specs
                "specs": phone_data.get('detailed_specs', []),
                
                # All images
                "all_thumbnails": phone_data.get('all_images', phone_data.get('images', []))
            }
            
            # Convert flat specs to detailed format if needed
            if not detailed_entry['specs'] and phone_data.get('specs'):
                detailed_entry['specs'] = convert_flat_specs_to_detailed(phone_data['specs'])
            
            formatted['result'].append(detailed_entry)
    
    return formatted


def convert_flat_specs_to_detailed(flat_specs: dict) -> List[Dict]:
    """
    Convert flat specs dictionary to detailed nested format.
    
    Args:
        flat_specs: Dictionary of spec_name: spec_value
        
    Returns:
        List of categorized specs
    """
    # Group specs by category
    categories = {
        "Display": ['Display', 'Screen', 'Resolution', 'Size', 'Type', 'Protection'],
        "Platform": ['OS', 'Chipset', 'CPU', 'GPU', 'Platform'],
        "Memory": ['RAM', 'Memory', 'Internal', 'Storage', 'Card slot'],
        "Main Camera": ['Main camera', 'Main Camera', 'Camera', 'Video'],
        "Selfie Camera": ['Selfie camera', 'Selfie Camera', 'Front camera'],
        "Sound": ['Loudspeaker', '3.5mm jack', 'Sound'],
        "Comms": ['WLAN', 'Bluetooth', 'GPS', 'NFC', 'Radio', 'USB'],
        "Battery": ['Battery', 'Charging', 'Type', 'Charging'],
        "Misc": ['Colors', 'Models', 'SAR', 'Price'],
    }
    
    detailed_specs = []
    
    for category_name, keywords in categories.items():
        details = []
        
        for spec_key, spec_value in flat_specs.items():
            # Check if this spec belongs to this category
            if any(keyword.lower() in spec_key.lower() for keyword in keywords):
                details.append({
                    "property": spec_key,
                    "value": spec_value
                })
        
        if details:
            detailed_specs.append({
                "title": category_name,
                "details": details
            })
    
    # Add remaining specs as "General"
    used_keys = set()
    for category in detailed_specs:
        for detail in category['details']:
            used_keys.add(detail['property'])
    
    general_details = []
    for spec_key, spec_value in flat_specs.items():
        if spec_key not in used_keys:
            general_details.append({
                "property": spec_key,
                "value": spec_value
            })
    
    if general_details:
        detailed_specs.append({
            "title": "General",
            "details": general_details
        })
    
    return detailed_specs


def save_detailed_results(results: dict, filename: str):
    """
    Save results in detailed Flipkart-like format.
    
    Args:
        results: Results from UniversalSearch.search_all()
        filename: Output JSON file path
    """
    formatted = format_detailed_results(results)
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(formatted, f, indent=2, ensure_ascii=False)
    
    print(f"\n[SAVED] Detailed results saved to: {filename}")
    return formatted


def print_detailed_phone(phone_data: dict):
    """Print a single phone in detailed format."""
    print("\n" + "="*80)
    print(f"NAME: {phone_data['name']}")
    print("="*80)
    
    print(f"\nPrice: {phone_data['current_price'] or 'N/A'}")
    if phone_data.get('original_price'):
        print(f"Original Price: {phone_data['original_price']}")
        print(f"Discounted: {phone_data['discounted']}")
    
    print(f"Rating: {phone_data['rating'] or 'N/A'}")
    print(f"In Stock: {phone_data['in_stock']}")
    print(f"Source: {phone_data['source']}")
    
    if phone_data.get('seller'):
        print(f"\nSeller: {phone_data['seller']['seller_name']}")
        if phone_data['seller'].get('seller_rating'):
            print(f"Seller Rating: {phone_data['seller']['seller_rating']}")
    
    if phone_data.get('highlights'):
        print("\nHighlights:")
        for highlight in phone_data['highlights'][:5]:
            print(f"  - {highlight}")
    
    if phone_data.get('offers'):
        print(f"\nOffers: {len(phone_data['offers'])} available")
        for offer in phone_data['offers'][:3]:
            if isinstance(offer, dict):
                print(f"  - {offer.get('offer_type', 'Offer')}: {offer.get('description', '')}")
    
    print(f"\nSpecifications: {len(phone_data.get('specs', []))} categories")
    for spec_category in phone_data.get('specs', [])[:3]:
        print(f"  [{spec_category['title']}] {len(spec_category['details'])} properties")
    
    print(f"\nImages: {len(phone_data.get('all_thumbnails', []))} available")
    print(f"URL: {phone_data['link']}")
    print("="*80)


if __name__ == "__main__":
    # Example usage
    from universal_search import UniversalSearch
    
    searcher = UniversalSearch()
    results = searcher.search_all("Samsung S24", max_results_per_site=2)
    
    # Format and save in detailed format
    detailed = save_detailed_results(results, "data/detailed_results.json")
    
    # Print first result
    if detailed['result']:
        print_detailed_phone(detailed['result'][0])
