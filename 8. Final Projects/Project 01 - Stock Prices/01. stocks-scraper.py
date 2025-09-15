import time
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc

# ----- SCRAPING THE DATA -----

"""
This script (currently commented out) shows how to launch a Chrome browser
using Selenium's standard webdriver. It sets Chrome options to:

- Ignore SSL and certificate errors
- Allow running insecure (HTTP) content
- Disable web security (same-origin protections)
- Disable extensions

These settings are useful when testing sites with invalid certificates or
mixed content, but they reduce browser security and should be used cautiously.
"""

# chrome_options = Options()
# chrome_options.add_argument('--ignore-ssl-errors')
# chrome_options.add_argument('--ignore-certificate-errors')
# chrome_options.add_argument('--ignore-certificate-errors-spki-list')
# chrome_options.add_argument('--allow-running-insecure-content')
# chrome_options.add_argument('--disable-web-security')
# chrome_options.add_argument('--disable-extensions')
# driver = webdriver.Chrome(options=chrome_options)
# driver.maximize_window()


"""
This script launches a Chrome browser using undetected_chromedriver (uc),
which is a modified version of ChromeDriver designed to bypass bot-detection
mechanisms on websites. It configures Chrome with options to:

- Disable the sandbox (improves compatibility in restricted environments)
- Disable the 'AutomationControlled' blink feature (helps hide automation)

The browser is started as a subprocess for better stability, and the window
is maximized to simulate a real user environment.
""" 
options = uc.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-blink-features=AutomationControlled")
driver = uc.Chrome(options=options,use_subprocess=True)
driver.maximize_window()

# explicit wait
wait = WebDriverWait(driver, 10)

# function to check if webpage is fully loaded
def wait_for_page_to_load(driver, wait):
	page_title = driver.title
	try:
		wait.until(
			lambda d: d.execute_script("return document.readyState") == "complete"
		)
  
	except:
		print(f"The page \"{page_title}\" did not get fully loaded within the given duration.\n")
  
	else:
		print(f"The page \"{page_title}\" is fully loaded.\n")

    
	    
# open the webpage
url = "https://finance.yahoo.com/"
driver.get(url)

wait_for_page_to_load(driver, wait) # wait for the page to load

# hovering on Markets menu

actions = ActionChains(driver)
markets_menu = wait.until(
    EC.presence_of_element_located((
        By.XPATH, '/html[1]/body[1]/div[2]/header[1]/div[1]/div[1]/div[1]/div[4]/div[1]/div[1]/ul[1]/li[3]/a[1]/span[1]'))
    )
actions.move_to_element(markets_menu).perform()

# Click on Trending Tickers
trending_tickers = wait.until(EC.element_to_be_clickable((
    By.XPATH, '/html[1]/body[1]/div[2]/header[1]/div[1]/div[1]/div[1]/div[4]/div[1]/div[1]/ul[1]/li[3]/div[1]/ul[1]/li[4]/a[1]/div[1]'))
)
trending_tickers.click()
wait_for_page_to_load(driver, wait) # wait for the page to load

# click on Most Active
most_active = wait.until(EC.element_to_be_clickable((
     By.XPATH, '/html[1]/body[1]/div[2]/main[1]/section[1]/section[1]/section[1]/section[1]/section[1]/div[1]/nav[1]/ul[1]/li[1]/a[1]/span[1]'))
)

most_active.click()
wait_for_page_to_load(driver, wait) # wait for the page to load 

data = []
# Scrapeing the data
while True:
    # Scrapping
    wait.until(EC.presence_of_element_located(( By.TAG_NAME, 'table')))   ## Checking if the table is present
    rows = driver.find_elements(By.CSS_SELECTOR, 'table tbody tr')  ## Checking if the rows are present
    
    for row in rows:
        values = row.find_elements(By.TAG_NAME, 'td')
        
        stock = {
            "Name": values[1].text,
            "Symbol": values[0].text,
            "Price": values[3].text,
			"Change": values[4].text,
			"Volume": values[6].text,
			"Market_cap": values[8].text,
			"Pe_ratio": values[9].text,
        }
        data.append(stock)
    
    # Click Next button
    try:
        next_button = wait.until(EC.element_to_be_clickable((
            By.XPATH, '//*[@id="main-content-wrapper"]/section[1]/div/div[3]/div[3]/button[3]'))
            )
    except:
        print("The \"next\" button is not clickable. We have navigated through all the pages.")
        break
    
    else:
        next_button.click()
        time.sleep(2) # wait for 2 seconds before scrapping the data
    

driver.quit() # Close the browser when done


# ----- CLEANING THE DATA -----
stock_df = (
    pd
    .DataFrame(data) # creating dataframe
    .apply(lambda col: col.str.strip() if col.dtype == "object" else col) # stripping unwanted spaces
    .assign(
        Price=lambda df_: pd.to_numeric(df_.Price), # converting to numeric
        Change=lambda df_: pd.to_numeric(df_.Change.str.replace('+', '')), # removing '+' sign and converting to numeric
        Volume=lambda df_: pd.to_numeric(df_.Volume.str.replace('M', '')), # converting to millions
        Market_cap=lambda df_: df_.Market_cap.apply(
            lambda val: float(val.replace('B', '')) if 'B' in val else float(val.replace('T', '')) * 1000 # converting to numeric and to billions
        ), 
        Pe_ratio=lambda df_: (
            df_.Pe_ratio  
            .replace("--", np.nan) # replacing '--' with NaN
            .str.replace(",", "")  # removing commas
            .pipe(lambda col: pd.to_numeric(col))  # converting to numeric
        )
    )
    .rename(columns={
        "Price": "Price (in $)", # renaming columns
        "Volume": "Volume (in millions)", # renaming columns
        "Market_cap": "Market Cap (in billions)", # renaming columns
        "Pe_ratio": "P/E Ratio" # renaming columns 
    })
)

# ----- STORING THE DATA -----
stock_df.to_csv("yahoo-stocks-data.csv", index=False)
# Reading the stored data 
df = pd.read_csv("yahoo-stocks-data.csv")
print(df.head())

