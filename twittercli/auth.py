from getpass import getpass
from os import system
from . import get_data

def manualAuth():
    userLogin = input('Username: ')
    userPass = getpass()
    return [userLogin, userPass]

def storeSecret(userLogin, userPass):
    secretFilePath = get_data('secret.gpg')
    print('Please enter your GPG user ID (it usually looks like an email address).')
    gpgID = input('GPG ID: ')
    printfCall = 'printf "%s\n%s" "{}" "{}"'.format(userLogin, userPass.replace('$', '\\$'))
    gpgCall = 'gpg -r {} --encrypt > {}'.format(gpgID,secretFilePath)
    systemCall = ' | '.join([printfCall, gpgCall])
    system(systemCall)

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
