import os
import subprocess
import sys

import pytest

# Add src directory to path so we can import browser_controller
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from browser_controller import BraveBrowserController


class TestWmctrl:
    """Test suite for wmctrl window detection functionality"""

    def test_wmctrl_available_and_functional(self):
        """Test that wmctrl is installed and can list windows"""
        try:
            result = subprocess.run(
                ["wmctrl", "-l"], capture_output=True, text=True, check=True
            )

            # Should return successfully with some output
            assert result.returncode == 0
            assert isinstance(result.stdout, str)
            # Should have at least some windows listed (even if no browser)
            assert len(result.stdout.strip()) > 0

        except FileNotFoundError:
            pytest.skip("wmctrl not installed - skipping window detection test")
        except subprocess.CalledProcessError as e:
            pytest.fail(f"wmctrl command failed: {e}")

    def test_wmctrl_geometry_output_format(self):
        """Test that wmctrl -lG returns parseable geometry information"""
        try:
            result = subprocess.run(
                ["wmctrl", "-lG"], capture_output=True, text=True, check=True
            )

            assert result.returncode == 0
            lines = result.stdout.strip().split("\n")

            # Should have at least one window
            assert len(lines) > 0

            # Check that at least one line has the expected format
            # Format: window_id desktop x y width height client_machine window_title
            for line in lines:
                if line.strip():  # Skip empty lines
                    parts = line.split(None, 7)  # Split into max 8 parts
                    assert len(parts) >= 6, f"Line doesn't have enough parts: {line}"

                    # Check that x, y, width, height are integers
                    try:
                        x, y, width, height = map(int, parts[2:6])
                        assert width > 0 and height > 0, (
                            f"Invalid dimensions: {width}x{height}"
                        )
                        break  # Found at least one valid window
                    except ValueError:
                        continue  # Try next line
            else:
                pytest.fail("No valid window geometry found in wmctrl output")

        except FileNotFoundError:
            pytest.skip("wmctrl not installed - skipping geometry test")
        except subprocess.CalledProcessError as e:
            pytest.fail(f"wmctrl -lG command failed: {e}")

    def test_wmctrl_detects_brave_window(self):
        """Test that wmctrl can detect a Brave browser window after launching it"""
        try:
            # Check if wmctrl is available first
            subprocess.run(["wmctrl", "-l"], capture_output=True, check=True)
        except (FileNotFoundError, subprocess.CalledProcessError):
            pytest.skip("wmctrl not available - skipping Brave window detection test")

        # Check if brave-browser command is available
        try:
            subprocess.run(
                ["brave-browser", "--version"], capture_output=True, check=True
            )
        except (FileNotFoundError, subprocess.CalledProcessError):
            pytest.skip(
                "brave-browser not available - skipping Brave window detection test"
            )

        browser_controller = BraveBrowserController()

        try:
            # Launch Brave browser
            browser_controller.open_browser()

            # Give browser extra time to fully start and register with window manager
            import time

            time.sleep(1)

            # Use wmctrl to find the Brave window
            result = subprocess.run(
                ["wmctrl", "-l"], capture_output=True, text=True, check=True
            )

            # Look for Brave in the window list
            brave_found = False

            for line in result.stdout.strip().split("\n"):
                if "Brave" in line:
                    brave_found = True
                    break

            assert brave_found, (
                f"Brave window not found in wmctrl output:\n{result.stdout}"
            )

            # Verify we can also get geometry information for the Brave window
            result_geometry = subprocess.run(
                ["wmctrl", "-lG"], capture_output=True, text=True, check=True
            )

            brave_geometry_found = False
            for line in result_geometry.stdout.strip().split("\n"):
                if "Brave" in line:
                    parts = line.split(None, 7)
                    assert len(parts) >= 6, (
                        f"Brave window line doesn't have geometry: {line}"
                    )

                    # Verify geometry values are valid integers
                    x, y, width, height = map(int, parts[2:6])
                    assert width > 0 and height > 0, (
                        f"Invalid Brave window dimensions: {width}x{height}"
                    )
                    brave_geometry_found = True
                    break

            assert brave_geometry_found, (
                f"Brave window geometry not found in wmctrl -lG output:\n{result_geometry.stdout}"
            )

        finally:
            # Always clean up the browser
            try:
                browser_controller.close_browser()
                # Give time for browser to close
                import time

                time.sleep(2)
            except Exception as e:
                print(f"Warning: Error closing browser: {e}")
