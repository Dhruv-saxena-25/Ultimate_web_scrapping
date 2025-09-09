import time 
from selenium import webdriver

## Initialization of webdriver

webdriver = webdriver.Chrome()

# maximize the browser window
webdriver.maximize_window()

# accessing a webpage using URL
url = "https://www.google.com"
webdriver.get(url)

# printing meta-data of webpage
print(f"Title: {webdriver.title}")
print(f"Current URL: {webdriver.current_url}")
# print(f"Page Source: {webdriver.page_source}")

# capture screenshot of webpage
webdriver.save_screenshot("google_homepage.png")
print("\n Screenshot captured: google_homepage.png")

## Introduce delay of 5s
total_delay = 5
time.sleep(total_delay)

# Close the browser
webdriver.quit()