"""
Configuration file demonstrating how the flipkart_scraper approach works.

Key insight from https://crates.io/crates/flipkart_scraper:
The scraper successfully works WITHOUT proxies by using realistic browser headers.

Source: https://docs.rs/flipkart_scraper/latest/src/flipkart_scraper/lib.rs.html#24-45
"""

# ============================================================================
# HOW FLIPKART_SCRAPER AVOIDS BLOCKING (WITHOUT PROXIES)
# ============================================================================

# 1. REALISTIC BROWSER HEADERS
#    Instead of using default library headers, it mimics a real browser
BROWSER_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:138.0) Gecko/20100101 Firefox/138.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',  # Do Not Track
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Cache-Control': 'max-age=0',
}

# 2. ERROR DETECTION
#    Detects when website blocks/challenges the scraper
BOT_DETECTION_INDICATORS = [
    'are you a human?',           # Flipkart's bot challenge
    'retry in',                   # Rate limit message
    'internal server error',      # Server issues
    'has been moved or deleted',  # Invalid page
    'captcha',                    # CAPTCHA challenge
    'cloudflare',                 # Cloudflare protection
]

# 3. SIMPLE HTTP CLIENT
#    Uses standard HTTP library (reqwest in Rust, requests in Python)
#    NO complex proxy rotation or Selenium overhead
HTTP_CLIENT_CONFIG = {
    'timeout': 30,              # 30 second timeout
    'follow_redirects': True,   # Follow redirects
    'verify_ssl': True,         # Verify SSL certificates
}

# 4. HTML PARSING
#    Parses static HTML using DOM selectors (not JavaScript execution)
PARSING_METHOD = 'BeautifulSoup'  # or 'scraper' crate in Rust

# 5. RATE LIMITING (OPTIONAL)
#    Not required by flipkart_scraper but recommended for heavy scraping
RATE_LIMIT_CONFIG = {
    'min_delay': 1,   # Minimum seconds between requests
    'max_delay': 3,   # Maximum seconds between requests
    'random': True,   # Randomize delays to appear human
}

# ============================================================================
# WHY THIS WORKS WITHOUT PROXIES
# ============================================================================
"""
1. MOST WEBSITES DON'T REQUIRE PROXIES
   - GSMArena, 91mobiles, Kimovil don't aggressively block scrapers
   - They mainly check for bot-like behavior (missing headers, high rate)

2. PROPER HEADERS ARE KEY
   - Default Python requests: "python-requests/2.31.0"
   - Real browser: "Mozilla/5.0 (Windows NT 10.0; Win64; x64)..."
   - Websites block obvious bots, not proper headers

3. STATIC HTML SCRAPING
   - These sites serve content in HTML (not heavy JavaScript)
   - No need for Selenium/Playwright for basic product pages
   - Faster and less resource-intensive

4. RESPECTFUL SCRAPING
   - Rate limiting prevents overwhelming servers
   - Session management (cookies) appears more natural
   - Error detection avoids hammering blocked endpoints

5. WHEN YOU MIGHT NEED PROXIES
   - Scraping thousands of pages per hour
   - Getting IP-banned after volume
   - Geographic restrictions
   - Very aggressive anti-bot systems (Google, Amazon)
"""

# ============================================================================
# IMPLEMENTATION COMPARISON
# ============================================================================
"""
FLIPKART_SCRAPER (Rust):
-----------------------
fn build_headers() -> HeaderMap {
    let mut headers = HeaderMap::new();
    headers.insert(
        USER_AGENT,
        HeaderValue::from_static(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:138.0) Gecko/20100101 Firefox/138.0"
        ),
    );
    headers.insert(ACCEPT_LANGUAGE, HeaderValue::from_static("en-US,en;q=0.5"));
    headers.insert(ACCEPT, HeaderValue::from_static("text/html,..."));
    headers
}

OUR IMPLEMENTATION (Python):
----------------------------
def _build_headers(self):
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:138.0)...',
        'Accept': 'text/html,application/xhtml+xml,...',
        'Accept-Language': 'en-US,en;q=0.5',
    }

SAME PRINCIPLE, DIFFERENT LANGUAGE!
"""
