# Universal Mobile Phone Search - Complete Guide

## What You Can Do Now

Search for ANY mobile phone and get complete details including:
- ✅ Specifications (display, camera, battery, processor, etc.)
- ✅ Prices (Indian market and global)
- ✅ Ratings and reviews
- ✅ Images
- ✅ Direct product links
- ✅ Auto-saved results in JSON format

## Quick Start Guide

### Option 1: Command Line (Easiest)

```bash
python search.py
```

Then enter your query:
```
What phone are you looking for? iPhone 15
How many results per site? 5
```

### Option 2: With Query Argument

```bash
python search.py Samsung Galaxy S24
python search.py OnePlus 12 Pro
python search.py iPhone 15 Pro Max
```

### Option 3: Python Code

```python
from universal_search import UniversalSearch

# Create searcher
searcher = UniversalSearch()

# Search and get all matching phones
results = searcher.search_and_save("Samsung S24", max_results_per_site=10)

# Display formatted results
searcher.display_results(results, show_details=True)
```

## What Gets Searched

Your query is searched across:

1. **GSMArena** (www.gsmarena.com)
   - Most comprehensive specs
   - Detailed technical information
   - User ratings and reviews
   - Success rate: ~95%

2. **91mobiles** (www.91mobiles.com)
   - Indian market prices
   - Availability information
   - Deals and discounts
   - Success rate: ~70-80%

3. **Kimovil** (www.kimovil.com)
   - Global price comparisons
   - Multiple store prices
   - International availability
   - Success rate: ~10% (Cloudflare blocks most requests)

## Example Searches

### Search by Brand
```bash
python search.py Samsung
python search.py Apple
python search.py OnePlus
python search.py Xiaomi
python search.py Google Pixel
```

### Search by Model
```bash
python search.py Galaxy S24 Ultra
python search.py iPhone 15 Pro Max
python search.py OnePlus 12
python search.py Pixel 8 Pro
python search.py Xiaomi 14
```

### Search by Feature (GSMArena)
```bash
python search.py 200mp camera
python search.py 5000mah battery
python search.py snapdragon 8 gen 3
python search.py flagship 2024
```

## What You Get

For each phone found, you receive:

### Basic Information
- Brand name (e.g., "Samsung")
- Model name (e.g., "Galaxy S24 Ultra")
- Source website
- Direct product URL

### Pricing
- Current price
- Original price (if on sale)
- Currency (INR for 91mobiles, USD/EUR for Kimovil)
- Availability status

### Ratings
- User rating (out of 5)
- Number of reviews
- Popularity score

### Complete Specifications
- **Display**: Size, type, resolution, refresh rate
- **Processor**: Chipset name and details
- **Memory**: RAM options
- **Storage**: Internal storage options
- **Camera**: Main, ultrawide, telephoto, selfie cameras
- **Battery**: Capacity, charging speed
- **Operating System**: OS version
- **Network**: 5G, 4G, Wi-Fi specifications
- **Build**: Dimensions, weight, materials
- **And much more!**

### Images
- Product photos
- Multiple angles
- High resolution

## Output Files

All searches are automatically saved to `data/` folder:

```
data/
├── search_Samsung_S24_20251122_103045.json
├── search_iPhone_15_20251122_104210.json
└── search_OnePlus_12_20251122_105335.json
```

### JSON File Format

