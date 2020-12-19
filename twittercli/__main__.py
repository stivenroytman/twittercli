from sys import argv
from twittercli.TwitterBot import TwitterBot

numArgs = len(argv)

if numArgs == 1:
    print(
"""
Usage: 
  twittercli <command> [options]

Commands:
  send [tweetBody]
  scrape [numSteps]
""")

elif numArgs == 2:
    tBot = TwitterBot()
    tBot.initCore(headless=True)
    command = argv[1]
    if command == 'send':
        tBot.sendTweet()
    elif command == 'scrape':
        tBot.scrapeTweets()
        for tweet in tBot.tweetDB:
            print(tweet)
    tBot.termCore()

elif numArgs == 3:
    tBot = TwitterBot()
    tBot.initCore(headless=True)
    command = argv[1]
    arg = argv[2]
    if command == 'send':
        tBot.sendTweet(arg)
    elif command == 'scrape':
        tBot.scrapeTweets(arg)
        for tweet in tBot.tweetDB:
            print(tweet)
    tBot.termCore()
