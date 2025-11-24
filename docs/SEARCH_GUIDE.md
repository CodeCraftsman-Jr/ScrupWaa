# Universal Mobile Phone Search

Search for any mobile phone across multiple websites and get complete specifications, prices, and ratings.

## Quick Start

### Method 1: Simple Command Line Search

```bash
python search.py
```

Then enter your search query when prompted:
```
What phone are you looking for? Samsung S24
How many results per site? 5
```

### Method 2: Search with Query as Argument

```bash
python search.py iPhone 15 Pro
```

### Method 3: Python Code

```python
from universal_search import UniversalSearch

# Create searcher
searcher = UniversalSearch()

# Search across all sites
results = searcher.search_and_save("Samsung Galaxy S24", max_results_per_site=5)

# Display results
searcher.display_results(results, show_details=True)
```

## Features

### 1. Multi-Site Search
Searches across:
- **GSMArena** - Complete specifications and features
- **91mobiles** - Indian market prices and availability
- **Kimovil** - Global price comparisons

### 2. Comprehensive Details
For each phone found, you get:
- Brand and Model name
- Current price (and original price if on sale)
- User ratings and reviews
- Complete specifications:
  - Display size and type
  - Processor/Chipset
  - RAM and Storage
  - Camera specifications
  - Battery capacity
  - Operating system
  - And much more!
- Product images
- Direct product URL

### 3. Auto-Save Results
All search results are automatically saved to JSON files in the `data/` folder with:
- Timestamp
- Query used
- Results from each scraper
- Complete phone details

Filename format: `data/search_<query>_<timestamp>.json`

### 4. Detailed Display
Results can be displayed with:
- Summary view (just names and prices)
- Detailed view (specs, ratings, URLs)
- Comparison view (side-by-side specs)

## Usage Examples

### Example 1: Find iPhone Models
```python
from universal_search import UniversalSearch

searcher = UniversalSearch()
results = searcher.search_all("iPhone", max_results_per_site=5)

print(f"Found {results['total_found']} iPhones")
```

### Example 2: Get Best Budget Phones
```python
results = searcher.search_all("Realme", max_results_per_site=10)

# Filter by price (if available)
affordable = []
for scraper_data in results['scrapers'].values():
    for phone in scraper_data['phones']:
        if phone.get('price'):
            # Extract numeric price
            price_str = phone['price'].replace(',', '').replace('₹', '')
            try:
                price = float(price_str.split()[0])
                if price < 20000:  # Under 20k INR
                    affordable.append(phone)
            except:
                pass

print(f"Found {len(affordable)} phones under ₹20,000")
```

### Example 3: Compare Specific Models
```python
# Search for specific models
s24_results = searcher.search_all("Samsung S24", max_results_per_site=3)
iphone15_results = searcher.search_all("iPhone 15", max_results_per_site=3)

# Get phones from GSMArena (most detailed specs)
s24_phones = [Phone(**p) for p in s24_results['scrapers']['gsmarena']['phones']]
iphone_phones = [Phone(**p) for p in iphone15_results['scrapers']['gsmarena']['phones']]

# Compare
comparison = searcher.compare_phones(s24_phones + iphone_phones)
```

### Example 4: Get Details from URL
```python
# If you have a specific product URL
phone = searcher.get_phone_details(
    "https://www.gsmarena.com/samsung_galaxy_s24_ultra-12771.php"
)

print(f"Found: {phone.brand} {phone.model}")
print(f"Display: {phone.specs.get('Display')}")
print(f"Camera: {phone.specs.get('Camera')}")
print(f"Battery: {phone.specs.get('Battery')}")
```

### Example 5: Search Multiple Brands
```python
brands = ["Samsung", "Apple", "OnePlus", "Xiaomi", "Google Pixel"]

all_results = {}
for brand in brands:
    results = searcher.search_all(brand, max_results_per_site=5)
    all_results[brand] = results['total_found']

# Display summary
for brand, count in all_results.items():
    print(f"{brand}: {count} phones found")
```

## Output Format

