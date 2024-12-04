from typing import List, Optional
from bs4 import BeautifulSoup
import re
from src.models.product import Product
from src.utils.request_handler import RequestHandler
from src.config.settings import AMAZON_BASE_URL

class AmazonScraper:
    def __init__(self):
        self.request_handler = RequestHandler()
    
    def _parse_price(self, product_elem: BeautifulSoup) -> Optional[float]:
        """Parse price from product element with enhanced selectors."""
        try:
            # Comprehensive list of price selectors
            price_selectors = [
                'span.a-price span.a-offscreen',
                'span.a-price:first-child span.a-offscreen',
                'span[data-a-color="price"] span.a-offscreen',
                'span.a-price span[aria-hidden="true"]',
                'span.a-price-whole',
                'span.a-color-price',
                'span.a-price:not(.a-text-price)',
                'span[data-a-strike="true"]',
                '.a-price .a-price-symbol + span.a-price-whole',
                '.a-section span.a-price span.a-offscreen'
            ]
            
            for selector in price_selectors:
                price_elem = product_elem.select_one(selector)
                if price_elem:
                    price_text = price_elem.text.strip()
                    # Handle different price formats
                    if price_text:
                        # Remove currency symbols and non-numeric chars except decimal point
                        cleaned_price = re.sub(r'[^\d.]', '', price_text)
                        if cleaned_price:
                            # Handle cases where price might be split (e.g., "1,234.56")
                            price = float(cleaned_price)
                            # Validate price is reasonable (e.g., not 0 or unreasonably high)
                            if 0 < price < 100000:  # adjust range as needed
                                return price
            
            # Try finding price in the whole product card text
            all_text = product_elem.get_text()
            price_pattern = r'(?:₹|RS\.?|INR)\s*(\d+(?:,\d+)*(?:\.\d{2})?)'
            price_match = re.search(price_pattern, all_text, re.IGNORECASE)
            if price_match:
                price_str = price_match.group(1).replace(',', '')
                price = float(price_str)
                if 0 < price < 100000:
                    return price
                
            return None
        
        except (ValueError, AttributeError) as e:
            print(f"Error parsing price: {str(e)}")
            return None
    
    def _parse_reviews(self, product_elem: BeautifulSoup) -> Optional[int]:
        """Parse total reviews count."""
        try:
            # Try multiple review selectors
            review_selectors = [
                'span.a-size-base.s-underline-text',
                'span.a-size-base[dir="auto"]',
                'a.a-link-normal span.a-size-base'
            ]
            
            for selector in review_selectors:
                reviews_elem = product_elem.select_one(selector)
                if reviews_elem and reviews_elem.text:
                    reviews_text = reviews_elem.text.strip()
                    if reviews_text:
                        reviews = int(re.sub(r'[^\d]', '', reviews_text))
                        return reviews
            return None
        except (ValueError, AttributeError):
            return None
    
    def _parse_product(self, product_elem: BeautifulSoup, search_query: str) -> Optional[Product]:
        """Parse product details with debug logging."""
        try:
            # Find product title and URL
            title_elem = product_elem.select_one('h2 a.a-link-normal span')
            if not title_elem:
                return None
            
            title = title_elem.text.strip()
            url_elem = product_elem.select_one('h2 a.a-link-normal')
            product_url = f"{AMAZON_BASE_URL}{url_elem['href']}" if url_elem else None
            
            # Parse price with debug logging
            price = self._parse_price(product_elem)
            if price is None:
                print(f"Warning: Could not parse price for product: {title[:50]}...")
                
                # Debug: Print the HTML structure around where price should be
                price_area = product_elem.select_one('.a-price')
                if price_area:
                    print(f"Price area HTML: {price_area.prettify()[:200]}")
                else:
                    print("No price area found with .a-price class")
            
            # Rest of the parsing logic
            img_elem = product_elem.select_one('img.s-image')
            image_url = img_elem['src'] if img_elem else None
            
            total_reviews = self._parse_reviews(product_elem)
            
            return Product(
                title=title,
                price=price,
                total_reviews=total_reviews,
                image_url=image_url,
                search_query=search_query,
                product_url=product_url
            )
        
        except Exception as e:
            print(f"Error parsing product: {str(e)}")
            return None
    
    def scrape_search_results(self, query: str, max_pages: int = 20 ) -> List[Product]:
        """Scrape products for a given search query."""
        products = []
        
        for page in range(1, max_pages + 1):
            url = f"{AMAZON_BASE_URL}/s?k={query}&page={page}"
            response = self.request_handler.get(url)
            
            if not response:
                continue
            
            soup = BeautifulSoup(response.content, 'html.parser')
            product_elements = soup.find_all('div', {'data-component-type': 's-search-result'})
            
            for product_elem in product_elements:
                product = self._parse_product(product_elem, query)
                if product:
                    products.append(product)
            
            print(f"Scraped page {page} for query '{query}' - Found {len(products)} products so far")
        
        return products 
    
    def _validate_price(self, price: float) -> bool:
        """Validate if the parsed price seems reasonable."""
        # Adjust these thresholds based on your products
        MIN_PRICE = 100    # Minimum reasonable price
        MAX_PRICE = 200000 # Maximum reasonable price
        
        if not isinstance(price, (int, float)):
            return False
        
        if price <= MIN_PRICE or price >= MAX_PRICE:
            return False
        
        return True