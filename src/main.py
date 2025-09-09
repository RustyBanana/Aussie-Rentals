from typing import List

from tqdm import tqdm

from constants import MIN_POSTCODE, POSTCODES_FILE
from scrape import scrape_realestate_postcode

if __name__ == "__main__":
    with open(POSTCODES_FILE, "r") as file:
        postcodes: List[str] = [line.strip() for line in file.readlines()]
        postcodes = [p for p in postcodes if p >= MIN_POSTCODE]

    if not postcodes:
        raise ValueError(
            f"No valid postcodes found in {POSTCODES_FILE} with minimum {MIN_POSTCODE}"
        )

    # Given the list of populated postcodes, scrape each one
    pbar = tqdm(postcodes, desc="Scraping Realestate Postcodes", unit="postcode")

    for postcode in pbar:
        scrape_realestate_postcode(postcode)
