# Project Conventions

This is a web scraping automation project that uses browser automation to collect real estate rental listings from property sales websites for Sydney postcodes. The project uses pyautogui for GUI automation and saves HTML pages for later processing.

## Code Organization

- `src/` - Main source code directory
  - `main.py` - Entry point that orchestrates the scraping process
  - `scrape.py` - Core scraping functionality with browser automation
- `data/` - Input data files containing postcodes and data sources
- `html_pages/` - Output directory for scraped HTML files
- Project uses flat module structure with clear separation of concerns

## Coding Style and Best Practices

### General Guidelines

- Write clear, readable Python code following PEP 8 conventions
- Use descriptive function and variable names that explain intent. Code should aim to be self documenting.
- Use comments sparsely to describe intent of the code and to capture intricacies of the code
- Keep functions focused on single responsibilities - each function should do one thing well
- Prefer explicit over implicit - make code behavior obvious
- Fail fast with clear error messages rather than defensive programming
- Use type hints where they add clarity
- Log important operations and errors for debugging
- Make functions pure and testable where possible by avoiding global state

### Browser Automation

- Use the Brave browser
- Use consistent wait patterns with randomization to appear human-like
- Always clean up browser resources in finally blocks
- Log all major browser operations for debugging
- Use absolute file paths for saving to avoid path issues

### Testing Conventions

- Unit tests should be limited in scope and should test a single invariant or behavior.
- Any repeated setup code should be put into a helper function.
- Name tests in the form: test_<subject>_<action>_<expected_outcome>. E.g. test_random_wait_sleeps_expected_duration, test_check_stop_returns_true_when_file_missing

## Testing

- Use pytest as the testing framework
- Place tests in a `tests/` directory mirroring the `src/` structure
- Mock external dependencies like file system operations and browser automation
- Test edge cases and error conditions

## Configuration

- Store configuration data in text files in the `data/` directory
- Use simple formats like line-separated values for postcode lists
- Keep hardcoded paths and settings as constants at module level
- Use environment variables for sensitive configuration

## Development Workflow

Your role as the AI assistant is to help me (the human) with developing this web scraping project. Focus on making the code more maintainable, testable, and robust while preserving the core browser automation functionality.

