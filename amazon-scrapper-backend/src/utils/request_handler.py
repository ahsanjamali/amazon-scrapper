import random
import time
from typing import Optional
import requests
from fake_useragent import UserAgent
from src.config.settings import REQUEST_DELAY, MAX_RETRIES

class RequestHandler:
    def __init__(self):
        self.user_agent = UserAgent()
        self.session = requests.Session()
    
    def get_headers(self) -> dict:
        """Generate random headers for each request."""
        return {
            'User-Agent': self.user_agent.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        }
    
    def get(self, url: str, retries: int = MAX_RETRIES) -> Optional[requests.Response]:
        """
        Make a GET request with retry mechanism and random delays.
        """
        for attempt in range(retries):
            try:
                # Add random delay between requests
                time.sleep(REQUEST_DELAY + random.uniform(0, 2))
                
                response = self.session.get(
                    url,
                    headers=self.get_headers(),
                    timeout=30
                )
                response.raise_for_status()
                return response
            
            except requests.RequestException as e:
                if attempt == retries - 1:
                    print(f"Failed to fetch {url} after {retries} attempts: {str(e)}")
                    return None
                continue
        
        return None
