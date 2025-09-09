import logging
import os
import random
import time
import traceback
from datetime import datetime

from browser_controller import BrowserController, BraveBrowserController
from constants import (
    OUTPUT_DIR,
    LOG_FILE,
    SEARCH_URL_TEMPLATE,
    ITERATION_WAIT,
)

os.makedirs(OUTPUT_DIR, exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def calculate_wait_time(base=5, jitter=5, max_wait=30):
    """Calculate wait time using exponential distribution - pure function"""
    return min(base + random.expovariate(1 / jitter), max_wait)


def random_wait(base=5, jitter=5, max_wait=30):
    """Random wait with exponential distribution"""
    wait_time = calculate_wait_time(base, jitter, max_wait)
    logging.info(f"Sleeping for {wait_time:.2f} seconds")
    time.sleep(wait_time)


def contains_residential_card(filename: str) -> bool:
    """Pure function to check if file contains 'ResidentialCard'"""
    with open(filename, "r", encoding="utf-8", errors="ignore") as file:
        content = file.read()
        return "ResidentialCard" in content


def check_stop(filename: str) -> bool:
    """Check if the file exists and if it contains 'ResidentialCard'"""
    logging.info(f"check_stop: {filename}")
    
    if not os.path.exists(filename):
        logging.error(f"check_stop: File does not exist: {filename}")
        return True

    if contains_residential_card(filename):
        logging.info("check_stop: Continue")
        return False

    logging.info(f"check_stop: Stop. Deleting file: {filename}")
    os.remove(filename)
    return True


def generate_search_url(postcode: str, page_num: int) -> str:
    """Pure function to generate search URL for given postcode and page"""
    return SEARCH_URL_TEMPLATE.format(postcode=postcode, page_num=page_num)


def generate_filename(postcode: str, page_num: int, timestamp: str = None) -> str:
    """Pure function to generate filename for scraped page"""
    if timestamp is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{OUTPUT_DIR}/{postcode}_{page_num}_{timestamp}.html"


def scrape_single_page(postcode: str, page_num: int, browser_controller: BrowserController) -> str:
    """Scrape a single page and return the filename"""
    url = generate_search_url(postcode, page_num)
    browser_controller.navigate_to(url)
    
    filename = generate_filename(postcode, page_num)
    browser_controller.save_page(filename)
    browser_controller.perform_human_like_activity()
    
    return filename


def scrape_all_pages(postcode: str, browser_controller: BrowserController) -> None:
    """Scrape all pages for a postcode until stopping condition is met"""
    page_num = 1
    while True:
        filename = scrape_single_page(postcode, page_num, browser_controller)
        
        if check_stop(filename):
            break
            
        page_num += 1


def scrape_realestate_postcode(
    postcode: str, browser_controller: BrowserController = None
) -> None:
    """Scrape realestate.com.au for a specific postcode using a browser controller"""
    if browser_controller is None:
        browser_controller = BraveBrowserController()

    logging.info(f"scrape_realestate_postcode: {postcode}")
    try:
        browser_controller.open_browser()
        scrape_all_pages(postcode, browser_controller)

    except Exception as e:
        logging.error(
            f"Error scraping postcode {postcode}: {e}\n{traceback.format_exc()}"
        )

    finally:
        browser_controller.close_browser()
        logging.info(f"Finished scraping postcode {postcode}")
        time.sleep(ITERATION_WAIT)
