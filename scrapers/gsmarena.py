"""
GSMArena scraper for mobile phone specifications.
"""

from bs4 import BeautifulSoup
from typing import Optional, List, Dict
import re

from utils.http_client import HTTPClient
from models.phone import Phone


class GSMArenaScraper:
    """Scraper for GSMArena website."""
    
    BASE_URL = "https://www.gsmarena.com"
    
    def __init__(self):
        self.client = HTTPClient()
    
    def scrape_phone(self, url: str) -> Optional[Phone]:
        """
        Scrape a single phone from GSMArena product page.
        
        Args:
            url: Full URL to GSMArena phone page
            
        Returns:
            Phone object or None if scraping failed
        """
        print(f"[SCRAPING] Scraping GSMArena: {url}")
        
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
            source="gsmarena"
        )
        
        # Extract price
        phone.price = self._extract_price(soup)
        
        # Extract images
        phone.images = self._extract_images(soup)
        if phone.images:
            phone.thumbnail = phone.images[0]
        
        # Extract specifications
        phone.specs = self._extract_specifications(soup)
        phone.detailed_specs = self._extract_detailed_specifications(soup)
        phone.all_images = phone.images.copy()  # Copy all images
        
        # Extract rating
        phone.rating = self._extract_rating(soup)
        
        # Extract highlights
        phone.highlights = self._extract_highlights(soup)
        
        print(f"[SUCCESS] Successfully scraped: {phone.brand} {phone.model}")
        return phone
    
    def _extract_brand_model(self, soup: BeautifulSoup) -> tuple:
        """Extract brand and model name."""
        title = soup.find('h1', class_='specs-phone-name-title')
        if title:
            text = title.get_text(strip=True)
            # Usually format is "Brand Model"
            parts = text.split(maxsplit=1)
            if len(parts) >= 2:
                return parts[0], parts[1]
            elif len(parts) == 1:
                return "Unknown", parts[0]
        return None, None
    
    def _extract_price(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract price information."""
        price_div = soup.find('div', class_='specs-price-title')
        if price_div:
            # Remove currency symbols and clean up
            price_text = price_div.get_text(strip=True)
            # Extract just the numeric part with currency
            match = re.search(r'[€$£₹¥]\s*[\d,]+', price_text)
            if match:
                return match.group(0)
        return None
    
    def _extract_images(self, soup: BeautifulSoup) -> List[str]:
        """Extract phone images."""
        images = []
        
        # Main image
        main_img = soup.find('div', class_='specs-photo-main')
        if main_img:
            img_tag = main_img.find('img')
            if img_tag and img_tag.get('src'):
                images.append(img_tag['src'])
        
        # Additional images
        carousel = soup.find('div', class_='specs-photo-carousel')
        if carousel:
            for img_tag in carousel.find_all('img'):
                if img_tag.get('src') and img_tag['src'] not in images:
                    images.append(img_tag['src'])
        
        return images
    
    def _extract_specifications(self, soup: BeautifulSoup) -> dict:
        """Extract all specifications."""
        specs = {}
        
        # GSMArena uses tables with specific structure
        spec_tables = soup.find_all('table', cellspacing='0')
        
        for table in spec_tables:
            rows = table.find_all('tr')
            for row in rows:
                # Get spec name
                name_cell = row.find('td', class_='ttl')
                if not name_cell:
                    continue
                
                spec_name = name_cell.get_text(strip=True)
                
                # Get spec value
                value_cell = row.find('td', class_='nfo')
                if value_cell:
                    spec_value = value_cell.get_text(strip=True)
                    specs[spec_name] = spec_value
        
        return specs
    
    def _extract_detailed_specifications(self, soup: BeautifulSoup) -> List[Dict]:
        """
        Extract specifications in detailed nested format (like Flipkart).
        Returns list of categories with their specifications.
        """
        detailed_specs = []
        
        # Find all specification sections
        spec_sections = soup.find_all('table', cellspacing='0')
        
        for table in spec_sections:
            # Get category title (usually in header row)
            category_title = None
            category_th = table.find('th')
            if category_th:
                category_title = category_th.get_text(strip=True)
            
            if not category_title:
                continue
            
            # Extract all specs in this category
            details = []
            rows = table.find_all('tr')
            
            for row in rows:
                name_cell = row.find('td', class_='ttl')
                value_cell = row.find('td', class_='nfo')
                
                if name_cell and value_cell:
                    property_name = name_cell.get_text(strip=True)
                    property_value = value_cell.get_text(strip=True)
                    
                    details.append({
                        'property': property_name,
                        'value': property_value
                    })
            
            if details:
                detailed_specs.append({
                    'title': category_title,
                    'details': details
                })
        
        return detailed_specs
    
    def _extract_rating(self, soup: BeautifulSoup) -> Optional[float]:
        """Extract user rating."""
        rating_div = soup.find('div', class_='rating-bar')
        if rating_div:
            rating_text = rating_div.get_text(strip=True)
            match = re.search(r'(\d+\.?\d*)', rating_text)
            if match:
                return float(match.group(1))
        return None
    
    def _extract_highlights(self, soup: BeautifulSoup) -> List[str]:
        """Extract key highlights/features."""
        highlights = []
        
        # Quick spec section often has highlights
        quickspec = soup.find('div', class_='quickspec-list')
        if quickspec:
            items = quickspec.find_all('div', class_='quickspec-item')
            for item in items:
                text = item.get_text(strip=True)
                if text:
                    highlights.append(text)
        
        return highlights
    
    def search_phones(self, query: str, max_results: int = 10) -> List[Phone]:
        """
        Search for phones on GSMArena.
        
        Args:
            query: Search query (e.g., "Samsung Galaxy S23")
            max_results: Maximum number of results to return
            
        Returns:
            List of Phone objects
        """
        print(f"[SEARCH] Searching GSMArena for: {query}")
        
        search_url = f"{self.BASE_URL}/results.php3?sQuickSearch=yes&sName={query}"
        response = self.client.get(search_url)
        
        if not response:
            print("[FAILED] Search failed")
            return []
        
        soup = BeautifulSoup(response.text, 'lxml')
        phones = []
        
        # Find all phone listings
        makers = soup.find('div', class_='makers')
        if not makers:
            print("[FAILED] No search results found")
            return []
        
        links = makers.find_all('a', limit=max_results)
        
        for link in links:
            href = link['href']
            # Ensure proper URL construction with slash
            if not href.startswith('/'):
                href = '/' + href
            phone_url = self.BASE_URL + href
            phone = self.scrape_phone(phone_url)
            if phone:
                phones.append(phone)
        
        print(f"[SUCCESS] Found {len(phones)} phones")
        return phones
