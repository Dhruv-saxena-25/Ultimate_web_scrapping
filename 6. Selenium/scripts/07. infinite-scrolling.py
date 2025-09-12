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


url = "https://www.google.com/search?q=arsenal&sca_esv=2c67fa53e20e5059&rlz=1C1CHBF_enAE882AE882&udm=2&biw=1280&bih=593&sxsrf=ADLYWIIKYvudBtBTWpu19du4uTiajPUkng%3A1733969038357&ei=jkRaZ9G8FYDG4-EPkf6F4AY&ved=0ahUKEwjRu9SEkqGKAxUA4zgGHRF_AWwQ4dUDCBE&uact=5&oq=arsenal&gs_lp=EgNpbWciB2Fyc2VuYWwyBBAjGCcyBBAjGCcyBhAAGAcYHjIGEAAYBxgeMgYQABgHGB4yBhAAGAcYHjIKEAAYgAQYQxiKBTILEAAYgAQYsQMYgwEyCxAAGIAEGLEDGIMBMgoQABiABBhDGIoFSLUoUABYAHADeACQAQCYAQCgAQCqAQC4AQPIAQCYAgOgAi-YAwCIBgGSBwEzoAcA&sclient=img"
driver.get(url)
time.sleep(1)


# Calculate H1

prev_height = driver.execute_script("return document.body.scrollHeight")

while True: 
    
    print(f"Webpage height: {prev_height:,} pixels")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)   
    
    # Calculate H2 
    new_height = driver.execute_script("return document.body.scrollHeight") 
    
    if prev_height == new_height:
        break   
    
    prev_height = new_height    
    