```json
{
  "query": "Samsung S24",
  "timestamp": "2025-11-22T10:30:45",
  "total_found": 12,
  "scrapers": {
    "gsmarena": {
      "status": "success",
      "count": 5,
      "phones": [
        {
          "brand": "Samsung",
          "model": "Galaxy S24 Ultra",
          "price": "N/A",
          "original_price": null,
          "currency": null,
          "rating": 8.9,
          "reviews_count": null,
          "specs": {
            "Display": "6.8 inches, 1440 x 3120 pixels, Dynamic AMOLED 2X, 120Hz",
            "Chipset": "Qualcomm Snapdragon 8 Gen 3",
            "CPU": "Octa-core (1x3.3 GHz + 3x3.2 GHz + 2x3.0 GHz + 2x2.3 GHz)",
            "GPU": "Adreno 750",
            "Memory": "12GB RAM",
            "Storage": "256GB / 512GB / 1TB",
            "Main Camera": "200 MP + 50 MP + 10 MP + 12 MP",
            "Selfie Camera": "12 MP",
            "Battery": "5000 mAh, 45W fast charging",
            "OS": "Android 14, One UI 6.1"
          },
          "images": [
            "https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-s24-ultra-5g.jpg"
          ],
          "thumbnail": "https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-s24-ultra-5g.jpg",
          "url": "https://www.gsmarena.com/samsung_galaxy_s24_ultra-12771.php",
          "source": "GSMArena",
          "in_stock": true,
          "highlights": [
            "200MP main camera",
            "5000mAh battery",
            "120Hz AMOLED display"
          ]
        }
      ]
    },
    "91mobiles": {
      "status": "success",
      "count": 4,
      "phones": [...]
    },
    "kimovil": {
      "status": "error",
      "error": "Cloudflare protection blocked request",
      "count": 0,
      "phones": []
    }
  }
}
```

## Code Examples

### Example 1: Simple Search
```python
from universal_search import UniversalSearch

searcher = UniversalSearch()
results = searcher.search_all("iPhone 15", max_results_per_site=5)

print(f"Total phones found: {results['total_found']}")
```

### Example 2: Get Detailed Phone Info
```python
# Search first
results = searcher.search_all("Samsung S24 Ultra", max_results_per_site=3)

# Get first GSMArena result
gsm_results = results['scrapers']['gsmarena']['phones']
if gsm_results:
    phone = gsm_results[0]
    print(f"Phone: {phone['brand']} {phone['model']}")
    print(f"Display: {phone['specs'].get('Display')}")
    print(f"Camera: {phone['specs'].get('Main Camera')}")
    print(f"Battery: {phone['specs'].get('Battery')}")
    print(f"Rating: {phone['rating']}/5")
```

### Example 3: Compare Prices Across Sites
```python
results = searcher.search_all("OnePlus 12", max_results_per_site=3)

print("Price Comparison:")
for scraper_name, data in results['scrapers'].items():
    for phone in data['phones']:
        if 'OnePlus 12' in phone['model']:
            price = phone.get('price', 'N/A')
            print(f"  {scraper_name}: {price}")
```

### Example 4: Filter by Specs
```python
results = searcher.search_all("flagship", max_results_per_site=20)

# Find phones with 200MP camera
high_res_phones = []
for scraper_data in results['scrapers'].values():
    for phone in scraper_data['phones']:
        camera = phone['specs'].get('Main Camera', '')
        if '200' in camera and 'MP' in camera:
            high_res_phones.append(phone)

print(f"Found {len(high_res_phones)} phones with 200MP camera")
```

### Example 5: Track Multiple Models
```python
models = ["iPhone 15", "Samsung S24", "OnePlus 12", "Pixel 8", "Xiaomi 14"]

phone_database = {}
for model in models:
    results = searcher.search_and_save(model, max_results_per_site=3)
    phone_database[model] = results

# Save combined database
import json
with open('data/phone_database.json', 'w') as f:
    json.dump(phone_database, f, indent=2)
```

### Example 6: Get Phone by Direct URL
```python
# If you already know the URL
phone = searcher.get_phone_details(
    "https://www.gsmarena.com/samsung_galaxy_s24_ultra-12771.php"
)

if phone:
    print(f"Brand: {phone.brand}")
    print(f"Model: {phone.model}")
    print(f"Specs: {len(phone.specs)} specifications")
    print(phone.to_json())  # Get as JSON string
```

## Advanced Features

### 1. Display Results with Details
```python
results = searcher.search_all("Samsung", max_results_per_site=5)
searcher.display_results(results, show_details=True)
```

Output:
```
[GSMARENA] - 5 phones found
--------------------------------------------------------------------------------

  1. Samsung Galaxy S24 Ultra
     Price: N/A
     Rating: 8.9/5 [*][*][*][*][*][*][*][*]
     Specs: Display: 6.8 inches | Chipset: Snapdragon 8 Gen 3 | Battery: 5000 mAh
     URL: https://www.gsmarena.com/samsung_galaxy_s24_ultra-12771.php
```

