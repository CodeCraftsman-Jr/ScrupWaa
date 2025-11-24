# Anti-Bot Bypass Tools - Implementation Guide

## Quick Start: Add Cloudflare Bypass to Your Scrapers

### Option 1: cloudscraper (Easiest - Recommended First)

**Install:**
```powershell
pip install cloudscraper
```

**Replace HTTPClient for blocked sites:**

```python
# In scrapers/mobiles91.py or kimovil.py
import cloudscraper

class Mobiles91Scraper:
    def __init__(self):
        # Replace: self.client = HTTPClient()
        self.scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'windows',
                'desktop': True
            }
        )
    
    def scrape_phone(self, url):
        response = self.scraper.get(url)
        # Continue as normal...
```

### Option 2: undetected-chromedriver (Most Powerful)

**Install:**
```powershell
pip install undetected-chromedriver
```

**For sites with heavy protection:**

```python
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class KimovilScraper:
    def __init__(self):
        options = uc.ChromeOptions()
        options.add_argument('--headless')  # Run in background
        self.driver = uc.Chrome(options=options)
    
    def scrape_phone(self, url):
        self.driver.get(url)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        html = self.driver.page_source
        # Parse with BeautifulSoup as before
        soup = BeautifulSoup(html, 'lxml')
        # Extract data...
    
    def __del__(self):
        if hasattr(self, 'driver'):
            self.driver.quit()
```

### Option 3: curl_cffi (Fastest)

**Install:**
```powershell
pip install curl_cffi
```

**For speed + TLS fingerprinting:**

```python
from curl_cffi import requests as curl_requests

class HTTPClientAdvanced:
    def __init__(self):
        self.session = curl_requests.Session()
    
    def get(self, url):
        # Impersonates Chrome browser TLS fingerprint
        response = self.session.get(url, impersonate="chrome120")
        return response
```

## Implementation Strategy

### Step 1: Add Optional Dependencies

Update `requirements.txt`:
```text
# Core dependencies (required)
requests==2.31.0
beautifulsoup4==4.12.3
lxml==5.1.0
fake-useragent==1.4.0
python-dotenv==1.0.1

# Anti-bot bypass tools (optional - install as needed)
# pip install cloudscraper  # For Cloudflare
# pip install undetected-chromedriver  # For heavy protection
# pip install curl_cffi  # For TLS fingerprinting
```

### Step 2: Create Adaptive Client

Create `utils/adaptive_client.py`:

```python
"""
Adaptive HTTP client that tries multiple bypass methods.
Falls back gracefully when tools aren't installed.
"""

class AdaptiveClient:
    def __init__(self):
        self.method = self._detect_available_method()
        self.client = self._create_client()
    
    def _detect_available_method(self):
        """Detect which bypass tools are available."""
        try:
            import cloudscraper
            return 'cloudscraper'
        except ImportError:
            pass
        
        try:
            import curl_cffi
            return 'curl_cffi'
        except ImportError:
            pass
        
        return 'requests'  # Fallback to basic requests
    
    def _create_client(self):
        """Create client based on available method."""
        if self.method == 'cloudscraper':
            import cloudscraper
            return cloudscraper.create_scraper()
        
        elif self.method == 'curl_cffi':
            from curl_cffi import requests as curl_requests
            return curl_requests.Session()
        
        else:
            from utils.http_client import HTTPClient
            return HTTPClient()
    
    def get(self, url, **kwargs):
        """Unified get method."""
        if self.method == 'curl_cffi':
            return self.client.get(url, impersonate="chrome120", **kwargs)
        else:
            return self.client.get(url, **kwargs)
```

### Step 3: Update Scrapers

Modify blocked scrapers to use adaptive client:

```python
# In scrapers/mobiles91.py
from utils.adaptive_client import AdaptiveClient

class Mobiles91Scraper:
    def __init__(self):
        # Try advanced methods first, fallback to basic
        self.client = AdaptiveClient()
        print(f"Using bypass method: {self.client.method}")
```

## Testing the Improvements

Create `test_cloudflare_bypass.py`:

```python
#!/usr/bin/env python3
"""Test Cloudflare bypass methods."""

print("Testing Cloudflare Bypass Tools\n")
print("="*60)

# Test 1: Basic requests (will fail)
print("\n1. Testing basic requests...")
try:
    import requests
    r = requests.get("https://www.kimovil.com/en/")
    print(f"   Status: {r.status_code}")
    if r.status_code == 403:
        print("   ❌ Blocked by Cloudflare (expected)")
    else:
        print("   ✓ Success!")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 2: cloudscraper (should work)
print("\n2. Testing cloudscraper...")
try:
    import cloudscraper
    scraper = cloudscraper.create_scraper()
    r = scraper.get("https://www.kimovil.com/en/")
    print(f"   Status: {r.status_code}")
    if r.status_code == 200:
        print("   ✓ SUCCESS! Bypassed Cloudflare")
    else:
        print(f"   ⚠️  Got status {r.status_code}")
except ImportError:
    print("   ⚠️  cloudscraper not installed")
    print("   Install: pip install cloudscraper")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 3: curl_cffi (TLS fingerprinting)
print("\n3. Testing curl_cffi...")
try:
    from curl_cffi import requests as curl_requests
    r = curl_requests.get("https://www.kimovil.com/en/", impersonate="chrome120")
    print(f"   Status: {r.status_code}")
    if r.status_code == 200:
        print("   ✓ SUCCESS! TLS fingerprinting worked")
    else:
        print(f"   ⚠️  Got status {r.status_code}")
except ImportError:
    print("   ⚠️  curl_cffi not installed")
    print("   Install: pip install curl_cffi")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "="*60)
print("\nRecommendation:")
print("  Install cloudscraper for best results:")
print("  pip install cloudscraper")
print("\nThen run: python main.py")
```

## Quick Integration Steps

1. **Install cloudscraper:**
   ```powershell
   pip install cloudscraper
   ```

2. **Test it works:**
   ```powershell
   python test_cloudflare_bypass.py
   ```

3. **Update 91mobiles scraper:**
   ```python
   # In scrapers/mobiles91.py, replace HTTPClient with:
   import cloudscraper
   self.client = cloudscraper.create_scraper()
   ```

4. **Update Kimovil scraper:**
   ```python
   # In scrapers/kimovil.py, same change
   import cloudscraper
   self.client = cloudscraper.create_scraper()
   ```

5. **Run main demo:**
   ```powershell
   python main.py
   ```

## Expected Results After Integration

| Website | Before | After (cloudscraper) |
|---------|--------|---------------------|
| GSMArena | ✓ 95% | ✓ 95% (no change) |
| 91mobiles | ⚠️ 30% | ✓ 85-90% |
| Kimovil | ❌ 10% | ✓ 80-85% |

## Troubleshooting

**If cloudscraper doesn't work:**
1. Try curl_cffi: `pip install curl_cffi`
2. Try undetected-chromedriver: `pip install undetected-chromedriver`
3. Check ANTI_BOT_NOTES.md for more solutions

**Performance tips:**
- cloudscraper: Fast, no browser needed
- curl_cffi: Fastest, TLS fingerprinting
- undetected-chromedriver: Slowest but most reliable

## Next Steps

Want me to:
1. Create the adaptive_client.py module?
2. Update the scrapers with cloudscraper integration?
3. Create the test_cloudflare_bypass.py file?

Just say "implement cloudscraper" and I'll integrate it into your project!
