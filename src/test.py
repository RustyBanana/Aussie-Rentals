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
    print(f"Saved: {filepath}")


def open_chrome() -> None:
    # First, visit the main site
    print("Opening Chrome with realestate.com.au...")
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
    print(f"Navigating to {url}")
            
    # Use keyboard shortcut to focus the address bar
    pyautogui.hotkey('ctrl', 'l')
    random_delay(1, 2)
    
    # Clear any existing text and search for the URL
    pyautogui.hotkey('ctrl', 'a')
    random_delay(0.5, 1)
    pyautogui.write(url)
    random_delay(1, 3)
    pyautogui.press('enter')


def check_stop(filename: str) -> bool:
    """ Check if the file exists and is not empty """
    if os.path.exists(filename):
        file_size = os.path.getsize(filename)
        if file_size > 0:
            print(f"File {filename} saved successfully.")
            return False
        else:
            print(f"File {filename} is empty. Stopping the process.")
            return True
    else:
        print(f"File {filename} does not exist. Stopping the process.")
        return True


def scrape_realestate_postcodes(postcodes: list[str]) -> None:
    """ Scrape realestate.com.au with specific postcodes using a real browser """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    open_chrome()
                    
    joined = '%3B+'.join(postcodes)
    # Now navigate to search pages for each postcode and capture
    for page_num in range(1, 2):
        url = f"https://www.realestate.com.au/rent/in-{joined}/list-{page_num}?includeSurrounding=false"
        navigate_to(url)
        
        # Wait for page to load
        time.sleep(3)

        # Generate file name
        filename = f"{OUTPUT_DIR}/{joined.replace('%3B+', '_')}_{page_num}_{timestamp}.html"
        save_page(filename)

        # Wait for save to finish before next page
        random_delay(1, 3)

        if check_stop(filename):
            break

    print(f"Data saved in {OUTPUT_DIR}")
            
    # Close the browser
    pyautogui.hotkey('alt', 'f4')

        
if __name__ == "__main__":    
    print("Starting realestate.com.au manual browser scraper")

    try:
        scrape_realestate_postcodes(['3215'])
    except Exception as e:
        print(f"Error during process: {e}")