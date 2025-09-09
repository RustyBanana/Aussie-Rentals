import logging
import os
import random
import shutil
import subprocess
import time
from abc import ABC, abstractmethod
from typing import Tuple

import pyautogui
from human_mouse import MouseController

from constants import (
    BASE_URL,
    BRAVE_BROWSER_COMMAND,
    BROWSER_OPEN_WAIT,
    KEYBOARD_DELAY,
    PAGE_LOAD_BASE_WAIT,
    PAGE_LOAD_JITTER,
    SAVE_DIALOG_WAIT,
    SAVE_WAIT,
    USER_DATA_DIR,
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

        print("Performing automated human-like browsing to appear natural")

        # Perform initial human-like activity instead of manual clicking
        mouse = MouseController(always_zigzag=True)
        screen_width, screen_height = pyautogui.size()

        # Brief initial browsing simulation
        self._simulate_reading_pattern(mouse, screen_width, screen_height)
        time.sleep(random.uniform(2, 4))
        self._simulate_natural_scrolling(mouse)

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

    def perform_human_like_activity(self) -> None:
        """Perform realistic human-like browsing behavior"""
        logging.info("Starting human-like browsing simulation")

        mouse = MouseController(always_zigzag=True)
        screen_width, screen_height = pyautogui.size()

        # Simulate reading the page content
        self._simulate_reading_pattern(mouse, screen_width, screen_height)

        # Natural scrolling behavior
        self._simulate_natural_scrolling(mouse)

        # Brief scanning of the page
        self._simulate_scanning_pattern(mouse, screen_width, screen_height)

        logging.info("Completed human-like browsing simulation")

    def _simulate_reading_pattern(
        self, mouse: MouseController, screen_width: int, screen_height: int
    ) -> None:
        """Simulate reading text in a natural left-to-right, top-to-bottom pattern"""
        # Start from top-left area where content typically begins
        start_x = int(screen_width * 0.1)  # 10% from left edge
        start_y = int(screen_height * 0.2)  # 20% from top

        # Simulate reading 3-4 lines of text
        num_lines = random.randint(3, 4)
        line_height = 25  # Approximate line height in pixels

        for line in range(num_lines):
            y_pos = start_y + (line * line_height)

            # Move to start of line with natural movement
            mouse.move(start_x, y_pos, speed_factor=random.uniform(0.8, 1.2))
            time.sleep(random.uniform(0.1, 0.3))  # Brief pause at line start

            # Read across the line (simulate eye movement)
            end_x = start_x + random.randint(400, 600)  # Variable line length
            mouse.move(end_x, y_pos, speed_factor=random.uniform(0.6, 1.0))

            # Pause at end of line (reading time)
            time.sleep(random.uniform(0.8, 1.5))

    def _simulate_scanning_pattern(
        self, mouse: MouseController, screen_width: int, screen_height: int
    ) -> None:
        """Simulate F-pattern scanning behavior common in web browsing"""
        # F-pattern: horizontal movements at top, middle, then vertical scan

        # Top horizontal scan
        top_y = int(screen_height * 0.15)
        mouse.move(
            int(screen_width * 0.1), top_y, speed_factor=random.uniform(0.8, 1.2)
        )
        time.sleep(0.2)
        mouse.move(
            int(screen_width * 0.7), top_y, speed_factor=random.uniform(0.6, 1.0)
        )
        time.sleep(random.uniform(0.5, 1.0))

        # Middle horizontal scan (shorter)
        mid_y = int(screen_height * 0.4)
        mouse.move(
            int(screen_width * 0.1), mid_y, speed_factor=random.uniform(0.8, 1.2)
        )
        time.sleep(0.2)
        mouse.move(
            int(screen_width * 0.5), mid_y, speed_factor=random.uniform(0.6, 1.0)
        )
        time.sleep(random.uniform(0.3, 0.8))

        # Vertical scan down the left side
        for progress in [0.6, 0.7, 0.8]:
            y_pos = int(screen_height * progress)
            mouse.move(
                int(screen_width * 0.15), y_pos, speed_factor=random.uniform(0.7, 1.1)
            )
            time.sleep(random.uniform(0.2, 0.5))

    def _simulate_natural_scrolling(self, mouse: MouseController) -> None:
        """Simulate natural scrolling behavior while reading"""
        num_scrolls = random.randint(2, 4)

        for _ in range(num_scrolls):
            # Move to a random position before scrolling (more natural)
            mouse.move_random(speed_factor=random.uniform(1.0, 2.0))
            time.sleep(random.uniform(0.2, 0.5))

            # Small scroll amounts like a human reading
            scroll_amount = random.randint(100, 300)
            pyautogui.scroll(-scroll_amount)  # Negative for scrolling down

            # Pause to "read" the new content
            reading_time = random.uniform(1.5, 3.0)
            time.sleep(reading_time)

            # Occasionally scroll back up slightly (like re-reading)
            if random.random() < 0.3:
                pyautogui.scroll(random.randint(50, 100))
                time.sleep(random.uniform(0.5, 1.0))

    def _random_wait(
        self, base: float = 5, jitter: float = 5, max_wait: float = 30
    ) -> None:
        """Private method for random wait times"""
        wait_time = calculate_wait_time(base, jitter, max_wait)
        logging.info(f"Sleeping for {wait_time:.2f} seconds")
        time.sleep(wait_time)