### JSON File Structure
```json
{
  "query": "Samsung S24",
  "timestamp": "2025-11-22T10:30:00",
  "total_found": 15,
  "scrapers": {
    "gsmarena": {
      "status": "success",
      "count": 5,
      "phones": [
        {
          "brand": "Samsung",
          "model": "Galaxy S24 Ultra",
          "price": "N/A",
          "rating": 8.9,
          "specs": {
            "Display": "6.8 inches, Dynamic AMOLED 2X",
            "Chipset": "Snapdragon 8 Gen 3",
            "Camera": "200 MP + 50 MP + 10 MP + 12 MP",
            "Battery": "5000 mAh"
          },
          "url": "https://www.gsmarena.com/...",
          "images": ["https://..."]
        }
      ]
    },
    "91mobiles": {
      "status": "success",
      "count": 3,
      "phones": [...]
    },
    "kimovil": {
      "status": "error",
      "error": "Cloudflare blocked",
      "count": 0,
      "phones": []
    }
  }
}
```

## Search Tips

### 1. Be Specific
- ✅ Good: "Samsung Galaxy S24 Ultra"
- ✅ Good: "iPhone 15 Pro Max"
- ⚠️ Okay: "Samsung S24"
- ❌ Too broad: "Samsung"

### 2. Use Model Names
- ✅ "OnePlus 12"
- ✅ "Pixel 8 Pro"
- ✅ "Xiaomi 14"

### 3. Search by Features (on GSMArena)
- "5000mah battery phone"
- "200mp camera phone"
- "flagship 2024"

### 4. Filter Results in Code
After getting results, you can filter by:
- Price range
- Rating (>4 stars)
- Specific specs (RAM, storage, etc.)
- Brand
- Availability

## Advanced Usage

### Interactive Mode
```python
from universal_search import interactive_search

interactive_search()
```

This launches an interactive CLI where you can:
1. Search for phones
2. Get details from URLs
3. Compare multiple phones

### Custom Scraper Selection
```python
# Search only GSMArena (fastest, most reliable)
searcher = UniversalSearch()
phones = searcher.gsmarena.search_phones("Samsung S24", max_results=10)

# Search only 91mobiles (Indian prices)
phones = searcher.mobiles91.search_phones("iPhone 15", max_results=5)
```

### Batch Processing
```python
import json

queries = ["iPhone 15", "Samsung S24", "OnePlus 12", "Pixel 8"]
all_results = []

for query in queries:
    results = searcher.search_and_save(query, max_results_per_site=3)
    all_results.append(results)

# Save combined results
with open('data/batch_results.json', 'w') as f:
    json.dump(all_results, f, indent=2)
```

## Troubleshooting

### No Results Found
- Try a different query format
- Use fewer/more specific words
- Try searching by model number
- Check internet connection

### Slow Searches
- Reduce `max_results_per_site`
- Skip Kimovil (often blocked)
- Search specific sites only

### Kimovil Blocked
- This is normal due to Cloudflare protection
- GSMArena and 91mobiles usually work fine
- For Kimovil, use direct product URLs

## Performance

Typical search times:
- GSMArena: 5-10 seconds for 5 results
- 91mobiles: 5-15 seconds for 5 results  
- Kimovil: 10-20 seconds (if not blocked)

Total for all 3 sites: ~20-45 seconds for 5 results per site

## Data Storage

All results are saved to `data/` folder:
```
data/
  ├── search_Samsung_S24_20251122_103045.json
  ├── search_iPhone_15_20251122_103210.json
  └── search_OnePlus_12_20251122_103335.json
```

Files include complete phone details and can be:
- Analyzed later
- Compared across searches
- Used for price tracking
- Imported into databases

## Success Rates

Based on testing:
- **GSMArena**: ~95% success rate
- **91mobiles**: ~70-80% success rate
- **Kimovil**: ~10% success rate (Cloudflare protection)

## Next Steps

1. Run `python search.py` to try it out
2. Check `data/` folder for saved results
3. See `examples_search.py` for more code examples
4. Integrate into your own projects

Happy phone hunting! 📱
