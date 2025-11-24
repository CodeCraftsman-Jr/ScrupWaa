"""
Kimovil scraper for mobile phone price comparisons across regions.
"""

from bs4 import BeautifulSoup
from typing import Optional, List
import re

from utils.adaptive_client import AdaptiveClient
from models.phone import Phone


class KimovilScraper:
    """Scraper for Kimovil website with Cloudflare bypass."""
    
    BASE_URL = "https://www.kimovil.com"
    
    def __init__(self):
        # Use AdaptiveClient for automatic Cloudflare bypass
        self.client = AdaptiveClient()
    
    def scrape_phone(self, url: str) -> Optional[Phone]:
        """
        Scrape a single phone from Kimovil product page.
        
        Args:
            url: Full URL to Kimovil phone page
            
        Returns:
            Phone object or None if scraping failed
        """
        print(f"[SCRAPING] Scraping Kimovil: {url}")
        
        response = self.client.get(url)
        if not response:
            print("[FAILED] Failed to fetch page")
            return None
        
        soup = BeautifulSoup(response.text, 'lxml')
        
        # Extract basic information
        brand, model = self._extract_brand_model(soup)
        if not brand or not model:
            print("[FAILED] Could not extract brand/model")
            return None
        
        phone = Phone(
            brand=brand,
            model=model,
            url=url,
            source="kimovil"
        )
        
        # Extract price (multiple currencies/regions)
        phone.price, phone.currency = self._extract_price(soup)
        
        # Extract images
        phone.images = self._extract_images(soup)
        if phone.images:
            phone.thumbnail = phone.images[0]
        
        # Extract specifications
        phone.specs = self._extract_specifications(soup)
        
        # Extract rating
        phone.rating = self._extract_rating(soup)
        
        # Extract highlights
        phone.highlights = self._extract_highlights(soup)
        
        # Extract description
        phone.description = self._extract_description(soup)
        
        print(f"[SUCCESS] Successfully scraped: {phone.brand} {phone.model}")
        return phone
    
    def _extract_brand_model(self, soup: BeautifulSoup) -> tuple:
        """Extract brand and model name."""
        # Try h1 with product title
        title = soup.find('h1', class_='pricing-title')
        if not title:
            title = soup.find('h1')
        
        if title:
            text = title.get_text(strip=True)
            # Usually format is "Brand Model"
            parts = text.split(maxsplit=1)
            if len(parts) >= 2:
                return parts[0], parts[1]
            elif len(parts) == 1:
                return "Unknown", parts[0]
        
        return None, None
    
    def _extract_price(self, soup: BeautifulSoup) -> tuple:
        """Extract price and currency from best offer."""
        price = None
        currency = "USD"
        
        # Look for price offers section
        price_section = soup.find('div', class_='pricing-price-best-section')
        if not price_section:
            price_section = soup.find('div', class_=re.compile(r'price'))
        
        if price_section:
            # Find price amount
            price_elem = price_section.find(class_=re.compile(r'pricing-price-value'))
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                
                # Extract currency symbol and amount
                # Common formats: $299, €349, £279, ₹14,999
                match = re.search(r'([€$£₹¥])\s*([\d,]+(?:\.\d{2})?)', price_text)
                if match:
                    symbol, amount = match.groups()
                    price = f"{symbol}{amount}"
                    
                    # Map symbol to currency code
                    currency_map = {
                        '$': 'USD',
                        '€': 'EUR',
                        '£': 'GBP',
                        '₹': 'INR',
                        '¥': 'JPY'
                    }
                    currency = currency_map.get(symbol, 'USD')
        
        return price, currency
    
    def _extract_images(self, soup: BeautifulSoup) -> List[str]:
        """Extract phone images."""
        images = []
        
        # Main product image
        main_img = soup.find('img', class_='img-gallery-main')
        if main_img:
            src = main_img.get('src') or main_img.get('data-src')
            if src:
                if src.startswith('//'):
                    src = 'https:' + src
                images.append(src)
        
        # Gallery images
        gallery = soup.find('div', class_='img-gallery-thumbnails')
        if gallery:
            for img_tag in gallery.find_all('img'):
                src = img_tag.get('src') or img_tag.get('data-src')
                if src and src not in images:
                    if src.startswith('//'):
                        src = 'https:' + src
                    images.append(src)
        
        return images
    
    def _extract_specifications(self, soup: BeautifulSoup) -> dict:
        """Extract all specifications."""
        specs = {}
        
        # Kimovil uses tables for specs
        spec_tables = soup.find_all('table', class_='specs')
        for table in spec_tables:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                if len(cells) >= 2:
                    # First cell is spec name, second is value
                    key = cells[0].get_text(strip=True)
                    value = cells[1].get_text(strip=True)
                    if key and value:
                        specs[key] = value
        
        # Alternative: spec rows with class
        spec_rows = soup.find_all('div', class_='spec-row')
        for row in spec_rows:
            label = row.find(class_='spec-label')
            value = row.find(class_='spec-value')
            if label and value:
                specs[label.get_text(strip=True)] = value.get_text(strip=True)
        
        return specs
    
    def _extract_rating(self, soup: BeautifulSoup) -> Optional[float]:
        """Extract user rating."""
        rating_elem = soup.find(class_=re.compile(r'rating'))
        if rating_elem:
            rating_text = rating_elem.get_text(strip=True)
            # Look for patterns like "4.5" or "4.5/5"
            match = re.search(r'(\d+\.?\d*)', rating_text)
            if match:
                return float(match.group(1))
        
        return None
    
    def _extract_highlights(self, soup: BeautifulSoup) -> List[str]:
        """Extract key highlights/features."""
        highlights = []
        
        # Look for key specs section
        key_specs = soup.find('div', class_='key-specs')
        if key_specs:
            items = key_specs.find_all(['li', 'div'])
            for item in items:
                text = item.get_text(strip=True)
                if text and len(text) > 5:
                    highlights.append(text)
        
        # Alternative: summary points
        summary = soup.find('ul', class_='summary')
        if summary:
            for li in summary.find_all('li'):
                text = li.get_text(strip=True)
                if text and text not in highlights:
                    highlights.append(text)
        
        return highlights[:10]  # Limit to top 10
    
    def _extract_description(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract product description."""
        desc_elem = soup.find('div', class_='description')
        if not desc_elem:
            desc_elem = soup.find('div', class_='product-description')
        
        if desc_elem:
            # Get first paragraph or limited text
            paragraphs = desc_elem.find_all('p')
            if paragraphs:
                return paragraphs[0].get_text(strip=True)
            else:
                text = desc_elem.get_text(strip=True)
                # Limit to reasonable length
                return text[:500] + '...' if len(text) > 500 else text
        
        return None
    
    def search_phones(self, query: str, max_results: int = 10) -> List[Phone]:
        """
        Search for phones on Kimovil.
        
        Note: Kimovil has aggressive Cloudflare protection that may block automated requests.
        For best results, use direct product URLs or consider Selenium with undetected-chromedriver.
        
        Args:
            query: Search query (e.g., "Samsung Galaxy S23")
            max_results: Maximum number of results to return
            
        Returns:
            List of Phone objects
        """
        print(f"[SEARCH] Searching Kimovil for: {query}")
        print("[WARNING]  Note: Kimovil may block automated search. Consider using direct product URLs.")
        
        # Try homepage first
        search_url = f"{self.BASE_URL}/en/"
        response = self.client.get(search_url)
        
        if not response or response.status_code != 200:
            print(f"[FAILED] Kimovil is blocking requests (Cloudflare protection)")
            print("[TIP] Solutions:")
            print("   1. Use direct product URLs: scraper.scrape_phone('https://www.kimovil.com/en/phone.htm')")
            print("   2. Try undetected-chromedriver (slower but more reliable)")
            print("   3. See CLOUDFLARE_BYPASS_GUIDE.md for advanced options")
            return []
        
        # Check for Cloudflare challenge
        if 'cloudflare' in response.text[:5000].lower() or 'captcha' in response.text[:5000].lower():
            print("[WARNING]  Cloudflare challenge detected - automated search may not work")
            return []
        
        soup = BeautifulSoup(response.text, 'lxml')
        phones = []
        
        # Find phone links (pattern: /en/phone-name-ID.htm)
        all_links = soup.find_all('a', href=True, limit=200)
        phone_links = []
        
        for link in all_links:
            href = link.get('href', '')
            # Kimovil pattern: /en/something-number.htm
            if '/en/' in href and '.htm' in href and any(c.isdigit() for c in href):
                link_text = link.get_text(strip=True).lower()
                # Filter by query
                if not query or any(word.lower() in link_text or word.lower() in href.lower() for word in query.split()):
                    if href not in phone_links:
                        phone_links.append(href)
                        if len(phone_links) >= max_results:
                            break
        
        if not phone_links:
            print("[FAILED] No phone links found. Kimovil may be blocking or page structure changed.")
            return []
        
        print(f"[SCRAPING] Found {len(phone_links)} potential matches")
        
        # Scrape each phone
        for href in phone_links:
            if not href.startswith('http'):
                if not href.startswith('/'):
                    href = '/' + href
                phone_url = self.BASE_URL + href
            else:
                phone_url = href
            
            try:
                phone = self.scrape_phone(phone_url)
                if phone:
                    phones.append(phone)
            except Exception as e:
                print(f"[WARNING]  Error scraping {phone_url}: {e}")
                continue
        
        print(f"[SUCCESS] Successfully scraped {len(phones)} phones")
        return phones
    
    def get_price_comparisons(self, phone_url: str) -> List[dict]:
        """
        Get price comparisons from different stores/regions for a phone.
        
        Args:
            phone_url: URL to Kimovil phone page
            
        Returns:
            List of dictionaries with store, price, and availability info
        """
        print(f"[PRICE] Getting price comparisons for: {phone_url}")
        
        response = self.client.get(phone_url)
        if not response:
            print("[FAILED] Failed to fetch page")
            return []
        
        soup = BeautifulSoup(response.text, 'lxml')
        comparisons = []
        
        # Find price comparison table
        price_table = soup.find('table', class_='pricing-offers')
        if price_table:
            rows = price_table.find_all('tr')
            for row in rows:
                store_elem = row.find(class_='pricing-offer-store')
                price_elem = row.find(class_='pricing-offer-price')
                
                if store_elem and price_elem:
                    comparison = {
                        'store': store_elem.get_text(strip=True),
                        'price': price_elem.get_text(strip=True),
                        'link': store_elem.find('a')['href'] if store_elem.find('a') else None
                    }
                    comparisons.append(comparison)
        
        print(f"[SUCCESS] Found {len(comparisons)} price comparisons")
        return comparisons
