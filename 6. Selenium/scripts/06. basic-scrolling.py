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


url = "https://en.wikipedia.org/wiki/Machine_learning"
driver.get(url)
time.sleep(2)



# scrolling to elements
ai_xpath = '//*[@id="Artificial_intelligence"]' 

# ai_subtopic = driver.find_element(by=By.XPATH, value= ai_xpath)
# driver.execute_script("arguments[0].scrollIntoView();", ai_subtopic)



# scrolling vertically down
driver.execute_script('window.scrollBy(0, 2000);')
time.sleep(4)

# scrolling vertically up
driver.execute_script('window.scrollBy(0, -500);')

# scrolling by page height
driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
time.sleep(3)
driver.execute_script("window.scrollTo(0, -document.body.scrollHeight);")

# Exit the browser
driver.quit()   