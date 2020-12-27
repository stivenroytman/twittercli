# twittercli


## Purpose

To provide a programmatic and terminal-friendly way of interacting with twitter
without having to go through the hoops of getting their API key. While somebody
out there probably already put something like this together, I don't care, I am
doing this for fun :)

## Compatibility

As of now, this program is only being tested on my personal setup. Will likely work
on any Linux distro, and maybe OSX, but don't take my word for it. Tweaks to make it
more compatible with Windows are coming... at some point.

Also, Firefox is a dependency :')

## Installation

### From source:
```bash
git clone https://github.com/stivenroytman/twittercli
cd twittercli
python -m pip install .
```
OR
```bash
python -m pip install git+https://github.com/stivenroytman/twittercli.git
```

### From latest release wheel:
```bash
python -m pip install https://github.com/stivenroytman/twittercli/releases/download/v.0.0.2/twittercli-0.0.2-py3-none-any.whl
```

## Usage

### Send Tweet

#### CLI
```bash
python -m twittercli send [tweetBody]
```

#### Python
```python
# Send tweet
from twittercli.TwitterBot import TwitterBot

tweetBody = "Beep boop."
tBot = TwitterBot() # initialize class object
tBot.initCore() # initialize selenium core (don't worry about it lol)

tBot.sendTweet(tweetBody) # send it out! 

```

You will be prompted to enter you username, email, and password.
Those are not stored anywhere, so you will be asked every time.
A way to store passwords securely coming soon.
If tweetBody not given, interactive input is triggered.

### Get feed

#### CLI
```bash
python -m twittercli scrape [numSteps]
```

#### Python
```python
from twittercli.TwitterBot import TwitterBot

tBot = TwitterBot() # initialize class object
tBot.initCore() # initialize selenium core

tBot.scrapeTweets(numSteps)
```

numSteps is an optional argument that is roughly proportional 
to the number of tweets that will be scraped off your feed.
Right now it just spits out a load of baloney into stdout.
Much work still needs to be done on the parsing front...

### Search feed

Coming soon...

## In the works...

* Scheduling twittercli jobs.
* Accessing, searching, and storing tweets from your feed.
* Secure twitter password storage via GPG or integration with https://www.passwordstore.org/

