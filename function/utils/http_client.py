"""
HTTP Client with simple headers - based on mobile-specs-api approach.
"""

import requests
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
        # Use shorter timeout when using proxies
        timeout = kwargs.pop('timeout', 15 if 'proxies' in kwargs else 30)
        
        for attempt in range(1, max_retries + 1):
            try:
                response = self.session.get(url, timeout=timeout, **kwargs)
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
                        print(f"❌ HTTP {e.response.status_code} (attempt {attempt}/{max_retries})")
                else:
                    print(f"❌ HTTP error (attempt {attempt}/{max_retries}): {str(e)[:80]}")
                
                if attempt == max_retries:
                    return None
                    
            except (requests.exceptions.Timeout, 
                    requests.exceptions.ConnectionError,
                    requests.exceptions.ProxyError) as e:
                # These errors are common with bad proxies, fail fast
                print(f"❌ Connection error (attempt {attempt}/{max_retries}): {type(e).__name__}")
                if attempt == max_retries:
                    return None
                time.sleep(1)  # Short delay before retry
                    
            except requests.exceptions.RequestException as e:
                print(f"❌ Request error (attempt {attempt}/{max_retries}): {str(e)[:80]}")
                if attempt == max_retries:
                    return None
                time.sleep(random.uniform(1, 3))
        
        return None
    
    def rotate_user_agent(self):
        """Rotate to a new random user agent."""
        # Use fixed user agent since fake_useragent was removed
        pass
