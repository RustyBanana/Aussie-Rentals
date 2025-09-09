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

# Human-like activity constants
MIN_ACTIVITY_ACTIONS = 3
MAX_ACTIVITY_ACTIONS = 6
MIN_SCROLL_AMOUNT = 100
MAX_SCROLL_AMOUNT = 1000
MIN_MOVE_DURATION = 0.2
MAX_MOVE_DURATION = 0.8
MIN_ACTIVITY_WAIT = 0.1
MAX_ACTIVITY_WAIT = 0.5
CLICK_PROBABILITY = 0.3
SCROLL_PROBABILITY = 0.9

# Browser automation timing constants
KEYBOARD_DELAY = 0.1
SAVE_DIALOG_WAIT = 1.0
