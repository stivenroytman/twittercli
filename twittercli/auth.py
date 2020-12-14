from getpass import getpass
from os import system

def manualAuth():
    userLogin = input('Username: ')
    userPass = getpass()
    return [userLogin, userPass]

def storeSecret(userLogin, userPass):
    print('Please enter your GPG user ID (it usually looks like an email address).')
    gpgID = input('GPG ID: ')
    printfCall = 'printf "%s\n%s" "{}" "{}"'.format(userLogin, userPass.replace('$', '\\$'))
    gpgCall = 'gpg -r {} --encrypt > .secret.gpg'.format(gpgID)
    systemCall = ' | '.join([printfCall, gpgCall])
    system(systemCall)

# Retrieving secret
def retrieveSecret():
    system('mkfifo .secret')
    system('gpg --decrypt .secret.gpg > .secret &')
    with open('.secret', 'r') as secretFile:
        secret = [secretData.strip() for secretData in secretFile.readlines()]
    system('rm .secret')
    return secret
