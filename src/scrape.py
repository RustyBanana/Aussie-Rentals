import logging
import os
import time
import traceback
from datetime import datetime
from typing import Optional

from browser_controller import (
    BrowserController,
    calculate_wait_time,
)
from constants import (
    ITERATION_WAIT,
    OUTPUT_DIR,
    SEARCH_URL_TEMPLATE,
)

os.makedirs(OUTPUT_DIR, exist_ok=True)


def random_wait(base: float = 5, jitter: float = 5, max_wait: float = 30) -> None:
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

    return True


def generate_search_url(postcode: str, page_num: int) -> str:
    """Pure function to generate search URL for given postcode and page"""
    return SEARCH_URL_TEMPLATE.format(postcode=postcode, page_num=page_num)


def generate_filename(
    postcode: str, page_num: int, timestamp: Optional[str] = None
) -> str:
    """Pure function to generate filename for scraped page"""
    if timestamp is None:
        date = datetime.now().strftime("%Y%m%d")
        # time = datetime.now().strftime("%H%M%S")
    return f"{OUTPUT_DIR}/{date}_{postcode}_{page_num}.html"


def generate_completed_filename(postcode: str, timestamp: Optional[str] = None) -> str:
    """Pure function to generate completed filename for a postcode"""
    if timestamp is None:
        date = datetime.now().strftime("%Y%m%d")
    return f"{OUTPUT_DIR}/{date}_{postcode}_completed.html"


def is_postcode_completed(postcode: str) -> bool:
    """Check if a postcode has already been completed"""
    completed_filename = generate_completed_filename(postcode)
    return os.path.exists(completed_filename)


def scrape_single_page(
    postcode: str, page_num: int, browser_controller: BrowserController
) -> str:
    """Scrape a single page and return the filename"""
    url = generate_search_url(postcode, page_num)
    browser_controller.navigate_to(url)

    filename = generate_filename(postcode, page_num)
    browser_controller.save_page(filename)
    browser_controller.perform_human_like_activity()

    return filename


def handle_stopping_file(filename: str, postcode: str) -> None:
    """Handle a file that triggers the stopping condition"""
    completed_filename = generate_completed_filename(postcode)
    os.rename(filename, completed_filename)
    logging.info(f"Renamed stopping file to: {completed_filename}")


def scrape_all_pages(postcode: str, browser_controller: BrowserController) -> None:
    """Scrape all pages for a postcode until stopping condition is met"""
    page_num = 1
    while True:
        filename = generate_filename(postcode, page_num)

        # Skip scraping if file already exists
        if os.path.exists(filename):
            logging.info(f"File already exists, skipping: {filename}")
            if check_stop(filename):
                handle_stopping_file(filename, postcode)
                break
            page_num += 1
            continue

        filename = scrape_single_page(postcode, page_num, browser_controller)

        if check_stop(filename):
            handle_stopping_file(filename, postcode)
            break

        page_num += 1


def scrape_realestate_postcode(
    postcode: str, browser_controller: BrowserController
) -> None:
    """Scrape realestate.com.au for a specific postcode using a browser controller"""
    if not postcode or not postcode.strip():
        raise ValueError(f"Invalid postcode provided: '{postcode}'")

    logging.info(f"scrape_realestate_postcode: {postcode}")
    try:
        scrape_all_pages(postcode, browser_controller)

    except Exception as e:
        logging.error(
            f"Unexpected error scraping postcode {postcode}: {e}\n{traceback.format_exc()}"
        )
        raise

    finally:
        logging.info(f"Finished scraping postcode {postcode}")
        time.sleep(ITERATION_WAIT)
