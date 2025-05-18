import subprocess
import time
import os
import pyautogui
import random
from datetime import datetime

# Ensure output directory exists
OUTPUT_DIR = "manual_scrape_results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def random_delay(min_sec=1, max_sec=3):
    """Wait a random amount of time"""
    delay = random.uniform(min_sec, max_sec)
    time.sleep(delay)

def visit_realestate_postcodes(postcodes):
    """
    Visit realestate.com.au with specific postcodes using a real browser
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    try:
        # First, visit the main site
        print("Opening Chrome with realestate.com.au...")
        
        # Open Chrome with a new user profile
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
        print("Waiting for browser to open...")
        time.sleep(2)
                       
        joined = '%3B+'.join(postcodes)
        # Now navigate to search pages for each postcode and capture
        for page_num in range(1, 2):
            target_url = f"https://www.realestate.com.au/rent/in-{joined}/list-{page_num}?includeSurrounding=false"
            
            print(f"Navigating to page {page_num}: {target_url}")
            
            # Use keyboard shortcut to focus the address bar
            pyautogui.hotkey('ctrl', 'l')
            random_delay(1, 2)
            
            # Clear any existing text and type the URL
            pyautogui.hotkey('ctrl', 'a')
            random_delay(0.5, 1)
            
            pyautogui.write(target_url)
            random_delay(1)
            
            pyautogui.press('enter')
            
            # Wait for page to load
            print("Waiting for page to load...")
                                                   
            # Wait between pages
            random_delay(5, 8)

            # if 'ResidentialCard' not in html:
            #   break
        
        print("\n" + "="*60)
        print("DATA COLLECTION COMPLETE!")
        print(f"Data saved in {OUTPUT_DIR}")
        print("="*60 + "\n")
                
        # Close the browser
        pyautogui.hotkey('alt', 'f4')
        
    except Exception as e:
        print(f"Error during process: {e}")
        
if __name__ == "__main__":    
    print("Starting realestate.com.au manual browser scraper")

    visit_realestate_postcodes(['3215'])