import subprocess
import time
import os
import pyautogui
from datetime import datetime
import logging
import traceback
import random
import shutil


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
    datefmt="%Y-%m-%d %H:%M:%S"
)


def random_wait(base=5, jitter=5, max_wait=30):
    wait = min(base + random.expovariate(1 / jitter), max_wait)
    logging.info(f"Sleeping for {wait:.2f} seconds")
    time.sleep(wait)


def random_mouse_activity():
    screenWidth, screenHeight = pyautogui.size()
    for _ in range(random.randint(3, 6)):
        x = random.randint(0, screenWidth - 1)
        y = random.randint(0, screenHeight - 1)
        
        # Move to random position on left monitor (x is negative)
        pyautogui.moveTo(-x, y, duration=random.uniform(0.2, 0.8))

        # Occasionally click
        if random.random() < 0.3:
            pyautogui.click()

        # Occasionally scroll
        if random.random() < 0.9:
            scroll_amount = random.randint(100, 1000)
            pyautogui.scroll(scroll_amount)

        time.sleep(random.uniform(0.1, 0.5))


def open_brave() -> None:
    logging.info('open_brave')
    # First, visit the main site
    user_data_dir = os.path.abspath(USER_DATA_DIR)

    # Delete the brave_manual_profile folder and all its contents if it exists
    if os.path.exists(user_data_dir):
        shutil.rmtree(user_data_dir, ignore_errors=True)

    os.makedirs(user_data_dir, exist_ok=True)
    
    # Launch Brave with a profile
    subprocess.Popen([
        BRAVE_BROWSER_COMMAND,
        "--user-data-dir=" + user_data_dir,
        #"--incognito",
        BASE_URL
    ])
    
    time.sleep(BROWSER_OPEN_WAIT)
    
    print('Click around to show that you are human')
    time.sleep(USER_INTERACTION_WAIT)


def close_brave() -> None:
    logging.info(f"scrape_realestate_postcode: Closing browser")
    pyautogui.hotkey('alt', 'f4')


def navigate_to(url: str) -> None:
    """ Navigate to a specific URL in the browser """   
    logging.info(f"navigate_to: {url}")         
    # Use keyboard shortcut to focus the address bar
    pyautogui.hotkey('ctrl', 'l')
    time.sleep(0.1)
    
    # Clear any existing text and search for the URL
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.1)
    pyautogui.write(url)
    time.sleep(0.1)
    pyautogui.press('enter')
        
    # Wait for page to load
    random_wait(base=PAGE_LOAD_BASE_WAIT, jitter=PAGE_LOAD_JITTER)


def save_page(filename: str) -> None:
    logging.info(f"save_page: {filename}")
    pyautogui.hotkey('ctrl', 's')
    time.sleep(1)

    filepath = os.path.abspath(filename)

    # Type the full file path and save
    pyautogui.write(filepath)
    
    # Select HTML only option
    pyautogui.press('tab')
    pyautogui.press('right')
    pyautogui.press('up')
    pyautogui.press('up')
    pyautogui.press('enter')

    # Press Save
    pyautogui.press('enter')

    # Wait for save to finish before next page
    time.sleep(SAVE_WAIT)


def check_stop(filename: str) -> bool:
    """ Check if the file exists and if it contains 'ResidentialCard' """
    logging.info(f"check_stop: {filename}")
    if not os.path.exists(filename):
        logging.error(f"check_stop: File does not exist: {filename}")
        return True

    with open(filename, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()
        if 'ResidentialCard' in content:
            logging.info(f"check_stop: Continue")
            return False
        
    logging.info(f"check_stop: Stop. Deleting file: {filename}")
    os.remove(filename)
    return True
                

def scrape_realestate_postcode(postcode: str) -> None:
    """ Scrape realestate.com.au for a specific postcode using a normal browser instance """
    logging.info(f"scrape_realestate_postcode: {postcode}")
    try:                        
        open_brave()

        # Now navigate to search pages for each postcode and capture
        page_num = 1
        while True:
            url = SEARCH_URL_TEMPLATE.format(postcode=postcode, page_num=page_num)
            navigate_to(url)

            # Generate file name
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{OUTPUT_DIR}/{postcode}_{page_num}_{timestamp}.html"
            save_page(filename)
            random_mouse_activity()

            if check_stop(filename):
                break

            page_num += 1

    except Exception as e:
        logging.error(f"Error scraping postcode {postcode}: {e}\n{traceback.format_exc()}")

    finally:
        close_brave()
        logging.info(f"Finished scraping postcode {postcode}")
        time.sleep(ITERATION_WAIT)
