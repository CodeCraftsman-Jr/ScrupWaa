# Quick Reference Card

## 🚀 Installation
```powershell
.\setup.ps1              # Run setup script
# OR
pip install -r requirements.txt
```

## 📱 Basic Usage

### GSMArena
```python
from scrapers.gsmarena import GSMArenaScraper

scraper = GSMArenaScraper()

# Search
phones = scraper.search_phones("Samsung S24", max_results=5)

# Direct URL
phone = scraper.scrape_phone("https://www.gsmarena.com/...")
```

### 91mobiles
```python
from scrapers.mobiles91 import Mobiles91Scraper

scraper = Mobiles91Scraper()
phones = scraper.search_phones("iPhone 15", max_results=5)
```

### Kimovil
```python
from scrapers.kimovil import KimovilScraper

scraper = KimovilScraper()
phones = scraper.search_phones("OnePlus 12", max_results=5)

# Get price comparisons
comparisons = scraper.get_price_comparisons(phone_url)
```

## 📊 Phone Data Structure

```python
phone.brand          # "Samsung"
phone.model          # "Galaxy S24 Ultra"
phone.price          # "$1199"
phone.currency       # "USD"
phone.specs          # {"Display": "6.8 inches", ...}
phone.images         # ["url1", "url2", ...]
phone.rating         # 4.5
phone.highlights     # ["120Hz", "200MP Camera", ...]
phone.source         # "gsmarena"

# Export
phone.to_json()      # JSON string
phone.to_dict()      # Dictionary
```

## 🔧 HTTP Client Configuration

```python
from utils.http_client import HTTPClient

# Custom delays
client = HTTPClient(delay_range=(2, 5))

# Make request
response = client.get(url, max_retries=5)

# Rotate user agent
client.rotate_user_agent()
```

## 🎯 Run Examples

```powershell
python main.py           # Full demo
python examples.py       # Usage examples
```

## 📁 Output

Results saved to `data/` folder:
- `gsmarena_results.json`
- `91mobiles_results.json`
- `kimovil_results.json`

## 🛡️ Anti-Blocking Headers

```python
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:138.0)...',
    'Accept': 'text/html,application/xhtml+xml,...',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
}
```

## ⚠️ Troubleshooting

### Getting blocked?
1. Increase delay: `HTTPClient(delay_range=(5, 10))`
2. Rotate user agent: `client.rotate_user_agent()`
3. Check if HTML structure changed

### No results?
1. Verify URL is correct
2. Check website is accessible
3. Run with smaller max_results

### Import errors?
```powershell
pip install -r requirements.txt
```

## 📚 Documentation

- `README.md` - Full documentation
- `HOW_IT_WORKS.md` - How it works without proxies
- `PROJECT_SUMMARY.md` - Complete project overview
- `config.py` - Configuration examples

## 🔗 Inspiration

Based on [flipkart_scraper](https://crates.io/crates/flipkart_scraper) which proves proxies aren't always needed!

## ⚡ Quick Tips

1. **Start small**: Use `max_results=1` when testing
2. **Be patient**: Rate limiting is automatic
3. **Check data**: Verify scraped info before using
4. **Respect ToS**: Use ethically and responsibly
5. **Save results**: Export to JSON for analysis

## 🎨 Example Output

```json
{
  "brand": "Samsung",
  "model": "Galaxy S24 Ultra",
  "price": "$1199",
  "currency": "USD",
  "specs": {
    "Display": "6.8 inches, Dynamic AMOLED 2X",
    "Processor": "Snapdragon 8 Gen 3",
    "RAM": "12GB",
    "Storage": "256GB"
  },
  "rating": 4.6,
  "source": "gsmarena"
}
```

---

**Need help?** Check the documentation files or review `examples.py`
