from scrape import scrape_realestate_postcode
from tqdm import tqdm
from datetime import datetime
import os


if __name__ == "__main__":    
    pbar = tqdm(range(0, 10000), desc="Scraping Realestate Postcodes", unit="postcode")
    for postcode in pbar:
        postcode = f'{postcode:04d}'
        scrape_realestate_postcode(postcode)