import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base configuration
AMAZON_BASE_URL='https://www.amazon.com'
REQUEST_DELAY=3
MAX_RETRIES=3

# File paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
# OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'output')

OUTPUT_DIR = os.path.join(
    os.path.dirname(PROJECT_ROOT),  # Go one directory back
    'amazon-scrapper-frontend',     # Frontend project directory
    'src',                         # src folder
    'output'                       # output directory
)


# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Input file paths
QUERIES_FILE = os.path.join(DATA_DIR, 'user_queries.json')
