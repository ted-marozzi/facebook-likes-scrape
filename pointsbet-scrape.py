# Web scaping imports
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

import time
import json

from matplotlib import pyplot as plt

from datetime import date


# Logs into facebook
def tryToLoginFB(username, password, pageName):
    # Path to your chromedriver.exe
    CHROMEDRIVER_PATH = 'C:/bin/chromedriver_win32/chromedriver.exe'
    WINDOW_SIZE = "1920,1080"

    chrome_options = Options()  

    # Should open window or not?
    chrome_options.add_argument("--headless")  

    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.add_argument("disable-notifications")
    # Opens page and fills in form
    driver = webdriver.Chrome(CHROMEDRIVER_PATH, options=chrome_options)
    pageName = '/' + pageName
    driver.get("https://www.facebook.com" + pageName)
    driver.find_element_by_xpath('//input[@id="email"]').send_keys(username)
    driver.find_element_by_xpath('//input[@id="pass"]').send_keys(password)
    driver.find_element_by_xpath('//input[@value="Log In"]').click()


    return driver


def printLoginTest(driver):

    if "logout" in driver.page_source:
        print("Login succeded")
    else:
        print("Login failed")


def getPageSoupOnline(driver, xpath="", scroll=False, maxScroll=20):

    try:
        if(xpath):
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
        
        if(scroll):
            SCROLL_PAUSE_TIME = 2

            # Get scroll height
            last_height = driver.execute_script("return document.body.scrollHeight")

            for i in range(maxScroll):
                print("Num Scrolls:", i)
                # Scroll down to bottom
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # Wait to load page
                time.sleep(SCROLL_PAUSE_TIME)

                # Calculate new scroll height and compare with last scroll height
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
            
            if( not scroll and not xpath):
                time.sleep(5)
    except:
        print("Exception element not located.")

    finally:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
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
    try:

        numberOfLikesArr = numberOfLikesArr[indexNumLikes].text.split(" ")[0].split(",")
    except IndexError:
        print("Empty Array")

    numberOfLikes = ""
    lenArr = len(numberOfLikesArr)

    for i in range(lenArr):
        numberOfLikes = numberOfLikesArr[lenArr - i - 1] + numberOfLikes

    return numberOfLikes



def getPageSoup(pageToScrape, update=True, xpath="", scroll=False):
  
    # Get HTML and write to file
    if(update):
        # Get Authentifaction
        secret = getSecretKeys()

        # Login to browser
        driver = tryToLoginFB(secret["Username"], secret["Password"], pageToScrape)
        # Test login
        printLoginTest(driver)

        pageSoup = getPageSoupOnline(driver, xpath=xpath, scroll=scroll)
        writeSoupToFile(pageSoup, pageToScrape)
    else:
        # Get HTML from file
        pageSoup = BeautifulSoup(open(pageToScrape+".html", encoding="utf8"), "html.parser")
    

    return pageSoup

# Function by https://gist.github.com/SanthoshBala18
def strToNum(x):
    total_stars = 0
    num_map = {'K':1000, 'M':1000000, 'B':1000000000, 'k':1000}
    if x.isdigit():
        total_stars = int(x)
    else:
        if len(x) > 1:
            total_stars = float(x[:-1]) * num_map.get(x[-1].upper(), 1)
    return int(total_stars)
#

def getPostLikes(pageSoup):
    elementToScrape = "span"
    classNumLikes = "pcp91wgn"
    
    
    # Extract number of page likes
    numLikesList = pageSoup.find_all(elementToScrape, class_= classNumLikes)

    del numLikesList[1::2]

    #Delete every second starting at 2nd element
    for i in range(len(numLikesList)):
       
        numLikesList[i] = strToNum(numLikesList[i].text)
        
        
    return list(reversed(numLikesList))


def plotLikes(pageName, postLikesList):
    # plt.bar(range(len(postLikesList)), postLikesList)
    plt.plot(postLikesList)

    plt.xlabel("Post number")
    plt.ylabel('Number of likes')
    plt.title(pageName + " likes per post over time." )
    plt.savefig(pageName + ".png")


def scrapeLikes(pageName, update=True):

    pageLog = pageName + ".txt"
    today = date.today()
    last_line = ""

    # Create the file if needed
    with open(pageLog, "a") as fileHandle:
        pass

    with open(pageLog, "r") as fileHandle:
        for last_line in fileHandle:
            pass  
    
        

    # Get Soup
    try:
        if(last_line.split(", ")[1].split('\n')[0] == today.strftime("%d/%m/%Y")):
            print("Date already logged")
            update = False
    except IndexError:
        pass

    soup = getPageSoup(pageName, update, scroll=True)

    # Get page and post likes
    pageLikes = getPageLikes(soup)
    postLikesList = getPostLikes(soup)

    print(pageName + " page likes: " + pageLikes)
    print(pageName + " post likes: ", end="")
    print(postLikesList)

    plotLikes(pageName, postLikesList)


    avLikes = sum(postLikesList)/len(postLikesList)
    
    if(update):   
        with open(pageLog, "a") as fileHandle: 

            if(last_line == ""):
                
                fileHandle.write("Page Likes, Date\n")

            fileHandle.write(pageLikes + today.strftime(", %d/%m/%Y\n"))

    return postLikesList
                
            
if __name__ == '__main__':
    postLikesList = scrapeLikes("pointsbet", update=True)
    

    
    

    


