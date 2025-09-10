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


url = 'https://demoqa.com/select-menu'
driver.get(url)
time.sleep(1)


cars_element = driver.find_element(by= By.XPATH, value='//*[@id="cars"]')
cars_ms = Select(cars_element)  

cars_ms.select_by_index(1)  # select by index

cars_ms.select_by_visible_text("Opel")

cars_ms.select_by_visible_text("Audi")
time.sleep(2)

# deselecting options
cars_ms.deselect_by_index(1)
time.sleep(1)   

cars_ms.deselect_all()
time.sleep(3)

# Exit the browser
driver.quit()

