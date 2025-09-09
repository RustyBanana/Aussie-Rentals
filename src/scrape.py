import logging
import os
import random
import time
import traceback
from datetime import datetime

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

os.makedirs(OUTPUT_DIR, exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def random_wait(base=5, jitter=5, max_wait=30):
    wait = min(base + random.expovariate(1 / jitter), max_wait)
    logging.info(f"Sleeping for {wait:.2f} seconds")
    time.sleep(wait)


def check_stop(filename: str) -> bool:
    """Check if the file exists and if it contains 'ResidentialCard'"""
    logging.info(f"check_stop: {filename}")
    if not os.path.exists(filename):
        logging.error(f"check_stop: File does not exist: {filename}")
        return True

    with open(filename, "r", encoding="utf-8", errors="ignore") as file:
        content = file.read()
        if "ResidentialCard" in content:
            logging.info("check_stop: Continue")
            return False

    logging.info(f"check_stop: Stop. Deleting file: {filename}")
    os.remove(filename)
    return True


def scrape_realestate_postcode(
    postcode: str, browser_controller: BrowserController = None
) -> None:
    """Scrape realestate.com.au for a specific postcode using a browser controller"""
    if browser_controller is None:
        browser_controller = BraveBrowserController()

    logging.info(f"scrape_realestate_postcode: {postcode}")
    try:
        browser_controller.open_browser()

        # Now navigate to search pages for each postcode and capture
        page_num = 1
        while True:
            url = SEARCH_URL_TEMPLATE.format(postcode=postcode, page_num=page_num)
            browser_controller.navigate_to(url)

            # Generate file name
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{OUTPUT_DIR}/{postcode}_{page_num}_{timestamp}.html"
            browser_controller.save_page(filename)
            browser_controller.perform_human_like_activity()

            if check_stop(filename):
                break

            page_num += 1

    except Exception as e:
        logging.error(
            f"Error scraping postcode {postcode}: {e}\n{traceback.format_exc()}"
        )

    finally:
        browser_controller.close_browser()
        logging.info(f"Finished scraping postcode {postcode}")
        time.sleep(ITERATION_WAIT)
