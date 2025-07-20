import subprocess
import time
import os
import pyautogui
from datetime import datetime
import logging
import traceback
import random


OUTPUT_DIR = f'html_pages'
os.makedirs(OUTPUT_DIR, exist_ok=True)
LOG_FILE = "scrape.log"
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
        # Negative x due to second monitor on the left
        pyautogui.moveTo(-x, y, duration=random.uniform(0.2, 0.8))
        if random.random() < 0.3:
            pyautogui.click()
        time.sleep(random.uniform(0.1, 0.5))


def open_chrome() -> None:
    logging.info('open_chrome')
    # First, visit the main site
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    user_data_dir = os.path.abspath("./chrome_manual_profile")
    os.makedirs(user_data_dir, exist_ok=True)
    
    # Launch Chrome with a profile
    subprocess.Popen([
        chrome_path,
        "--user-data-dir=" + user_data_dir,
        #"--incognito",
        "https://www.realestate.com.au/"
    ])
    
    # Give browser time to open
    time.sleep(3)
    # Maximize window
    pyautogui.hotkey('win', 'up')
    
    print('Click around to show that you are human')
    time.sleep(30)  # Allow user to interact with browser


def close_chrome() -> None:
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
    random_wait(base=10, jitter=5)
    random_mouse_activity()


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
    time.sleep(6)


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
        # Now navigate to search pages for each postcode and capture
        page_num = 1
        while True:
            url = f"https://www.realestate.com.au/rent/in-{postcode}/list-{page_num}?includeSurrounding=false"
            navigate_to(url)

            # Generate file name
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{OUTPUT_DIR}/{postcode}_{page_num}_{timestamp}.html"
            save_page(filename)

            if check_stop(filename):
                break

            page_num += 1

    except Exception as e:
        logging.error(f"Error scraping postcode {postcode}: {e}\n{traceback.format_exc()}")