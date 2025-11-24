# 📦 Detailed Product Search - Complete Information Format

## Overview

Get **COMPLETE** product information in a structured format similar to Flipkart API. Every detail about phones including specifications, offers, images, seller info, and more.

## Quick Start

### Command Line:
```bash
python search_detailed.py Samsung Galaxy S24
```

Or using batch file:
```bash
search_detailed.bat iPhone 15 Pro
```

### Python Code:
```python
from universal_search import UniversalSearch
from format_results import format_detailed_results

searcher = UniversalSearch()
results = searcher.search_all("Samsung S24", max_results_per_site=5)

# Convert to detailed format
detailed = format_detailed_results(results)

# Save to file
import json
with open('data/detailed_output.json', 'w') as f:
    json.dump(detailed, f, indent=2)
```

## Output Format

### JSON Structure:
```json
{
  "total_result": 22,
  "query": "samsung",
  "query_params": {
    "page_number": null,
    "sort": null,
    "min_price": null,
    "max_price": null,
    "others": null
  },
  "timestamp": "2025-11-22T10:30:00",
  "result": [
    {
      "name": "Samsung Galaxy S24 Ultra",
      "link": "https://www.gsmarena.com/samsung_galaxy_s24_ultra-12771.php",
      "current_price": "$1,199",
      "original_price": "$1,299",
      "discounted": true,
      "thumbnail": "https://...",
      "query_url": "https://...",
      "rating": 8.9,
      "in_stock": true,
      "f_assured": false,
      "source": "gsmarena",
      
      "seller": {
        "seller_name": "GSMArena",
        "seller_rating": null
      },
      
      "highlights": [
        "6.8 inch Dynamic AMOLED 2X display",
        "200MP main camera",
        "5000mAh battery",
        "Snapdragon 8 Gen 3"
      ],
      
      "offers": [
        {
          "offer_type": "Bank Offer",
          "description": "5% cashback on credit cards"
        }
      ],
      
      "specs": [
        {
          "title": "Display",
          "details": [
            {
              "property": "Type",
              "value": "Dynamic AMOLED 2X, 120Hz, HDR10+"
            },
            {
              "property": "Size",
              "value": "6.8 inches"
            },
            {
              "property": "Resolution",
              "value": "1440 x 3120 pixels"
            }
          ]
        },
        {
          "title": "Platform",
          "details": [
            {
              "property": "OS",
              "value": "Android 14, One UI 6.1"
            },
            {
              "property": "Chipset",
              "value": "Snapdragon 8 Gen 3"
            },
            {
              "property": "CPU",
              "value": "Octa-core"
            }
          ]
        },
        {
          "title": "Memory",
          "details": [
            {
              "property": "RAM",
              "value": "12GB"
            },
            {
              "property": "Internal",
              "value": "256GB / 512GB / 1TB"
            }
          ]
        },
        {
          "title": "Main Camera",
          "details": [
            {
              "property": "Quad",
              "value": "200 MP + 50 MP + 10 MP + 12 MP"
            },
            {
              "property": "Features",
              "value": "LED flash, auto-HDR, panorama"
            },
            {
              "property": "Video",
              "value": "8K@30fps, 4K@60fps"
            }
          ]
        },
        {
          "title": "Selfie Camera",
          "details": [
            {
              "property": "Single",
              "value": "12 MP"
            },
            {
              "property": "Video",
              "value": "4K@60fps"
            }
          ]
        },
        {
          "title": "Battery",
          "details": [
            {
              "property": "Type",
              "value": "Li-Ion 5000 mAh, non-removable"
            },
            {
              "property": "Charging",
              "value": "45W wired, 15W wireless"
            }
          ]
        }
      ],
      
      "all_thumbnails": [
        "https://image1.jpg",
        "https://image2.jpg",
        "https://image3.jpg",
        "https://image4.jpg"
      ]
    }
  ]
}
```

## What You Get

### For Each Phone:

#### 1. Basic Information
- **name**: Full phone name
- **link**: Direct product URL
- **source**: Data source (gsmarena/91mobiles/kimovil)
- **query_url**: Original query URL

#### 2. Pricing
- **current_price**: Current selling price
- **original_price**: MRP/Original price (if available)
- **discounted**: Boolean - is product on sale?

#### 3. Images
- **thumbnail**: Main product image
- **all_thumbnails**: Array of all available images
  - Multiple angles
  - Different colors
  - High resolution

#### 4. Ratings
- **rating**: User rating (out of 5 or 10)
- **in_stock**: Availability status

#### 5. Seller Information
- **seller_name**: Seller/Source name
- **seller_rating**: Seller rating (if available)
- **f_assured**: Flipkart Assured equivalent

#### 6. Highlights
Array of key features:
- Display size and type
- Main camera specs
- Battery capacity
- Processor name
- Special features

#### 7. Offers
Array of available offers:
```json
{
  "offer_type": "Bank Offer",
  "description": "5% cashback on Axis Bank cards"
}
```

#### 8. Detailed Specifications
Nested array with categories:
- **Display**: Size, type, resolution, refresh rate
- **Platform**: OS, chipset, CPU, GPU
- **Memory**: RAM, internal storage
- **Main Camera**: All camera specs
- **Selfie Camera**: Front camera details
- **Sound**: Audio features
- **Comms**: Connectivity (WiFi, Bluetooth, NFC)
- **Battery**: Capacity and charging
- **General**: Other specifications

