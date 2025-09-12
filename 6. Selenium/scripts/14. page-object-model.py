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



url = "https://github.com/login"
driver.get(url)  # Navigate to the URL  
time.sleep(1)  # Wait for the page to load


class LoginPage:
    
    def __init__(self, driver):
        self.driver = driver
        self.username = (By.ID, "login_field")
        self.password = (By.ID, "password")
        self.login_button = (By.NAME, "commit") 
        
    def login(self, username, password):
        self.driver.find_element(*self.username).send_keys(username)
        self.driver.find_element(*self.password).send_keys(password)
        time.sleep(1)
        self.driver.find_element(*self.login_button).click()
    
login_page = LoginPage(driver)
login_page.login("Dhruv123", "Pass123")

time.sleep(2)  # Wait for a few seconds to observe the result

driver.quit()  # Close the browser and end the session  
