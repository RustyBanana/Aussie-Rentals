import logging
from typing import List

from browser_controller import BraveBrowserController
from constants import MIN_POSTCODE, POSTCODES_FILE

logging.basicConfig(
    # filename=LOG_FILE,
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

if __name__ == "__main__":
    with open(POSTCODES_FILE, "r") as file:
        postcodes: List[str] = [line.strip() for line in file.readlines()]
        postcodes = [p for p in postcodes if p >= MIN_POSTCODE]

    if not postcodes:
        raise ValueError(
            f"No valid postcodes found in {POSTCODES_FILE} with minimum {MIN_POSTCODE}"
        )

    # Initialize browser once for all postcodes
    browser_controller = BraveBrowserController()

    try:
        browser_controller.open_browser()
        browser_controller.perform_initial_setup()
        browser_controller.save_page(
            "/home/william/projects/Aussie-Rentals/data/test.html"
        )

        # Given the list of populated postcodes, scrape each one
        # pbar = tqdm(postcodes, desc="Scraping Realestate Postcodes", unit="postcode")

        # for postcode in pbar:
        #     scrape_realestate_postcode(postcode, browser_controller)

    finally:
        browser_controller.close_browser()
