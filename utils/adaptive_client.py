"""
Adaptive HTTP client for Appwrite deployment.
Uses basic HTTP client only for maximum compatibility.
"""

from typing import Optional
import requests as base_requests


class AdaptiveClient:
    """
    HTTP client wrapper that uses the basic HTTPClient.
    Simplified version for Appwrite serverless deployment.
    """
    
    def __init__(self, delay_range: tuple = (1, 3)):
        """Initialize adaptive client with HTTPClient."""
        self.delay_range = delay_range
        self.method = 'requests'
        self.client = self._create_client()
        
        print(f"[AdaptiveClient] Using basic HTTP client for Appwrite")
    
    def _create_client(self):
        """Create basic HTTP client."""
        from utils.http_client import HTTPClient
        return HTTPClient(delay_range=self.delay_range)
    
    def get(self, url: str, max_retries: int = 3, **kwargs) -> Optional[base_requests.Response]:
        """
        Get method using basic HTTP client.
        
        Args:
            url: URL to fetch
            max_retries: Maximum retry attempts
            **kwargs: Additional arguments
        
        Returns:
            Response object or None if failed
        """
        try:
            response = self.client.get(url, max_retries=max_retries, **kwargs)
            return response
        except Exception as e:
            print(f"[AdaptiveClient] Error: {e}")
            return None


# Convenience function
def create_adaptive_client(delay_range=(1, 3)) -> AdaptiveClient:
    """Create an adaptive client with basic HTTP."""
    return AdaptiveClient(delay_range=delay_range)
