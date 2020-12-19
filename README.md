# twittercli


## Purpose

To provide a programmatic and terminal-friendly way of interacting with twitter
without having to go through the hoops of getting their API key. While somebody
out there probably already put something like this together, I don't care, I am
doing this for fun :)


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

Coming soon...

### Search feed

Coming soon...

## In the works...

* Scheduling twittercli jobs.
* Accessing, searching, and storing tweets from your feed.
* Secure twitter password storage via GPG or integration with https://www.passwordstore.org/

