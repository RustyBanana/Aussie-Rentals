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

    def test_generate_random_coordinates_returns_valid_coordinates(self):
        """Test that random coordinate generation returns valid screen coordinates"""
        browser_controller = BraveBrowserController()
        screen_width = 1920
        screen_height = 1080

        x, y = browser_controller.generate_random_coordinates(
            screen_width, screen_height
        )

        assert 0 <= x < screen_width
        assert 0 <= y < screen_height

    def test_generate_random_coordinates_different_values(self):
        """Test that random coordinate generation produces different values"""
        browser_controller = BraveBrowserController()
        screen_width = 1920
        screen_height = 1080

        coords1 = browser_controller.generate_random_coordinates(
            screen_width, screen_height
        )
        coords2 = browser_controller.generate_random_coordinates(
            screen_width, screen_height
        )

        # Very unlikely to get the same coordinates twice
        assert coords1 != coords2
