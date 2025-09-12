import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC    

# This code does not detect captchas
options = uc.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-blink-features=AutomationControlled")
driver = uc.Chrome(options=options,use_subprocess=True)
driver.maximize_window()


url = "https://www.google.com/"
driver.get(url)
time.sleep(2)


search_bar = driver.find_element(by= By.XPATH, value='//*[@id="APjFqb"]')
search_bar.send_keys("Machine Learning")


# Implementing Explicit Wait

wait = WebDriverWait(driver= driver, timeout= 5)
wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[4]/form/div[1]/div[1]/div[3]/center/input[1]')))


search_bar.send_keys(Keys.ENTER)

time.sleep(2)   


# Exit the Browser
driver.quit()


