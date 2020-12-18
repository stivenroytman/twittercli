from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox import options
from os import system
from time import sleep

def driverInit(headLess=False):
    """Create the webdriver object."""
    if headLess:
        opts = options.Options()
        opts.headless = True
        driver = webdriver.Firefox(options=opts)
    else: 
        driver = webdriver.Firefox()
    return driver

def getLoginMethods(driver):    
    spanList = driver.find_elements_by_tag_name('span')
    if '.' in [span.text for span in spanList][1]:
        loginMethods = [span.text for span in spanList][2]\
            .lower().split(' or ')
    else:
        loginMethods = [span.text for span in spanList][1]\
            .lower().split(' or ')
    return loginMethods

def parseLoginType(userLogin):
    if '@' in userLogin:
        loginGiven = 'email'
    else: 
        loginGiven = 'username'
    return loginGiven

def authUser(userLogin, userPass, driver):
    driver.find_element_by_name('session[username_or_email]')\
            .send_keys(userLogin)
    driver.find_element_by_name('session[password]')\
            .send_keys(userPass)
    driver.find_element_by_name('session[password]')\
            .submit()
    return driver

def loginTwitter(userLogin, userPass, driver):
    # TODO - debug
    """Authenticate the user."""
    # Go to twitter login page.
    driver.get('https://www.twitter.com')
    driver.find_element_by_link_text('Log in').click()
    # Check given login type.
    loginGiven = parseLoginType(userLogin)
    # Determine valid login methods.
    loginMethods = getLoginMethods(driver)
    # Authenticate if valid login method given.
    if loginGiven in loginMethods:
        authUser(userLogin, userPass, driver)
        return driver
    else:
        print('Alternate login required by twitter.')
        altLogin = input('Please enter %s or %s' % tuple(loginMethods))
        authUser(altLogin, userPass, driver)
        return driver


def sendTweet(driver, tweet=None):
    if tweet == None: input('Tweet body: ')
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

def scrapeTweets(driver, numSteps):
    """Scrape tweets for given number of full scrolls."""
    JScroll = 'window.scrollTo(0,document.body.scrollHeight);'
    tweetList = list()
    for step in range(numSteps):
        tweetList += [article.text for article in driver.find_elements_by_tag_name('article')]
        driver.execute_script(JScroll)
        sleep(3)
    return tweetList

def parseTweet(tweet):
    """Extract data out of tweet."""
    # tweet : str, output of scrapeTweets

    tweetFrame = {
            'attributes': list(),
            'date': str(),
            'user': str(),
            'tag': str(),
            'text': str()
    }
    
    splitTweet = tweet.split('\n')
    textMaxIndex = [entry.isnumeric() for entry in tweet].index(True) - 1

    if 'Promoted' in splitTweet[-1]:
        tweetFrame['attributes'].append('promoted')

    if 'Retweeted' in splitTweet[0]:
        tweetFrame['attributes'].append('retweet')
        tweetFrame['user'] = (
            splitTweet[0].replace(' Retweeted',''),
            splitTweet[1]
        )
        if '@' in splitTweet[2]:
            tweetFrame['tag'] = splitTweet[2]
        if '·' in splitTweet[3]:
            tweetFrame['date'] = splitTweet[4]
            tweetFrame['text'] = splitTweet[5]

    elif '@' in splitTweet[1] and '·' in splitTweet[2]:
        tweetFrame['attributes'].append('original')
        tweetFrame['user'] = splitTweet[0]
        tweetFrame['tag'] = splitTweet[1]
        tweetFrame['date'] = splitTweet[3]
        tweetFrame['text'] = '\n'.join(splitTweet[4:textMaxIndex])

    else:
        tweetFrame = None

    return tweetFrame

def rawTweetBaker(tweetList):
    for tweet in tweetList:
        yield tweet.split('\n')

def tweetParser(tweetList):
    for tweet in tweetList:
        yield parseTweet(tweet)