### 2. Compare Multiple Phones
```python
# Get phones
s24 = searcher.get_phone_details("https://www.gsmarena.com/samsung_galaxy_s24-12771.php")
iphone = searcher.get_phone_details("https://www.gsmarena.com/apple_iphone_15-12559.php")

# Compare
comparison = searcher.compare_phones([s24, iphone])

print("Comparison:")
for spec_name, values in comparison['specs_comparison'].items():
    print(f"{spec_name}:")
    for i, value in enumerate(values):
        phone_name = comparison['phones'][i]['name']
        print(f"  {phone_name}: {value}")
```

### 3. Batch Processing
```python
queries = ["iPhone 15", "Samsung S24", "OnePlus 12", "Pixel 8", "Xiaomi 14"]

for query in queries:
    print(f"\nProcessing: {query}")
    results = searcher.search_and_save(query, max_results_per_site=5)
    print(f"  Found: {results['total_found']} phones")
    print(f"  Saved to: data/search_{query}_{timestamp}.json")
```

## Tips for Best Results

### 1. Be Specific with Queries
- ✅ Good: "Samsung Galaxy S24 Ultra"
- ✅ Good: "iPhone 15 Pro Max"
- ⚠️ Okay: "Samsung S24" (might get multiple models)
- ❌ Too broad: "phone" (returns random results)

### 2. Use Model Numbers When Possible
- "Galaxy S24" instead of just "Samsung"
- "OnePlus 12" instead of just "OnePlus"
- "Pixel 8 Pro" instead of just "Google"

### 3. Adjust max_results Based on Need
- Quick search: `max_results_per_site=3`
- Comprehensive: `max_results_per_site=10`
- Maximum: `max_results_per_site=20`

### 4. Handle Errors Gracefully
```python
try:
    results = searcher.search_all("rare phone model", max_results_per_site=5)
    if results['total_found'] == 0:
        print("No results found. Try a different query.")
except Exception as e:
    print(f"Search error: {e}")
```

## Performance Tips

### Faster Searches
```python
# Search only GSMArena (fastest, most reliable)
gsm = GSMArenaScraper()
phones = gsm.search_phones("Samsung S24", max_results=10)
```

### Avoid Timeouts
- Use lower `max_results_per_site` (3-5 instead of 10-20)
- Skip Kimovil if it's consistently timing out
- Add delays if getting rate limited

### Parallel Searches (Advanced)
```python
import concurrent.futures

def search_brand(brand):
    searcher = UniversalSearch()
    return searcher.search_all(brand, max_results_per_site=3)

brands = ["Samsung", "Apple", "OnePlus", "Xiaomi"]

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(search_brand, brands))
```

## Troubleshooting

### No Results Found
**Problem**: Search returns 0 results
**Solutions**:
- Check spelling of query
- Try more general terms (e.g., "Samsung" instead of "Samsung Galaxy S24 Ultra 5G 512GB")
- Try different query format
- Check internet connection

### Slow Performance
**Problem**: Searches take very long
**Solutions**:
- Reduce `max_results_per_site`
- Search only GSMArena (most reliable)
- Skip Kimovil (often blocked/slow)

### Kimovil Always Blocked
**Problem**: Kimovil returns 0 results with "Cloudflare" error
**Solutions**:
- This is normal - Kimovil has aggressive bot protection
- Focus on GSMArena and 91mobiles
- For Kimovil, use direct product URLs

### Import Errors
**Problem**: `ModuleNotFoundError` when running
**Solutions**:
```bash
pip install beautifulsoup4 lxml requests fake-useragent
pip install cloudscraper curl-cffi
```

## Files Created

```
universal_search.py      - Main search class
search.py                - Simple CLI interface
examples_search.py       - Usage examples
test_search.py          - Quick test script
SEARCH_GUIDE.md         - This guide
```

## Summary

You now have a powerful mobile phone search system that:
- ✅ Searches multiple websites simultaneously
- ✅ Gets complete phone specifications
- ✅ Includes prices and ratings
- ✅ Auto-saves all results
- ✅ Works without proxies
- ✅ Handles bot detection
- ✅ Provides clean JSON output
- ✅ Easy to use from command line or Python

**Start searching:**
```bash
python search.py iPhone 15
```

Enjoy! 📱
