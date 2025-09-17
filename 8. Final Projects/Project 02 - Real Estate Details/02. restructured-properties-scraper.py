from concurrent.futures import wait
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


class PropertyScraper:
    def __init__(self, url, timeout=5):
        self.url = url
        self.data = []
        self.driver = self._initialize_driver()
        self.wait = WebDriverWait(self.driver, timeout)
        
    def _initialize_driver(self):
        # This code does not detect captchas
        options = uc.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--incognito")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--enable-features=NetworkServiceInProcess")
        options.add_argument("--disable-features=NetworkService")

        driver = uc.Chrome(options=options, use_subprocess=True)
        driver.maximize_window()

        return driver
        

    def _wait_for_page_to_load(self):
        title = self.driver.title
        try:
            self.wait.until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
        except:
            print(f"The webpage \"{title}\" did not get fully loaded.\n")
        else:
            print(f"The webpage \"{title}\" did get fully loaded.\n")

    def access_website(self):
        self.driver.get(self.url)
        self._wait_for_page_to_load()
    
    def search_properties(self, text):
        # locating and entering text in search bar
        try:
            search_bar = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="keyword2"]')))

        except:
            print("Timeout Exception: The search bar is not found.\n")
            
        else:
            search_bar.clear()
            search_bar.send_keys("Chennai")
            
        # selecting valid option from list
        try:
            vaild_option = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="0"]')))

        except:
            print("Timeout Exception: The valid option is not found.\n")

        else:
            vaild_option.click()
            
        # click on Search button
        try:
            search_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="searchform_search_btn"]')))

        except:
            print("Timeout Exception: The Search button is not found.\n")
            
        else:
            search_button.click()
            self._wait_for_page_to_load()
    
    def adjust_budget_slider(self, offset: int):
        try:
            slider = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="budgetLeftFilter_max_node"]')))

        except:
            print("Timeout Exception: The Budget Slider is not found.\n")

        else:
            actions = ActionChains(self.driver)
            (
                actions
                .click_and_hold(slider) # Click and hold the slider
                .move_by_offset(offset, 0) # Adjust this value as needed
                .release()              # Release the slider
                .perform()
            ) 
            time.sleep(1)
    
    def apply_filters(self):
        time.sleep(0.5)
        # 1. Verified
        verified = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div/div[4]/div[3]/div[1]/div[3]/section/div/div/div/div/div[1]/div/div[3]'))
                            )
        verified.click()
        time.sleep(1)

        # 2. Ready To Move
        ready_to_move = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div/div[4]/div[3]/div[1]/div[3]/section/div/div/div/div/div[1]/div/div[5]'))
                                )
        ready_to_move.click()  
        time.sleep(1)


        # moving to the right side to unhide remaining filters
        while True:
            try:
                filter_right_button = self.wait.until(EC.presence_of_element_located((
                    By.XPATH, "//i[@class='iconS_Common_24 icon_upArrow cc__rightArrow']"
                )))
            except:
                print("Timeout Exception: The right arrow button is not found.\n")
                break
            else:
                filter_right_button.click()
                

        # 3. With Photos
        with_photos = self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html[1]/body[1]/div[1]/div[1]/div[1]/div[4]/div[3]/div[1]/div[3]/section[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[6]/span[2]')))
        with_photos.click() 
        time.sleep(1)

        # 4. With Videos
        with_videos = self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html[1]/body[1]/div[1]/div[1]/div[1]/div[4]/div[3]/div[1]/div[3]/section[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[7]/span[2]')))
        with_videos.click()
        time.sleep(1)
    
    def _extract_data(self, row, by, value):
        try:
            return row.find_element(by, value).text
        except:
            return np.nan
    
    def scrape_webpage(self):
        # Scrape the data
        rows = self.driver.find_elements(By.CLASS_NAME, "tupleNew__contentWrap")
        for row in rows:
            property = {
                "name": self._extract_data(row, By.CLASS_NAME, "tupleNew__headingNrera"),
                "location": self._extract_data(row,By.CSS_SELECTOR, ".tupleNew__tupleHeadingTopaz, .tupleNew__tupleHeading, .tupleNew__tupleHeadingPlat"),
                "price": self._extract_data(row, By.CLASS_NAME, "tupleNew__priceValWrap"),
            }
            # property area and bhk
            try:
                elements = row.find_elements(By.CLASS_NAME, "tupleNew__area1Type")
            except:
                property["area"], property["bhk"] = [np.nan, np.nan]
                print("Area and BHK not found")
            else:
                property["area"], property["bhk"] = [ele.text for ele in elements]
            
            self.data.append(property)
    
    def navigate_pages_and_scrape_data(self):
        page_count = 0
        while True:
            page_count += 1
            try:
                time.sleep(1)
                self.scrape_webpage()
                next_page_button = self.driver.find_element(By.XPATH, "//a[normalize-space()='Next Page >']")
            except:
                print(f"Timeout because we have navigated all the {page_count} pages.\n")
                break
            else:
                try:
                    self.driver.execute_script("window.scrollBy(0, arguments[0].getBoundingClientRect().top - 100);", next_page_button)
                    time.sleep(1)
                    
                    self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Next Page >']"))
                    ).click()
                    time.sleep(5)
                except:
                    print("Timeout while clicking on \"Next Page\".\n")
    
    def clean_data_and_save_as_excel(self, file_name):
        df_properties = (
        pd
        .DataFrame(self.data)
        .drop_duplicates()
        .apply(lambda col: col.str.strip().str.lower() if col.dtype == "object" else col)
        .assign(
            starred = lambda df_: df_['name'].str.extract(r'\n([\d.]+)')[0].fillna(0).astype(float),
            name = lambda df_: (
                df_['name']
                .str.replace("\n[0-9.]+", "", regex=True)
                .str.strip()
                .replace("adroit district s", "adroit district's")
            ),
            location = lambda df_: (
                df_['location']
                .str.replace("chennai", "")
                .str.strip()
                .str.replace(",$", "", regex=True)
                .str.split("in")
                .str[-1]
                .str.strip()
            ),
            price = lambda df_: (
                df_['price']
                .loc[df_['price'].str.strip().str.lower() != 'price on request']
                .str.replace("₹", "")
                .str.strip()
                .apply(lambda val: float(val.replace("lac", "").strip()) if "lac" in val else float(val.replace("cr", "").strip()) * 100)
            ),
            area = lambda df_: (
                df_['area']
                .str.replace("sqft", "", regex=True)
                .str.strip()
                .str.replace(",", "")
                .pipe(lambda ser: pd.to_numeric(ser))
            ),
            bhk=lambda df_: (
                df_['bhk']
                .str.replace("bhk", "")
                .str.strip()
                .pipe(lambda ser: pd.to_numeric(ser))
            )
        )
        .rename(columns={
            "price": "price (in lacs)",
            "area": "area (in sqft)"
        })
        .reset_index(drop=True)
        .to_csv(f"{file_name}.csv", index=False)
        )

    def run(self, text="Chennai", offset=-100, file_name="properties"):
        try:
            self.access_website()
            self.search_properties(text)
            self.adjust_budget_slider(offset)
            self.apply_filters()
            self.navigate_pages_and_scrape_data()
            self.clean_data_and_save_as_excel(file_name)
        finally:
            time.sleep(2)
            self.driver.quit()
    
    
if __name__ == "__main__":
	scraper = PropertyScraper(url="https://www.99acres.com/")
	scraper.run(
		text="chennai",
		offset=-73,
		file_name="chennai-properties"
	)
    