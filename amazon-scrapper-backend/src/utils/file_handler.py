import json
import os
from typing import List, Dict, Any
from src.config.settings import QUERIES_FILE, OUTPUT_DIR
from src.models.product import Product

class FileHandler:
    @staticmethod
    def read_queries() -> List[str]:
        """Read search queries from the JSON file."""
        try:
            with open(QUERIES_FILE, 'r', encoding='utf-8') as f:
                queries = json.load(f)
            return queries
        except Exception as e:
            print(f"Error reading queries file: {str(e)}")
            return []
    
    @staticmethod
    def save_products(products: List[Product], query: str) -> bool:
        """Save scraped products to a JSON file."""
        try:
            output_file = os.path.join(OUTPUT_DIR, f"{query.replace(' ', '_')}.json")
            
            # Convert products to dictionaries
            products_data = [product.to_dict() for product in products]
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(products_data, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"Error saving products for query '{query}': {str(e)}")
            return False
