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
        pass
    
    def adjust_budget_slider(self, offset):
        pass
    
    def apply_filters(self):
        pass
    
    def _extract_data(self, row, by, value):
        pass
    
    
    def scrape_webpage(self):
        pass
    
    def navigate_pages_and_scrape_data(self):
        pass
    
    def clean_data_and_save_as_excel(self, file_name):
        pass
    
    def run(self, text="Chennai", offset=-100, file_name="properties"):
        pass
    
    
if __name__ == "__main__":
	scraper = PropertyScraper(url="https://www.99acres.com/")
	scraper.run(
		text="chennai",
		offset=-73,
		file_name="chennai-properties"
	)
 

    