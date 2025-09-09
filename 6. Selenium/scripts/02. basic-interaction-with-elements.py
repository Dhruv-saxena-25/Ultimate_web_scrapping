import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc

# driver = webdriver.Chrome()
# driver.maximize_window()

# This code does not detect captchas

options = uc.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-blink-features=AutomationControlled")
driver = uc.Chrome(options=options,use_subprocess=True)
driver.maximize_window()

# Accessing the Google homepage
url = "https://www.google.com"
driver.get(url)
time.sleep(1)


# Locating the search bar using XPath
search_bar_xpath = '//*[@id="APjFqb"]'
search_bar = driver.find_element(by=By.XPATH, value=search_bar_xpath)

# Clear Fields
search_bar.clear()

# Enter Query
search_bar.send_keys("Machine Learning")
time.sleep(2)

# # Clear Fields
# search_bar.clear()
# time.sleep(1)

# Simulating Enter Key 
search_bar.send_keys(Keys.ENTER)
time.sleep(2)

# Clicking Link
link_xpath = '//*[@id="rso"]/div[2]/div/div/div/div[1]/div/div/span/a/h3'
link = driver.find_element(by=By.XPATH, value=link_xpath)
link.click()
time.sleep(2)

# Close the browser
driver.quit()