import logging
import time

from browser_controller import BraveBrowserController


class TestBraveBrowserController:
    """Test suite for BraveBrowserController with Wikipedia page"""

    def test_wikipedia_human_activity_integration(self):
        """Integration test that opens Wikipedia WWII page and performs human-like activity"""
        logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
        browser_controller = BraveBrowserController()

        try:
            # Open browser (will start at Wikipedia)
            browser_controller.open_browser()

            # Give user time to see the page load
            print("Wikipedia page loaded. Starting human-like activity simulation...")
            time.sleep(2)

            # Perform human-like activity on the Wikipedia page
            browser_controller.perform_human_like_activity()

            print("Human-like activity simulation completed successfully")

            # Keep browser open for a moment to observe the behavior
            time.sleep(3)

        finally:
            browser_controller.close_browser()
