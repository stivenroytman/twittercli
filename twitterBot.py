from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox import options
from os import system
from time import sleep
from pdb import set_trace

# Retrieving secret
def retrieveSecret():
    system('gpg --decrypt secret.txt.gpg > secret &')
    with open('secret', 'r') as secretFile:
        secret = [secretData.strip() for secretData in secretFile.readlines()]
    return secret

# Logging in
def driverInit(userLogin, userPass, headLess=False):
    if headLess:
        opts = options.Options()
        opts.headless = True
        driver = webdriver.Firefox(options=opts)
    else: 
        driver = webdriver.Firefox()
    driver.get('https://www.twitter.com')
    driver.find_element_by_link_text('Log in').click()
    driver.find_element_by_name('session[username_or_email]')\
            .send_keys(userLogin)
    driver.find_element_by_name('session[password]')\
            .send_keys(userPass)
    driver.find_element_by_name('session[password]')\
            .submit()
    sleep(5)
    return driver

def sendTweet(driver, tweet):
    # typing the tweet
    dataContainer = driver.find_element_by_class_name('DraftEditor-editorContainer')
    inputLine = dataContainer.find_element_by_tag_name('div')
    inputLine.send_keys(tweet)
    # sending the tweet
    divList = driver.find_elements_by_tag_name('div')
    for div in divList:
        if div.get_attribute('data-testid') == 'tweetButtonInline':
            tweetButton = div
            break
    tweetButton.click()

    
  
    
    
    