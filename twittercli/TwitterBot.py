from time import sleep
from twittercli import login
from selenium.common.exceptions import NoSuchElementException

class TwitterBot:

    def __init__(self):
        self.tweetDB = list()
        self.tCores = list()
        self.authInfo = login.manualAuth()
     
    def initCore(self, headless=False):
        self.tCores.append(login.driverInit(headless))
        self.loginTwitter(self.tCores[-1])
        
    def loginTwitter(self, core):
        core.get('https://www.twitter.com')
        core.find_element_by_link_text('Log in').click()
        sleep(1)
        loginSpan = 'Log in to Twitter'
        firstSpan = core.find_elements_by_tag_name('span')[0].text
        while loginSpan in firstSpan:
            # Determine valid login methods.
            loginMethods = login.getLoginMethods(core)
            if not loginMethods: break
            # Authenticate if valid login method given.
            if 'username' in loginMethods:
                login.authUser(self.authInfo['username'],
                               self.authInfo['password'], core)
            elif 'email' in loginMethods:
                login.authUser(self.authInfo['email'],
                               self.authInfo['password'], core)
            else:
                print('Alternate login required by twitter.')
                altLogin = input('Please enter your %s or %s: ' \
                        % tuple(loginMethods))
                login.authUser(altLogin, 
                               self.authInfo['password'], core)
            firstSpan = core.find_elements_by_tag_name('span')[0].text
            #if len(firstSpan) == 0: 
            #    break
            #else:
            #    firstSpan = firstSpan[0].text
            sleep(1)
        
    def sendTweet(self, tweet=None, coreNum = -1):
        """Send out a new tweet."""
        core = self.tCores[coreNum]
        if not tweet:
            tweet = input('Tweet: ')
        dataContainer = None
        # writing the tweet
        while not dataContainer:
            try:
                dataContainer = core.find_element_by_class_name('DraftEditor-editorContainer')
            except NoSuchElementException:
                dataContainer = None
                sleep(1)
        inputLine = dataContainer.find_element_by_tag_name('div')
        inputLine.send_keys(tweet)
        # sending the tweet
        divList = core.find_elements_by_tag_name('div')
        for div in divList:
            if div.get_attribute('data-testid') == 'tweetButtonInline':
                tweetButton = div
                break
        tweetButton.click()


    def scrapeTweets(self, numSteps=1, coreNum = -1):
        """Scrape tweets for given number of full scrolls."""
        core = self.tCores[coreNum]
        JScroll = 'window.scrollTo(0,document.body.scrollHeight);'
        for step in range(numSteps):
            self.tweetDB += [article.text for article in core.find_elements_by_tag_name('article')]
            core.execute_script(JScroll)
            sleep(3)
            
    def termCore(self, coreNum = -1):
        if len(self.tCores) > 0:
            core = self.tCores.pop(coreNum)
            core.quit()
            del core
        else:
            print('No cores are active.')
