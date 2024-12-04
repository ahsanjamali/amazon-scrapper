import concurrent.futures
from typing import List
from src.scrapers.amazon_scraper import AmazonScraper
from src.utils.file_handler import FileHandler
from src.models.product import Product

def scrape_query(query: str, max_pages: int = 20) -> List[Product]:
    """Scrape products for a single query."""
    scraper = AmazonScraper()
    products = scraper.scrape_search_results(query, max_pages)
    
    # Save products to file
    if products:
        FileHandler.save_products(products, query)
    
    return products

def main():
    # Read queries
    queries = FileHandler.read_queries()
    if not queries:
        print("No queries found. Exiting...")
        return
    
    print(f"Starting scraping for {len(queries)} queries...")
    
    # Use ThreadPoolExecutor for parallel scraping
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        future_to_query = {executor.submit(scrape_query, query): query for query in queries}
        
        for future in concurrent.futures.as_completed(future_to_query):
            query = future_to_query[future]
            try:
                products = future.result()
                print(f"Completed scraping for '{query}' - Found {len(products)} products")
            except Exception as e:
                print(f"Error scraping '{query}': {str(e)}")

if __name__ == "__main__":
    main()
