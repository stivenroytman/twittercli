from getpass import getpass
from os import system,listdir
from . import get_data
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox import options
from time import sleep

def manualAuth():
    return {
        'username': input('Username: '),
        'email': input('Email: '),
        'password': getpass()
    }

def storeSecret(userLogin, userPass):
    secretFilePath = get_data('secret.gpg')
    print('Please enter your GPG user ID (it usually looks like an email address).')
    gpgID = input('GPG ID: ')
    printfCall = 'printf "%s\n%s" "{}" "{}"'.format(userLogin, userPass.replace('$', '\\$'))
    gpgCall = 'gpg -r {} --encrypt > {}'.format(gpgID,secretFilePath)
    systemCall = ' | '.join([printfCall, gpgCall])
    system(systemCall)
    
def resetSecret():
    dataDirPath = get_data('')
    dataDirContent = listdir(dataDirPath)
    if 'secret.gpg' in dataDirContent:
        system('rm {}'.format(dataDirPath + 'secret.gpg'))
    else:
        print('No secret stored.')

# Retrieving secret
def retrieveSecret():
    secretPipePath = get_data('secret')
    secretFilePath = get_data('secret.gpg')
    system('mkfifo {}'.format(secretPipePath))
    system('gpg --decrypt {} > {} &'.format(secretFilePath,secretPipePath))
    with open(secretPipePath, 'r') as secretPipe:
        secret = [secretData.strip() for secretData in secretPipe.readlines()]
    system('rm {}'.format(secretPipePath))
    return secret


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
    try:
        unparsedMethods = driver.find_elements_by_tag_name('label')[0].text
    except IndexError:
        return False
    parsedMethods = unparsedMethods\
            .lower().replace('or','')\
            .replace(',','').replace('  ',' ').split(' ')
    return parsedMethods

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


