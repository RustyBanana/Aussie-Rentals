# Configuration constants
BRAVE_BROWSER_COMMAND = "brave-browser"
USER_DATA_DIR = "./brave_manual_profile"
DEFAULT_URL = "https://en.wikipedia.org/wiki/World_War_II"
BASE_URL = "https://www.realestate.com.au/"
SEARCH_URL_TEMPLATE = "https://www.realestate.com.au/rent/in-{postcode}/list-{page_num}?includeSurrounding=false"
OUTPUT_DIR = "html_pages"
LOG_FILE = "scrape.log"
POSTCODES_FILE = "data/postcodes sydney.txt"
MIN_POSTCODE = "2008"

# Wait time constants
BROWSER_OPEN_WAIT = 1.2
PAGE_LOAD_BASE_WAIT = 2
PAGE_LOAD_JITTER = 1
SAVE_WAIT = 2
ITERATION_WAIT = 1.6

# Browser automation timing constants
KEYBOARD_DELAY = 0.1
SAVE_DIALOG_WAIT = 1.0
