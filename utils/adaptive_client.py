"""
Adaptive HTTP client that automatically selects the best bypass method.
Falls back gracefully when advanced tools aren't installed.
"""

import sys
from typing import Optional
import requests as base_requests


class AdaptiveClient:
    """
    Smart HTTP client that tries multiple bypass methods:
    1. curl_cffi (fastest, TLS fingerprinting)
    2. cloudscraper (Cloudflare bypass)
    3. requests (fallback, basic)
    """
    
    def __init__(self, delay_range: tuple = (1, 3)):
        """Initialize adaptive client with best available method."""
        self.delay_range = delay_range
        self.method = self._detect_available_method()
        self.client = self._create_client()
        
        print(f"[AdaptiveClient] Using method: {self.method}")
    
    def _detect_available_method(self) -> str:
        """Detect which bypass tools are available."""
        # Try curl_cffi first (fastest + TLS fingerprinting)
        try:
            import curl_cffi
            return 'curl_cffi'
        except ImportError:
            pass
        
        # Try cloudscraper (Cloudflare specific)
        try:
            import cloudscraper
            return 'cloudscraper'
        except ImportError:
            pass
        
        # Fallback to basic requests
        return 'requests'
    
    def _create_client(self):
        """Create client based on available method."""
        if self.method == 'curl_cffi':
            from curl_cffi import requests as curl_requests
            return curl_requests.Session()
        
        elif self.method == 'cloudscraper':
            import cloudscraper
            return cloudscraper.create_scraper(
                browser={
                    'browser': 'chrome',
                    'platform': 'windows',
                    'desktop': True
                }
            )
        
        else:
            # Use our existing HTTPClient as fallback
            try:
                from utils.http_client import HTTPClient
                return HTTPClient(delay_range=self.delay_range)
            except:
                # Ultimate fallback: basic requests session
                session = base_requests.Session()
                session.headers.update({
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                })
                return session
    
    def get(self, url: str, max_retries: int = 3, **kwargs) -> Optional[base_requests.Response]:
        """
        Unified get method that works with any client type.
        
        Args:
            url: URL to fetch
            max_retries: Maximum retry attempts
            **kwargs: Additional arguments
        
        Returns:
            Response object or None if failed
        """
        try:
            if self.method == 'curl_cffi':
                # curl_cffi with Chrome impersonation
                response = self.client.get(
                    url, 
                    impersonate="chrome120",
                    timeout=30,
                    **kwargs
                )
                return response
            
            elif self.method == 'cloudscraper':
                # cloudscraper handles Cloudflare automatically
                response = self.client.get(url, timeout=30, **kwargs)
                return response
            
            else:
                # Use HTTPClient or basic session
                if hasattr(self.client, 'get'):
                    response = self.client.get(url, max_retries=max_retries, **kwargs)
                    return response
                else:
                    response = self.client.get(url, timeout=30, **kwargs)
                    response.raise_for_status()
                    return response
        
        except Exception as e:
            print(f"[AdaptiveClient] Error with {self.method}: {e}")
            return None
    
    @staticmethod
    def install_instructions():
        """Print installation instructions for bypass tools."""
        print("\n" + "="*60)
        print("To improve success rates, install bypass tools:")
        print("="*60)
        print("\n1. cloudscraper (recommended for Cloudflare):")
        print("   pip install cloudscraper")
        print("\n2. curl_cffi (fastest, TLS fingerprinting):")
        print("   pip install curl_cffi")
        print("\n3. undetected-chromedriver (most powerful):")
        print("   pip install undetected-chromedriver")
        print("\nRestart scraper after installing for auto-detection.")
        print("="*60 + "\n")


# Convenience function
def create_adaptive_client(delay_range=(1, 3)) -> AdaptiveClient:
    """Create an adaptive client with the best available method."""
    return AdaptiveClient(delay_range=delay_range)
