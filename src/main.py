import logging
from typing import List

import tqdm

from browser_controller import BraveBrowserController
from constants import BASE_URL, MIN_POSTCODE, POSTCODES_FILE
from scrape import scrape_realestate_postcode, is_postcode_completed

logging.basicConfig(
    # filename=LOG_FILE,
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

if __name__ == "__main__":
    with open(POSTCODES_FILE, "r") as file:
        postcodes: List[str] = [line.strip() for line in file.readlines()]
        postcodes = [p.split(" ")[0] for p in postcodes]

    if not postcodes:
        raise ValueError(
            f"No valid postcodes found in {POSTCODES_FILE} with minimum {MIN_POSTCODE}"
        )

    # Filter out already completed postcodes before starting
    remaining_postcodes = [p for p in postcodes if not is_postcode_completed(p)]
    
    if not remaining_postcodes:
        logging.info("All postcodes already completed")
        exit(0)
    
    logging.info(f"Found {len(remaining_postcodes)} postcodes to scrape out of {len(postcodes)} total")

    # Initialize browser once for all postcodes
    browser_controller = BraveBrowserController(BASE_URL)
    # Given the list of populated postcodes, scrape each one
    pbar = tqdm.tqdm(remaining_postcodes, desc="Scraping Realestate Postcodes", unit="postcode")

    for postcode in pbar:
        try:
            browser_controller.open_browser()
            browser_controller.perform_initial_setup()
            scrape_realestate_postcode(postcode, browser_controller)

        finally:
            browser_controller.close_browser()
