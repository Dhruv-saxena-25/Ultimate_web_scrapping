import time
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ----- SCRAPING THE DATA -----
def wait_for_page_to_load(driver, wait):
	title = driver.title
	try:
		wait.until(
			lambda d: d.execute_script("return document.readyState") == "complete"
		)
	except:
		print(f"The webpage \"{title}\" did not get fully laoded.\n")
	else:
		print(f"The webpage \"{title}\" did get fully laoded.\n")
  
  
# options
chrome_options = Options()
chrome_options.add_argument("--disable-http2")
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--enable-features=NetworkServiceInProcess")
chrome_options.add_argument("--disable-features=NetworkService")
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
)

driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

# explicit wait
wait = WebDriverWait(driver, 5)

# accessing the target webpage
url = "https://www.99acres.com/"
driver.get(url)
wait_for_page_to_load(driver, wait)

# identify and enter text into search bar
try:
    search_bar = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="keyword2"]')))

except:
    print("Timeout Exception: The search bar is not found.\n")
    
else:
    search_bar.clear()
    search_bar.send_keys("Chennai")
    
# selecting valid option from list
try:
    vaild_option =wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="0"]')))

except:
    print("Timeout Exception: The valid option is not found.\n")

else:
    vaild_option.click()
    
# click on Search button
try:
    search_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="searchform_search_btn"]')))

except:
    print("Timeout Exception: The Search button is not found.\n")
    
else:
    search_button.click()
    wait_for_page_to_load(driver, wait)

time.sleep(2)   
driver.quit()

