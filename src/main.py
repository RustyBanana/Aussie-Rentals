from scrape import scrape_realestate_postcode
from constants import POSTCODES_FILE, MIN_POSTCODE
from tqdm import tqdm


if __name__ == "__main__":    
    with open(POSTCODES_FILE, "r") as file:
        postcodes = [line.strip() for line in file.readlines()]
        postcodes = [p for p in postcodes if p >= MIN_POSTCODE]

    # Given the list of populated postcodes, scrape each one
    pbar = tqdm(postcodes, desc="Scraping Realestate Postcodes", unit="postcode")
    
    for postcode in pbar:
        scrape_realestate_postcode(postcode)
