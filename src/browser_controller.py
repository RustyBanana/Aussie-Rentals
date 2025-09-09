import logging
import os
import random
import shutil
import subprocess
import time
from abc import ABC, abstractmethod

import pyautogui


class BrowserController(ABC):
    """Abstract interface for browser operations"""

    @abstractmethod
    def open_browser(self) -> None:
        pass

    @abstractmethod
    def close_browser(self) -> None:
        pass

    @abstractmethod
    def navigate_to(self, url: str) -> None:
        pass

    @abstractmethod
    def save_page(self, filepath: str) -> None:
        pass

    @abstractmethod
    def perform_human_like_activity(self) -> None:
        pass


class BraveBrowserController(BrowserController):
    """Concrete implementation for Brave browser automation"""

    def open_browser(self) -> None:
        logging.info("open_browser")
        user_data_dir = os.path.abspath(USER_DATA_DIR)

        # Delete the brave_manual_profile folder and all its contents if it exists
        if os.path.exists(user_data_dir):
            shutil.rmtree(user_data_dir)

        os.makedirs(user_data_dir, exist_ok=True)

        # Launch Brave with a profile
        subprocess.Popen(
            [BRAVE_BROWSER_COMMAND, "--user-data-dir=" + user_data_dir, BASE_URL]
        )

        time.sleep(BROWSER_OPEN_WAIT)

        print("Click around to show that you are human")
        time.sleep(USER_INTERACTION_WAIT)

    def close_browser(self) -> None:
        logging.info("close_browser")
        pyautogui.hotkey("alt", "f4")

    def navigate_to(self, url: str) -> None:
        logging.info(f"navigate_to: {url}")
        # Use keyboard shortcut to focus the address bar
        pyautogui.hotkey("ctrl", "l")
        time.sleep(0.1)

        # Clear any existing text and search for the URL
        pyautogui.hotkey("ctrl", "a")
        time.sleep(0.1)
        pyautogui.write(url)
        time.sleep(0.1)
        pyautogui.press("enter")

        # Wait for page to load
        random_wait(base=PAGE_LOAD_BASE_WAIT, jitter=PAGE_LOAD_JITTER)

    def save_page(self, filepath: str) -> None:
        logging.info(f"save_page: {filepath}")
        pyautogui.hotkey("ctrl", "s")
        time.sleep(1)

        absolute_filepath = os.path.abspath(filepath)

        # Type the full file path and save
        pyautogui.write(absolute_filepath)

        # Select HTML only option
        pyautogui.press("tab")
        pyautogui.press("right")
        pyautogui.press("up")
        pyautogui.press("up")
        pyautogui.press("enter")

        # Press Save
        pyautogui.press("enter")

        # Wait for save to finish before next page
        time.sleep(SAVE_WAIT)

    def perform_human_like_activity(self) -> None:
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
