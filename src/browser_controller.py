import logging
import os
import random
import shutil
import subprocess
import time
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple

import pyautogui

from constants import (
    BASE_URL,
    BRAVE_BROWSER_COMMAND,
    BROWSER_OPEN_WAIT,
    CLICK_PROBABILITY,
    KEYBOARD_DELAY,
    MAX_ACTIVITY_ACTIONS,
    MAX_ACTIVITY_WAIT,
    MAX_MOVE_DURATION,
    MAX_SCROLL_AMOUNT,
    MIN_ACTIVITY_ACTIONS,
    MIN_ACTIVITY_WAIT,
    MIN_MOVE_DURATION,
    MIN_SCROLL_AMOUNT,
    PAGE_LOAD_BASE_WAIT,
    PAGE_LOAD_JITTER,
    SAVE_DIALOG_WAIT,
    SAVE_WAIT,
    SCROLL_PROBABILITY,
    USER_DATA_DIR,
    USER_INTERACTION_WAIT,
)


def calculate_wait_time(
    base: float = 5, jitter: float = 5, max_wait: float = 30
) -> float:
    """Calculate wait time using exponential distribution - pure function"""
    return min(base + random.expovariate(1 / jitter), max_wait)


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
        time.sleep(KEYBOARD_DELAY)

        # Clear any existing text and search for the URL
        pyautogui.hotkey("ctrl", "a")
        time.sleep(KEYBOARD_DELAY)
        pyautogui.write(url)
        time.sleep(KEYBOARD_DELAY)
        pyautogui.press("enter")

        # Wait for page to load
        self._random_wait(base=PAGE_LOAD_BASE_WAIT, jitter=PAGE_LOAD_JITTER)

    def save_page(self, filepath: str) -> None:
        logging.info(f"save_page: {filepath}")
        pyautogui.hotkey("ctrl", "s")
        time.sleep(SAVE_DIALOG_WAIT)

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

    def generate_random_coordinates(
        self, screen_width: int, screen_height: int
    ) -> Tuple[int, int]:
        """Pure function to generate random screen coordinates"""
        x = random.randint(0, screen_width - 1)
        y = random.randint(0, screen_height - 1)
        return x, y

    def generate_activity_plan(
        self, num_actions: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Pure function to generate a plan of human-like activities"""
        if num_actions is None:
            num_actions = random.randint(MIN_ACTIVITY_ACTIONS, MAX_ACTIVITY_ACTIONS)

        activities = []
        for _ in range(num_actions):
            activity = {
                "should_click": random.random() < CLICK_PROBABILITY,
                "should_scroll": random.random() < SCROLL_PROBABILITY,
                "scroll_amount": random.randint(MIN_SCROLL_AMOUNT, MAX_SCROLL_AMOUNT),
                "move_duration": random.uniform(MIN_MOVE_DURATION, MAX_MOVE_DURATION),
                "wait_time": random.uniform(MIN_ACTIVITY_WAIT, MAX_ACTIVITY_WAIT),
            }
            activities.append(activity)
        return activities

    def perform_human_like_activity(self) -> None:
        screenWidth, screenHeight = pyautogui.size()
        activities = self.generate_activity_plan()

        for activity in activities:
            x, y = self.generate_random_coordinates(screenWidth, screenHeight)

            # Move to random position on left monitor (x is negative)
            pyautogui.moveTo(-x, y, duration=activity["move_duration"])

            # Occasionally click
            if activity["should_click"]:
                pyautogui.click()

            # Occasionally scroll
            if activity["should_scroll"]:
                pyautogui.scroll(activity["scroll_amount"])

            time.sleep(activity["wait_time"])

    def _random_wait(
        self, base: float = 5, jitter: float = 5, max_wait: float = 30
    ) -> None:
        """Private method for random wait times"""
        wait_time = calculate_wait_time(base, jitter, max_wait)
        logging.info(f"Sleeping for {wait_time:.2f} seconds")
        time.sleep(wait_time)
