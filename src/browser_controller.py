import logging
import os
import random
import shutil
import subprocess
import time
from abc import ABC, abstractmethod
from typing import Optional, Tuple

import pyautogui
from human_mouse import MouseController

from constants import (
    BRAVE_BROWSER_COMMAND,
    BROWSER_OPEN_WAIT,
    DEFAULT_URL,
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
    def perform_initial_setup(self) -> None:
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

    def __init__(self, initial_url: str = DEFAULT_URL):
        """Initialize with configurable starting URL"""
        self.initial_url = initial_url
        self.browser_bounds: Optional[Tuple[int, int, int, int]] = None

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

        # Detect browser window after launch
        self._detect_browser_window()
        logging.info("open_browser: Browser initialization complete")

    def perform_initial_setup(self) -> None:
        """Perform initial human-like browsing setup after browser is opened"""
        logging.info(
            "perform_initial_setup: Beginning initial human-like browsing simulation"
        )

        mouse = MouseController(always_zigzag=True)

        # Brief initial browsing simulation
        logging.info("perform_initial_setup: Simulating initial reading pattern")
        self._simulate_reading_pattern(mouse)

        wait_time = random.uniform(2, 4)
        logging.info(
            f"perform_initial_setup: Pausing for {wait_time:.2f} seconds between activities"
        )
        time.sleep(wait_time)

        logging.info("perform_initial_setup: Simulating initial natural scrolling")
        self._simulate_natural_scrolling(mouse)

        logging.info("perform_initial_setup: Initial setup complete")

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

    def _detect_browser_window(self) -> None:
        """Detect and store browser window bounds using wmctrl"""
        try:
            # Use wmctrl to get window geometry
            result = subprocess.run(
                ["wmctrl", "-lG"], capture_output=True, text=True, check=True
            )

            # Parse wmctrl output to find browser window
            # Format: window_id desktop x y width height client_machine window_title
            for line in result.stdout.strip().split("\n"):
                if line and ("Brave" in line or "Mozilla" in line or "Chrome" in line):
                    parts = line.split(None, 7)  # Split into max 8 parts
                    if len(parts) >= 6:
                        try:
                            x, y, width, height = map(int, parts[2:6])
                            self.browser_bounds = (x, y, x + width, y + height)
                            logging.info(
                                f"_detect_browser_window: Found browser window at {self.browser_bounds}"
                            )
                            return
                        except ValueError:
                            continue

            # No browser window found
            logging.warning(
                "_detect_browser_window: No browser window found, using full screen"
            )
            screen_width, screen_height = pyautogui.size()
            self.browser_bounds = (0, 0, screen_width, screen_height)

        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            logging.error(f"_detect_browser_window: wmctrl error: {e}")
            screen_width, screen_height = pyautogui.size()
            self.browser_bounds = (0, 0, screen_width, screen_height)
        except Exception as e:
            logging.error(f"_detect_browser_window: Unexpected error: {e}")
            screen_width, screen_height = pyautogui.size()
            self.browser_bounds = (0, 0, screen_width, screen_height)

    def _get_browser_content_area(self) -> Tuple[int, int, int, int]:
        """Get the content area of the browser (excluding title bar and toolbars)"""
        if not self.browser_bounds:
            self._detect_browser_window()

        if self.browser_bounds:
            left, top, right, bottom = self.browser_bounds
            # Add margins to avoid title bar, address bar, and scrollbars
            content_left = left + 20
            content_top = top + 100  # Account for title bar and address bar
            content_right = right - 20  # Account for scrollbar
            content_bottom = bottom - 50  # Account for status bar

            # Ensure we have a valid area
            if content_right > content_left and content_bottom > content_top:
                return content_left, content_top, content_right, content_bottom

        # Fallback to screen center area
        screen_width, screen_height = pyautogui.size()
        return (
            int(screen_width * 0.1),
            int(screen_height * 0.1),
            int(screen_width * 0.9),
            int(screen_height * 0.9),
        )

    def generate_random_coordinates(self) -> Tuple[int, int]:
        """Generate random coordinates within browser content area"""
        content_left, content_top, content_right, content_bottom = (
            self._get_browser_content_area()
        )

        x = random.randint(content_left, content_right - 1)
        y = random.randint(content_top, content_bottom - 1)
        return x, y

    def perform_human_like_activity(self) -> None:
        """Perform realistic human-like browsing behavior"""
        logging.info(
            "perform_human_like_activity: Starting comprehensive human-like browsing simulation"
        )

        mouse = MouseController(always_zigzag=True)

        # Simulate reading the page content
        logging.info("perform_human_like_activity: Phase 1 - Simulating page reading")
        self._simulate_reading_pattern(mouse)

        # Natural scrolling behavior
        logging.info(
            "perform_human_like_activity: Phase 2 - Simulating natural scrolling"
        )
        self._simulate_natural_scrolling(mouse)

        logging.info(
            "perform_human_like_activity: All human-like browsing simulation phases complete"
        )

    def _simulate_reading_pattern(self, mouse: MouseController) -> None:
        """Simulate reading text in a natural left-to-right, top-to-bottom pattern"""
        content_left, content_top, content_right, content_bottom = (
            self._get_browser_content_area()
        )

        # Start from top-left area of browser content where text typically begins
        start_x = content_left + 50  # Small margin from left edge
        start_y = content_top + 50  # Small margin from top
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

            # Read across the line (simulate eye movement) - stay within browser bounds
            max_line_length = min(600, content_right - start_x - 50)
            end_x = start_x + random.randint(300, max_line_length)
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

            # Move to a random position within browser before scrolling (more natural)
            speed = random.uniform(1.0, 2.0)
            logging.info(
                f"_simulate_natural_scrolling: Moving to random position with speed {speed:.2f}"
            )
            # Generate random coordinates within browser bounds
            rand_x, rand_y = self.generate_random_coordinates()

            mouse.move(rand_x, rand_y, speed_factor=speed)

            move_pause = random.uniform(0.2, 0.5)
            logging.info(
                f"_simulate_natural_scrolling: Pausing {move_pause:.2f}s before scrolling"
            )
            time.sleep(move_pause)

            # Small scroll amounts like a human reading
            scroll_amount = random.randint(3, 12)
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
                back_scroll = random.randint(3, 12)
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
