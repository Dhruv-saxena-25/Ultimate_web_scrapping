"""
Selenium Implicit Wait Demo

This script demonstrates the use of implicit wait in Selenium WebDriver.
Implicit wait tells the WebDriver to wait for a certain amount of time when trying
to find an element if it is not immediately present.

Key Features:
- Sets a global implicit wait of 10 seconds
- Uses undetected_chromedriver to avoid bot detection               
- Performs a Google search to demonstrate element interaction
- Shows how implicit wait automatically applies to all element finding operations

Note: Implicit wait is set once and applies to all find_element() calls in the session.
If an element is found before the timeout, the script continues immediately.
"""

# Import necessary libraries
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc

# Set up Chrome driver with undetected chromedriver to avoid bot detection
# This code does not detect captchas
options = uc.ChromeOptions()
options.add_argument("--no-sandbox")  # Disable sandbox mode
options.add_argument("--disable-blink-features=AutomationControlled")  # Disable automation detection
driver = uc.Chrome(options=options, use_subprocess=True)  # Create driver instance
driver.maximize_window()  # Maximize browser window for better visibility

# Set implicit wait - the driver will wait up to 10 seconds for elements to be found
# Implicit wait applies globally to all find_element() calls
# It waits for elements to become available in the DOM before throwing NoSuchElementException
driver.implicitly_wait(10)

# Navigate to Google's homepage
url = "https://www.google.com/"
driver.get(url)
time.sleep(1)  # Brief pause to ensure page loads

# Find the search input field using XPath locator
# The implicit wait will automatically wait up to 10 seconds if the element is not immediately found
search_bar = driver.find_element(by=By.XPATH, value='//*[@id="APjFqb"]')
search_bar.send_keys("Machine Learning")  # Type the search query
time.sleep(1)   # Brief pause for user visibility

# Submit the search by pressing Enter key
search_bar.send_keys(Keys.ENTER)
time.sleep(2)  # Wait for search results to load

# Close the browser and end the WebDriver session
driver.quit()
