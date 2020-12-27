from time import sleep
from twittercli import login
from selenium.common.exceptions import NoSuchElementException
from twittercli import get_data
import logging

# INITIALIZE LOGGER
LOG_FORMAT = "%(name)s %(levelname)s - %(asctime)s - %(message)s"
logging.basicConfig(filename = get_data('log.txt'),
                    level = logging.DEBUG,
                    format = LOG_FORMAT)
logger = logging.getLogger()
logger.info('Logger initialized successfully.')


# MAIN CLASS
class TwitterBot:

    def __init__(self):
        self.tweetDB = list()
        self.tCores = list()
        self.authInfo = login.manualAuth()
        logger.info('TwitterBot created for {}.'\
                    .format(self.authInfo['username']))
     
    def initCore(self, headless=False):
        logger.info('Initializing tCore...')
        self.tCores.append(login.driverInit(headless))
        self.loginTwitter(self.tCores[-1])
        logger.info('Core initialized.')
        logger.info(('numCores = %d') % (len(self.tCores)))
        
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
                logger.info('Login Method = username')
                login.authUser(self.authInfo['username'],
                               self.authInfo['password'], core)
            elif 'email' in loginMethods:
                logger.info('Login Method = email')
                login.authUser(self.authInfo['email'],
                               self.authInfo['password'], core)
            else:
                logger.warning('Neither default login method accepted.')
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


    def scrapeTweets(self, numSteps=1, stepFactor = 0.5, coreNum = -1):
        """Scrape tweets for given number of full scrolls."""
        logger.info('Scraping tweets over %d steps.' % (numSteps))
        logger.info('stepFactor = %f' % (stepFactor))
        initialSize = len(self.tweetDB)
        core = self.tCores[coreNum]
        JScroll = 'window.scrollTo(0,document.body.scrollHeight);'
        for step in range(numSteps):
            priorSize = len(self.tweetDB)
            self.tweetDB += [article.text for article in core.find_elements_by_tag_name('article')]
            netScraped = len(self.tweetDB) - priorSize
            self.tweetDB = list(set(self.tweetDB))
            netUnique = len(self.tweetDB) - priorSize
            netRedundant = netScraped - netUnique
            logger.debug('%d tweets scraped.' % (netScraped))
            logger.debug('redundant = %d' % (netRedundant))
            logger.debug('unique = %d' % (netUnique))
            logger.debug('netTweets = %d' % (len(self.tweetDB)))
            core.execute_script(JScroll)
            sleep(3)
        sizeChange = len(self.tweetDB) - initialSize
        logger.info('Total of %d tweets gathered.' % (sizeChange))
        
            
    def termCore(self, coreNum = -1):
        logger.info('Terminating tCore...')
        if len(self.tCores) > 0:
            core = self.tCores.pop(coreNum)
            core.quit()
            del core
            logger.info('Core terminated.')
            logger.info(('numCores = %d') % (len(self.tCores)))
        else:
            logger.warning('No cores remaining!')
