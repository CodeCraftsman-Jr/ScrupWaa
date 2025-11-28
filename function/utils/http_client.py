"""
HTTP Client with simple headers - based on mobile-specs-api approach.
"""

import requests
from fake_useragent import UserAgent
from typing import Optional, Dict
import time
import random


class HTTPClient:
    """Simple HTTP client for scraping."""
    
    def __init__(self, delay_range: tuple = (2, 5)):
        """
        Initialize HTTP client with session and simple headers.
        
        Args:
            delay_range: Tuple of (min, max) seconds to wait between requests
        """
        self.session = requests.Session()
        self.ua = UserAgent()
        self.delay_range = delay_range
        
        # Set simple browser headers (mobile-specs-api approach)
        self.session.headers.update(self._build_headers())
    
    def _build_headers(self) -> Dict[str, str]:
        """
        Build simple browser headers - minimal approach that works.
        """
        return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
    
    def get(self, url: str, max_retries: int = 3, **kwargs) -> Optional[requests.Response]:
        """
        Make GET request with automatic retries and rate limiting.
        Simplified approach based on mobile-specs-api.
        Supports proxy injection via kwargs['proxies']
        
        Args:
            url: URL to fetch
            max_retries: Maximum number of retry attempts
            **kwargs: Additional arguments to pass to requests.get()
                     Can include 'proxies' dict for proxy support
        
        Returns:
            Response object or None if all retries failed
        """
        for attempt in range(1, max_retries + 1):
            try:
                # Log if using proxy
                if 'proxies' in kwargs and kwargs['proxies']:
                    proxy_str = kwargs['proxies'].get('http', 'Unknown')
                    # Mask credentials in log
                    if '@' in proxy_str:
                        proxy_str = proxy_str.split('@')[1] if '@' in proxy_str else proxy_str
                    print(f"🔒 Request via proxy: {proxy_str[:50]}")
                
                response = self.session.get(url, timeout=30, **kwargs)
                response.raise_for_status()
                return response
                
            except requests.exceptions.HTTPError as e:
                if hasattr(e, 'response') and e.response is not None:
                    if e.response.status_code == 429:
                        # Rate limited - wait longer with exponential backoff
                        wait_time = (2 ** attempt) * 5  # 10s, 20s, 40s
                        print(f"❌ Rate limited (attempt {attempt}/{max_retries}) - Waiting {wait_time}s...")
                        if attempt < max_retries:
                            time.sleep(wait_time)
                            continue
                    elif e.response.status_code in [403, 401]:
                        print(f"⚠️  Access denied (attempt {attempt}/{max_retries})")
                    else:
                        print(f"❌ HTTP error (attempt {attempt}/{max_retries}): {e}")
                else:
                    print(f"❌ HTTP error (attempt {attempt}/{max_retries}): {e}")
                
                if attempt == max_retries:
                    return None
                    
            except requests.exceptions.RequestException as e:
                print(f"❌ Request error (attempt {attempt}/{max_retries}): {e}")
                if attempt == max_retries:
                    return None
                time.sleep(random.uniform(2, 5))
        
        return None
    
    def rotate_user_agent(self):
        """Rotate to a new random user agent."""
        self.session.headers['User-Agent'] = self.ua.random
