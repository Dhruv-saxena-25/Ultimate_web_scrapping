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



url = "https://www.w3schools.com/js/tryit.asp?filename=tryjs_prompt"
driver.get(url)  # Navigate to the URL  
time.sleep(1)  # Wait for the page to load

iframe_element = driver.find_element(by= By.ID, value='iframeResult')
driver.switch_to.frame(iframe_element)  # Switch to the iframe containing the alert button


button = driver.find_element(by= By.XPATH, value= '/html/body/button')
button.click()  # Click the button to trigger the alert

print(f"Alert Text: {driver.switch_to.alert.text}")

driver.switch_to.alert.send_keys("Dhruv Saxena")  # Send text to the prompt alert
driver.switch_to.alert.accept()  # Accept the alert
print(f"\nYou entered: Dhruv Saxena")
time.sleep(1)  # Wait for a few seconds to observe the result

# driver.switch_to.alert.dismiss()  # Dismiss the alert if needed

driver.switch_to.default_content()  # Switch back to the main content


driver.quit()  # Close the browser and end the session
