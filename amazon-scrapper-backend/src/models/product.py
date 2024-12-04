from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Product:
    title: str
    price: Optional[float]
    total_reviews: Optional[int]
    image_url: str
    search_query: str
    product_url: str
    scrape_date: datetime = datetime.now()
    
    def to_dict(self) -> dict:
        """Convert the product instance to a dictionary."""
        return {
            'title': self.title,
            'price': self.price,
            'total_reviews': self.total_reviews,
            'image_url': self.image_url,
            'search_query': self.search_query,
            'product_url': self.product_url,
            'scrape_date': self.scrape_date.isoformat()
        }
