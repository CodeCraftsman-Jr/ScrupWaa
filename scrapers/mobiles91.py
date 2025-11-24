"""
91mobiles scraper for mobile phone prices and specifications.
"""

from bs4 import BeautifulSoup
from typing import Optional, List
import re

from utils.adaptive_client import AdaptiveClient
from models.phone import Phone


class Mobiles91Scraper:
    """Scraper for 91mobiles website with Cloudflare bypass."""
    
    BASE_URL = "https://www.91mobiles.com"
    
    def __init__(self):
        # Use AdaptiveClient for automatic Cloudflare bypass
        self.client = AdaptiveClient()
    
    def scrape_phone(self, url: str) -> Optional[Phone]:
        """
        Scrape a single phone from 91mobiles product page.
        
        Args:
            url: Full URL to 91mobiles phone page
            
        Returns:
            Phone object or None if scraping failed
        """
        print(f"📱 Scraping 91mobiles: {url}")
        
        response = self.client.get(url)
        if not response:
            print("❌ Failed to fetch page")
            return None
        
        soup = BeautifulSoup(response.text, 'lxml')
        
        # Extract basic information
        brand, model = self._extract_brand_model(soup)
        if not brand or not model:
            print("❌ Could not extract brand/model")
            return None
        
        phone = Phone(
            brand=brand,
            model=model,
            url=url,
            source="91mobiles",
            currency="INR"  # Indian Rupees
        )
        
        # Extract price
        phone.price, phone.original_price = self._extract_price(soup)
        
        # Extract images
        phone.images = self._extract_images(soup)
        if phone.images:
            phone.thumbnail = phone.images[0]
        
        # Extract specifications
        phone.specs = self._extract_specifications(soup)
        
        # Extract rating
        phone.rating, phone.reviews_count = self._extract_rating(soup)
        
        # Extract highlights
        phone.highlights = self._extract_highlights(soup)
        
        # Extract availability
        phone.in_stock = self._check_availability(soup)
        
        print(f"✅ Successfully scraped: {phone.brand} {phone.model}")
        return phone
    
    def _extract_brand_model(self, soup: BeautifulSoup) -> tuple:
        """Extract brand and model name."""
        # Try h1 with phone name
        title = soup.find('h1', class_=re.compile(r'prdocutPage_.*_heading'))
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
        """Extract current and original price."""
        current_price = None
        original_price = None
        
        # Look for price section
        price_section = soup.find('div', class_=re.compile(r'price'))
        if price_section:
            # Current price
            price_span = price_section.find('span', class_=re.compile(r'pricee'))
            if not price_span:
                price_span = price_section.find('span')
            
            if price_span:
                price_text = price_span.get_text(strip=True)
                # Extract numeric value with ₹ symbol
                match = re.search(r'₹\s*[\d,]+', price_text)
                if match:
                    current_price = match.group(0)
            
            # Original/MRP price (if discounted)
            mrp_span = price_section.find('span', string=re.compile(r'MRP|Original'))
            if mrp_span:
                parent = mrp_span.find_parent()
                if parent:
                    price_text = parent.get_text(strip=True)
                    match = re.search(r'₹\s*[\d,]+', price_text)
                    if match:
                        original_price = match.group(0)
        
        return current_price, original_price
    
    def _extract_images(self, soup: BeautifulSoup) -> List[str]:
        """Extract phone images."""
        images = []
        
        # Main product image gallery
        gallery = soup.find('div', class_=re.compile(r'gallery|image'))
        if gallery:
            for img_tag in gallery.find_all('img'):
                src = img_tag.get('src') or img_tag.get('data-src')
                if src and src not in images:
                    # Convert to full URL if needed
                    if src.startswith('//'):
                        src = 'https:' + src
                    elif src.startswith('/'):
                        src = self.BASE_URL + src
                    images.append(src)
        
        return images
    
    def _extract_specifications(self, soup: BeautifulSoup) -> dict:
        """Extract all specifications."""
        specs = {}
        
        # Find spec tables/sections
        spec_section = soup.find('div', class_=re.compile(r'spec'))
        if spec_section:
            # Look for key-value pairs
            items = spec_section.find_all('li')
            for item in items:
                text = item.get_text(strip=True)
                # Usually format is "Key: Value" or "Key Value"
                if ':' in text:
                    key, value = text.split(':', 1)
                    specs[key.strip()] = value.strip()
                else:
                    # Sometimes just listed as single values
                    specs[text] = text
        
        # Alternative structure with divs/rows
        spec_rows = soup.find_all('div', class_=re.compile(r'spec.*row|spec.*item'))
        for row in spec_rows:
            label = row.find(class_=re.compile(r'label|key|name'))
            value = row.find(class_=re.compile(r'value|data'))
            
            if label and value:
                specs[label.get_text(strip=True)] = value.get_text(strip=True)
        
        return specs
    
    def _extract_rating(self, soup: BeautifulSoup) -> tuple:
        """Extract user rating and review count."""
        rating = None
        reviews = None
        
        # Look for rating element
        rating_elem = soup.find(class_=re.compile(r'rating'))
        if rating_elem:
            rating_text = rating_elem.get_text(strip=True)
            match = re.search(r'(\d+\.?\d*)\s*/\s*\d+', rating_text)
            if match:
                rating = float(match.group(1))
            
            # Reviews count
            reviews_match = re.search(r'(\d+)\s*(?:reviews?|ratings?)', rating_text, re.IGNORECASE)
            if reviews_match:
                reviews = int(reviews_match.group(1))
        
        return rating, reviews
    
    def _extract_highlights(self, soup: BeautifulSoup) -> List[str]:
        """Extract key highlights/features."""
        highlights = []
        
        # Look for key features section
        features_section = soup.find('div', class_=re.compile(r'feature|highlight|key'))
        if features_section:
            items = features_section.find_all(['li', 'p', 'div'])
            for item in items:
                text = item.get_text(strip=True)
                if text and len(text) > 5:  # Filter out empty/short items
                    highlights.append(text)
        
        return highlights[:10]  # Limit to top 10
    
    def _check_availability(self, soup: BeautifulSoup) -> bool:
        """Check if phone is in stock."""
        text = soup.get_text().lower()
        out_of_stock_indicators = [
            'out of stock',
            'not available',
            'coming soon',
            'discontinued'
        ]
        return not any(indicator in text for indicator in out_of_stock_indicators)
    
    def search_phones(self, query: str, max_results: int = 10) -> List[Phone]:
        """
        Search for phones on 91mobiles.
        
        Args:
            query: Search query (e.g., "Samsung Galaxy S23")
            max_results: Maximum number of results to return
            
        Returns:
            List of Phone objects
        """
        print(f"[SEARCH] Searching 91mobiles for: {query}")
        
        # Use homepage - most reliable, has latest phones
        search_url = f"{self.BASE_URL}/"
        query_lower = query.lower()
        
        response = self.client.get(search_url)
        
        if not response or response.status_code != 200:
            print(f"[WARNING] Search failed (status: {response.status_code if response else 'None'})")
            print("[TIP] Tip: Try using direct product URLs instead")
            return []
        
        soup = BeautifulSoup(response.text, 'lxml')
        phones = []
        
        # Find all phone links on the page
        all_links = soup.find_all('a', href=True, limit=100)
        phone_links = []
        
        for link in all_links:
            href = link.get('href', '')
            # 91mobiles uses pattern: /phone-name-price-in-india
            if 'price-in-india' in href:
                # Filter by query if possible
                link_text = link.get_text(strip=True).lower()
                if not query_lower or any(word in link_text or word in href.lower() for word in query_lower.split()):
                    if href not in phone_links:
                        phone_links.append(href)
                        if len(phone_links) >= max_results:
                            break
        
        # If no matches with query, get any phones from homepage
        if not phone_links and query_lower:
            print(f"[INFO] No exact matches for '{query}', showing latest phones from homepage")
            for link in all_links:
                href = link.get('href', '')
                if 'price-in-india' in href and href not in phone_links:
                    phone_links.append(href)
                    if len(phone_links) >= max_results:
                        break
        
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
                print(f"[WARNING] Error scraping {phone_url}: {e}")
                continue
        
        print(f"[SUCCESS] Successfully scraped {len(phones)} phones")
        return phones
