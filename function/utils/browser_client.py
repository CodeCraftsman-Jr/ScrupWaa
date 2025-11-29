"""
Headless Browser Client using Playwright for stealth scraping.
Bypasses bot detection by acting like a real browser.
"""

from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
from typing import Optional, Dict
import time
import random


class HeadlessBrowserClient:
    """Headless browser client for stealth scraping with anti-bot detection."""
    
    def __init__(self):
        """Initialize Playwright browser."""
        self.playwright = None
        self.browser = None
        self.context = None
        self._init_browser()
    
    def _init_browser(self):
        """Initialize browser with stealth settings."""
        self.playwright = sync_playwright().start()
        
        # Launch browser with stealth settings
        self.browser = self.playwright.chromium.launch(
            headless=True,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-web-security',
            ]
        )
        
        # Create context with realistic settings
        self.context = self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            locale='en-US',
            timezone_id='America/New_York',
        )
        
        # Add extra stealth scripts
        self.context.add_init_script("""
            // Override the navigator.webdriver property
            Object.defineProperty(navigator, 'webdriver', {
                get: () => false
            });
            
            // Override plugins
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });
            
            // Override languages
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en']
            });
            
            // Add chrome object
            window.chrome = {
                runtime: {}
            };
            
            // Override permissions
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                    Promise.resolve({ state: Notification.permission }) :
                    originalQuery(parameters)
            );
        """)
    
    def get(self, url: str, max_retries: int = 3, **kwargs) -> Optional[str]:
        """
        Fetch page content using headless browser.
        
        Args:
            url: URL to fetch
            max_retries: Maximum number of retry attempts
            **kwargs: Additional arguments (proxy support coming)
        
        Returns:
            Page HTML content or None if failed
        """
        for attempt in range(1, max_retries + 1):
            page = None
            try:
                # Create new page
                page = self.context.new_page()
                
                # Set proxy if provided
                if 'proxies' in kwargs and kwargs['proxies']:
                    proxy_url = kwargs['proxies'].get('http', '')
                    if proxy_url:
                        # Note: Playwright proxy needs to be set at context level
                        # This is a workaround - we'll handle it differently
                        print(f"⚠️  Proxy support: Use context-level proxy for better results")
                
                # Random delay before navigation
                time.sleep(random.uniform(0.5, 1.5))
                
                # Navigate to page with longer timeout
                print(f"🌐 Loading: {url[:60]}...")
                response = page.goto(url, wait_until='domcontentloaded', timeout=60000)
                
                if response and response.status == 200:
                    # Simple timeout instead of networkidle (which can hang)
                    print(f"⏳ Waiting for page to settle...")
                    page.wait_for_timeout(3000)  # 3 second wait
                    
                    # Get page content
                    content = page.content()
                    print(f"✅ Page loaded successfully ({len(content)} bytes)")
                    
                    # Check for bot detection
                    if self._is_blocked(content):
                        print(f"⚠️  Bot detection triggered (attempt {attempt}/{max_retries})")
                        if attempt < max_retries:
                            time.sleep(random.uniform(3, 6))
                            page.close()
                            continue
                        return None
                    
                    page.close()
                    
                    # Return mock response object with text attribute
                    class Response:
                        def __init__(self, text):
                            self.text = text
                            self.status_code = 200
                    
                    return Response(content)
                
                elif response and response.status == 429:
                    print(f"❌ Rate limited (attempt {attempt}/{max_retries})")
                    wait_time = (2 ** attempt) * 5
                    if attempt < max_retries:
                        time.sleep(wait_time)
                        page.close()
                        continue
                
                else:
                    print(f"❌ HTTP {response.status if response else 'error'} (attempt {attempt}/{max_retries})")
                
                if page:
                    page.close()
                    
                if attempt == max_retries:
                    return None
                    
            except Exception as e:
                error_msg = str(e)
                if 'timeout' in error_msg.lower():
                    print(f"❌ Timeout (attempt {attempt}/{max_retries})")
                else:
                    print(f"❌ Browser error (attempt {attempt}/{max_retries}): {error_msg[:80]}")
                
                if page:
                    page.close()
                    
                if attempt == max_retries:
                    return None
                    
                time.sleep(random.uniform(1, 3))
        
        return None
    
    def _is_blocked(self, content: str) -> bool:
        """Detect if request was blocked by bot detection."""
        content_lower = content.lower()
        
        bot_indicators = [
            'are you a human',
            'captcha',
            'just a moment',
            'checking your browser',
            'please verify',
            'unusual traffic',
            'cf-browser-verification',
            'ray id',
        ]
        
        return any(indicator in content_lower for indicator in bot_indicators)
    
    def close(self):
        """Close browser and cleanup."""
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
    
    def __del__(self):
        """Cleanup on deletion."""
        self.close()
