from scrape import scrape_realestate_postcodes
from tqdm import tqdm


if __name__ == "__main__":    
    pbar = tqdm(range(0, 10000), desc="Scraping Realestate Postcodes", unit="postcode")
    for postcode in pbar:
        if postcode != 3215:
            continue
        postcode = f'{postcode:04d}'
        try:
            scrape_realestate_postcodes(postcode)
        except Exception as e:
            print(f"Error during scraping {postcode}: {e}")