from sys import argv
from . import auth,driver

if len(argv) == 2:
    tweetBody = argv[1]
else:
    tweetBody = input('Tweet body: ')

twit = driver.driverInit(*auth.authModule(), headLess=True)
driver.sendTweet(twit, tweetBody)
twit.quit()

