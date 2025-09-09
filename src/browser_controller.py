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

    def __init__(self, initial_url: str = BASE_URL):
        """Initialize with configurable starting URL"""
        self.initial_url = initial_url

    def open_browser(self) -> None:
        logging.info("open_browser: Starting browser initialization")
        user_data_dir = os.path.abspath(USER_DATA_DIR)

        # Delete the brave_manual_profile folder and all its contents if it exists
        if os.path.exists(user_data_dir):
            logging.info("open_browser: Cleaning up existing user data directory")
            shutil.rmtree(user_data_dir)

        os.makedirs(user_data_dir, exist_ok=True)
        logging.info(f"open_browser: Created user data directory at {user_data_dir}")

        # Launch Brave with a profile
        logging.info(
            f"open_browser: Launching Brave browser with URL {self.initial_url}"
        )
        subprocess.Popen(
            [
                BRAVE_BROWSER_COMMAND,
                "--user-data-dir=" + user_data_dir,
                self.initial_url,
            ]
        )

        logging.info(
            f"open_browser: Waiting {BROWSER_OPEN_WAIT} seconds for browser to start"
        )
        time.sleep(BROWSER_OPEN_WAIT)

        print("Performing automated human-like browsing to appear natural")
        logging.info("open_browser: Beginning initial human-like browsing simulation")

        # Perform initial human-like activity instead of manual clicking
        mouse = MouseController(always_zigzag=True)
        screen_width, screen_height = pyautogui.size()
        logging.info(
            f"open_browser: Screen dimensions detected: {screen_width}x{screen_height}"
        )

        # Brief initial browsing simulation
        logging.info("open_browser: Simulating initial reading pattern")
        self._simulate_reading_pattern(mouse, screen_width, screen_height)

        wait_time = random.uniform(2, 4)
        logging.info(
            f"open_browser: Pausing for {wait_time:.2f} seconds between activities"
        )
        time.sleep(wait_time)

        logging.info("open_browser: Simulating initial natural scrolling")
        self._simulate_natural_scrolling(mouse)
        logging.info("open_browser: Browser initialization and setup complete")

    def close_browser(self) -> None:
        logging.info("close_browser")
        pyautogui.hotkey("alt", "f4")

    def navigate_to(self, url: str) -> None:
        logging.info(f"navigate_to: Navigating to {url}")

        # Use keyboard shortcut to focus the address bar
        logging.info("navigate_to: Focusing address bar with Ctrl+L")
        pyautogui.hotkey("ctrl", "l")
        time.sleep(KEYBOARD_DELAY)

        # Clear any existing text and search for the URL
        logging.info("navigate_to: Clearing existing text and entering URL")
        pyautogui.hotkey("ctrl", "a")
        time.sleep(KEYBOARD_DELAY)
        pyautogui.write(url)
        time.sleep(KEYBOARD_DELAY)

        logging.info("navigate_to: Pressing Enter to navigate")
        pyautogui.press("enter")

        # Wait for page to load
        logging.info("navigate_to: Waiting for page to load")
        self._random_wait(base=PAGE_LOAD_BASE_WAIT, jitter=PAGE_LOAD_JITTER)
        logging.info("navigate_to: Navigation complete")

    def save_page(self, filepath: str) -> None:
        logging.info(f"save_page: Saving page to {filepath}")

        logging.info("save_page: Opening save dialog with Ctrl+S")
        pyautogui.hotkey("ctrl", "s")
        time.sleep(SAVE_DIALOG_WAIT)

        absolute_filepath = os.path.abspath(filepath)
        logging.info(f"save_page: Using absolute path: {absolute_filepath}")

        # Type the full file path and save
        logging.info("save_page: Entering file path")
        pyautogui.write(absolute_filepath)

        # Select HTML only option
        logging.info("save_page: Navigating to HTML-only save format")
        pyautogui.press("tab")
        pyautogui.press("right")
        pyautogui.press("up")
        pyautogui.press("up")
        pyautogui.press("enter")

        # Press Save
        logging.info("save_page: Confirming save operation")
        pyautogui.press("enter")

        # Wait for save to finish before next page
        logging.info(f"save_page: Waiting {SAVE_WAIT} seconds for save to complete")
        time.sleep(SAVE_WAIT)
        logging.info("save_page: Save operation complete")

    def generate_random_coordinates(
        self, screen_width: int, screen_height: int
    ) -> Tuple[int, int]:
        """Pure function to generate random screen coordinates"""
        x = random.randint(0, screen_width - 1)
        y = random.randint(0, screen_height - 1)
        return x, y

    def perform_human_like_activity(self) -> None:
        """Perform realistic human-like browsing behavior"""
        logging.info(
            "perform_human_like_activity: Starting comprehensive human-like browsing simulation"
        )

        mouse = MouseController(always_zigzag=True)
        screen_width, screen_height = pyautogui.size()
        logging.info(
            f"perform_human_like_activity: Using screen dimensions {screen_width}x{screen_height}"
        )

        # Simulate reading the page content
        logging.info("perform_human_like_activity: Phase 1 - Simulating page reading")
        self._simulate_reading_pattern(mouse, screen_width, screen_height)

        # Natural scrolling behavior
        logging.info(
            "perform_human_like_activity: Phase 2 - Simulating natural scrolling"
        )
        self._simulate_natural_scrolling(mouse)

        # Brief scanning of the page
        logging.info("perform_human_like_activity: Phase 3 - Simulating page scanning")
        self._simulate_scanning_pattern(mouse, screen_width, screen_height)

        logging.info(
            "perform_human_like_activity: All human-like browsing simulation phases complete"
        )

    def _simulate_reading_pattern(
        self, mouse: MouseController, screen_width: int, screen_height: int
    ) -> None:
        """Simulate reading text in a natural left-to-right, top-to-bottom pattern"""
        # Start from top-left area where content typically begins
        start_x = int(screen_width * 0.1)  # 10% from left edge
        start_y = int(screen_height * 0.2)  # 20% from top
        logging.info(
            f"_simulate_reading_pattern: Starting reading simulation at ({start_x}, {start_y})"
        )

        # Simulate reading 3-4 lines of text
        num_lines = random.randint(3, 4)
        line_height = 25  # Approximate line height in pixels
        logging.info(
            f"_simulate_reading_pattern: Will simulate reading {num_lines} lines"
        )

        for line in range(num_lines):
            y_pos = start_y + (line * line_height)
            logging.info(
                f"_simulate_reading_pattern: Reading line {line + 1} at y={y_pos}"
            )

            # Move to start of line with natural movement
            speed = random.uniform(0.8, 1.2)
            logging.info(
                f"_simulate_reading_pattern: Moving to line start with speed factor {speed:.2f}"
            )
            mouse.move(start_x, y_pos, speed_factor=speed)

            pause_time = random.uniform(0.1, 0.3)
            logging.info(
                f"_simulate_reading_pattern: Pausing {pause_time:.2f}s at line start"
            )
            time.sleep(pause_time)  # Brief pause at line start

            # Read across the line (simulate eye movement)
            end_x = start_x + random.randint(400, 600)  # Variable line length
            read_speed = random.uniform(0.6, 1.0)
            logging.info(
                f"_simulate_reading_pattern: Reading across line to x={end_x} with speed {read_speed:.2f}"
            )
            mouse.move(end_x, y_pos, speed_factor=read_speed)

            # Pause at end of line (reading time)
            read_time = random.uniform(0.8, 1.5)
            logging.info(
                f"_simulate_reading_pattern: Reading pause of {read_time:.2f}s at line end"
            )
            time.sleep(read_time)

        logging.info("_simulate_reading_pattern: Reading pattern simulation complete")

    def _simulate_scanning_pattern(
        self, mouse: MouseController, screen_width: int, screen_height: int
    ) -> None:
        """Simulate F-pattern scanning behavior common in web browsing"""
        logging.info(
            "_simulate_scanning_pattern: Starting F-pattern scanning simulation"
        )
        # F-pattern: horizontal movements at top, middle, then vertical scan

        # Top horizontal scan
        top_y = int(screen_height * 0.15)
        logging.info(f"_simulate_scanning_pattern: Top horizontal scan at y={top_y}")

        speed1 = random.uniform(0.8, 1.2)
        logging.info(
            f"_simulate_scanning_pattern: Moving to top-left with speed {speed1:.2f}"
        )
        mouse.move(int(screen_width * 0.1), top_y, speed_factor=speed1)
        time.sleep(0.2)

        speed2 = random.uniform(0.6, 1.0)
        logging.info(
            f"_simulate_scanning_pattern: Scanning across top with speed {speed2:.2f}"
        )
        mouse.move(int(screen_width * 0.7), top_y, speed_factor=speed2)

        pause1 = random.uniform(0.5, 1.0)
        logging.info(
            f"_simulate_scanning_pattern: Pausing {pause1:.2f}s after top scan"
        )
        time.sleep(pause1)

        # Middle horizontal scan (shorter)
        mid_y = int(screen_height * 0.4)
        logging.info(f"_simulate_scanning_pattern: Middle horizontal scan at y={mid_y}")

        speed3 = random.uniform(0.8, 1.2)
        logging.info(
            f"_simulate_scanning_pattern: Moving to middle-left with speed {speed3:.2f}"
        )
        mouse.move(int(screen_width * 0.1), mid_y, speed_factor=speed3)
        time.sleep(0.2)

        speed4 = random.uniform(0.6, 1.0)
        logging.info(
            f"_simulate_scanning_pattern: Scanning across middle (shorter) with speed {speed4:.2f}"
        )
        mouse.move(int(screen_width * 0.5), mid_y, speed_factor=speed4)

        pause2 = random.uniform(0.3, 0.8)
        logging.info(
            f"_simulate_scanning_pattern: Pausing {pause2:.2f}s after middle scan"
        )
        time.sleep(pause2)

        # Vertical scan down the left side
        logging.info("_simulate_scanning_pattern: Beginning vertical left-side scan")
        for i, progress in enumerate([0.6, 0.7, 0.8]):
            y_pos = int(screen_height * progress)
            speed = random.uniform(0.7, 1.1)
            logging.info(
                f"_simulate_scanning_pattern: Vertical scan point {i + 1}/3 at y={y_pos} with speed {speed:.2f}"
            )
            mouse.move(int(screen_width * 0.15), y_pos, speed_factor=speed)
            pause = random.uniform(0.2, 0.5)
            logging.info(
                f"_simulate_scanning_pattern: Pausing {pause:.2f}s at scan point"
            )
            time.sleep(pause)

        logging.info("_simulate_scanning_pattern: F-pattern scanning complete")

    def _simulate_natural_scrolling(self, mouse: MouseController) -> None:
        """Simulate natural scrolling behavior while reading"""
        num_scrolls = random.randint(2, 4)
        logging.info(
            f"_simulate_natural_scrolling: Will perform {num_scrolls} scroll actions"
        )

        for i in range(num_scrolls):
            logging.info(
                f"_simulate_natural_scrolling: Scroll action {i + 1}/{num_scrolls}"
            )

            # Move to a random position before scrolling (more natural)
            speed = random.uniform(1.0, 2.0)
            logging.info(
                f"_simulate_natural_scrolling: Moving to random position with speed {speed:.2f}"
            )
            mouse.move_random(speed_factor=speed)

            move_pause = random.uniform(0.2, 0.5)
            logging.info(
                f"_simulate_natural_scrolling: Pausing {move_pause:.2f}s before scrolling"
            )
            time.sleep(move_pause)

            # Small scroll amounts like a human reading
            scroll_amount = random.randint(100, 300)
            logging.info(
                f"_simulate_natural_scrolling: Scrolling down {scroll_amount} pixels"
            )
            pyautogui.scroll(-scroll_amount)  # Negative for scrolling down

            # Pause to "read" the new content
            reading_time = random.uniform(1.5, 3.0)
            logging.info(
                f"_simulate_natural_scrolling: Reading pause of {reading_time:.2f}s"
            )
            time.sleep(reading_time)

            # Occasionally scroll back up slightly (like re-reading)
            if random.random() < 0.3:
                back_scroll = random.randint(50, 100)
                logging.info(
                    f"_simulate_natural_scrolling: Re-reading - scrolling back up {back_scroll} pixels"
                )
                pyautogui.scroll(back_scroll)

                reread_time = random.uniform(0.5, 1.0)
                logging.info(
                    f"_simulate_natural_scrolling: Re-reading pause of {reread_time:.2f}s"
                )
                time.sleep(reread_time)
            else:
                logging.info("_simulate_natural_scrolling: No re-reading this time")

        logging.info(
            "_simulate_natural_scrolling: Natural scrolling simulation complete"
        )

    def _random_wait(
        self, base: float = 5, jitter: float = 5, max_wait: float = 30
    ) -> None:
        """Private method for random wait times"""
        wait_time = calculate_wait_time(base, jitter, max_wait)
        logging.info(f"Sleeping for {wait_time:.2f} seconds")
        time.sleep(wait_time)