## Usage Examples

### Example 1: Get Detailed Info for One Phone
```python
from universal_search import UniversalSearch
from format_results import format_detailed_results

searcher = UniversalSearch()
results = searcher.search_all("Samsung S24 Ultra", max_results_per_site=1)
detailed = format_detailed_results(results)

# Get first phone
if detailed['result']:
    phone = detailed['result'][0]
    print(f"Name: {phone['name']}")
    print(f"Price: {phone['current_price']}")
    print(f"Rating: {phone['rating']}")
    print(f"\nSpecifications:")
    for category in phone['specs']:
        print(f"\n{category['title']}:")
        for spec in category['details']:
            print(f"  {spec['property']}: {spec['value']}")
```

### Example 2: Compare Multiple Phones
```python
queries = ["Samsung S24", "iPhone 15", "OnePlus 12"]

all_phones = []
for query in queries:
    results = searcher.search_all(query, max_results_per_site=1)
    detailed = format_detailed_results(results)
    if detailed['result']:
        all_phones.append(detailed['result'][0])

# Compare specifications
for phone in all_phones:
    print(f"\n{phone['name']}:")
    print(f"  Price: {phone['current_price']}")
    print(f"  Rating: {phone['rating']}")
    
    # Find battery spec
    for category in phone['specs']:
        if category['title'] == 'Battery':
            for spec in category['details']:
                if 'Type' in spec['property']:
                    print(f"  Battery: {spec['value']}")
```

### Example 3: Extract All Images
```python
results = searcher.search_all("Samsung S24", max_results_per_site=3)
detailed = format_detailed_results(results)

for phone in detailed['result']:
    print(f"\n{phone['name']}:")
    print(f"Images: {len(phone['all_thumbnails'])}")
    for i, img_url in enumerate(phone['all_thumbnails'], 1):
        print(f"  {i}. {img_url}")
```

### Example 4: Find Best Deals
```python
results = searcher.search_all("flagship phones", max_results_per_site=10)
detailed = format_detailed_results(results)

deals = []
for phone in detailed['result']:
    if phone['discounted'] and phone['current_price']:
        deals.append({
            'name': phone['name'],
            'current': phone['current_price'],
            'original': phone['original_price'],
            'source': phone['source']
        })

# Sort by discount
for deal in sorted(deals, key=lambda x: x['name']):
    print(f"{deal['name']}: {deal['current']} (was {deal['original']})")
```

### Example 5: Get Specific Specifications
```python
def get_spec_value(phone, category_name, property_name):
    """Extract specific spec value from phone data."""
    for category in phone.get('specs', []):
        if category['title'] == category_name:
            for detail in category['details']:
                if property_name.lower() in detail['property'].lower():
                    return detail['value']
    return None

# Usage
results = searcher.search_all("Samsung S24", max_results_per_site=1)
detailed = format_detailed_results(results)

if detailed['result']:
    phone = detailed['result'][0]
    
    display = get_spec_value(phone, 'Display', 'Size')
    camera = get_spec_value(phone, 'Main Camera', 'Quad')
    battery = get_spec_value(phone, 'Battery', 'Type')
    
    print(f"Display: {display}")
    print(f"Camera: {camera}")
    print(f"Battery: {battery}")
```

## Advantages

### 1. Complete Information
- All specifications in one place
- Structured and organized
- Easy to parse programmatically

### 2. Multiple Sources
- Data from 3 different websites
- Cross-reference information
- More complete picture

### 3. Standard Format
- Consistent JSON structure
- Easy integration with other systems
- Compatible with existing tools

### 4. Rich Metadata
- Offers and deals
- Seller information
- Multiple images
- Ratings and reviews

## Command Line Usage

### Simple Search:
```bash
python search_detailed.py Samsung
```

### With Arguments:
```bash
python search_detailed.py iPhone 15 Pro Max
```

### Batch File (Windows):
```bash
search_detailed.bat OnePlus 12
```

## Output Files

Files are saved to `data/` folder with format:
```
data/detailed_<query>_<timestamp>.json
```

Examples:
```
data/detailed_Samsung_S24_20251122_103045.json
data/detailed_iPhone_15_20251122_104210.json
```

## Tips

### 1. Get More Details
Use fewer results per site but process them thoroughly:
```bash
python search_detailed.py "Samsung S24" 
# Enter: 3 results per site
```

### 2. Save for Later Analysis
All data is saved in JSON format for:
- Price tracking over time
- Specification comparison
- Market analysis
- Database import

### 3. Extract Specific Data
Use Python to extract exactly what you need:
```python
# Get only phones with 200MP camera
high_res = []
for phone in detailed['result']:
    for category in phone['specs']:
        if category['title'] == 'Main Camera':
            for spec in category['details']:
                if '200' in spec['value'] and 'MP' in spec['value']:
                    high_res.append(phone)
```

## Summary

**You now have a complete product information system** that:
- ✅ Extracts ALL specifications in structured format
- ✅ Gets pricing, images, ratings, offers
- ✅ Organizes data like Flipkart API
- ✅ Saves in standard JSON format
- ✅ Easy to use from command line or Python
- ✅ Perfect for integration with other tools

**Start getting detailed product info:**
```bash
python search_detailed.py Samsung Galaxy S24
```
