# Web scaping
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from bs4 import BeautifulSoup

import datetime


def parse(url):
    #CHROME_PATH = '/usr/bin/google-chrome'
    CHROMEDRIVER_PATH = 'C:/Users/Maroz/Documents/chromedriver_win32/chromedriver.exe'
    WINDOW_SIZE = "1920,1080"

    chrome_options = Options()  
    chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    #chrome_options.binary_location = CHROME_PATH

    
    driver = webdriver.Chrome(CHROMEDRIVER_PATH, options=chrome_options)
    print(url)
    driver.get(url)
    try:
        WebDriverWait(driver, 45).until(EC.presence_of_element_located((By.CSS_SELECTOR,"span.ng-binding")))
    except:
        print("Exception")

    finally:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        return soup
        

if __name__ == '__main__':
    # main here
