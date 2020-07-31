# Web scaping imports
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

import time
import json


# Logs into facebook
def tryToLoginFB(username, password, pageName):
    # Path to your chromedriver.exe
    CHROMEDRIVER_PATH = 'C:/bin/chromedriver_win32/chromedriver.exe'
    WINDOW_SIZE = "1920,1080"

    chrome_options = Options()  

    # Should open window or not?
    chrome_options.add_argument("--headless")  

    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    # Opens page and fills in form
    browser = webdriver.Chrome(CHROMEDRIVER_PATH, options=chrome_options)
    pageName = '/' + pageName
    browser.get("https://www.facebook.com" + pageName)
    browser.find_element_by_xpath('//input[@id="email"]').send_keys(username)
    browser.find_element_by_xpath('//input[@id="pass"]').send_keys(password)
    browser.find_element_by_xpath('//input[@value="Log In"]').click()


    return browser


def printLoginTest(browser):

    if "logout" in browser.page_source:
        print("Log in Success")
    else:
        print("Log in Failure")


def getPageSoupOnline(browser, xpath=""):

    try:
        if(xpath):
            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
        else:
            time.sleep(2)
    except:
        print("Exception element not located.")

    finally:
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        browser.quit()
        return soup


def writeSoupToFile(pageSoup, pageName):
    with open(pageName + ".html", "w", encoding="utf=8") as file:
        file.write(str(pageSoup))


# Need a json file in directory with Username and Password fields
def getSecretKeys():
    with open('secret.json') as fileHandle:
        return json.load(fileHandle)

# Works as of 31/07/2020
def getPageLikes(pageSoup):
    elementToScrape = "span"
    classNumLikes = "oi732d6d ik7dh3pa d2edcug0 qv66sw1b c1et5uql jq4qci2q a3bd9o3v knj5qynh oo9gr5id"
    indexNumLikes = 1
    
    # Extract number of page likes
    numberOfLikesArr = pageSoup.find_all(elementToScrape, class_= classNumLikes)

    numberOfLikesArr = numberOfLikesArr[indexNumLikes].text.split(" ")[0].split(",")
    
    numberOfLikes = ""
    lenArr = len(numberOfLikesArr)

    for i in range(lenArr):
        numberOfLikes = numberOfLikesArr[lenArr - i - 1] + numberOfLikes

    return numberOfLikes



def getPageSoup(pageToScrape, update, xpath=""):
    elementToScrape = "span"
    classNumLikes = "oi732d6d ik7dh3pa d2edcug0 qv66sw1b c1et5uql jq4qci2q a3bd9o3v knj5qynh oo9gr5id"
    indexNumLikes = 1
    # Get HTML and write to file
    if(update):
        # Get Authentifaction
        secret = getSecretKeys()

        # Login to browser
        browser = tryToLoginFB(secret["Username"], secret["Password"], pageToScrape)
        # Test login
        printLoginTest(browser)

        pageSoup = getPageSoupOnline(browser, xpath)
        writeSoupToFile(pageSoup, pageToScrape)
    else:
        # Get HTML from file
        pageSoup = BeautifulSoup(open(pageToScrape+".html"), "html.parser")
    

    return pageSoup


def getPostLikes(pageToScrape, update):
    pass


if __name__ == '__main__':

    xpathPageLikes = "/html/body/div[1]/div/div/div[1]/div[3]/div/div/div[1]/div/div[4]/div[2]/div/div[1]/div[2]/div[1]/div/div/div/div[2]/div[4]/div/div/div[2]/div/div/span/span"
    pageSoup = getPageSoup("pointsbet", False, xpathPageLikes)

    print(getPageLikes(pageSoup))
    
    xpathPostLikes = "/html/body/div[1]/div/div/div[1]/div[3]/div/div/div[1]/div/div[4]/div[2]/div/div[2]/div/div/div/div[1]/div[2]/div/div/div/div/div/div/div/div/div/div[2]/div/div[4]/div/div/div[1]/div[1]/div/div[1]/div/span/div/span[2]/span/span"
    pageSoup = getPageSoup("pointsbet", False, xpathPostLikes)
    
    

    


