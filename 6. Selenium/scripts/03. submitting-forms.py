import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc


# This code does not detect captchas
options = uc.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-blink-features=AutomationControlled")
driver = uc.Chrome(options=options,use_subprocess=True)
driver.maximize_window()


url = "https://github.com/login"
driver.get(url)
time.sleep(2)


# Username Field
username_field = driver.find_element(By.ID, 'login_field')
username_field.send_keys("Dhruv")
time.sleep(1)

# Password Field    
password_field = driver.find_element(By.ID, 'password') 
password_field.send_keys("Test@1234")
time.sleep(1)

# Submit Button Field
submit_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/main/div/div[2]/form/div[3]/input')
submit_button.click()
time.sleep(2)



# Exit the Browser

driver.quit()