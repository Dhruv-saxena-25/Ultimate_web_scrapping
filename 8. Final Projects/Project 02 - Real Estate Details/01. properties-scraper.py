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
import undetected_chromedriver as uc

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
  
  
# # options
# chrome_options = Options()
# chrome_options.add_argument("--disable-http2")
# chrome_options.add_argument("--incognito")
# chrome_options.add_argument("--disable-blink-features=AutomationControlled")
# chrome_options.add_argument("--ignore-certificate-errors")
# chrome_options.add_argument("--enable-features=NetworkServiceInProcess")
# chrome_options.add_argument("--disable-features=NetworkService")
# chrome_options.add_argument(
#     "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
# )
# driver = webdriver.Chrome(options=chrome_options)
# driver.maximize_window()


# This code does not detect captchas
options = uc.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--incognito")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--enable-features=NetworkServiceInProcess")
options.add_argument("--disable-features=NetworkService")


driver = uc.Chrome(options=options,use_subprocess=True)
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


# Adjust the Budget Slider
try:
    slider = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="budgetLeftFilter_max_node"]')))

except:
    print("Timeout Exception: The Budget Slider is not found.\n")

else:
    actions = ActionChains(driver)
    (
        actions
        .click_and_hold(slider) # Click and hold the slider
        .move_by_offset(-73, 0) # Adjust this value as needed
        .release()              # Release the slider
        .perform()
    ) 
    time.sleep(1) 
    
# filter results to show genuine listings
# 1. Verified
verified = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div/div[4]/div[3]/div[1]/div[3]/section/div/div/div/div/div[1]/div/div[3]'))
                      )
verified.click()
time.sleep(1)

# 2. Ready To Move
ready_to_move = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div/div[4]/div[3]/div[1]/div[3]/section/div/div/div/div/div[1]/div/div[5]'))
                           )
ready_to_move.click()  
time.sleep(1)


# moving to the right side to unhide remaining filters
while True:
    try:
        filter_right_button = wait.until(EC.presence_of_element_located((
            By.XPATH, "//i[@class='iconS_Common_24 icon_upArrow cc__rightArrow']"
        )))
    except:
        print("Timeout Exception: The right arrow button is not found.\n")
        break
    else:
        filter_right_button.click()
           

# 3. With Photos
with_photos = wait.until(EC.element_to_be_clickable((By.XPATH, '/html[1]/body[1]/div[1]/div[1]/div[1]/div[4]/div[3]/div[1]/div[3]/section[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[6]/span[2]')))
with_photos.click() 
time.sleep(1)

# 4. With Videos
with_videos = wait.until(EC.element_to_be_clickable((By.XPATH, '/html[1]/body[1]/div[1]/div[1]/div[1]/div[4]/div[3]/div[1]/div[3]/section[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[7]/span[2]')))
with_videos.click()
time.sleep(1)


# navigate pages and extract data
data = []
page_count = 0
while True:
	page_count += 1
	try:
		time.sleep(2)
		next_page_button = driver.find_element(By.XPATH, "//a[normalize-space()='Next Page >']")
	except:
		print(f"Timeout because we have navigated all the {page_count} pages.\n")
		break
	else:
		try:
			driver.execute_script("window.scrollBy(0, arguments[0].getBoundingClientRect().top - 100);", next_page_button)
			time.sleep(2)
	
			# Scrape the data
			rows = driver.find_elements(By.CLASS_NAME, "tupleNew__contentWrap")
			for row in rows:
				# Property Name
				try:
					name = row.find_element(By.CLASS_NAME, "tupleNew__headingNrera").text
				except:
					name = 	np.nan
					print("Name not found")

				# Property location
				try:
					location = row.find_element(By.CLASS_NAME, "tupleNew__tupleHeadingTopaz").text
				except:
					location = np.nan
					print("Location not found")
				
				# Property price
				try:
					price = row.find_element(By.CLASS_NAME, "tupleNew__priceValWrap").text
				except:
					price = np.nan
					print("Price not found")

				# property area and bhk
				try:
					elements = row.find_elements(By.CLASS_NAME, "tupleNew__area1Type")
				except:
					area, bhk =[np.nan, np.nan]
					print("Area and BHK not found")
				else:
					area, bhk = [ele.text for ele in elements]
			
   			# store data in dictionary			
			property = {
					"name": name,
					"location": location,
					"price": price,
					"area": area,
					"bhk": bhk	
				}
   
			print(property)

			# append dictionary to data list
			data.append(property)	
	
			# click on Next Page button
			wait.until(
				EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Next Page >']"))
			).click()
			time.sleep(5)
		except:
			print("Timeout while clicking on \"Next Page\".\n")
    
        


time.sleep(1)   
driver.quit()

