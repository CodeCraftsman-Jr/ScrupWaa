"""
Data model for mobile phone information.
"""

from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, List
import json


@dataclass
class Phone:
    """Mobile phone data model - comprehensive product information."""
    
    # Basic Information
    brand: str
    model: str
    url: str
    
    # Pricing
    price: Optional[str] = None
    original_price: Optional[str] = None
    currency: str = "USD"
    discounted: bool = False
    
    # Availability
    in_stock: bool = True
    
    # Specifications (dict for flexible key-value pairs)
    specs: Dict[str, str] = field(default_factory=dict)
    detailed_specs: List[Dict] = field(default_factory=list)  # Nested specs like Flipkart
    
    # Media
    images: List[str] = field(default_factory=list)
    all_images: List[str] = field(default_factory=list)  # All available images
    thumbnail: Optional[str] = None
    
    # Ratings and Reviews
    rating: Optional[float] = None
    reviews_count: Optional[int] = None
    
    # Additional Info
    highlights: List[str] = field(default_factory=list)
    description: Optional[str] = None
    
    # Seller Information
    seller_name: Optional[str] = None
    seller_rating: Optional[float] = None
    f_assured: bool = False
    
    # Offers and Deals
    offers: List[Dict] = field(default_factory=list)
    bank_offers: List[str] = field(default_factory=list)
    exchange_offers: List[str] = field(default_factory=list)
    
    # Technical Details
    launch_year: Optional[str] = None
    launch_date: Optional[str] = None
    dimensions: Dict[str, str] = field(default_factory=dict)
    weight: Optional[str] = None
    colors: List[str] = field(default_factory=list)
    variants: List[Dict] = field(default_factory=list)
    
    # Warranty and Service
    warranty: Optional[str] = None
    warranty_summary: Optional[str] = None
    service_type: Optional[str] = None
    
    # Source
    source: str = ""  # gsmarena, 91mobiles, kimovil
    
    # Query metadata
    total_results: Optional[int] = None
    query_params: Dict = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        """Convert phone object to dictionary."""
        return asdict(self)
    
    def to_json(self) -> str:
        """Convert phone object to JSON string."""
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)
    
    def __repr__(self) -> str:
        """String representation of phone."""
        price_str = f"{self.price} {self.currency}" if self.price else "N/A"
        return f"Phone({self.brand} {self.model}, Price: {price_str}, Rating: {self.rating})"
