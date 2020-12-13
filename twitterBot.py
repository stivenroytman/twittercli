from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox import options
from os import system
from time import sleep

tweetBody = input('Enter tweet: ')

# Retrieving secret
system('gpg --decrypt params.py.gpg > secret &')
with open('secret', 'r') as secretFile:
    exec(secretFile.read())

# Logging in
driver = webdriver.Firefox()
driver.get('https://www.twitter.com')
driver.find_element_by_link_text('Log in').click()
driver.find_element_by_name('session[username_or_email]')\
        .send_keys(userLogin); del userLogin
driver.find_element_by_name('session[password]')\
        .send_keys(userPass); del userPass
driver.find_element_by_name('session[password]')\
        .submit()
sleep(5)

# Typing tweet
dataContainer = driver.find_element_by_class_name('DraftEditor-editorContainer')
inputLine = dataContainer.find_element_by_tag_name('div')
inputLine.send_keys(tweetBody)

# Sending tweet
divList = driver.find_elements_by_tag_name('div')
for div in divList:
    if div.get_attribute('data-testid') == 'tweetButtonInline':
        tweetButton = div
        break
        
tweetButton.click()
