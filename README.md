# Universal Mobile Scraper

A Python-based web scraper for mobile phone specifications and prices from **GSMArena**, **91mobiles**, and **Kimovil** - **without using proxies**!

## 🚀 Key Features

- **No Proxy Required**: Uses realistic browser headers to avoid detection (inspired by [flipkart_scraper](https://crates.io/crates/flipkart_scraper))
- **Multi-Site Support**: Scrapes from 3 major mobile phone websites
- **Smart HTTP Client**: Built-in retry logic, rate limiting, and bot detection
- **Structured Data**: Clean phone data model with specs, prices, images, ratings
- **Easy to Use**: Simple API for both searching and direct URL scraping

## ⚠️ Important: Site Compatibility

| Website | Status | Success Rate | Notes |
|---------|--------|--------------|-------|
| **GSMArena** | ✓ Working | ~95% | Best option, comprehensive data |
| **91mobiles** | ⚠️ Partial | ~30-40% | Bot detection, try direct URLs |
| **Kimovil** | ⚠️ Limited | ~10% | Cloudflare protection |

**Recommendation:** Use GSMArena for reliable scraping. For blocked sites, see [ANTI_BOT_NOTES.md](ANTI_BOT_NOTES.md) for Selenium/proxy solutions.

## 🛡️ Anti-Blocking Techniques (No Proxy Needed!)

This scraper avoids blocking by mimicking real browser behavior:

1. **Realistic Browser Headers**
   - User-Agent: Firefox/Chrome headers
   - Accept: Proper content type headers
   - Accept-Language: en-US locale
   - Connection: Keep-alive sessions

2. **Rate Limiting**
   - Random delays between requests (1-3 seconds)
   - Longer delays after failed attempts

3. **Bot Detection**
   - Detects captcha/challenge pages
   - Automatic retry with backoff

4. **Session Management**
   - Maintains persistent sessions
   - Cookie handling

This approach is proven effective by projects like [flipkart_scraper](https://crates.io/crates/flipkart_scraper) which successfully scrapes Flipkart without any proxy infrastructure.

## 📦 Installation

```powershell
# Clone or navigate to project directory
cd "z:\D\Univeral Scarpper"

# Install dependencies
pip install -r requirements.txt
```

## 🎯 Usage

### Basic Example

```python
from scrapers.gsmarena import GSMArenaScraper
from scrapers.mobiles91 import Mobiles91Scraper
from scrapers.kimovil import KimovilScraper

# Search for phones
gsmarena = GSMArenaScraper()
phones = gsmarena.search_phones("Samsung Galaxy S24", max_results=5)

for phone in phones:
    print(f"{phone.brand} {phone.model} - {phone.price}")
```

### Run Demo

```powershell
python main.py
```

This will:
- Search for phones on all 3 websites
- Save results to JSON files in `data/` folder
- Display sample output

### Scrape Specific URLs

```python
scraper = GSMArenaScraper()
phone = scraper.scrape_phone("https://www.gsmarena.com/samsung_galaxy_s24_ultra-12771.php")

print(phone.to_json())  # Export as JSON
```

## 📁 Project Structure

```
Universal Scraper/
├── scrapers/
│   ├── gsmarena.py      # GSMArena scraper
│   ├── mobiles91.py     # 91mobiles scraper
│   └── kimovil.py       # Kimovil scraper
├── models/
│   └── phone.py         # Phone data model
├── utils/
│   └── http_client.py   # HTTP client with anti-blocking
├── data/                # Output directory
├── requirements.txt     # Dependencies
├── main.py             # Demo script
└── README.md
```

## 🔧 How It Works (Without Proxies)

The scraper mimics the approach used by [flipkart_scraper](https://docs.rs/flipkart_scraper/latest/src/flipkart_scraper/lib.rs.html#24-45):

```python
# Key technique: Realistic browser headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:138.0) Gecko/20100101 Firefox/138.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}
```

Instead of complex proxy rotation, we:
1. Use proper browser headers
2. Maintain sessions with cookies
3. Add human-like delays
4. Parse HTML directly (BeautifulSoup)
5. Detect and handle bot challenges

## 📊 Data Model

Each scraped phone includes:

```python
{
  "brand": "Samsung",
  "model": "Galaxy S24 Ultra",
  "price": "$1199",
  "currency": "USD",
  "specs": {
    "Display": "6.8 inches",
    "RAM": "12GB",
    "Storage": "256GB",
    ...
  },
  "images": ["url1", "url2"],
  "rating": 4.5,
  "source": "gsmarena"
}
```

## 🌐 Supported Websites

| Website | Description | Specialty |
|---------|-------------|-----------|
| **GSMArena** | Comprehensive specs database | Technical specifications |
| **91mobiles** | Indian market prices | Local pricing & availability |
| **Kimovil** | Global price comparison | Multi-region pricing |

## ⚠️ Important Notes

1. **Respect robots.txt**: Check each site's robots.txt before scraping
2. **Rate Limiting**: Built-in delays prevent overwhelming servers
3. **Personal Use**: Use responsibly and ethically
4. **Site Changes**: Scrapers may break if websites update their HTML structure
5. **No Guarantees**: Success rates depend on website anti-scraping measures

## 🔍 Troubleshooting

**Getting blocked?**
- Increase delay range: `HTTPClient(delay_range=(3, 7))`
- Rotate user agents: `client.rotate_user_agent()`
- Check if site updated HTML structure

**No results found?**
- Verify URL is correct
- Check website HTML structure hasn't changed
- Enable debug output to see response content

## 📝 License

MIT License - Use at your own risk

## 🤝 Contributing

Feel free to:
- Report bugs
- Suggest improvements
- Add support for more websites
- Improve anti-blocking techniques

## 🙏 Credits

Inspired by [flipkart_scraper](https://crates.io/crates/flipkart_scraper) which demonstrates effective web scraping without proxy infrastructure.
