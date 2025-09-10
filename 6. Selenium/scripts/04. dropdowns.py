import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import undetected_chromedriver as uc


# This code does not detect captchas
options = uc.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-blink-features=AutomationControlled")
driver = uc.Chrome(options=options,use_subprocess=True)
driver.maximize_window()


url= 'https://www.miniclip.com/careers/vacancies'
driver.get(url)
time.sleep(2)


# identify the element
department_field = driver.find_element(by= By.XPATH, value='//*[@id="__layout"]/div/div/section[2]/div/fieldset[3]/select')

# convert to dropdown element
department_dropdown = Select(department_field)

department_dropdown.select_by_index(5)

time.sleep(2)   

# select option by display value

department_dropdown.select_by_value("Art")
time.sleep(1)

# Exit the browser
driver.quit()   
