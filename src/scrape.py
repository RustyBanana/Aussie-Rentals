import subprocess
import time
import os
import pyautogui
import random
from datetime import datetime

# Ensure output directory exists
OUTPUT_DIR = "html_pages"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def random_delay(min_sec:int|float=1, max_sec:int|float=3) -> None:
    """Wait a random amount of time"""
    delay = random.uniform(min_sec, max_sec)
    time.sleep(delay)


def open_chrome() -> None:
    # First, visit the main site
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    user_data_dir = os.path.abspath("./chrome_manual_profile")
    os.makedirs(user_data_dir, exist_ok=True)
    
    # Launch Chrome with a profile
    subprocess.Popen([
        chrome_path,
        "--user-data-dir=" + user_data_dir,
        "https://www.realestate.com.au/"
    ])
    
    # Give browser time to open
    time.sleep(2)


def navigate_to(url: str) -> None:
    """ Navigate to a specific URL in the browser """            
    # Use keyboard shortcut to focus the address bar
    pyautogui.hotkey('ctrl', 'l')
    random_delay(1, 2)
    
    # Clear any existing text and search for the URL
    pyautogui.hotkey('ctrl', 'a')
    random_delay(0.5, 1)
    pyautogui.write(url)
    random_delay(1, 3)
    pyautogui.press('enter')
        
    # Wait for page to load
    time.sleep(3)


def save_page(filename: str) -> None:
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
    random_delay(1, 3)


def check_stop(filename: str) -> bool:
    """ Check if the file exists and if it contains 'ResidentialCard' """
    if not os.path.exists(filename):
        return True

    with open(filename, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()
        return 'ResidentialCard' not in content
        

def scrape_realestate_postcodes(postcode: str) -> None:
    """ Scrape realestate.com.au for a specific postcode using a normal browser instance """
    open_chrome()
                    
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
            
    # Close the browser
    pyautogui.hotkey('alt', 'f4')