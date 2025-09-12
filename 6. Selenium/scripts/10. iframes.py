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


# Navigate to the iframe page
url = "https://www.w3schools.com/html/tryit.asp?filename=tryhtml_iframe_target"
driver.get(url)
time.sleep(1)

# Identify iframe element and switch context

iframe_element = driver.find_element(by= By.XPATH, value= '//*[@id="iframeResult"]')
driver.switch_to.frame(iframe_element)  


link = driver.find_element(by = By.XPATH, value= '/html/body/p[1]/a')
link.click()
time.sleep(1)

# switch back to default context
driver.switch_to.default_content()  

# Exit the web-browser
driver.quit()
