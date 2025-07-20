from scrape import scrape_realestate_postcode
from tqdm import tqdm


if __name__ == "__main__":    
    with open("data/postcodes sydney.txt", "r") as file:
        postcodes = [line.strip() for line in file.readlines()]

    # Given the list of populated postcodes, scrape each one
    pbar = tqdm(postcodes, desc="Scraping Realestate Postcodes", unit="postcode")
    
    for postcode in pbar:
        scrape_realestate_postcode(postcode)