# Configuration constants
BRAVE_BROWSER_COMMAND = "brave-browser"
USER_DATA_DIR = "./brave_manual_profile"
BASE_URL = "https://www.realestate.com.au/"
SEARCH_URL_TEMPLATE = "https://www.realestate.com.au/rent/in-{postcode}/list-{page_num}?includeSurrounding=false"
OUTPUT_DIR = "html_pages"
LOG_FILE = "scrape.log"
POSTCODES_FILE = "data/postcodes sydney.txt"
MIN_POSTCODE = "2008"

# Wait time constants
BROWSER_OPEN_WAIT = 3
USER_INTERACTION_WAIT = 30
PAGE_LOAD_BASE_WAIT = 10
PAGE_LOAD_JITTER = 5
SAVE_WAIT = 6
ITERATION_WAIT = 2
