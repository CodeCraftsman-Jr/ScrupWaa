"""
HTTP Client with realistic browser headers to avoid blocking.
Mimics the approach used by flipkart_scraper (no proxy needed).
"""

import requests
from fake_useragent import UserAgent
from typing import Optional, Dict
import time
import random


class HTTPClient:
    """HTTP client with anti-blocking features using realistic browser headers."""
    
    def __init__(self, delay_range: tuple = (1, 3)):
        """
        Initialize HTTP client with session and realistic headers.
        
        Args:
            delay_range: Tuple of (min, max) seconds to wait between requests
        """
        self.session = requests.Session()
        self.ua = UserAgent()
        self.delay_range = delay_range
        
        # Set realistic browser headers (similar to flipkart_scraper approach)
        self.session.headers.update(self._build_headers())
    
    def _build_headers(self) -> Dict[str, str]:
        """
        Build realistic browser headers that mimic Firefox/Chrome.
        This is the KEY to avoiding blocks without proxies.
        Enhanced to bypass Cloudflare and similar protections.
        """
        return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Cache-Control': 'max-age=0',
        }
    
    def get(self, url: str, max_retries: int = 3, **kwargs) -> Optional[requests.Response]:
        """
        Make GET request with automatic retries and rate limiting.
        
        Args:
            url: URL to fetch
            max_retries: Maximum number of retry attempts
            **kwargs: Additional arguments to pass to requests.get()
        
        Returns:
            Response object or None if all retries failed
        """
        for attempt in range(max_retries):
            try:
                # Add random delay between requests to appear more human-like
                if attempt > 0:
                    delay = random.uniform(*self.delay_range)
                    time.sleep(delay)
                
                # Add referer header dynamically if not provided
                if 'headers' not in kwargs:
                    kwargs['headers'] = {}
                
                # Set referer to make request look more natural
                if 'Referer' not in kwargs['headers']:
                    from urllib.parse import urlparse
                    parsed = urlparse(url)
                    kwargs['headers']['Referer'] = f"{parsed.scheme}://{parsed.netloc}/"
                
                response = self.session.get(url, timeout=30, **kwargs)
                
                # Check for bot detection
                if self._is_blocked(response):
                    print(f"⚠️  Bot detection triggered on attempt {attempt + 1}/{max_retries}")
                    if attempt < max_retries - 1:
                        time.sleep(random.uniform(5, 10))  # Longer delay before retry
                        continue
                    return None
                
                response.raise_for_status()
                return response
                
            except requests.exceptions.HTTPError as e:
                # Don't print 403/401 as request errors - they're bot detection
                if e.response.status_code in [403, 401]:
                    print(f"⚠️  Access denied (attempt {attempt + 1}/{max_retries}) - Website blocking scraper")
                else:
                    print(f"❌ Request error (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt == max_retries - 1:
                    return None
            except requests.exceptions.RequestException as e:
                print(f"❌ Request error (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt == max_retries - 1:
                    return None
        
        return None
    
    def _is_blocked(self, response: requests.Response) -> bool:
        """
        Detect if the request was blocked or challenged.
        Similar to flipkart_scraper's error detection.
        """
        content = response.text.lower()
        
        # Common bot detection indicators
        bot_indicators = [
            'are you a human',
            'captcha',
            'access denied',
            'just a moment',  # Cloudflare
            'checking your browser',  # Cloudflare
            'please verify',
            'unusual traffic',
            'robot',
            'cf-browser-verification',  # Cloudflare
            'ray id',  # Cloudflare error
        ]
        
        return any(indicator in content for indicator in bot_indicators)
    
    def rotate_user_agent(self):
        """Rotate to a new random user agent."""
        self.session.headers['User-Agent'] = self.ua.random
